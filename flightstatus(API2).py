<<<<<<< Updated upstream
=======
#Audrey
>>>>>>> Stashed changes
import requests
import json
import unittest
import os
import math
import matplotlib.pyplot as plt

<<<<<<< Updated upstream
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

    url = ('https://api.traveltimeapp.com/v4/time-filter'
        'apiKey=8dd3b29c0e475934424a9f54446aee3f''appId=9955bc4d')
=======

###########################################
#Group: Melissa Wang, Emma Sternquist, Audrey Thedford             #
###########################################
def read_data_from_file(filename):

    url = ('https://partners.api.skyscanner.net/apiservices/v3/flights/indicative/search')
>>>>>>> Stashed changes
    response = requests.get(url)
    print(response.json())

    full_path = os.path.join(os.path.dirname(__file__), filename)
    f = open(full_path)
    file_data = f.read()
    f.close()
    json_data = json.loads(file_data)
<<<<<<< Updated upstream
    return json_data

def main():
   pass
=======
    print(json_data)
    return  json_data


>>>>>>> Stashed changes
