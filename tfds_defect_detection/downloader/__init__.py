from pathlib import Path
from typing import Iterable

from typing_extensions import Literal

import tfds_defect_detection as tfdd


def download_and_prepare(
        cache_dir: Path,
        names: Iterable[Literal["mvtec", "visa"]],
        download=True,
        image_validation=False
):
    from tfds_defect_detection.downloader.mvtec import \
        restructure_mvtec_style_dataset
    from tfds_defect_detection.downloader.visual_anomalies import \
        convert_to_mvtec_style
    from tfds_defect_detection.utils import validate_images

    result = (
        cache_dir / "train_images",
        cache_dir / "test_images",
        cache_dir / "test_masks"
    )
    if download is False:
        return result

    cache_dir.mkdir(exist_ok=True, parents=True)

    if "mvtec" in names:
        mvtec_root = tfdd.downloader.mvtec.download_and_extract(cache_dir)

        result = restructure_mvtec_style_dataset(mvtec_root,
                                                 mask_suffix="_mask")

    if "visa" in names:
        visa_root = tfdd.downloader.visual_anomalies.download_and_extract(
            cache_dir)

        visa_mvtec_style = convert_to_mvtec_style(visa_root)
        result = restructure_mvtec_style_dataset(visa_mvtec_style,
                                                 mask_suffix="")

    train_image_dir, test_image_dir, test_mask_dir = result

    if image_validation:
        for image_dir in result:
            validate_images(image_dir)

    return train_image_dir, test_image_dir, test_mask_dir
