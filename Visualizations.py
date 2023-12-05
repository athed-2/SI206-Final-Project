import requests
import os
import sqlite3
import matplotlib.pyplot as plt 

def calc_avg_risk_score_per_income_level(cur):
    lvl_one_total = 0
    lvl_two_total = 0
    lvl_three_total = 0
    lvl_four_total = 0
    cur.execute("SELECT name, risk_score, income_level FROM country_data")
    data = cur.fetchall()
   # print(data)
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

    return [round(avg_one,3), round(avg_two,3), round(avg_three,3), round(avg_four,3)]

#Group By: Join Table. then Group by language.
# def calc_avg_risk_score_per_language(cur):
#     cur.execute("SELECT country_data.name, country_data.language_id, country_data FROM country_data JOIN LanguageTable ON country_data.language_id = LanguageTable.id")
#     data = cur.fetchall()
#     for country in data:
#         pass

def bar_graph_risk_score(cur, conn):
    avg_risk_scores = calc_avg_risk_score_per_income_level(cur) #returns a list of the calc avg of risk_score from each income_level
    cur.execute("SELECT DISTINCT income_level from country_data")
    income_level = cur.fetchall()
    income_level_num = []
    for tup in income_level:
        income_level_num.append(int(tup[0]))
# creating the bar plot
    fig, ax = plt.subplots()
    ax.bar(income_level_num, avg_risk_scores) 
    ax.set_xticks(income_level_num)
    ax.set_xlabel("Income Level")
    ax.set_ylabel("Average Advisory Risk Score")
    ax.set_title("Average Advisory Risk Score to Country Income Level")
    plt.show()

def main():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + '/'+ "final_data.db")
    cur = conn.cursor()
    calc_avg_risk_score_per_income_level(cur)
    bar_graph_risk_score(cur, conn)

main()
