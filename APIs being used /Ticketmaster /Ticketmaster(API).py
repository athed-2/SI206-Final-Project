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

  #  response = requests.post(
   #     'https://app.ticketmaster.com/discovery/v2/events.json?countryCode=US&apikey=lBPGy21CtCmhDGnkeu87LQVQ3ANF5eh8'
  #  )
   # print(response.content)
    
    

def main():
   #read_data_from_file("Final Proj Code.py")
    response = requests.get(
        'https://app.ticketmaster.com/discovery/v2/events.json?countryCode=US&apikey=lBPGy21CtCmhDGnkeu87LQVQ3ANF5eh8'
    )
    object = json.loads(response.content)
    d = dict()
    for key in object['_embedded']['events']:
        print(key)

main()
#find and unique key to make primary key 
#event id as the outermost key of a nested dictiornary, then have a dictornary with values....