from lib import load_all_datasets, clean_and_filter_datasets, generate_and_save_plots


def load_data():
    """Load all datasets and return a combined DataFrame."""
    return load_all_datasets()


def process_data(df):
    """Process the data to filter and aggregate by state and year."""
    return clean_and_filter_datasets(df)


def produce_plots(datasets):
    """Generate and save plots for each state and year group."""
    generate_and_save_plots(datasets)


def main():
    # Step 1: Load data
    df = load_data()

    # Step 2: Process data
    data_tx_ok, data_wa_or, data_fl_ga = process_data(df)

    # Step 3: Produce plots
    produce_plots([data_tx_ok, data_wa_or, data_fl_ga])


if __name__ == "__main__":
    main()
