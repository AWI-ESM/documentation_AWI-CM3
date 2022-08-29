#!/scratch/users/stepanek/bin/anaconda3/bin/python3

#Produces plots towards a comparison of PI insolation in ECHAM6 and openIFS.
#There are five sections to this script:
#1. For reference, insolation is computed for 1850 based on PMIP4 orbital settings.
#   In this case, orbital elements are documented for PI by Otto-Bliesner et al., (2017),
#   and daily insolation is computed based on the function daily_insolation of the
#   python package climlab.
#2. The insolation for openIFS (file atm_remapped_1m_tisr_1m_1850-1850.nc, monthly means)
#   is plotted as is from the model output. The data stems from a simulation provided by
#   Jan Streffing.
#3. The insolation for ECHAM6 (file mpiesm_PI_ctrl_ham_CMIP6_output_echam6_echamday_1850_srad0d.nc,
#   daily means) is plotted as is from the model output. The data stems from the control run
#   performed for PMIP4 Last Interglacial simulation (Scussolini et al., 2019;
#   Scussolini et al. 2020; Otto-Bliesner et al., 2021).
#4. As per section 3, but towards comparability with the monthly mean insolation of openIFS,
#   the insolation for ECHAM6 is re-plotted from a) monthly means, that have been computed
#   using CDO, and b) interpolated to the openIFS resolution for the computation of an anomaly.
#5. The anomaly openIFS minus ECHAM6 is computed and plotted based on the monthly average ECHAM6
#   isolation that has been interpolated to the resolution of openIFS.
#
#references:
#Otto-Bliesner et al., The PMIP4 contribution to CMIP6 – Part 2: Two interglacials, scientific objective and experimental design for Holocene and Last Interglacial simulations, Geoscientific Model Development, 10, 3979-4003, 2017. 
#Otto-Bliesner et al., Large-scale features of the Last Interglacial climate: results from evaluating the lig127k simulations for the Coupled Model Intercomparison Project (CMIP6)-Paleoclimate Model Intercomparison Project (PMIP4), Climate of the Past, 17(1), 63-94, 2021.
#Scussolini et al., Agreement between reconstructed and modeled boreal precipitation of the Last Interglacial, Science Advances, 5(11), eaax7047, 2019.
#Scussolini et al., Global River Discharge and Floods in the Warmer Climate of the Last Interglacial, Goephysical Research Letters, 47, e2020G, 2020.


#Christian Stepanek, Alfred Wegener Institute, 29th of August 2022


#load relevant packages
import numpy as np
import matplotlib.pyplot as plt
from climlab import constants as const
from climlab.solar.insolation import daily_insolation
import matplotlib.colors as colors
from netCDF4 import Dataset


#define time vector for mid-month days
days_midmonth = [16, 46, 75, 106, 136, 167, 197, 228, 259, 289, 320, 350]
days=range(1,366,1)




#%%Section 1: Create insolation plot based on orbital parameters for PI


#get latitudes from the openIFS data set of insolation to compute
#PI insolation at exactly these latitudes
data=Dataset("atm_remapped_1m_tisr_1m_1850-1850.nc")
lat=data.variables['lat'][:]
lon=data.variables['lon'][:]


#define array for insolation and define the orbital parameters for PI
Q_1850=np.zeros((np.shape(lat)[0],np.shape(days_midmonth)[0]))
orb_1850={'ecc': 0.016764, 'long_peri': 100.33, 'obliquity': 23.459}


#compute insolation in a loop over time and latitude
for t in range(np.shape(days_midmonth)[0]):
  print("working on day "+str(t))
  for l in range(np.shape(lat)[0]):
    Q_1850[l,t] = daily_insolation(lat[l], days_midmonth[t], orb_1850)


#define plot parameters
level_min=0
level_max=600
stepsize=20
levels=np.arange(level_min,level_max+stepsize,stepsize)
cmap=colors.LinearSegmentedColormap.from_list('mycmap', 
     ['blue', 'cornflowerblue', 'aqua', 'lightcyan', 'white', 'yellow', 'orange', 'red', 'maroon'],
     (level_max-level_min)/stepsize+1) #+1 adds one level for the center


#plot PI insolation
fig, ax = plt.subplots()
hc=ax.contourf(days_midmonth,lat,Q_1850, cmap=cmap, levels=levels, vmin=level_min-.5, vmax=level_max+.5, extend='both')
ax.set_ylim(-90,90); ax.set_yticks([-90,-60,-30,-0,30,60,90])
ax.set_xlim(1,365); ax.set_xticks([30,60,90,120,150,180,210,240,270,300,330,360])
ax.set_ylabel('Latitude')
ax.set_xlabel('day of year')
plt.colorbar(hc,label="W/m²")
ax.grid()
ax.set_title('Daily average insolation PI (PMIP4)')
plt.savefig("insolation_absolute_PI_PMIP4.png")




#%%Section 2: Create plot of insolation as computed by openIFS for PI


