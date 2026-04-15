# multi_decadal_acceleration
Code associated with the manuscript 'Melt-induced ice surface steepening drives multi-decadal acceleration of the Greenland Ice Sheet interior', submitted for peer-review in April 2026.

## 📁 Repository Structure
```text
├── data/
│   └── flowline_sampled/
│       ├── arcticDEM_v4_sampled_100m.csv
│       └── bedMachine_v5_sampled_150m.csv
│   └── PPP_outputs/
│       ├── f003_2021/
│       │   └── f003_1260.csv
│       ├── f004_2021/
│       │   └── f004_1210.csv
│       ├── kanu_2021/
│       │   └── kanu_1210.csv
│       ├── lev5_2009/
│       │   ├── lev51270.csv
│       │   └── lev51270.pos
│       ├── lev5_2021/
│       │   ├── lev5_1280_ol.csv
│       │   └── lev5_1280_ol.pos
│       ├── lev6_2009/
│       │   ├── lev61270.csv
│       │   └── lev61270.pos
│       └── lev6_2021/
│           ├── lev6_1260.csv
│           └── lev6_1260.pos
├── code/
│   ├── figure_1c.ipynb
│   ├── figure_2.ipynb
│   ├── figure_3.ipynb
│   ├── figure_4.ipynb
│   ├── figure_5a.ipynb
│   ├── figure_6.ipynb
│   ├── figure_7.ipynb
│   ├── figure_S2.ipynb
│   └── processing/
│       ├── driving_stress_calculation.ipynb
│       ├── ice_displacement_analysis.ipynb
│       └── extract_mean_X_Y_Z_from_PPP.ipynb
└── README.md
```

## 📊 Data Availability

| Dataset | Period | Repository/Location |
| :--- | :--- | :--- | 
| Ice velocity (F003, F004) | 1996 | [Buffalo Remote Sensing Lab](https://ubwp.buffalo.edu/glyremotesensinglab/2024/05/22/mass-balance-and-velocity-data-for-greenlands-ice-sheets-at-high-elevations-data/) | 
| Ice velocity (LEV5, LEV6) | 2009–2013 | [Tedstone & Nienow (2018)](https://doi.org/10.5285/1f69fba3-4c62-47ad-8119-08cfeec05e46) |
| Ice velocity (LEV5, LEV6, KAN_U, F003, F004) | 2021–2024 | [Tedstone et al. (2026)](https://doi.org/10.5281/zenodo.18611668) |
| Vertical displacement (LEV6) | 2023 | [Tedstone et al. (2026)](https://doi.org/10.5281/zenodo.18611668) |
| Automatic weather station (KAN_M & KAN_U) | 2009-2023 | [PROMICE Network](https://www.promice.org) |
| Ice surface elevation (Porter et al. 2023) | - | `data/flowline_sampled/` |
| Bed elevation (Morlighem et al. 2022) | - | `data/flowline_sampled/` |
| PPP outputs (LEV5, LEV6, KAN_U, F003, F004) | 2009 & 2021 | `data/PPP_outputs/` |

## 📩 Queries
For questions regarding the code or data, please contact: Hannah Picton (hannah.picton@ed.ac.uk) 
