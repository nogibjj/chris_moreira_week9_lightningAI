import os
import pandas as pd
from lib import (
    load_all_datasets,
    clean_and_filter_datasets,
    generate_and_save_plots,
)


def test_load():
    # Test if load_all_datasets returns a DataFrame
    df = load_all_datasets()
    assert isinstance(df, pd.DataFrame), "load_all_datasets should return a DataFrame"
    assert not df.empty, "DataFrame should not be empty"
    print("load_all_datasets test passed!")


def test_clean_and_filter():
    # Test if clean_and_filter_datasets returns three DataFrames
    df = load_all_datasets()
    data_tx_ok, data_wa_or, data_fl_ga = clean_and_filter_datasets(df)
    for dataset in [data_tx_ok, data_wa_or, data_fl_ga]:
        assert isinstance(dataset, pd.DataFrame), "Each output should be a DataFrame"
    print("clean_and_filter_datasets test passed!")


def test_generate_and_save_plots():
    # Test if generate_and_save_plots runs without error and saves files
    df = load_all_datasets()
    data_tx_ok, data_wa_or, data_fl_ga = clean_and_filter_datasets(df)
    generate_and_save_plots([data_tx_ok, data_wa_or, data_fl_ga])

    # Check if images folder and sample plot file exist
    assert os.path.exists("images"), "images directory should exist"
    assert any(
        fname.endswith(".png") for fname in os.listdir("images")
    ), "At least one .png file should be saved in the images directory"
    print("generate_and_save_plots test passed!")


if __name__ == "__main__":
    test_load()
    test_clean_and_filter()
    test_generate_and_save_plots()
    print("All tests in test_lib.py passed!")
