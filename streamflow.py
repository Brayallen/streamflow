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
    plt.savefig("provo_streamflow.png", dpi=150, bbox_inches="tight")
    plt.show()

# Summarize the streamflow for each gauge
def summarize(dates, flows, sites):
     # Verified in Excel for gauge 10163000:
     # Maximum flow = 131.0 cfs
     # Average flow = 57.0 cfs (rounded)
    results = []

    for i, site in enumerate(sites):
        values = flows[:, i]

        max_flow = np.nanmax(values)
        min_flow = np.nanmin(values)
        avg_flow = np.nanmean(values)

        max_index = np.nanargmax(values)
        max_date = dates[max_index]

        results.append({
            "Gauge": site,
            "Max (cfs)": round(max_flow, 1),
            "Date of max": str(max_date),
            "Min (cfs)": round(min_flow, 1),
            "Avg (cfs)": round(avg_flow, 1)
        })

    summary = pd.DataFrame(results)

    print(summary.to_string(index=False))
    summary.to_csv("streamflow_summary.csv", index=False)
# Main program
sites = ["10163000", "10155200", "10155500",
         "10154200", "10155000"]

dates, flows = load_streamflow(
    "June-2021-Provo-River-Streamflow-Rates.csv"
)

plot_streamflow(dates, flows, sites)
summarize(dates, flows, sites)

# Ask the user for a flow threshold
threshold = float(input("Enter a flow threshold (cfs): "))

# Calculate hours above the threshold for each gauge
for i, site in enumerate(sites):
    hours = np.sum(flows[:, i] > threshold) * 0.25
    print(f"Gauge {site}: {hours:.2f} hours above {threshold} cfs")
