# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.4
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Calculate positioning changes between occupation periods
#
# Purposes:
#
# 1. Calculate distances between historical and reestablished sites on ~first day of occupation.
# 2. At each of LEV5 and LEV6, constrain the height change at each of these sites over the elapsed period, the horizontal baseline distance between the sites in each of the years and the resulting slope change.
# 3. (Check KAN_M snow heights as part of considering height uncertainties).
#
# This script mainly ingests outputs of the CSRS-PPP service (the .sum files). It assumes that all processing used the IGS Repro3 frame.
#
# For some historic occupations, RINEX data are not available and only a single coordinate is reported - these are hard-coded in below in the 'sites' dict.
#
# Usage:
#
# 1. Update `ANALYSIS_ROOT` as needed (the repository `data/` folder).
# 2. The PPP outputs are provided in `data/PPP_outputs/`, with the contents of each PPP zip file within its own folder (see also the file paths in the `sites` dict below).
# 3. Update `KANM_FILE` to point to `KAN_M_hour.csv` (hourly AWS data, available from PROMICE).
# 4. Outputs are saved to `data/PPP_outputs/`.
#
# Author: Andrew Tedstone, 29-30 September 2026.

# %%
import pandas as pd
from pathlib import Path
from io import StringIO
import re
import math
import numpy as np
import pyproj

# %% [markdown]
# ## Options, file paths, data

# %%
# -- PROVIDE PATHS -- #
ANALYSIS_ROOT = Path('../../data')  # UPDATE FILEPATH
PPP_ROOT = ANALYSIS_ROOT / 'PPP_outputs'
KANM_FILE = Path('.../data/KAN_M_hour.csv')  # UPDATE FILEPATH - hourly AWS data, available from PROMICE
FRAME = 'IGSR3'
CHECK_REF_FRAME = True

# All h_exppole_m values are taken from field notes and indicate distance from bottom antenna to snow surface. 
# There is no further consideration of snow depth.
sites = {
    'lev5':{
        2009: {
            'file': 'lev5_2009/lev51270',
            'h_exppole_m': 1.07 # PWN paper notes (20250623-100910-Scan_depuis_staff-geo08.pdf)
        },
        2021: {
            'file': 'lev5_2021/lev5_1280_ol',
            'h_exppole_m': 1.60 # installation_lev5.docx
        } 
    },
    'lev6':{
        2009: {
            'file': 'lev6_2009/lev61270',
            'h_exppole_m': 1.00 # PWN paper notes (20250623-100910-Scan_depuis_staff-geo08.pdf)
        },
        2021: {
            'file': 'lev6_2021/lev6_1260',
            'h_exppole_m': 2.60 # installation_lev6.docx
        }
    },
    'f003':{
        1996: {
            'latlon':[67.179997, -46.860852],
            'source':'Thomas 2000 Velocities_Data.csv'
        },
        2021: {
            'file': 'f003_2021/f003_1260'
        }
    },
    'f004':{
        1996: {
            'latlon': [66.918883, -47.029927],
            'source':'Thomas 2000 Velocities_Data.csv'
        },
        2021: {
            'file': 'f004_2021/f004_1210'
        }
    },
    'kanu':{
        2009: {
            'latlon': [67.00, -47.02],
            'source': 'Doyle 2014 p.900'
        },
        2021: {
            'file': 'kanu_2021/kanu_1210'
        }
    }      
   
}


# %% [markdown]
# ## Data loading and analysis functions

# %%
def get_sum_pos(fn):
    """ Load CSRS-PPP .sum file POS block as a dataframe for further processing. """
    with open(fn, 'r') as f:
        lines = [line for line in f if line.startswith(f'POS')]
        
    # 1-index colspecs
    colspecs = [(1,4), (5,8), (9,14), (15,27), (30,45), (48,63), (67,74), (79,85), (86,93), (94,101), (102,109)]
    # Convert to 0-index colspecs
    colspecs0 = [(c[0]-1, c[1]-1) for c in colspecs]
    headers = ['POS', 'CRD', 'SYST', 'EPOCH', 'A_PRIORI', 'ESTIMATED', 'DIFF', 'SIGMA(95%)', 'CORR1', 'CORR2', 'CORR3']
    dtypes = [str, str, str, str, str, str, float, float, float, float, float]
    
    df = pd.read_fwf(StringIO(''.join(lines)), colspecs=colspecs0, names=headers, skiprows=1, dtypes=dtypes)
    
    return df
  
def dms_to_dd(degrees, minutes, seconds, direction=None):
    """
    Converts Degrees, Minutes, Seconds to Decimal Degrees.
    Accepts directions: 'N', 'S', 'E', 'W' (case-insensitive);
    or leave as None if degrees has sign included, conversion is then handled in code.
    """
    # Calculate absolute decimal value
    degrees = float(degrees)
    
    flag = False
    if degrees < 0:
        flag = True
        degrees = degrees *-1

    if direction is not None and flag:
        raise ValueError
            
    dd = float(degrees) + float(minutes)/60 + float(seconds)/3600

    # If a negative coordinate the convert
    if flag:
        dd = -abs(dd)
        
    if direction is not None:
        # If the direction indicates Southern or Western hemisphere, negate the result
        if direction.upper() in ['S', 'W'] or float(degrees) < 0:
            dd = -abs(dd)
            
    return dd
    
