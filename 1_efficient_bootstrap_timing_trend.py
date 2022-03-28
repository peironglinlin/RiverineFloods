import pandas as pd
import numpy as np
from netCDF4 import Dataset
import glob
import math

def calc_flood_timing_trend(df,aaa):
    #df: input df_doymax [nyears x nriv]
    dftmp = df[np.array(jlist),:]-df[np.array(ilist),:]
    del df
    dfk = np.zeros(dftmp.shape,dtype=np.float32)  #adjustment K for circular statistics
    dfk[dftmp>365.25/2] = -365.25/2
    dfk[dftmp<-365.25/2] = 365.25/2
    print('   ... calculated fenzi ...')
    
    #beta = (Dj-Di+k)/(j-i)
    beta = dftmp + dfk
    del dftmp,dfk
    
    #transpose beta such that division works for every element
    beta = beta.T
    beta = (beta/aaa).astype(np.float32) #division by vector (takes some time)
    print('   ... calculated fenmu ...')
    beta = np.reshape(beta,(len(beta),nn,780))
    
    #calculate median slope to get the adjusted Theil-Sen slope
    dfnew = pd.DataFrame(np.median(beta,axis=2),dtype=np.float32)
#     import pdb;pdb.set_trace()
    
    return dfnew


def random_create_index_list():
    ilist = np.random.randint(40, size=nn*780, dtype=np.int16)  #780=number of (i,j) pairs for 40-year data
    jlist = np.random.randint(40, size=nn*780, dtype=np.int16)
#     import pdb;pdb.set_trace()
    return (ilist,jlist)


def calc_aaa():
    ilist = []
    jlist = []
    for i in range(40):
        for j in range(i+1,40):
#             print(' (i,j) = (%s,%s)'%(i,j))
            ilist.append(i)
            jlist.append(j)
    aaa = np.array(jlist)-np.array(ilist)
    aaa = np.tile(aaa,nn)
    return aaa
    
if __name__ == '__main__':
    
    for myiter in range(500):  #number of bootstrap
        nn = 10 #this number changes based on max memory allowed

        #create (i,j) pair list for efficient calculation later
        ilist,jlist = random_create_index_list()  #note: change hard-coded year number and number of (i,j) pairs

        #calculate j-i
        aaa = calc_aaa()  #note: change hard-coded year number 

        for pfaf in range(1,9):  #no need for pfaf if only inputs DOYMAX
            print('... processing pfaf = %02d ...'%pfaf)
            fin = 'data/pfaf_%02d_19802019_indices.nc'%pfaf
            nc = Dataset(fin)
            doymax = nc.variables['DOYMAX'][:,:]
            doymax = doymax.astype(np.int16)
    #         df_doymax = pd.DataFrame(doymax)
            
            #DOYMAX as inputs
            data = calc_flood_timing_trend(doymax,aaa)

            #write to file
            fon = 'data/bootstrap/bootstrap_iter_%02d_pfaf_%02d.csv'%(myiter,pfaf)
            print('... writing to %s ...'%fon)
            data.to_csv(fon,index=False)
        
