from pathlib import Path
from typing import Iterable

from typing_extensions import Literal



class BaseDownloader:
    mask_suffix = ""

    def __init__(self, delete_tmp=True):
        self.delete_tmp = delete_tmp

    def download_and_extract(self, cache_dir) -> Path:
        raise NotImplemented

    def convert_to_mvtec_style(self, root: Path):
        return root


class MvtecDownloader(BaseDownloader):
    mask_suffix = "_mask"

    def download_and_extract(self, cache_dir) -> Path:
        import tfds_defect_detection.downloader.mvtec as mvtec
        return mvtec.download_and_extract(cache_dir)


class VisaDownloader(BaseDownloader):
    mask_suffix = ""

    def download_and_extract(self, cache_dir) -> Path:
        import tfds_defect_detection.downloader.visual_anomalies as visa
        return visa.download_and_extract(cache_dir)

    def convert_to_mvtec_style(self, root: Path):
        import tfds_defect_detection.downloader.visual_anomalies as visa
        return visa.convert_to_mvtec_style(
                root,
                delete_tmp=self.delete_tmp
            )



def download_and_prepare(
        cache_dir: Path,
        names: Iterable[Literal["mvtec", "visa"]],
        download=True,
        image_validation=False,
        delete_tmp=True
):
    from tfds_defect_detection.downloader.mvtec import \
        restructure_mvtec_style_dataset
    from tfds_defect_detection.utils import validate_images

    downloaders = {
        "mvtec": MvtecDownloader(delete_tmp=delete_tmp),
        "visa": VisaDownloader(delete_tmp=delete_tmp)
    }
    for name in names:
        cache_dir = cache_dir / name
        result = (
            cache_dir / "train_images",
            cache_dir / "test_images",
            cache_dir / "test_masks"
        )
        if download is False:
            return result

        cache_dir.mkdir(exist_ok=True, parents=True)

        base_root = downloaders[name].download_and_extract(cache_dir)
        root = downloaders[name].convert_to_mvtec_style(base_root)

        result = restructure_mvtec_style_dataset(
                root,
                mask_suffix=downloaders[name].mask_suffix,
                delete_tmp=delete_tmp
            )

        train_image_dir, test_image_dir, test_mask_dir = result

        if image_validation:
            for image_dir in result:
                validate_images(image_dir)

        yield train_image_dir, test_image_dir, test_mask_dir
