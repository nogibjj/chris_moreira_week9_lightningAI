from main import load_data, process_data, produce_plots, main
import pandas as pd


def test_main_load():
    # Test if load_data function returns a DataFrame
    df = load_data()
    assert isinstance(df, pd.DataFrame), "load_data should return a DataFrame"
    print("load_data test passed!")


def test_main_processing():
    # Test if process_data returns three DataFrames
    df = load_data()
    data_tx_ok, data_wa_or, data_fl_ga = process_data(df)
    for dataset in [data_tx_ok, data_wa_or, data_fl_ga]:
        assert isinstance(dataset, pd.DataFrame), "Each output should be a DataFrame"
    print("process_data test passed!")


def test_main_plotting():
    # Test if produce_plots runs without errors
    df = load_data()
    data_tx_ok, data_wa_or, data_fl_ga = process_data(df)
    produce_plots([data_tx_ok, data_wa_or, data_fl_ga])
    print("produce_plots test passed!")


def test_main():
    # Run the entire main function to check for any errors
    main()
    print("main function test passed!")


if __name__ == "__main__":
    test_main_load()
    test_main_processing()
    test_main_plotting()
    test_main()
    print("All tests in test_main.py passed!")
