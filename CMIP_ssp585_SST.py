#!/usr/bin/env python
# coding: utf-8

# In[2]:


get_ipython().run_line_magic('matplotlib', 'inline')
import numpy as np
import pandas as pd
from datetime import datetime,timedelta
from matplotlib import pyplot as plt
from netCDF4 import Dataset


# In[3]:


ds=Dataset(r'D:\UNSW\CMIP_ssp585_Oday_tos-mean.nc')
url_1="https://raw.githubusercontent.com/sydney-machine-learning/cyclonedatasets/main/SouthIndian-SouthPacific-Ocean/South_pacific_hurricane.csv"
df_1 = pd.read_csv(url_1, sep=',',error_bad_lines=False)
df_1


# In[5]:


ds


# In[9]:


df_1['Time']=pd.to_datetime(df_1['Time'],format='%Y%m%d%H')
time=ds.variables['time'][:]
lat=ds.variables['latitude'][:]
lon=ds.variables['longitude'][:]
sst=ds.variables['tos_mean_mean']
# sd=ds.variables['expver']


# In[11]:


df_1['Time']=pd.to_datetime(df_1['Time'],format='%Y%m%d%H')
time=ds.variables['time'][:]
lat=ds.variables['latitude'][:]
lon=ds.variables['longitude'][:]
sst=ds.variables['tos_mean_mean']


# In[12]:


df_1


# In[13]:


intial=1900010100
initial_date=pd.to_datetime(intial,format='%Y%m%d%H')
df_1["diff"]=df_1['Time']-initial_date
df_1


# In[14]:


df_1['total_1']=(df_1['diff']/timedelta(seconds=1))/3600
df_1['sst_1']=""


# In[18]:


for index,row in df_1.iterrows():
    latitude=row['lat_tenth']
    longitude=row['lon_tenth']
    total_1=row['total_1']

    
    diff_lat=(lat-latitude)**2
    diff_lon=(lon-longitude)**2
    diff_time=(time-total_1)**2

    
    min_lat=diff_lat.argmin()
    min_lon= diff_lon.argmin()
    min_time=diff_time.argmin()

    
    df_1.loc[index,'sst_1']=sst[min_time,min_lat,min_lon]


# In[19]:


df_1


# In[26]:


df_1.to_csv('Subs_CMIP_ssp585.csv',index=False)
with open('Subs_CMIP_ssp585.csv','r') as in_file, open('Output_sp.csv','w') as out_file:
  
    seen = set() 
    
    for line in in_file:
        if line in seen: 
          continue 

        seen.add(line)
        out_file.write(line)


# In[28]:


df = pd.read_csv('Output_sp.csv')
df


# In[29]:


for index,row in df.iterrows():
        start=df['total_1'][index]
        for days in range(1,31):
            start=start-24*days

            latitude=df['lat_tenth'][index]
            longitude=df['lon_tenth'][index]

            diff_lat=(lat-latitude)**2
            diff_lon=(lon-longitude)**2
            diff_time=(time-start)**2


            min_lat=diff_lat.argmin()
            min_lon= diff_lon.argmin()
            min_time=diff_time.argmin()



            df.loc[index,days]=sst[min_time,min_lat,min_lon] 


# In[30]:


df = df.reset_index(drop=True)


# In[31]:


df.to_csv('CMIP_ssp585_Oday_tos-mean')


# In[33]:


df = pd.read_csv('CMIP_ssp585_Oday_tos-mean.csv')


# In[34]:


df=df.drop(columns='Unnamed: 0')


# In[35]:


for index,row in df.iterrows():
    sub=0
    for weeks in range(1,5):
        sum1=0
        for days in range(1,8):
            sub+=1
            su=str(sub)
            sum1+=df[su][index]
            
        sum1=sum1/7
        s='Week'+'_'+ str(weeks)+'_'+ 'Mean'
        df.loc[index,s]=sum1


# In[37]:


from math import *


# In[38]:


for index,row in df.iterrows():
    sub1=0
    sub2=0
    for weeks in range(1,5):
        sum1=0
        sum2=0
        for days in range(1,8):
            sub1+=1
            su=str(sub1)
            sum1+=df[su][index]
            
        sum1=sum1/7
        for days in range(1,8):
            sub2+=1
            su=str(sub2)
            sum2+=(df[su][index]-sum1)*(df[su][index]-sum1)
        sum2=sum2/7
        s='Week'+'_'+ str(weeks)+'_'+ 'SD'
        df.loc[index,s]=sqrt(sum2)


# In[39]:


dict={0:[],1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[],9:[],10:[],11:[],12:[],13:[],14:[],15:[],16:[],17:[],18:[],19:[],20:[],21:[],22:[],23:[],24:[],25:[],26:[],27:[],28:[],29:[],30:[],31:[],32:[],33:[],34:[],35:[],36:[],37:[],38:[],39:[],40:[]} 
for index,row in df.iterrows():
    add=dict[df["No. of Cycl"][index]]
    add.append(df["Speed(knots)"][index])


# In[40]:


df.sort_values(["No. of Cycl"],axis=0, ascending=True,inplace=True,na_position='first')
df


# In[41]:


df['Avg_Wind_speed']=""
df['Deviation_Wind_speed']=""
for i in range(1,39):
    c=0
    d=0
    if(len(dict[i])!=0):
        for j in range(0,len(dict[i])):
            c=c+dict[i][j]
            d=d+dict[i][j]*dict[i][j]
        c=c/len(dict[i])
        d=d/len(dict[i])
        for index,row in df.iterrows():
            if(df['No. of Cycl'][index]==i):
                df.loc[index,'Avg_Wind_speed']=c
                df.loc[index,'Deviation_Wind_speed']=sqrt(d-c*c)
                break


# In[42]:


df = df.reset_index(drop=True)


# In[43]:


df.to_csv("CMIP_ssp585_with_Mean_nd_Dev.csv")


# In[ ]:




