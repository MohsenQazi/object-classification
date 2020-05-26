#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import json
import pandas as pd


# In[2]:


def sample(r1,r2,d1,d2,n,clas):
    
    url = "http://skyserver.sdss.org/dr16/en/tools/search/x_sql.aspx"
    payload = {
        "format": "json",
        "cmd": """
            SELECT top {0} s.class, s.z, s.ra, s.dec,
                p.deVRad_u, p.deVRad_g, p.deVRad_r, p.deVRad_i, p.deVRad_z,
                p.dered_u, p.dered_g, p.dered_r, p.dered_i, p.dered_z,
                p.extinction_u, p.extinction_g, p.extinction_r, p.extinction_i, p.extinction_z
            FROM SpecObjAll s JOIN PhotoObjAll p ON s.specObjID = p.specObjID
            WHERE s.class='{5}' and p.clean = 1 and s.zWarning = 0
                AND s.ra between {1} and {2}
                AND p.dec between {3} and {4}
        """.format(n,r1,r2,d1,d2,clas).strip()
    }
    
    try:
        resp = requests.post(url, params=payload, timeout=600)
    except requests.exceptions.RequestException as e:
        print(e)
        return None

    data = resp.json()[0]['Rows']
    df = pd.DataFrame(data)

    return df


# In[12]:


r1, r2, d1, d2, n, clas = input('enter coordinates, number and class: ').split()
df = sample(r1,r2,d1,d2,n,clas)
df.to_csv("{0}[{1}-{2}].csv".format(clas,r1,r2), index=False)

