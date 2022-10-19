from pathlib import Path
from typing import Optional, Any

import numpy as np
import tensorflow as tf

import albumentations as A
from keras.utils import image_dataset_from_directory
from polygenerator import random_polygon
import matplotlib.pyplot as plt
from skimage.draw import polygon2mask
from typing_extensions import Literal

from tfds_defect_detection.utils import random_slice, blend_merge, masking, \
    combine_binary_masks

from pydantic import BaseModel


class DatasetBuilder(BaseModel):
    class Config:
        underscore_attrs_are_private = True
        arbitrary_types_allowed = True

    color_dict = {
        0: (0, 0, 0),
        1: (255, 255, 255),
    }
    shuffle = True
    peek = True
    image_directory = Path("images")
    mask_directory: Optional[Path] = None
    pairing_mode: Literal[
        "result_only",
        "result_with_original",
        "result_with_contrastive_pair",
    ] = "result_only"
    create_artificial_anomalies = True
    drop_masks = False
    validation_split = 0.2
    subset: Literal[
        "training",
        "validation",
        ""
    ] = "training"
    width = 256
    height = 256
    repeat = True
    anomaly_size: Optional[int] = None
    process_deviation = A.Compose([])
    global_transform = A.Compose([])
    anomaly_composition = A.Compose([])
    batch_size = 8
    seed = 123

    _num_classes = None
    _class_names = None
    _num_files = None
    _ds = None
    _raw_ds = None
    _mask_ds = None
    _rand_images_by_label = None

    def __init__(self, **data: Any):
        super().__init__(**data)

        self._create_image_dataset()
        if self.peek:
            print(self.ds)
            self.peek_dataset()

    @property
    def ds(self):
        return self._ds

    @property
    def num_classes(self):
        return self._num_classes

    @property
    def num_files(self):
        return self._num_files

    def _create_image_dataset(self):
        self._init_properties()
        self._init_partial_datasets()
        self._ds = self._synth_and_combine_datasets()

        return self.ds

    def _init_properties(self):
        self._num_files = len([
            ""
            for subdir in self.image_directory.rglob("*.*")
            if subdir.is_file()
        ])
        self._class_names = sorted([
            subdir.stem
            for subdir in self.image_directory.glob("*")
            if subdir.is_dir()
        ])
        self._num_classes = len(self._class_names)

    def _init_partial_datasets(self):
        self._raw_ds: tf.data.Dataset = image_dataset_from_directory(
            directory=self.image_directory,
            validation_split=self.validation_split,
            subset=self.subset,
            seed=self.seed,
            image_size=(self.width, self.height),
            batch_size=1,
            shuffle=self.shuffle
        ).unbatch()
        if self.repeat:
            self._raw_ds = self._raw_ds.repeat()

        if self.mask_directory is not None:

            self._mask_ds = image_dataset_from_directory(
                directory=self.mask_directory,
                validation_split=self.validation_split,
                subset=self.subset,
                seed=self.seed,
                shuffle=self.shuffle,
                image_size=(self.width, self.height),
                batch_size=1,
                color_mode='grayscale',
                interpolation="nearest"
            ).unbatch()

            if self.repeat:
                self._mask_ds = self._mask_ds.repeat()
            self._mask_ds = (
                self._mask_ds
                .map(lambda x, y: x / 255)
                .map(lambda x: masking(
                    x,
                    [self.color_dict[i] for i in range(2)]
                ))
            )
        contrastive_ds: tf.data.Dataset = image_dataset_from_directory(
            directory=self.image_directory,
            validation_split=self.validation_split,
            subset=self.subset,
            shuffle=True,
            seed=self.seed + 1,
            image_size=(self.width, self.height),
            batch_size=1
        ).unbatch()
        self._rand_images_by_label = {}
        for label in range(self._num_classes):
            filtered_ds = contrastive_ds.filter(lambda x, y: tf.equal(y, label))
            filtered_ds = filtered_ds.repeat()
            self._rand_images_by_label[label] = iter(filtered_ds)

    def peek_dataset(self):
        batches = next(self.ds.take(10).as_numpy_iterator())
        # print(list([batch.shape for batch in batches]))
        original_batch, image_batch, mask_batch = None, None, None

        if self.pairing_mode == "result_only" and not self.drop_masks:
            image_batch, mask_batch = batches
        if self.pairing_mode == "result_only" and self.drop_masks:
            image_batch = batches
        if self.pairing_mode != "result_only" and not self.drop_masks:
            (original_batch, image_batch), mask_batch = batches
        if self.pairing_mode != "result_only" and self.drop_masks:
            original_batch, image_batch = batches

        columns = 4
        rows = self.batch_size
        plt.figure(figsize=(columns * 2.5, rows * 2.5))
        subtitle = (
            f"Subset: "
            f"{self.subset}, "
            f"Artificial Anomalies Created: "
            f"{self.create_artificial_anomalies}, "
            f"Drop Masks: "
            f"{self.drop_masks}\n"
            f"Manual Masks provided: "
            f"{self._mask_ds is not None}, "
            f"Pairing mode: "
            f"{self.pairing_mode}"
        )
        # plt.suptitle(subtitle, fontsize=16)
        for i in range(rows):
            plt.subplot(rows, columns, i * columns + 1)
            if original_batch is not None:
                # print(original_batch.shape)
                plt.imshow((original_batch[i] * 255).astype("uint8"))
                plt.title("Paired")
            plt.axis("off")

            plt.subplot(rows, columns, i * columns + 2)
            # print(image_batch.shape)
            plt.imshow((image_batch[i] * 255).astype("uint8"))
            plt.title("Image")
            plt.axis("off")

            plt.subplot(rows, columns, i * columns + 3)
            if original_batch is not None:
                plt.imshow(
                    np.max(abs(original_batch[i] - image_batch[i]), axis=-1))
                plt.colorbar()
                plt.title("Diff Image")
            plt.axis("off")

            plt.subplot(rows, columns, i * columns + 4)
            if mask_batch is not None:
                # print(mask_batch.shape)
                plt.imshow(mask_batch[i][..., 1], cmap="Greys_r", vmin=0,
                           vmax=1)
                plt.colorbar()
                plt.title("GT Mask")
            plt.axis("off")

        plt.tight_layout()
        # plt.subplots_adjust(top=0.90)
        plt.show()

    def _create_anomalies(
            self,
            good_image,
            future_anomaly_image,
    ):

        orig_img = good_image.numpy().copy()
        orig_img = self.global_transform(image=(orig_img.astype(np.uint8)))[
            'image']

        # Create a second image that should depict the
        # same part, but has deviations
        # which are within the process robustness
        np_img = future_anomaly_image.numpy()  # .copy()
        np_img = self.process_deviation(image=(np_img.astype(np.uint8)))[
            'image']

        fg_label = np.zeros(np_img.shape[:2], dtype=bool)

        if self.create_artificial_anomalies:
            if self.anomaly_size is None:
                anomaly_size = np.random.randint(self.width // 8,
                                                 self.width // 4)
            else:
                anomaly_size = self.anomaly_size

            # Slice a part of the image that will be used to
            # alter the image to the point
            # where it becomes an anomaly
            src_slice = random_slice(np_img, anomaly_size)
            dest_slice = random_slice(np_img, anomaly_size)

            crop = np_img[src_slice].copy()

            # Randomly augment the cropped patch, including rotation
            crop = self.anomaly_composition(
                image=crop.astype(np.uint8)
            )['image']

            crop = crop.astype(np.float32)

            # Masking the crop in the shape of a random polygon
            polygon = random_polygon(20)
            polygon = np.asarray(polygon) * anomaly_size
            mask = polygon2mask((anomaly_size, anomaly_size), polygon)

            # Blur the borders of the polygon, so it blends when pasted back
            background = np_img[dest_slice].copy()
            np_img[dest_slice] = blend_merge(crop, background, mask)
            fg_label[dest_slice] = mask

        bg_label = ~fg_label
        onehot_mask = np.stack([bg_label, fg_label], axis=-1)

        return (
            orig_img.astype(np.float32) / 255,
            np_img.astype(np.float32) / 255,
            onehot_mask.astype(np.float32)
        )

    def _synthetic_image_label_pairs(self):

        for image, label in self._raw_ds:
            yield self._create_anomalies(
                good_image=(
                    next(
                        self._rand_images_by_label[label.numpy()]
                    )[0]
                    if self.pairing_mode == "result_with_contrastive_pair"
                    else image
                ),
                future_anomaly_image=image
            )

    def _synth_and_combine_datasets(self):
        ds = (
            tf.data.Dataset.from_generator(
                lambda: self._synthetic_image_label_pairs(),
                output_types=(
                    tf.float32,
                    tf.float32,
                    tf.float32
                ),
                output_shapes=(
                    [self.width, self.height, 3],
                    [self.width, self.height, 3],
                    [self.width, self.height, 2]
                )
            ).map(lambda x, y, z: ((x, y), z))
        )

        if self._mask_ds is not None:
            ds = tf.data.Dataset.zip((ds, self._mask_ds)).map(
                lambda ds_1, ds_2: (
                    ds_1[0],
                    combine_binary_masks(ds_1[1], ds_2)
                )
            )

        if self.pairing_mode == "result_only":
            ds = ds.map(lambda x, y: (x[1], y))

        if self.drop_masks:
            ds = ds.map(lambda x, y: x)

        ds = ds.batch(self.batch_size).prefetch(tf.data.AUTOTUNE)
        return ds


if __name__ == "__main__":
    DatasetBuilder()
