#!/usr/bin/env python
# coding: utf-8

# In[3]:


get_ipython().system('pip install scikit-learn==1.0.2')


# In[11]:


import pickle
import pandas as pd
import numpy as np


# In[6]:


with open('model.bin', 'rb') as f_in:
    dv, lr = pickle.load(f_in)


# In[7]:


categorical = ['PUlocationID', 'DOlocationID']

def read_data(filename):
    df = pd.read_parquet(filename)
    
    df['duration'] = df.dropOff_datetime - df.pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    
    return df


# In[8]:


df = read_data('../data/fhv_tripdata_2021-02.parquet')


# In[9]:


dicts = df[categorical].to_dict(orient='records')
X_val = dv.transform(dicts)
y_pred = lr.predict(X_val)


# ## Q1. Notebook
# Run this notebook for the February 2021 FVH data.
# 
# What's the mean predicted duration for this dataset?
# 
# - 11.19
# - 16.19
# - 21.19
# - 26.19

# In[13]:


print(f"The mean predicted duration for this dataset is {np.mean(y_pred)}")


# ## Q2. Preparing the output
# 
# Like in the course videos, we want to prepare the dataframe with the output.
# 
# First, let's create an artificial ride_id column:

# In[17]:


year = 2021
month = 2


# In[18]:


df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')


# Next, write the ride id and the predictions to a dataframe with results.

# In[20]:


df_result = df.copy(deep=True)


# In[31]:


df_result.drop(df_result.columns.difference(['ride_id']), 1, inplace=True)


# In[36]:


df_result["predictions"] = y_pred


# In[37]:


df_result.to_parquet(
    "../data/results.parquet",
    engine='pyarrow',
    compression=None,
    index=False
)


# ## Q3. Creating the scoring script
# 

# Now let's turn the notebook into a script.
# 
# Which command you need to execute for that?

# **Answer**: 

# ```
# jupyter nbconvert --to script homework_answrs.ipynb
# ```

# In[ ]:




