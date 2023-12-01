import requests
import re
import os
import csv
import sqlite3
import json

countries_by_economic_class = {
    'High Income': [
        ('USA', 'US'), ('Germany', 'DE'), ('Japan', 'JP'), ('Canada', 'CA'),
        ('Australia', 'AU'), ('United Kingdom', 'GB'), ('France', 'FR'), ('Italy', 'IT'),
        ('South Korea', 'KR'), ('Netherlands', 'NL'), ('Switzerland', 'CH'), ('Sweden', 'SE'),
        ('Singapore', 'SG'), ('Norway', 'NO'), ('Denmark', 'DK'), ('Finland', 'FI'),
        ('Austria', 'AT'), ('Belgium', 'BE'), ('Ireland', 'IE')
    ],
    'Upper-Middle Income': [
        ('Brazil', 'BR'), ('China', 'CN'), ('Russia', 'RU'), ('South Africa', 'ZA'),
        ('Turkey', 'TR'), ('Mexico', 'MX'), ('Malaysia', 'MY'), ('Thailand', 'TH'),
        ('Chile', 'CL'), ('Poland', 'PL'), ('Hungary', 'HU'), ('Czech Republic', 'CZ'),
        ('Greece', 'GR'), ('Argentina', 'AR'), ('Colombia', 'CO'), ('Saudi Arabia', 'SA'),
        ('Qatar', 'QA'), ('Kuwait', 'KW'), ('United Arab Emirates', 'AE'), ('Israel', 'IL')
    ],
    'Lower-Middle Income': [
        ('India', 'IN'), ('Indonesia', 'ID'), ('Philippines', 'PH'), ('Vietnam', 'VN'),
        ('Pakistan', 'PK'), ('Bangladesh', 'BD'), ('Sri Lanka', 'LK'), ('Egypt', 'EG'),
        ('Nigeria', 'NG'), ('Kenya', 'KE'), ('Ghana', 'GH'), ('Ukraine', 'UA'),
        ('Bulgaria', 'BG'), ('Romania', 'RO'), ('Morocco', 'MA'), ('Peru', 'PE'),
        ('Ecuador', 'EC'), ('Bolivia', 'BO'), ('Guatemala', 'GT'), ('El Salvador', 'SV')
    ],
    'Low Income': [
        ('Afghanistan', 'AF'), ('Haiti', 'HT'), ('Nepal', 'NP'), ('Madagascar', 'MG'),
        ('Yemen', 'YE'), ('Malawi', 'MW'), ('Mozambique', 'MZ'), ('Rwanda', 'RW'),
        ('Tajikistan', 'TJ'), ('Kyrgyzstan', 'KG'), ('Lesotho', 'LS'), ('Liberia', 'LR'),
        ('Sierra Leone', 'SL'), ('Burundi', 'BI'), ('Myanmar', 'MM'), ('South Sudan', 'SS'),
        ('Chad', 'TD'), ('Burkina Faso', 'BF'), ('Niger', 'NE'), ('Central African Republic', 'CF')
    ]
}
gdpHeaders = {
    "X-API-Key": "RuywgWptpkNtVLBd+a4iCA==Z7iNudr1RvBuFnmj",
}

'''
https://restcountries.com/#endpoints-code - RESTCountries API (country data)
https://api-ninjas.com/api/country - ApiNinja - Sign up and get API key (gets GDP)
https://www.travel-advisory.info/data-api - Travel Advisory API (travel advisory data)
Graph income level of country to average travel advisory level 
Graph top 10 highest advisory level countries
'''

# def populateDatabase():
#     for section in countries_by_economic_class.keys():
#         for countryTuple in countries_by_economic_class[section]:
#             countryName, isoCode = countryTuple
#             countryDataApiUrl = "https://restcountries.com/v3.1/name/{}".format(countryName)
#             gdpDataApiUrl = "https://api.api-ninjas.com/v1/country?name={}".format(countryName)
#             riskDataApiUrl = "https://www.travel-advisory.info/api?countrycode={}".format(isoCode)
#             countryDataResponse = requests.get(countryDataApiUrl)
#             gdpDataResponse = requests.get(gdpDataApiUrl, headers=gdpHeaders)
#             riskDataResponse = requests.get(riskDataApiUrl)
#             if countryDataResponse.status_code != 200:
#                 print("Country API didn't work. Check country name.", countryName)
#                 return
#             elif gdpDataResponse.status_code != 200:
#                 print("GDP Data API didn't work. Check country name.", countryName)
#                 return
#             elif riskDataResponse.status_code != 200:
#                 print("Risk Data API didn't work. Check ISO code.", countryName)
#                 return
#             else:
#                 countryData = countryDataResponse.json()
#                 print(countryData)
#                 gdpData = gdpDataResponse.json()
#                 riskData = riskDataResponse.json()
#                 input(countryData[0]["population"])
#     return

def populateDatabase():
    for section in countries_by_economic_class.keys():
        for countryTuple in countries_by_economic_class[section]:
            countryName, isoCode = countryTuple
            countryDataApiUrl = "https://restcountries.com/v3.1/name/{}".format(countryName)
            gdpDataApiUrl = "https://api.api-ninjas.com/v1/country?name={}".format(countryName)
            riskDataApiUrl = "https://www.travel-advisory.info/api?countrycode={}".format(isoCode)
            countryDataResponse = requests.get(countryDataApiUrl)
            gdpDataResponse = requests.get(gdpDataApiUrl, headers=gdpHeaders)
            riskDataResponse = requests.get(riskDataApiUrl)
            
            jsonCountryData = json.loads(riskDataApiUrl.content)
            jsonGDP = json.loads(riskDataApiUrl.content)
            jsonRiskData = json.loads(riskDataApiUrl.content)
            


            if countryDataResponse.status_code != 200:
                print("Country API didn't work. Check country name.", countryName)
                return
            elif gdpDataResponse.status_code != 200:
                print("GDP Data API didn't work. Check country name.", countryName)
                return
            elif riskDataResponse.status_code != 200:
                print("Risk Data API didn't work. Check ISO code.", countryName)
                return
            else:
                countryData = countryDataResponse.json()
                print(countryData)
                gdpData = gdpDataResponse.json()
                riskData = riskDataResponse.json()
                input(countryData[0]["population"])
    return

def setUpDatabase(db_name):
    # Takes in database name (string) as input. Returns database cursor and connection as outputs.
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn


populateDatabase()