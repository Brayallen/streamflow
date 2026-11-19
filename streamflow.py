import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Load streamflow data from the CSV file
filename = "June-2021-Provo-River-Streamflow-Rates.csv"

data = np.genfromtxt(
    filename, delimiter=",",
    skip_header=1, dtype=str, encoding="utf-8-sig"
)

# Convert the first column to dates
dates = pd.to_datetime(data[:, 0], errors="coerce")

# Keep rows containing valid dates
valid = ~pd.isna(dates)
x = dates[valid]

# Extract streamflow values for each site
y_1 = pd.to_numeric(data[valid, 1], errors="coerce")
y_2 = pd.to_numeric(data[valid, 2], errors="coerce")
y_3 = pd.to_numeric(data[valid, 3], errors="coerce")
y_4 = pd.to_numeric(data[valid, 4], errors="coerce")
y_5 = pd.to_numeric(data[valid, 5], errors="coerce")

# Graph the streamflow data
plt.figure(figsize=(10, 6))

plt.plot(x, y_1, label="10163000")
plt.plot(x, y_2, label="10155200")
plt.plot(x, y_3, label="10155500")
plt.plot(x, y_4, label="10154200")
plt.plot(x, y_5, label="10155000")

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
