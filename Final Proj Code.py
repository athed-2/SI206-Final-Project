import requests
import json
import unittest
import os
import math
import matplotlib.pyplot as plt


###########################################
# Your name: Melissa Wang                 #
# Who you worked with:                    #
###########################################

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

    url = ('https://api.currentsapi.services/v1/latest-news?'
        'language=us&'
        'apiKey=3tKwqe2XNq2v5Uq1Ku_tgAgO-YoXodmS2NNSyO1M-9iijDS5')
    response = requests.get(url)
    print(response.json())

    full_path = os.path.join(os.path.dirname(__file__), filename)
    f = open(full_path)
    file_data = f.read()
    f.close()
    json_data = json.loads(file_data)
    return json_data

def main():
   pass