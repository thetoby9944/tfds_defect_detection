import shutil
from pathlib import Path

from keras.utils import get_file
from tqdm import tqdm
import PIL.Image

from tfds_defect_detection.utils import copy_to_folder


def _prepare_good_images(
        download_directory: Path,
        new_root="train_images",
        skip_if_image_exists=True
):
    old_root = download_directory.name
    result = Path(str(download_directory).replace(old_root, new_root))
    all_images = list(download_directory.rglob("**/*train/good/*.*"))

    if not len(all_images) and result.is_dir():
        return result

    print("Preparing", old_root, new_root)
    for path in tqdm(all_images):
        if path.name.startswith("."):
            continue
        target = Path(str(path).replace(old_root, new_root))
        if skip_if_image_exists and target.is_file():
            continue
        copy_to_folder(path, target)

    return result


def _prepare_anomaly_images_with_masks(
        download_directory: Path,
        new_root_images="test_images",
        new_root_masks="test_masks",
        mask_suffix="_mask",
        skip_if_image_exists=True
):
    old_root = download_directory.name

    result = (
        Path(str(download_directory).replace(old_root, new_root_images)),
        Path(str(download_directory).replace(old_root, new_root_masks))
    )
    all_images = list(download_directory.rglob("**/*test/**/*.*"))

    if not len(all_images) and result[0].is_dir() and result[1].is_dir():
        return result

    print("Preparing", old_root, new_root_images, "and", new_root_masks)

    for img_path in tqdm():
        if img_path.name.startswith("."):
            continue
        img_target = Path(str(img_path).replace(old_root, new_root_images))
        if skip_if_image_exists and img_target.is_file():
            continue

        mask_path = Path(str(img_path).replace("test", "ground_truth"))
        mask_path = mask_path.parent / (mask_path.stem + mask_suffix + ".png")
        mask_target = Path(str(img_path).replace(old_root, new_root_masks))
        mask_target = mask_target.with_suffix(".png")

        copy_to_folder(img_path, img_target)

        if not mask_path.is_file():
            img_size = PIL.Image.open(img_path).size
            mask = PIL.Image.new(mode="L", size=img_size, color="black")
            mask_target.parent.mkdir(exist_ok=True, parents=True)
            mask.save(mask_target)
        elif not mask_target.is_file():
            copy_to_folder(mask_path, mask_target)

    return result


def restructure_mvtec_style_dataset(
        root_dir: Path,
        new_root_train_images="train_images",
        new_root_test_images="test_images",
        new_root_test_masks="test_masks",
        mask_suffix="_mask",
        delete_tmp=True
):
    result = (
        _prepare_good_images(
            root_dir,
            new_root_train_images
        ),
        *_prepare_anomaly_images_with_masks(
            root_dir,
            new_root_test_images,
            new_root_test_masks,
            mask_suffix
        )
    )
    if delete_tmp:
        shutil.rmtree(root_dir, ignore_errors=True)
        root_dir.mkdir(parents=True, exist_ok=True)

    return result


if __name__ == "__main__":
    _prepare_anomaly_images_with_masks(
        Path("E:\\VisA_mvtec_style"),
        mask_suffix=""
    )


def download_and_extract(cache_dir):
    mvtec_name = "mvtec_anomaly_detection.tar.xz"
    mvtec_folder_name = "mvtec_download"
    mvtec_root = cache_dir / mvtec_folder_name
    if not mvtec_root.is_dir():
        get_file(
            fname=mvtec_name,
            origin=MVTEC_ORIGIN,
            extract=True,
            cache_dir=cache_dir,
            cache_subdir=mvtec_folder_name
        )
    return mvtec_root


MVTEC_ORIGIN = "https://www.mydrive.ch/shares/38536/3830184030e49fe74747669442f0f282/download/420938113-1629952094/mvtec_anomaly_detection.tar.xz"
