# Contains the subroutines to manipulate data.

# Jon Parsons
# 12-15-2020

import json
import pandas as pd
import numpy as np
import plotly.express as px

from datetime import datetime

################################################################################
def add_job(applied_list,company,date,type,location):
## Adds a new job to the jobs applied for. Returns updated input.
# applied_list : dict with job application entries
# company : name of company applied for, str
# data : date applied, str
# type : type of job, str
# location : city of job, str

    job_num = len(applied_list['jobs'])
    applied_list['jobs'].append({
        'JID': job_num,
        'Company': company,
        'Applied': date,
        'Type': type,
        'Location': location,
    })

    return applied_list

################################################################################
def update_job(applied_list,job_id,key,val):
## updates an existing application
# applied_list : dict with job entries
# job_id : primary key of job to update, int
# key : new key to add
# val : value to set new key to, string

    for job in applied_list['jobs']:
        if job['Job ID'] == job_id:
            job.update({key:val})

    return applied_list

################################################################################
def load_data(f_name):
## subroutine to load in the saved job data as a dataframe
# f_name : name of file to open, str
    loaded_data = pd.read_json(f_name,orient='index')

    return loaded_data

################################################################################
def save_data(f_name,data):
## subroutine to save data as a json file
# f_name : name of file to save to, overwritten, str
    if isinstance(data, pd.DataFrame):
        data.to_json(f_name,orient='index')
    else:
        with open(f_name,'w') as FO:
            json.dump(data, FO, indent=3)

    return

################################################################################
def days_since(df):
## returns the horizontal bar graph with the number of days since applying to a job
# df : pandas dataframe with the data

    today = datetime.now()

    df['Days'] = (today-pd.to_datetime(df['Applied']))/np.timedelta64(1,'D')

    avg = df['Days'].mean()

    hbar = px.bar(
        df,x='Days',y='JID',
        color='Company',
        orientation='h',
        title="<b>Number of Days Since Application</b><br>Average: {:.2f} Days".format(avg)
        ).update(
                layout=dict(title=dict(x=0.5))
                )

    return hbar

################################################################################
def insert_new_job(df,company,applied,type,location,data_file):
## adds new job data to the dataframe
# original job list
# df : pandas dataframe with the data
# company : company applied for, str
# applied : date applied, date
# type : type of job applied for, str
# location : city job is in, str

    job_num = len(df.index)+1
    ndf = pd.DataFrame({
        'JID': [job_num],
        'Company': [company],
        'Applied': [applied],
        'Type': [type],
        'Location': [location],
    })
    df = df.append(ndf, ignore_index=True)
    save_data(data_file,df)
    df = load_data(data_file)

    return df