#load data from netCDF
data=Dataset("atm_remapped_1m_tisr_1m_1850-1850.nc")
lat=data.variables['lat'][:]
lon=data.variables['lon'][:]
tisr=data.variables['tisr'][:]


#plot PI insolation reusing the plot parameters defined at section 1
#physical unit of insolation is converted from Joules / m² to Watts / m²
#considering the accumulation period of 6 hours applied by openIFS
#(division by 3600 s per hour and by 6 hours)
fig, ax = plt.subplots()
hc=ax.contourf(days_midmonth,lat,np.transpose(np.mean(tisr,axis=2))/3600/6, cmap=cmap, levels=levels, vmin=level_min-.5, vmax=level_max+.5, extend='both')
ax.set_ylim(-90,90); ax.set_yticks([-90,-60,-30,-0,30,60,90])
ax.set_xlim(1,365); ax.set_xticks([30,60,90,120,150,180,210,240,270,300,330,360])
ax.set_ylabel('Latitude')
ax.set_xlabel('day of year')
plt.colorbar(hc,label="W/m²")
ax.grid()
ax.set_title('monthly average insolation PI openIFS')
plt.savefig("insolation_absolute_PI_openIFS.png")




#%%Section 3: Create plot of insolation as computed by MPI-ESM for PI


#load data from netCDF
data=Dataset("mpiesm_PI_ctrl_ham_CMIP6_output_echam6_echamday_1850_srad0d.nc4c")
lat=data.variables['lat'][:]
lon=data.variables['lon'][:]
srad0d=data.variables['srad0d'][:]


#plot PI insolation reusing the plot parameters defined at section 1
fig, ax = plt.subplots()
z=np.transpose(np.mean(srad0d,axis=2))
hc=ax.contourf(days,lat,z, cmap=cmap, levels=levels, vmin=level_min-.5, vmax=level_max+.5, extend='both')
ax.set_ylim(-90,90); ax.set_yticks([-90,-60,-30,-0,30,60,90])
ax.set_xlim(1,365); ax.set_xticks([30,60,90,120,150,180,210,240,270,300,330,360])
ax.set_ylabel('Latitude')
ax.set_xlabel('day of year')
plt.colorbar(hc,label="W/m²")
ax.grid()
ax.set_title('Daily average insolation PI ECHAM6')
plt.savefig("insolation_absolute_PI_ECHAM6_daily.png")




#%%Section 4: Create plot of insolation as computed by MPI-ESM for PI,
#             but now as a monthly average and interpolated to the
#             grid-resolution of openIFS


#load data from netCDF
data=Dataset("mpiesm_PI_ctrl_ham_CMIP6_output_echam6_echamday_1850_srad0d_monmean_remapped.nc")
lat=data.variables['lat'][:]
lon=data.variables['lon'][:]
srad0d=data.variables['srad0d'][:]


#plot PI insolation reusing the plot parameters defined at section 1
fig, ax = plt.subplots()
z=np.transpose(np.mean(srad0d,axis=2))
hc=ax.contourf(days_midmonth,lat,z, cmap=cmap, levels=levels, vmin=level_min-.5, vmax=level_max+.5, extend='both')
ax.set_ylim(-90,90); ax.set_yticks([-90,-60,-30,-0,30,60,90])
ax.set_xlim(1,365); ax.set_xticks([30,60,90,120,150,180,210,240,270,300,330,360])
ax.set_ylabel('Latitude')
ax.set_xlabel('day of year')
plt.colorbar(hc,label="W/m²")
ax.grid()
ax.set_title('Monthly average insolation PI ECHAM6')
plt.savefig("insolation_absolute_PI_ECHAM6_monthly.png")




#%%Section 5: Create plot of PI insolation anomaly as computed by MPI-ESM
#             vs. openIfs


#define plot parameters
level_min=-1
level_max=1
stepsize=0.1
levels=np.arange(level_min,level_max+stepsize,stepsize)
cmap=colors.LinearSegmentedColormap.from_list('mycmap', 
     ['blue', 'cornflowerblue', 'aqua', 'lightcyan', 'white', 'yellow', 'orange', 'red', 'maroon'],
     (level_max-level_min)/stepsize+1) #+1 adds one level for the center


#plot PI insolation anomaly openIFS vs. ECHAM6
fig, ax = plt.subplots()
z=np.transpose(np.mean(tisr,axis=2))/3600/6-np.transpose(np.mean(srad0d,axis=2))
hc=ax.contourf(days_midmonth,lat,z, cmap=cmap, levels=levels, vmin=level_min-.5, vmax=level_max+.5, extend='both')
ax.set_ylim(-90,90); ax.set_yticks([-90,-60,-30,-0,30,60,90])
ax.set_xlim(1,365); ax.set_xticks([30,60,90,120,150,180,210,240,270,300,330,360])
ax.set_ylabel('Latitude')
ax.set_xlabel('day of year')
plt.colorbar(hc,label="W/m²")
ax.grid()
ax.set_title('insolation anomaly PI, openIFS - ECHAM6')
plt.savefig("insolation_anomaly_PI_openIFS-ECHAM6_monthly.png")
