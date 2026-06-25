# Working example demonstrating the usage of the package.

from GAIA_HR import query
from GAIA_HR import plot

df = query.fetch_gaia_data(ra = 136, dec = 16, radius = 1)
plot.plot_hr(df)
