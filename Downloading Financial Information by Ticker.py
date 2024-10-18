import requests
import pandas as pd
import numpy as np
import openpyxl

# Replace YOUREMAIL@DOMAINNAME.com with your own email

headers = {'User-Agent': 'YOUREMAIL@DOMAINNAME.com'}

# Get all companies' CIKs

ciks = requests.get("https://www.sec.gov/files/company_tickers.json", headers = headers)
ciks_all = pd.DataFrame(ciks.json()).T
ciks_all['cik_str']=ciks_all['cik_str'].astype(str).str.zfill(10)

# Request input for the ticker symbol of a company

ticker = str(input("Please enter the company's ticker:"))
cik = ciks_all[ciks_all['ticker'] == ticker]['cik_str'].iloc[0]

# Get facts

facts = requests.get(f'https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json', headers = headers)
tags = facts.json()['facts']['us-gaap'].keys()

# Compile all downloaded facts into a DataFrame

data_all = pd.DataFrame()
data = pd.DataFrame()
dummykey = {}
key_dic = {}
for tag in tags:
    concepts = requests.get(f'https://data.sec.gov/api/xbrl/companyconcept/CIK{cik}/us-gaap/{tag}.json', headers = headers)
    condition = concepts.json()['units'].keys()
    for i in condition:
        dummykey[i]= i
        key_dic.update(dummykey)
        unit = key_dic.keys()
        for j in unit:
            if j in condition:
                data_all = pd.DataFrame(concepts.json()['units'][j])
                data_all['acct'] = tag
                data_all['unit'] = j
		data_all['ticker'] = ticker
                data = pd.concat([data, data_all],join = 'outer') 

# Save to an Excel file
data.to_csv('secfilings.csv')