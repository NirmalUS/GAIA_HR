# GAIA_HR

Library that plots HR diagram from GAIA dataset

[![A rectangular badge, half black half purple containing the text made at Code Astro](https://img.shields.io/badge/Made%20at-Code/Astro-blueviolet.svg)](https://semaphorep.github.io/codeastro/)
## Motivation

This package queries data and plots Hertzsprung-Russell diagram for a user specified region of the sky (ra, dec, radius) from Gaia data release 3. It also compares  a user specified parameter of different stars in the region using a colormap.

## Installation

The package is installable on Python 3.x. To install the package, simply write

`pip install Gaia_HR`

Otherwise, clone this repo, and follow the below specified commands

`cd Gaia_HR`

`pip install -e .`

A list of dependencies is available in requirements.txt

## Additional Information

Gaia HR diagrams is valid when the the relative precision on parallax is lower than 20%. This uncertainity has been included by using the parameter "parallax_over_error > 20" during the query [1].

This work has made use of data from the European Space Agency (ESA) mission Gaia (https://www.cosmos.esa.int/gaia), processed by the Gaia Data Processing and Analysis Consortium (DPAC, https://www.cosmos.esa.int/web/gaia/dpac/consortium). Funding for the DPAC has been provided by national institutions, in particular the institutions participating in the Gaia Multilateral Agreement. [2, 3]

This research has made use of the VizieR catalogue access tool, CDS, Strasbourg, France (DOI : 10.26093/cds/vizier). The original description of the VizieR service was published in 2000, A&AS 143, 23.

## References:

1. Gaia Data Release 2 - Observational Hertzsprung-Russell diagrams. Gaia Collaboration, C.  Babusiaux, et al. A&A 616 A10 (2018). DOI: [10.1051/0004-6361/201832843](https://doi.org/10.1051/0004-6361/201832843)

2. The Gaia mission. Gaia Collaboration, T.  Prusti, et al. A&A 595 A1 (2016). DOI: [10.1051/0004-6361/201629272](https://doi.org/10.1051/0004-6361/201629272)

3. Gaia Data Release 3 - Summary of the content and survey properties. Gaia Collaboration, A.  Vallenari, et al. A&A 674 A1 (2023). DOI: [10.1051/0004-6361/202243940](https://doi.org/10.1051/0004-6361/202243940)
