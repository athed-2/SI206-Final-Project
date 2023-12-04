import requests
import os
import sqlite3
import matplotlib.pyplot as plt 
import numpy as np

def calc_avg_risk_score_per_income_level(cur):
    lvl_one_total = 0
    lvl_two_total = 0
    lvl_three_total = 0
    lvl_four_total = 0
    cur.execute("SELECT name, risk_score, income_level FROM country_data")
    data = cur.fetchall()
    for country in data :
        if (country[2] == 1):
            lvl_one_total += float(country[1])
        elif(country[2] == 2):
            lvl_two_total += float(country[1])
        elif (country[2] == 3):
            lvl_three_total += float(country[1])
        else:
            lvl_four_total += float(country[1])

        avg_one = lvl_one_total/25
        avg_two = lvl_two_total/25
        avg_three = lvl_three_total/25
        avg_four = lvl_four_total/25
    return [avg_one, avg_two, avg_three, avg_four] #rounding

#Group By: Join Table. then Group by language.
def calc_avg_risk_score_per_language(cur):
    cur.execute("SELECT country_data.name, country_data.language_id, country_data FROM country_data JOIN LanguageTable ON country_data.type = Types.id WHERE Types.type = '{}'")

def bar_graph_risk_score(cur, conn):
    avg_risk_scores = calc_avg_risk_score_per_income_level(cur) #returns a list of the calc avg of risk_score from each income_level
    cur.execute("SELECT income_level from country_data")
    income_level = cur.fetchall()#list of values
  
    fig = plt.figure(figsize = (4, 5))
 
# creating the bar plot
    plt.bar(avg_risk_scores, income_level, color ='blue', 
            width = 0.4)
    
    plt.xlabel("Income Level")
    plt.ylabel("Average Advisory Risk Score")
    plt.title("Average Advisory Risk Score to Country Income Level")
    plt.show()

def main():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + '/'+ "final_data.db")
    cur = conn.cursor()
    bar_graph_risk_score(cur, conn)
