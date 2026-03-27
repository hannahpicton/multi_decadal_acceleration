# multi_decadal_acceleration
Code associated with the manuscript 'Ice surface steepening drives multi-decadal acceleration of the Greenland Ice Sheet interior', submitted for peer-review in April 2026.

## 📁 Repository Structure
```text
├── data/
│   └── flowline_sampled/
│       ├── arcticDEM_v4_sampled_100m.csv
│       └── bedMachine_v5_sampled_150m.csv
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
