# Importing necessary packages
from astroquery.utils.tap.core import TapPlus
import pandas as pd
import numpy as np
from astroquery.gaia import Gaia
import pyvo
import os, sys



class HiddenPrints:
    """Print Enabler/Disabler
    
    Context Manager to prevent print statement from executing within the statement setup. (Source: https://stackoverflow.com/questions/8391411)
    """

    def __enter__(self):
        """Enter function
        
        Disables the print statement from executing when placed within the HiddenPrints statement.
        """

        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """Exit function
        
        Enables the print statement during runs when outside the HiddenPrints statement.

        Args:
            exc_type: indicates class of exception. 
            exc_value: indicates type of exception . like divide_by_zero error, floating_point_error, which are types of arithmetic exception. 
            exc_traceback: traceback is a report which has all of the information needed to solve the exception.
        """
        sys.stdout.close()
        sys.stdout = self._original_stdout

class ALL_SERVER:
    """GAIA Server Status Checker

    Checks if the GAIA servers are connecting to the system using a simple ADQL query and returns the connection status.
    """
    def check_gaia_server(self):
        """ESA GAIA server checker

        Function to verify the ESA GAIA server responsiveness.
        """
        try:
            job = Gaia.launch_job("SELECT TOP 1 * FROM gaiadr3.gaia_source")
            results = job.get_results()

            print("GAIA Server is up and responding properly!")
            print(f"Successfully retrieved {len(results)} row(s).")

            return 1

        except Exception as e:
            print("GAIA Server is not responding")
            print(f"Error details: {e}")

    def check_vizier_server(self):
        """TAPVizieR server checker

        Function to verify the TAPVizier GAIA server responsiveness.
        """
        url = "http://tapvizier.u-strasbg.fr/TAPVizieR/tap"
        print(f"Pinging {url}...")

        try:
            # Initialize connection
            vizier_tap = TapPlus(url=url)

            # Run the lightest possible query (just 1 row)
            job = vizier_tap.launch_job("SELECT TOP 1 * FROM \"I/355/gaiadr3\"")
            results = job.get_results()
            
            print("VIZIER Server is UP and responding properly!")
            print(f"Successfully retrieved {len(results)} row(s).")

            return 1
            
        except Exception as e:
            print("VIZIER Server appears to be DOWN or unreachable.")
            print(f"Error details: {e}")

    def check_ari_server(self):
        """ARI server checker

        Function to verify the ARI GAIA server responsiveness.
        """
        url = "https://gaia.ari.uni-heidelberg.de/tap"
        print(f"Pinging {url}...")

        try:
            # Initialize connection
            ari_tap = TapPlus(url=url)
            
            # Run the lightest possible query (just 1 row)
            job = ari_tap.launch_job("SELECT TOP 1 * FROM gaiadr3.gaia_source_lite")
            results = job.get_results()
            
            print("ARI (Heidelberg) Server is UP and responding properly!")
            print(f"Successfully retrieved {len(results)} row(s).")

            return 1
            
        except Exception as e:
            print("ARI Server appears to be DOWN or unreachable.")
            print(f"Error details: {e}")

    def check_aip_server(self):
        """AIP server checker

        Function to verify the AIP GAIA server responsiveness.
        """
        url = "https://gaia.aip.de/tap"
        print(f"Pinging {url}...")

        try:
            # Initialize connection using pyvo
            service = pyvo.dal.TAPService(url)
            
            # Run the lightest possible query (just 1 row)
            # Force the format parameter directly on execution to bypass strict header negotiation 
            # (asked by AIP server while using TapPlus)
            job = service.search("SELECT TOP 1 * FROM gaiadr3.gaia_source_lite", response_format='votable')
            
            print("AIP (Potsdam) Server is UP and responding properly!")
            print(f"Successfully retrieved {len(job)} row(s).")

            return 1
 
        except Exception as e:
            print("AIP Server appears to be DOWN or unreachable.")
            print(f"Error details: {e}")
        
    def check_all_server(self):
        """ Check the responsiveness of all GAIA servers

        Verifies whether all the servers are responding and provides exceptions if it fails.
        """
        self.check_gaia_server()
        print("\n")
        self.check_vizier_server()
        print("\n")
        self.check_ari_server()
        print("\n")
        self.check_aip_server()


# Dictionaries to map columns from different servers to rename with a common name.

column_mapping = {'source_id':'sid', 
                  'ra':'ra', 
                  'dec':'dec', 
                  'parallax':'parallax',
                  'phot_g_mean_mag':'g_mean_mag', 
                  'bp_rp':'bp_rp', 
                  'teff_gspphot':'teff',
                  'logg_gspphot':'logg', 
                  'mh_gspphot': 'mh',
                  'pm':'pm', 
                  'radial_velocity':'rv', 
                  'lum_flame':'lum_flame',
                  'radius_flame':'radius_flame', 
                  'mass_flame':'mass_flame',}

