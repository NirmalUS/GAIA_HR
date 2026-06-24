from astroquery.utils.tap.core import TapPlus
import pandas as pd
import numpy as np
from astroquery.gaia import Gaia
import matplotlib.pyplot as plt

# Fetch data
query = """
SELECT TOP 100000
    source_id,
    ra,
    dec,
    parallax,
    phot_g_mean_mag,
    bp_rp,
    teff_gspphot,
    logg_gspphot,
    mh_gspphot
FROM gaiadr3.gaia_source
WHERE parallax_over_error > 20
"""

job = Gaia.launch_job_async(query)
stars = job.get_results()
df = stars.to_pandas()

df["mag"] = df["phot_g_mean_mag"] + 5 + 5 * np.log10(df["parallax"] / 1000)

plt.style.use(["dark_background"])
fig, ax = plt.subplots(1, 1)
ax.yaxis.set_inverted(True)
ax.scatter(df["bp_rp"], df["mag"], s=2, cmap="coolwarm", c=df["bp_rp"])
ax.set_xlabel("BP-RP")
ax.set_ylabel("GAIA magnitude")

plt.show()