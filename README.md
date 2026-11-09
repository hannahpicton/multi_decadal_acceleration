# multi_decadal_acceleration
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19955500.svg)](https://doi.org/10.5281/zenodo.19955500)

Code associated with the manuscript 'Melt-induced ice surface steepening drives multi-decadal acceleration of the south-west Greenland Ice Sheet interior', revised in November 2026.

## 📁 Repository Structure
```text
├── data/
│   └── flowline_sampled/
│       ├── arcticDEM_v4_sampled_100m.csv
│       └── bedMachine_v5_sampled_150m.csv
│   └── PPP_outputs/                                    # CSRS-PPP outputs (IGSR3, static mode), all output files
│       ├── f003_2021/
│       ├── f004_2021/
│       ├── kanu_2021/
│       ├── lev5_2009/
│       ├── lev5_2021/
│       ├── lev6_2009/
│       └── lev6_2021/
│       ├── site_coords_IGSR3_ellps_polecorrected.csv   # Site coordinates and pole-corrected heights (Table S2)
│       ├── PPP_lev5_lev6_baselines_IGSR3.csv           # LEV5–LEV6 baseline distances (2009, 2021)
│       └── PPP_lev5_lev6_baseline_slopes_IGSR3.csv     # LEV5–LEV6 surface slopes (2009, 2021)
│   └── seasonal_annual_2009_2013/                      # LEV5 & LEV6 seasonal/annual displacements, 2009–2013 (recalculated with summer ending 31 August)
├── code/
│   ├── figure_1c.ipynb
│   ├── figure_2.ipynb
│   ├── figure_3.ipynb
│   ├── figure_4.ipynb
│   ├── figure_5a.ipynb
│   ├── figure_6.ipynb
│   ├── figure_7.ipynb
│   ├── figure_S2.ipynb
│   ├── figure_S3a.ipynb
│   └── processing/
│       ├── driving_stress_calculation.ipynb
│       ├── ice_displacement_analysis.ipynb
│       └── process_site_positions.py
└── README.md
```

Each site folder in `data/PPP_outputs/` contains the full set of CSRS-PPP output files (`.sum`, `.pos`, `.csv`, `.clk`, `.tro`, `.pdf`, `errors.txt`); see `output_descriptions.txt` in each folder for details. All sites were processed in static mode in the IGSR3 reference frame using IGS Repro3 products. `process_site_positions.py` (A. Tedstone) derives the site coordinates, baseline distances and surface slopes from these outputs.


## 📊 Data Availability

| Dataset | Period | Repository/Location |
| :--- | :--- | :--- | 
| Ice velocity (F003, F004) | 1996 | [Buffalo Remote Sensing Lab](https://ubwp.buffalo.edu/glyremotesensinglab/2024/05/22/mass-balance-and-velocity-data-for-greenlands-ice-sheets-at-high-elevations-data/) | 
| Ice velocity (LEV5, LEV6) | 2009–2013 | `data/seasonal_annual_2009_2013/` (recalculated from [Tedstone & Nienow (2018)](https://doi.org/10.5285/1f69fba3-4c62-47ad-8119-08cfeec05e46) with summer ending 31 August) |
| Ice velocity (KAN_U) | 2009–2012 | [Doyle et al. (2014)](https://doi.org/10.1002/2013GL058933) |
| Ice velocity (LEV5, LEV6, KAN_U, F003, F004) | 2021–2024 | [Tedstone et al. (2026)](https://doi.org/10.5281/zenodo.18611668) |
| Vertical displacement (LEV6) | 2021, 2023 | [Tedstone et al. (2026)](https://doi.org/10.5281/zenodo.18611668) |
| Automatic weather station (KAN_M & KAN_U) | 2009-2023 | [PROMICE Network](https://www.promice.org) |
| Sentinel-1 and Sentinel-2 imagery | 2021, 2023 | [Copernicus Data Space Ecosystem](https://dataspace.copernicus.eu) |
| Ice surface elevation (Porter et al. 2023) | - | `data/flowline_sampled/` |
| Bed elevation (Morlighem et al. 2022) | - | `data/flowline_sampled/` |
| PPP outputs (LEV5, LEV6, KAN_U, F003, F004) | 2009 & 2021 | `data/PPP_outputs/` |

## 📩 Queries
For questions regarding the code or data, please contact: Hannah Picton (hannah.picton@ed.ac.uk) 
