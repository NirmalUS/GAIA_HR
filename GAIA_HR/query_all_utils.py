# Importing necessary packages
from astroquery.utils.tap.core import TapPlus
import pandas as pd
import numpy as np
from astroquery.gaia import Gaia
import pyvo
import os, sys

class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout

class ALL_SERVER:
    def check_gaia_server(self):
        try:
            job = Gaia.launch_job("SELECT TOP 1 * FROM gaiadr3.gaia_source")
            results = job.get_results()

            print("✅GAIA Server is up and responding properly!")
            print(f"✅Successfully retrieved {len(results)} row(s).")

            return 1

        except Exception as e:
            print("❌GAIA Server is not responding")
            print(f"Error details: {e}")

    def check_vizier_server(self):
        url = "http://tapvizier.u-strasbg.fr/TAPVizieR/tap"
        print(f"Pinging {url}...")

        try:
            # Initialize connection
            vizier_tap = TapPlus(url=url)

            # Run the lightest possible query (just 1 row)
            job = vizier_tap.launch_job("SELECT TOP 1 * FROM \"I/355/gaiadr3\"")
            results = job.get_results()
            
            print("✅ VIZIER Server is UP and responding properly!")
            print(f"✅ Successfully retrieved {len(results)} row(s).")

            return 1
            
        except Exception as e:
            print("❌ VIZIER Server appears to be DOWN or unreachable.")
            print(f"Error details: {e}")

    def check_ari_server(self):
        url = "https://gaia.ari.uni-heidelberg.de/tap"
        print(f"Pinging {url}...")

        try:
            # Initialize connection
            ari_tap = TapPlus(url=url)
            
            # Run the lightest possible query (just 1 row)
            job = ari_tap.launch_job("SELECT TOP 1 * FROM gaiadr3.gaia_source_lite")
            results = job.get_results()
            
            print("✅ ARI (Heidelberg) Server is UP and responding properly!")
            print(f"✅ Successfully retrieved {len(results)} row(s).")

            return 1
            
        except Exception as e:
            print("❌ ARI Server appears to be DOWN or unreachable.")
            print(f"Error details: {e}")

    def check_aip_server(self):
        url = "https://gaia.aip.de/tap"
        print(f"Pinging {url}...")

        try:
            # Initialize connection using pyvo
            service = pyvo.dal.TAPService(url)
            
            # Run the lightest possible query (just 1 row)
            # Force the format parameter directly on execution to bypass strict header negotiation 
            # (asked by AIP server while using TapPlus)
            job = service.search("SELECT TOP 1 * FROM gaiadr3.gaia_source_lite", response_format='votable')
            
            print("✅ AIP (Potsdam) Server is UP and responding properly!")
            print(f"✅ Successfully retrieved {len(job)} row(s).")

            return 1
 
        except Exception as e:
            print("❌ AIP Server appears to be DOWN or unreachable.")
            print(f"Error details: {e}")
        
    def check_all_server(self):
        self.check_gaia_server()
        print("\n")
        self.check_vizier_server()
        print("\n")
        self.check_ari_server()
        print("\n")
        self.check_aip_server()

def fetch_gaia_data():
    # Run a query to extract the data (Common query for all servers except TapVizier)
    # TapVizier gets an updated query
    query = """
    SELECT TOP 10000
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
    AND parallax_over_error > 20
    """

    with HiddenPrints():
        if ALL_SERVER().check_gaia_server() == 0:

            print("Connecting to main Gaia server")

            job = Gaia.launch_job_async(query)
            stars = job.get_results()
            df = stars.to_pandas()
            
            return df

        elif ALL_SERVER().check_ari_server() == 0:
            url = "https://gaia.ari.uni-heidelberg.de/tap"
            ari_tap = TapPlus(url=url)

            print("Connecting to Heidelberg server")

            job = ari_tap.launch_job_async(query)
            stars = job.get_results()
            df = stars.to_pandas()
            
            return df
        
        elif ALL_SERVER().check_aip_server() == 1:
            url = "https://gaia.aip.de/tap"
            service = pyvo.dal.TAPService(url)

            print("Connecting to Potsdam server")

            job = service.search(query, response_format='votable')
            astropy_table = job.to_table()
            df = astropy_table.to_pandas()

            return df

        elif ALL_SERVER().check_vizier_server() == 0:
            query = """
            SELECT TOP 10000
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
            AND RPlx > 20
            """
            
            url = "http://tapvizier.u-strasbg.fr/TAPVizieR/tap"
            print(f"Connecting to {url}...")
            
            # Initialize connection
            vizier_tap = TapPlus(url=url)
            
            print("Executing query...")
            job = vizier_tap.launch_job(query)
            results = job.get_results()
            
            # Convert the result to a Pandas DataFrame
            df = results.to_pandas()
            return  df
