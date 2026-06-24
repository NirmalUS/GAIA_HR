import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.colors import LogNorm

df = pd.read_csv("/home/nirmal/CodeAstro/GAIA_HR/Sample_data_both_table.csv")

plt.style.use(["dark_background"])

def plot_hr(df, property_name = "bp_rp", cmap="coolwarm", log_plot=False):

    fig, ax = plt.subplots(figsize=(8, 10))

    if log_plot:
        scatter = ax.scatter(
            df["bp_rp"],
            df["mag"],
            c=df[property_name],
            cmap=cmap,
            s=2,
            norm = LogNorm(vmax=np.nanpercentile(df[property_name], 99)))
    else:
        scatter = ax.scatter(
            df["bp_rp"],
            df["mag"],
            c=df[property_name],
            cmap=cmap,
            s=2,
            vmax=np.nanpercentile(df[property_name], 99))

    ax.invert_yaxis()

    ax.set_xlabel("BP - RP")
    ax.set_ylabel("Absolute Magnitude")

    ax.set_title(
        f"HR Diagram Colored by {property_name}"
    )


    cbar = plt.colorbar(scatter)

    cbar.set_label(property_name)

    plt.show()

plot_hr(df, "lum_flame", log_plot=True)