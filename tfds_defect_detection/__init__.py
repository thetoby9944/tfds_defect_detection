__version__ = "0.1.0"

from pathlib import Path
from typing import Optional, Iterable

from typing_extensions import Literal
import albumentations as A


def load(
        names: Iterable[Literal["mvtec", "visa"]] = ("mvtec", "visa"),
        data_dir=Path("anomaly_datasets"),
        pairing_mode: Literal[
            "result_only",
            "result_with_original",
            "result_with_contrastive_pair"
        ] = "result_with_contrastive_pair",
        create_artificial_anomalies=True,
        validation_split=0.2,
        subset_mode: Optional[Literal[
            "training",
            "validation",
            "test",
            "holdout"
        ]] = "training",
        drop_masks=False,
        width=256,
        height=256,
        repeat=True,
        anomaly_size: Optional[int] = None,
        process_deviation=A.Compose([]),
        global_transform=A.Compose([]),
        anomaly_composition=A.Compose([]),
        batch_size=8,
        seed=123,
        shuffle=True,
        peek=True,
        download=True,
        image_validation=False,
):
    """

    Convenience wrapper for download_and_prepare + DatasetBuilder
    Returns a tf.data.Dataset

    - ``tfds_defect_detection.downloader.download_and_prepare``
    - ``tfds_defect_detection.data.DatasetBuilder``

    Executes ``download_and_prepare`` first.
    Then builds a ``tf.data.Dataset`` according to the arguments

    .. WARNING::
        Warning: calling this function might potentially trigger the download
        of 30+ GiB to disk. Refer to the download argument.


    names : ``Iterable[Literal["mvtec", "visa"]]``
        List of named datasets to load. Defaults to ["mvtec", "visa"]
    data_dir : ``pathlib.Path``
        directory to read/write data. Images cached here will be included in consecutive runs without the need for further download.
    pairing_mode : ``str``
        - "result_only" - the X variable of the dataset only holds the processed image.
        - "result_with_original" - the X variable of the dataset holds a tuple  of the processed image and original image
        - "result_with_contrastive_pair" - the X variable holds a tuple of the processed image and a random image of the same class
    create_artificial_anomalies : ``bool``
        Creates artifical anomalies on the
        processed image. Anomalies are created by copying a random polygon from the
        image and smoothly pasting it onto a different part of the image.
        You can alter the appearance of the anomaly with the 'anomaly_composition'
        and 'anomaly_size' argument. Default is True
    validation_split : ``float``
        .. list-table:: Example splits for ``validation_split=0.2`` (default)
           :widths: 15 10 30
           :header-rows: 1

           * - Split
             - Amount
             - Source
           * - Training
             - 80% (1 - 0.2) of
             - train folder
           * - Validation
             - 20% (0.2) of
             - train folder
           * - Test
             - 80% (1 - 0.2) of
             - test folder
           * - Holdout
             - 20% (0.2) of
             - test folder


    subset_mode : optional, ``str``
        - "training" - Returns the training split.
            Note that training images in
            mvtec and visa are non-anomalous images due to the
            unsupervised nature of the task. For semi-supervised
            learning see the parameter 'create_artificial_anomalies'
        - "validation" - Returns the validation split.
            (Part of the train folder). Like the training split, for VisA and
            MVTEC  this only contains defect-free images.
            Useful in combination with synthetic defects.
        - "test" - Returns the majority of the real test data.
            These images contain real defects and human annotated masks.
            You may want to set 'create_artificial_anomalies' to False.
        - "holdout" - Holdout set for final evaluation on human annotated defects.
            You may want to set 'create_artificial_anomalies' to False.
        - ``None`` - returns all of the above in a dictionary.
    drop_masks : ``bool``
        whether to drop the masks, i.e. the Y variable of the dataset.
        Useful for inference tasks.
    width : ``int``
        Width of the images in a batch
    height : ``int``
        Height of the images in a batch
    repeat: ``bool``
        Whether to infinitely repeat the data. Defaults to ``True``
    anomaly_size : optional, ``int``
        if None the anomaly size will be random with min=width/8 and max=width/4
    process_deviation : ``albumentations.Transform``
        Data augmentation of the processed images
    global_transform : ``albumentations.Transform``
        data augmentation of all images
    anomaly_composition: ``albumentations.Transform``
        data augmentation of the synthetic anomaly patches.
    batch_size : ``int``
        Size of the batches of data. Default: 8
    seed : ``int``
        Optional random seed for shuffling.
    shuffle : ``bool``
        Whether to shuffle the input files. Defaults to True.
    peek : ``bool``
        Whether to plot first batch of images of the loaded data.
        Defaults to True.
    download : optional, ``bool``
        Whether to call download_and_prepare. If download is set to ``False``,
        the function expects ``data_dir`` to already hold the requested data.
        Defaults to ``True``
    image_validation : optional, ``bool``
        Whether to open all images beforehand calling the DatasetBuilder.
        This will print the name of corrupted image files,
        which cannot be read by tensorflow. Defaults to ``False``

    ``tf.data.Dataset``
        the dataset requested, or if subset_mode is None,
        a dict<key: subset_mode, value: tf.data.Dataset>.
    """
    from tfds_defect_detection.downloader import download_and_prepare
    from tfds_defect_detection.data import DatasetBuilder

    kwargs = locals().copy()

    train_folder, test_image_folder, test_mask_folder = download_and_prepare(
        cache_dir=data_dir,
        names=names,
        download=download,
        image_validation=image_validation
    )

    result = {
        "training": lambda: DatasetBuilder(
            image_directory=train_folder,
            subset="training",
            **kwargs
        ).ds,
        "validation": lambda: DatasetBuilder(
            image_directory=train_folder,
            subset="validation",
            **kwargs
        ).ds,
        "test": lambda: DatasetBuilder(
            image_directory=test_image_folder,
            mask_directory=test_mask_folder,
            subset="training",
            **kwargs
        ).ds,
        "holdout": lambda: DatasetBuilder(
            image_directory=test_image_folder,
            mask_directory=test_mask_folder,
            subset="validation",
            **kwargs
        ).ds
    }

    if subset_mode is None:
        return {k: v() for k, v in result.items()}
    else:
        return result[subset_mode]()


if __name__ == '__main__':
    pass