def calc_pos_dd(df, key='ESTIMATED'):
    """ From the CSRS-PPP summary file POS block, convert DMS to decimal degrees

    key : by default use ESTIMATED, but can alternatively supply A_PRIORI.

    returns: tuple (lon, lat)
    """
    def _retr_dms(df, v):
        dms = df[df.CRD == v][key]
        assert len(dms) == 1
        dms = dms.iloc[0]
        dms = re.split(r"\s+", dms)
        dd = dms_to_dd(*dms)
        return dd
        
    lat = _retr_dms(df, 'LAT')
    lon = _retr_dms(df, 'LON')
    return (lon, lat)

def calc_dist(x1,y1,x2,y2):
    return np.sqrt((y2 - y1)**2 + (x2 - x1)**2)



# %% [markdown]
# ## Build coordinates table

# %%
store = []

for site in sites:
    for year in sites[site]:
        d = sites[site][year]
        
        # Set up a new row.
        row = {}   
        
        if 'file' in d:
            # Get the position block of the .sum PPP file.
            df = get_sum_pos(PPP_ROOT / f'{d["file"]}.sum')
    
            # Make sure that the reference frame is the one specified above.
            if CHECK_REF_FRAME:
                assert df['SYST'].iloc[0] == FRAME
    
            row['site'] = site
            row['year'] = year
    
            # Ellipsoidal height, then correct for exposed pole length if value provided
            row['hgt_ellps_m'] = float(df[df.CRD == 'HGT']['ESTIMATED'].iloc[0])
            if 'h_exppole_m' in d:
                row['hgt_ellps_polecorrected_m'] = row['hgt_ellps_m'] - d['h_exppole_m']
            row['hgt_sigma95_m'] = float(df[df.CRD == 'HGT']['SIGMA(95%)'].iloc[0])
    
            # Position are provided as degrees minutes seconds. 
            # Convert them to decimal degrees.
            lon, lat = calc_pos_dd(df)
            row['lon'] = lon
            row['lon_sigma95_m'] = float(df[df.CRD == 'LON']['SIGMA(95%)'].iloc[0])
            row['lat'] = lat          
            row['lat_sigma95_m'] = float(df[df.CRD == 'LAT']['SIGMA(95%)'].iloc[0])
            row['source'] = 'PPP'
        else:
            row['site'] = site
            row['year'] = year
            row['lon'] = d['latlon'][1]
            row['lat'] = d['latlon'][0]
            row['source'] = d['source']
        
        store.append(row)

coords = pd.DataFrame(store)
coords.index = [coords.site, coords.year]
coords = coords.drop(columns=['site', 'year'])

# Convert decimal degrees to EPSG3413 for distance calculations
pstere = pyproj.Proj('epsg:3413')
x,y = pstere(coords['lon'], coords['lat'])
coords['x_3413'] = x
coords['y_3413'] = y

# %%
# Calculate distances between occupations
coords['distance_x_m'] = coords.groupby(level=0)['x_3413'].diff()
coords['distance_y_m'] = coords.groupby(level=0)['y_3413'].diff()
coords['distance_m'] = np.sqrt(coords['distance_y_m']**2 + coords['distance_x_m']**2)
coords

# %%
coords.to_csv(PPP_ROOT / f'site_coords_{FRAME}_ellps_polecorrected.csv', index=False)

# %% [markdown]
# ## Calculate height changes

# %%
hchange = coords.groupby(level='site')['hgt_ellps_polecorrected_m'].diff().dropna()
hchange


# %% [markdown]
# ## Calculate Lev5-Lev6 baseline distances

# %%
def l56_baseline(yr):
    return calc_dist(
        coords.loc['lev5',yr].x_3413,
        coords.loc['lev5',yr].y_3413,
        coords.loc['lev6',yr].x_3413,
        coords.loc['lev6',yr].y_3413
    )

d09 = l56_baseline(2009)
d21 = l56_baseline(2021)

bd = pd.Series([d09, d21], index=[2009, 2021], name='lev5_lev6_distance_m')
bd.to_csv(PPP_ROOT / f'PPP_lev5_lev6_baselines_{FRAME}.csv')
bd


# %% [markdown]
# ## Slope angles

# %%
# Calculate slope between sites
def l56_slope(yr, distance):
    return (coords.loc['lev6',yr]['hgt_ellps_polecorrected_m'] - coords.loc['lev5',yr]['hgt_ellps_polecorrected_m']) / distance

s09 = l56_slope(2009, d09)
s21 = l56_slope(2021, d21)

print('2009:', math.degrees(math.atan(s09)))
print('2021:', math.degrees(math.atan(s21)))

slopes = pd.Series([s09, s21], index=[2009, 2021], name='lev5_lev6_slope')
slopes.to_csv(PPP_ROOT / f'PPP_lev5_lev6_baseline_slopes_{FRAME}.csv')

# %% [markdown]
# ## KAN_M seasonal snow heights
#
# We briefly look at these to identify the potential impact that winter snowpack accumulation by Mays 2009 and 2021 could have on the respective pole heights.

# %%
# Acquired from PROMICE.
kanm = pd.read_csv(KANM_FILE, index_col='time', parse_dates=True)

# %%
import matplotlib.pyplot as plt
plt.figure()
kanm['z_surf_combined'].plot()
plt.grid()


# %%
# September surface minima
def _sepmin(df):
    return df[df.index.month == 9].min()
mins = kanm['z_surf_combined'].resample('1A-APR').apply(_sepmin)

# Following April surface maxima, with same timestamp
def _maymax(df):
    return df[df.index.month == 4].max()
maxes = kanm['z_surf_combined'].resample('1A-APR').apply(_maymax)

# Differences
maxes - mins

# %%
mins

# %%
maxes

# %%
