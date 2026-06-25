import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.colors import LogNorm

#Applies matplotlib's built in dark theme
plt.style.use(["dark_background"])

def plot_hr(df, property_name = "bp_rp", cmap="coolwarm", log_plot=False):
    """
    The plot_hr functions plots the HR diagram , using the data stored in dataframe. The stars are plotted with bp-rp on x axis and absolute magnitude. 
    Additonal properties(tempreature , surface gravity , radial velocity, metalicity,proper motion, mass , radius) of the stars can be compared using colormap.The 
    function supports both linear and logarithmic scaling
    Args:
            df(pandas.DataFrame):A pandas dataset containing stellar data. 
                                The data set must contain bp-rp, absolute magnitude
            property_name(str, optional):
                            Default: "bp-rp"
                            Specifies which property of the stellar data will be used for the color map 
            cmap(str,optional):
                        Default: "coolwarm"
                        Specifies the matplotlib colormap used for the stars 
            log_plot(boolean,optional):
                        Default: False
                        To determine whether colorscale to be logarithmic or linear
                        True :logarithmic color scale 
                        False : linear color scale
    Return:
            This function doesnt return anything , instead it shows the H-R diagram using plt.show()
                        
    """
    df["mag"] = df["phot_g_mean_mag"] + 5 + 5 * np.log10(df["parallax"] / 1000)

    # Creates a new figure and axes object
    fig, ax = plt.subplots(figsize=(8, 10))

    #If log_plot is true the scatter plot uses logarithimic normalization                       
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
            vmax=np.nanpercentile(df[property_name], 99)) # Gives maximum color to top outliers
            
    # In H-R diagram lower magnitude represents brighter stars , hence y axis is reverted
    ax.invert_yaxis() 

   # Sets X-axis label to BP-RP
    ax.set_xlabel("BP - RP")
   # Sets Y-axis label to Absolute magnitude
    ax.set_ylabel("Absolute Magnitude")

   # Creates the title for the property currently being displayed by the colormap
    ax.set_title(
        f"HR Diagram Colored by {property_name}"
    )

   # Creates a color bar associated witht the scatter plot 
    cbar = plt.colorbar(scatter)
   # Labels the color bar according to the property 
    cbar.set_label(property_name)

    # Renders the entire H-R diagram on the screen
    plt.show()
