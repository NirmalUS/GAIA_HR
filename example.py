# Working example demonstrating the usage of the package.

from GAIA_HR import query
from GAIA_HR import plot

df = query.fetch_gaia_data(ra = 136, dec = 16, radius = 1, d_min=30, server="aip")
plot.plot_hr(df, property_name="radius_flame", cmap="plasma", log_plot=True)
# plot.plot_radec(df, property_name="radius_flame", cmap="plasma", log_plot=True)
# Available colourmap parameters : ra, dec, parallax, g_mean_mag, bp_rp, teff, logg, mh, pm, rv, lum_flame,
# radius_flame, mass_flame

