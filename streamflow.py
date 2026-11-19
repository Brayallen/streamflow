import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


# Load data from the CSV file
def load_streamflow(filename):
    data = np.genfromtxt(
        filename, delimiter=",",
        skip_header=1, dtype=str, encoding="utf-8-sig"
    )

    dates = pd.to_datetime(data[:, 0], errors="coerce")
    valid = ~pd.isna(dates)

    dates = dates[valid]

    flows = np.column_stack([
        pd.to_numeric(data[valid, i], errors="coerce")
        for i in range(1, 6)
    ])

    return dates, flows


# Create the streamflow graph
def plot_streamflow(dates, flows, sites):
    plt.figure(figsize=(10, 6))

    for i, site in enumerate(sites):
        plt.plot(dates, flows[:, i], label=site)

    plt.title("Provo River Streamflow Data (2021)")
    plt.xlabel("Date")
    plt.ylabel("Flowrate (cfs)")

    plt.gca().xaxis.set_major_formatter(
        mdates.DateFormatter("%Y-%m-%d")
    )

    plt.xticks(rotation=45)
    plt.legend(title="Site Numbers")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# Main program
sites = ["10163000", "10155200", "10155500",
         "10154200", "10155000"]

dates, flows = load_streamflow(
    "June-2021-Provo-River-Streamflow-Rates.csv"
)

plot_streamflow(dates, flows, sites)