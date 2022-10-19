from pathlib import Path


def unit_test():
    from tfds_defect_detection import load
    defaults = {
        "data_dir": Path("E://data"),
        "download": False,
        "shuffle": False
    }

    load(**defaults)

    load(**defaults, pairing_mode="result_only")

    load(**defaults, pairing_mode="result_with_original")

    load(**defaults, subset_mode="test")

    load(**defaults, subset_mode="test", create_artificial_anomalies=False)

    load(**defaults, drop_masks=True)


if __name__ == '__main__':
    unit_test()
