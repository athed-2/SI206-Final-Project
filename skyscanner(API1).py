import requests
import json
import unittest
import os
import math
import matplotlib.pyplot as plt

def read_data_from_file(filename):
    """
    Reads data from a file with the given filename.

    Parameters
    -----------------------
    filename: str
        The name of the file to read.

    Returns
    -----------------------
    dict:
        Parsed JSON data from the file.
    """

    


    headers = {
        'x-api-key': 'sh428739766321522266746152871799',
        'content-type': 'application/x-www-form-urlencoded',
    }

    data = '{ "query": { "market": "UK", "locale": "en-GB", "currency": "GBP", "queryLegs": [{ "originPlace": { "queryPlace": { "iata": "LHR" } }, "destinationPlace": { "queryPlace": { "iata": "LAX" } }, "anytime": true }] } }'

    response = requests.post(
        'https://partners.api.skyscanner.net/apiservices/v3/flights/indicative/search',
        headers=headers,
        data=data,
    )
    print(response.content)
    
    return None

def main():
   read_data_from_file("Final Proj Code.py")

main()