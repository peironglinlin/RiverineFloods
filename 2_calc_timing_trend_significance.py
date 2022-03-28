import pandas as pd
import numpy as np
import glob
import math

def calc_p_value(df,df0):
    x = df0.values.T
    x0 = df.beta.values
    count = np.logical_or(x>=np.abs(x0),x<=-np.abs(x0)) #two-tailed
    df['p_value'] = np.sum(count,axis=0)/500
    return df

    
if __name__ == '__main__':
    
    for pfaf in range(1,9):
        print('... processing pfaf = %02d ...'%pfaf)
        
        #calculated trend based on median slope
        df = pd.read_csv('data/flood_timing_trend_pfaf_%02d.csv'%pfaf)
        #calculated trend based on bootstrap for n times (here n=500; normally n needs to be 1000+, but 500 is acceptable with computational constraints)
        df0 = pd.read_csv('data/bootstrap/combined_pfaf_%02d.csv'%pfaf)
#         import pdb;pdb.set_trace()
                
        data = calc_p_value(df,df0)
        
        #write to file
        fon = 'data/flood_timing_trend_pfaf_%02d.csv'%pfaf
        print('... writing to %s ...'%fon)
        data.to_csv(fon,index=False)
        
