import os
import shutil
import csv
from pathlib import Path

from keras.utils import get_file
from tqdm import tqdm

from PIL import Image
import numpy as np


def _mkdirs_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)


def convert_to_mvtec_style(data_dir: Path):
    print("Converting", str(data_dir), "to mvtec-style dataset")
    split_file = data_dir / "split_csv" / "1cls.csv"
    save_folder = data_dir.parent / (data_dir.stem + "_mvtec_style")

    if save_folder.is_dir():
        return save_folder

    data_list = ['candle', 'capsules', 'cashew', 'chewinggum', 'fryum',
                 'macaroni1', 'macaroni2', 'pcb1', 'pcb2',
                 'pcb3', 'pcb4', 'pipe_fryum']

    for data in data_list:
        train_folder = os.path.join(save_folder, data, 'train')
        test_folder = os.path.join(save_folder, data, 'test')
        mask_folder = os.path.join(save_folder, data, 'ground_truth')

        train_img_good_folder = os.path.join(train_folder, 'good')
        test_img_good_folder = os.path.join(test_folder, 'good')
        test_img_bad_folder = os.path.join(test_folder, 'bad')
        test_mask_bad_folder = os.path.join(mask_folder, 'bad')

        _mkdirs_if_not_exists(train_img_good_folder)
        _mkdirs_if_not_exists(test_img_good_folder)
        _mkdirs_if_not_exists(test_img_bad_folder)
        _mkdirs_if_not_exists(test_mask_bad_folder)

    with open(split_file, 'r') as file:
        csvreader = csv.reader(file)
        _ = next(csvreader)  # header
        for row in tqdm(list(csvreader)):
            object, set, label, image_path, mask_path = row
            if label == 'normal':
                label = 'good'
            else:
                label = 'bad'
            image_name = image_path.split('/')[-1]
            mask_name = mask_path.split('/')[-1]
            img_src_path = data_dir / image_path
            msk_src_path = data_dir / mask_path
            img_dst_path = save_folder / object / set / label / image_name
            msk_dst_path = save_folder / object / 'ground_truth' / label / mask_name
            shutil.copyfile(img_src_path, img_dst_path)
            if set == 'test' and label == 'bad':
                mask = Image.open(msk_src_path)

                # binarize mask
                mask_array = np.array(mask)
                mask_array[mask_array != 0] = 255
                mask = Image.fromarray(mask_array.astype(np.uint8)).convert("L")

                mask.save(msk_dst_path)

    return save_folder


if __name__ == '__main__':
    convert_to_mvtec_style(Path("E:\\VisA"))
VISA_ORIGIN = "https://amazon-visual-anomaly.s3.us-west-2.amazonaws.com/VisA_20220922.tar"


def download_and_extract(cache_dir):
    visa_folder_name = "VisA"
    visa_name = "VisA.tar"
    visa_root = cache_dir / visa_folder_name
    if not visa_root.is_dir():
        get_file(
            fname=str(cache_dir / visa_name),
            origin=VISA_ORIGIN,
            untar=True,
            cache_dir=cache_dir,
            cache_subdir=visa_folder_name
        )
    return visa_root
