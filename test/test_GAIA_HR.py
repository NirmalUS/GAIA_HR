import pytest
import pandas as pd
from GAIA_HR import query
from GAIA_HR import plot
from unittest.mock import patch


def test_fetch_gaia_data():
    """
    Unit test to evaluate correctness of fetch_gaia_data() function
    """
    # Pleiades
    df = query.fetch_gaia_data(56.75, 24.12, 2, d_min=300, d_max=600, max_source=20000, server="aip")

    assert df.shape[0] == 1419
    assert df.shape[1] == 15


def test_plot_hr():
    """
    Unit test to evaluate correctness of plot_hr() function
    """
    df = pd.read_csv("Sample_data.csv")
    with patch("matplotlib.pyplot.show"):
        plot.plot_hr(df, property_name="radius_flame", cmap="plasma", log_plot=True)


def test_plot_radec():
    """
    Unit test to evaluate correctness of plot_radec() function
    """
    df = pd.read_csv("Sample_data.csv")
    with patch("matplotlib.pyplot.show"):
        plot.plot_radec(df, property_name="radius_flame", cmap="plasma", log_plot=True)    

def end_to_end_test():
    """
    End-to-end test to evaluate correctness of GAIA_HR module
    """
    df = query.fetch_gaia_data(56.75, 24.12, 2, d_min=300, d_max=600, max_source=20000, server="aip")
    
    with patch("matplotlib.pyplot.show"):
        plot.plot_hr(df, property_name="radius_flame", cmap="plasma", log_plot=True)
    with patch("matplotlib.pyplot.show"):
        plot.plot_radec(df, property_name="radius_flame", cmap="plasma", log_plot=True) 

    assert df.shape[0] == 1419
    assert df.shape[1] == 15