column_mapping_Vizier = {'Source':'sid', 
                         'RA_ICRS':'ra', 
                         'DE_ICRS':'dec', 
                         'Plx':'parallax',
                         'Gmag':'g_mean_mag', 
                         'BP-RP':'bp_rp', 
                         'Teff':'teff',
                         'logg':'logg', 
                         '[Fe/H]': 'mh',
                         'PM':'pm', 
                         'RV':'rv', 
                         'Lum-Flame':'lum_flame',
                         'Rad-Flame':'radius_flame', 
                         'Mass-Flame':'mass_flame',}

def fetch_gaia_data(ra, dec, radius, d_max = -1, d_min = 0, max_source = 10000):
    """Fetches a sample of star data from the Gaia DR3 dataset.
    
    Executes ADQL query to retrive sources with parallax_over_error > 20 from user specified region.
    Joins standard astrometric data with evaluated astrophysical parameters for available sources.
    Function utilises a fallback mechanism, attempting to connect t multiple servers until successful
    connectiona nd query are made.

    Args:
        ra (float): Right Ascension of region you want to query (in degrees)
        dec (float): Declination of region you want to query (in degrees)
        radius (float): Radius of region you want to query (in degrees)
        d_max (float, optional): 
                            Default: -1, No input was given
                            Maximum distance to sources (in lightyears)
        d_min (float, optional):
                            Default: 0
                            Minimum diatance to sources (in lightyears)
        max_sources (int, optional):
                            Default: 10000
                            Maximum number of sources to be queried
    
    Returns:
        pandas.DataFrame: gaia star data
    """

    # Query construction from user input
    query = f"""
    SELECT TOP {max_source}
        gs.source_id,
        gs.ra,
        gs.dec,
        gs.parallax,
        gs.phot_g_mean_mag,
        gs.bp_rp,
        gs.teff_gspphot,
        gs.logg_gspphot,
        gs.mh_gspphot,
        gs.pm,
        gs.radial_velocity,
        ap.lum_flame,
        ap.radius_flame,
        ap.mass_flame
    FROM gaiadr3.gaia_source AS gs
    JOIN gaiadr3.astrophysical_parameters AS ap
    ON gs.source_id = ap.source_id
    WHERE 1 = CONTAINS(
        POINT("ICRS", gs.ra, gs.dec),
        CIRCLE("ICRS", {ra}, {dec}, {radius})
    )
    AND parallax_over_error > 20
    """

    with HiddenPrints():
        # Server 1 : esa.gaia
        if ALL_SERVER().check_gaia_server() == 0:

            print("Connecting to main Gaia server")

            job = Gaia.launch_job_async(query)
            stars = job.get_results()
            df = stars.to_pandas()
            
            # Rename column names to have a common format
            df = df.rename(columns=column_mapping, errors = 'raise')

            return df

        # Server 2 : gaia.ari
        elif ALL_SERVER().check_ari_server() == 0:
            url = "https://gaia.ari.uni-heidelberg.de/tap"
            ari_tap = TapPlus(url=url)

            print("Connecting to Heidelberg server")

            job = ari_tap.launch_job_async(query)
            stars = job.get_results()
            df = stars.to_pandas()

            # Rename column names to have a common format
            df = df.rename(columns=column_mapping, errors = 'raise')
            
            return df
        
        # Server 3 : gaia.aip
        elif ALL_SERVER().check_aip_server() == 1:
            url = "https://gaia.aip.de/tap"
            service = pyvo.dal.TAPService(url)

            print("Connecting to Potsdam server")

            job = service.search(query, response_format='votable')
            astropy_table = job.to_table()
            df = df = astropy_table.to_pandas()

            # Rename column names to have a common format
            df = df.rename(columns=column_mapping, errors = 'raise')

            return df

        # Server 4 : vizier 
        elif ALL_SERVER().check_vizier_server() == 0:
            query = """
            SELECT TOP {max_source}
                gs.Source,
                gs.RA_ICRS,
                gs.DE_ICRS,
                gs.Plx,
                gs.Gmag,
                gs."BP-RP",
                gs.Teff,
                gs.logg,
                gs."[Fe/H]",
                gs.PM,
                gs.RV,
                ap."Lum-Flame",
                ap."Rad-Flame",
                ap."Mass-Flame"
            FROM "I/355/gaiadr3" AS gs
            JOIN "I/355/paramp" AS ap
            ON gs.Source = ap.Source
            WHERE 1 = CONTAINS(
                POINT("ICRS", gs.RA_ICRS, gs.DE_ICRS),
                CIRCLE("ICRS", {ra}, {dec}, {radius})
            )
            AND RPlx > 20
            """
            
            url = "http://tapvizier.u-strasbg.fr/TAPVizieR/tap"
            print(f"Connecting to {url}...")
            
            vizier_tap = TapPlus(url=url)
            
            print("Executing query...")
            job = vizier_tap.launch_job(query)
            results = job.get_results()

            df = results.to_pandas()

            # Rename column names to have a common format
            df = df.rename(columns=column_mapping_Vizier, errors = 'raise')

            return  df
        
        # Edge case: No server response
        else:
            raise ConnectionError("No servers are responding. Kindly try again later!!")
