import os
import pandas as pd
import matplotlib.pyplot as plt


def load_all_datasets():
    """Load datasets from URLs and concatenate into one DataFrame."""
    urls = [
        "https://raw.githubusercontent.com/wpinvestigative/arcos-api/refs/"
        "heads/master/data/buyer_monthly2006.csv",
        "https://raw.githubusercontent.com/wpinvestigative/arcos-api/refs/"
        "heads/master/data/buyer_monthly2007.csv",
        "https://raw.githubusercontent.com/wpinvestigative/arcos-api/refs/"
        "heads/master/data/buyer_monthly2008.csv",
        "https://raw.githubusercontent.com/wpinvestigative/arcos-api/refs/"
        "heads/master/data/buyer_monthly2009.csv",
        "https://raw.githubusercontent.com/wpinvestigative/arcos-api/refs/"
        "heads/master/data/buyer_monthly2010.csv",
        "https://raw.githubusercontent.com/wpinvestigative/arcos-api/refs/"
        "heads/master/data/buyer_monthly2011.csv",
        "https://raw.githubusercontent.com/wpinvestigative/arcos-api/refs/"
        "heads/master/data/buyer_monthly2012.csv",
        "https://raw.githubusercontent.com/wpinvestigative/arcos-api/refs/"
        "heads/master/data/buyer_monthly2013.csv",
        "https://raw.githubusercontent.com/wpinvestigative/arcos-api/refs/"
        "heads/master/data/buyer_monthly2014.csv",
    ]
    datasets = [pd.read_csv(url) for url in urls]
    return pd.concat(datasets, ignore_index=True)


def clean_and_filter_datasets(df):
    """Clean, filter, and aggregate data based on state regulations."""
    df = df[df["BUYER_STATE"].isin(["TX", "FL", "GA", "OR", "WA", "OK"])].copy()
    df["county-year"] = df["BUYER_COUNTY"] + "-" + df["year"].astype(str)
    df2 = df.groupby(
        ["BUYER_COUNTY", "BUYER_STATE", "year", "county-year"], as_index=False
    )["DOSAGE_UNIT"].sum()

    # Regulation effective in 2007 for TX/OK
    data_tx_ok = df2[
        (df2["BUYER_STATE"].isin(["OK", "TX"]))
        & (df2["year"].isin([2006, 2007, 2008, 2009, 2010]))
    ]
    # Regulation effective in 2012 for WA/OR
    data_wa_or = df2[
        (df2["BUYER_STATE"].isin(["WA", "OR"]))
        & (df2["year"].isin([2010, 2011, 2012, 2013, 2014]))
    ]
    # Regulation effective in 2010 for FL/GA
    data_fl_ga = df2[
        (df2["BUYER_STATE"].isin(["FL", "GA"]))
        & (df2["year"].isin([2008, 2009, 2010, 2011, 2012, 2013]))
    ]
    return data_tx_ok, data_wa_or, data_fl_ga


def generate_and_save_plots(datasets):
    """Generate detailed plots for each state group with annotations."""
    plot_dir = "images"
    os.makedirs(plot_dir, exist_ok=True)

    state_pairs = [("TX", "OK", 2007), ("WA", "OR", 2012), ("FL", "GA", 2010)]
    colors = [("b", "g"), ("b", "g"), ("b", "g")]

    for i, (data, (state1, state2, year), (color1, color2)) in enumerate(
        zip(datasets, state_pairs, colors), start=1
    ):
        # Separate data for each state and group by year
        data_state1 = (
            data[data["BUYER_STATE"] == state1]
            .groupby("year", as_index=False)["DOSAGE_UNIT"]
            .sum()
        )
        data_state2 = (
            data[data["BUYER_STATE"] == state2]
            .groupby("year", as_index=False)["DOSAGE_UNIT"]
            .sum()
        )

        # Annotation values for the specified year
        sum_dosage_state1 = data_state1[data_state1["year"] == year][
            "DOSAGE_UNIT"
        ].values[0]
        sum_dosage_state2 = data_state2[data_state2["year"] == year][
            "DOSAGE_UNIT"
        ].values[0]

        # Plot for state1
        plt.figure(figsize=(10, 6))
        plt.plot(
            data_state1["year"],
            data_state1["DOSAGE_UNIT"],
            marker="o",
            color=color1,
            linewidth=2,
            label="Dosage Unit",
        )
        plt.title(f"Dosage Unit by Year for {state1}")
        plt.xlabel("Year")
        plt.ylabel("Total Volume of Opioids Legally Purchased")
        for _, row in data_state1.iterrows():
            plt.text(
                row["year"],
                row["DOSAGE_UNIT"],
                f"{row['DOSAGE_UNIT'] / 1_000_000:.0f}M",
                ha="center",
                va="bottom",
                fontsize=9,
                color=color1,
            )
        plt.axvspan(year - 0.5, year + 0.5, color="gray", alpha=0.3)
        plt.text(
            year,
            sum_dosage_state1 * 0.9,
            f"Sum in {year}: {sum_dosage_state1 / 1_000_000:.0f}M",
            ha="center",
            color="black",
            fontsize=10,
        )
        plt.ylim(0, data_state1["DOSAGE_UNIT"].max() * 1.2)
        plt.xticks(
            range(int(data_state1["year"].min()), int(data_state1["year"].max()) + 1)
        )
        plt.legend()
        plt.savefig(f"{plot_dir}/plot_{state1}_{i}.png", dpi=300, bbox_inches="tight")
        plt.close()

        # Plot for state2
        plt.figure(figsize=(10, 6))
        plt.plot(
            data_state2["year"],
            data_state2["DOSAGE_UNIT"],
            marker="o",
            color=color2,
            linewidth=2,
            label="Dosage Unit",
        )
        plt.title(f"Dosage Unit by Year for {state2}")
        plt.xlabel("Year")
        plt.ylabel("Total Volume of Opioids Legally Purchased")
        for _, row in data_state2.iterrows():
            plt.text(
                row["year"],
                row["DOSAGE_UNIT"],
                f"{row['DOSAGE_UNIT'] / 1_000_000:.0f}M",
                ha="center",
                va="bottom",
                fontsize=9,
                color=color2,
            )
        plt.axvspan(year - 0.5, year + 0.5, color="gray", alpha=0.3)
        plt.text(
            year,
            sum_dosage_state2 * 0.9,
            f"Sum in {year}: {sum_dosage_state2 / 1_000_000:.0f}M",
            ha="center",
            color="black",
            fontsize=10,
        )
        plt.ylim(0, data_state2["DOSAGE_UNIT"].max() * 1.2)
        plt.xticks(
            range(int(data_state2["year"].min()), int(data_state2["year"].max()) + 1)
        )
        plt.legend()
        plt.savefig(f"{plot_dir}/plot_{state2}_{i}.png", dpi=300, bbox_inches="tight")
        plt.close()
