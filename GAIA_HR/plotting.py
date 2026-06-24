from astroquery.utils.tap.core import TapPlus
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("GAIA_HR/Sample_data.csv").head(10000)

df["mag"] = df["phot_g_mean_mag"] + 5 + 5 * np.log10(df["parallax"] / 1000)

plt.style.use(["dark_background"])
fig, ax = plt.subplots(1, 1)
ax.yaxis.set_inverted(True)
ax.scatter(df["bp_rp"], df["mag"], s=2, cmap="coolwarm", c=df["bp_rp"])
ax.set_xlabel("BP-RP")
ax.set_ylabel("GAIA magnitude")

plt.show()