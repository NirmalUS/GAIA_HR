# Working example demonstrating the usage of the package.

from GAIA_HR import query
from GAIA_HR import plot

df = query.fetch_gaia_data(ra = 136, dec = 16, radius = 1, d_min=30, condition = "teff_gspphot > 2000")
plot.plot_hr(df, property_name="radius_flame", cmap="plasma", log_plot=True)
# plot.plot_radec(df, property_name="radius_flame", cmap="plasma", log_plot=True)
