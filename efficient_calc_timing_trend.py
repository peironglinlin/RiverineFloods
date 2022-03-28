import pandas as pd
import numpy as np
from netCDF4 import Dataset
import glob
import math

def calc_flood_timing_trend(df):
    #df: input df_doymax [nyears x nriv]
    dftmp = df[np.array(jlist),:]-df[np.array(ilist),:]
    dfk = np.zeros(dftmp.shape)  #adjustment K for circular statistics
    dfk[dftmp>365.25/2] = -365.25/2
    dfk[dftmp<-365.25/2] = 365.25/2
    
    #beta = (Dj-Di+k)/(j-i)
    beta = dftmp + dfk
    aaa = np.array(jlist)-np.array(ilist)
    beta = beta/aaa[:,np.newaxis]  #division by vector (online search result)
       
    #calculate median slope to get the adjusted Theil-Sen slope
    dfnew = pd.DataFrame({'beta':np.median(beta,axis=0)})
    
    return dfnew

def create_index_list():
    ilist = []
    jlist = []
    for i in range(40):
        for j in range(i+1,40):
            print(' (i,j) = (%s,%s)'%(i,j))
            ilist.append(i)
            jlist.append(j)
    return (ilist,jlist)
    
if __name__ == '__main__':
    #create (i,j) pair list for efficient calculation later
    ilist,jlist = create_index_list()
    
    for pfaf in range(1,9):
        print('... processing pfaf = %02d ...'%pfaf)
        fin = 'data/pfaf_%02d_19802019_indices.nc'%pfaf
        nc = Dataset(fin)
        doymax = nc.variables['DOYMAX'][:,:]
#         df_doymax = pd.DataFrame(doymax)
        
        breakpoint()
        data = calc_flood_timing_trend(doymax)
        
        #write to file
        fon = 'data/flood_timing_trend_pfaf_%02d.csv'%pfaf
        print('... writing to %s ...'%fon)
        data.to_csv(fon,index=False)
        
