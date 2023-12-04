import requests
import os
import sqlite3
import matplotlib.pyplot as plt 
import numpy as np


INCOME_TO_ID = {"High Income":1, "Upper-Middle Income": 2, "Lower-Middle Income": 3, "Low Income":4}
ID_TO_INCOME = {1:"High Income", 2:"Upper-Middle Income", 3:"Lower-Middle Income", 4:"Low Income"}


countries_by_economic_class = {
    'High Income': [
        ('USA', 'US'), ('Germany', 'DE'), ('Japan', 'JP'), ('Canada', 'CA'),
        ('Australia', 'AU'), ('United Kingdom', 'GB'), ('France', 'FR'), ('Italy', 'IT'),
        ('South Korea', 'KR'), ('Netherlands', 'NL'), ('Switzerland', 'CH'), ('Sweden', 'SE'),
        ('Singapore', 'SG'), ('Norway', 'NO'), ('Denmark', 'DK'), ('Finland', 'FI'),
        ('Austria', 'AT'), ('Belgium', 'BE'), ('Ireland', 'IE'), ('New Zealand', 'NZ'),
        ('Luxembourg', 'LU'), ('Iceland', 'IS'), ('Cyprus', 'CY'), ('Malta', 'MT'),
        ('Bahrain', 'BH')
    ],
    'Upper-Middle Income': [
        ('Brazil', 'BR'), ('China', 'CN'), ('Russia', 'RU'), ('South Africa', 'ZA'),
        ('Turkey', 'TR'), ('Mexico', 'MX'), ('Malaysia', 'MY'), ('Thailand', 'TH'),
        ('Chile', 'CL'), ('Poland', 'PL'), ('Hungary', 'HU'), ('Czech Republic', 'CZ'),
        ('Greece', 'GR'), ('Argentina', 'AR'), ('Colombia', 'CO'), ('Saudi Arabia', 'SA'),
        ('Qatar', 'QA'), ('Kuwait', 'KW'), ('United Arab Emirates', 'AE'), ('Israel', 'IL'),
        ('Portugal', 'PT'), ('Estonia', 'EE'), ('Latvia', 'LV'), ('Lithuania', 'LT'),
        ('Slovenia', 'SI')
    ],
    'Lower-Middle Income': [
        ('India', 'IN'), ('Indonesia', 'ID'), ('Philippines', 'PH'), ('Vietnam', 'VN'),
        ('Pakistan', 'PK'), ('Bangladesh', 'BD'), ('Sri Lanka', 'LK'), ('Egypt', 'EG'),
        ('Nigeria', 'NG'), ('Kenya', 'KE'), ('Ghana', 'GH'), ('Ukraine', 'UA'),
        ('Bulgaria', 'BG'), ('Romania', 'RO'), ('Morocco', 'MA'), ('Peru', 'PE'),
        ('Ecuador', 'EC'), ('Bolivia', 'BO'), ('Guatemala', 'GT'), ('El Salvador', 'SV'),
        ('Moldova', 'MD'), ('North Macedonia', 'MK'), ('Bosnia and Herzegovina', 'BA'),
        ('Armenia', 'AM'), ('Azerbaijan', 'AZ')
    ],
    'Low Income': [
        ('Afghanistan', 'AF'), ('Haiti', 'HT'), ('Nepal', 'NP'), ('Madagascar', 'MG'),
        ('Yemen', 'YE'), ('Malawi', 'MW'), ('Mozambique', 'MZ'), ('Rwanda', 'RW'),
        ('Tajikistan', 'TJ'), ('Kyrgyzstan', 'KG'), ('Lesotho', 'LS'), ('Liberia', 'LR'),
        ('Sierra Leone', 'SL'), ('Burundi', 'BI'), ('Myanmar', 'MM'), ('South Sudan', 'SS'),
        ('Chad', 'TD'), ('Burkina Faso', 'BF'), ('Niger', 'NE'), ('Central African Republic', 'CF'),
        ('Eritrea', 'ER'), ('Somalia', 'SO'), ('Djibouti', 'DJ'), ('Comoros', 'KM'),
        ('Timor-Leste', 'TL')
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

def set_up_database(db_name):
    # Takes in database name (string) as input. Returns database cursor and connection as outputs.
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def create_tables(cur):
    # Create LanguageTable
    cur.execute("CREATE TABLE IF NOT EXISTS LanguageTable (id INTEGER PRIMARY KEY, language_name TEXT UNIQUE)")

    # Create Country table with a foreign key reference to LanguageTable
    cur.execute("""
        CREATE TABLE IF NOT EXISTS country_data (
            id INTEGER PRIMARY KEY,
            name TEXT,
            isoCode TEXT UNIQUE,
            gdp NUMERIC,
            population INTEGER,
            language_id INTEGER,
            risk_score NUMERIC,
            income_level NUMERIC,
            FOREIGN KEY (language_id) REFERENCES LanguageTable(id)
        )
    """)

def populate_database(cur, conn):
    create_tables(cur)
    cur.execute("SELECT COUNT (*) FROM country_data")
    index = int(cur.fetchone()[0])
    section = ID_TO_INCOME[index // 25 + 1]
    for countryTuple in countries_by_economic_class[section]:
        countryName, isoCode = countryTuple
        countryDataApiUrl = "https://restcountries.com/v3.1/name/{}".format(countryName)
        gdpDataApiUrl = "https://api.api-ninjas.com/v1/country?name={}".format(isoCode)
        riskDataApiUrl = "https://www.travel-advisory.info/api?countrycode={}".format(isoCode)
        countryDataResponse = requests.get(countryDataApiUrl)
        gdpDataResponse = requests.get(gdpDataApiUrl, headers=gdpHeaders)
        riskDataResponse = requests.get(riskDataApiUrl)
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
            #each loop will only contain json of 1 coountry's data
            countryData = countryDataResponse.json()
            gdpData = gdpDataResponse.json()
            riskData = riskDataResponse.json()
            population = countryData[0]['population']
            language = list(countryData[0]['languages'].keys())[0]
            gdp = gdpData[0]['gdp']                    
            riskScore = riskData['data'][isoCode]['advisory']['score']
            print(countryName)
            # Extracting language information
            try:
                cur.execute("SELECT id FROM LanguageTable WHERE language_name = {}".format(language))
                language_row = cur.fetchone()
                language_id = language_row[0]
            except:
                cur.execute("INSERT OR IGNORE INTO LanguageTable (language_name) VALUES (?)", (language,))
                language_id = cur.lastrowid
                    
            # Insert data into Country table with language_id
            cur.execute("INSERT OR IGNORE INTO country_data (name, isoCode, gdp, population, language_id, risk_score, income_level) VALUES (?, ?, ?, ?, ?, ?, ?)", (countryName, isoCode, gdp, population, language_id, riskScore, INCOME_TO_ID[section]))
            index += 1
            conn.commit()
            if (index % 25 == 0):
                print("Should be done section.")
                return
                
def sanity_check():
    for section in countries_by_economic_class.keys():
        if len(countries_by_economic_class[section]) != 25:
            print("ERROR!!!", section, len(countries_by_economic_class[section]))
    print("SANITY CHECK PASSED.")
    return



def main():
    cur, conn = set_up_database('final_data.db')
    sanity_check()
    populate_database(cur,conn)


main()