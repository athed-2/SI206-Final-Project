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

# Refugees, GDP, Travel Risk

def get_color(avg_risk_score):
    if avg_risk_score >= 4.5:
        return "red"
    elif 3.5 <= avg_risk_score < 4.5:
        return "orange"
    elif 2.5 <= avg_risk_score < 3.5:
        return "yellow"
    elif 0 <= avg_risk_score < 2.5:
        return "green"

def bar_graph_risk_score(cur, conn):
    avg_risk_scores = calc_avg_risk_score_per_income_level(cur) #returns a list of the calc avg of risk_score from each income_level
    cur.execute("SELECT DISTINCT income_level from country_data")
    income_level = cur.fetchall()
    income_level_num = []
    for tup in income_level:
        income_level_num.append(int(tup[0]))

    colors = [get_color(score) for score in avg_risk_scores]
    # Creating the bar plot
    fig, ax = plt.subplots()
    bars = ax.bar(income_level_num, avg_risk_scores, color=colors)

    # Adding color legend
    legend_labels = ["0-2.5 (Safe)", "2.5-3.5 (Medium Risk)", "3.5-4.5 (High Risk)", "4.5-5 (Extreme Warning)"]
    legend = ax.legend(bars, legend_labels, loc = "upper left", bbox_to_anchor=(1, 1), title="Risk Category")
    ax.set_xticks(income_level_num)
    ax.set_xlabel("Income Level")
    ax.set_ylabel("Average Advisory Risk Score")
    ax.set_title("Average Advisory Risk Score to Country Income Level")
    plt.subplots_adjust(right=0.7)
    plt.show()

def main():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + '/'+ "final_data.db")
    cur = conn.cursor()
    calc_avg_risk_score_per_income_level(cur)
    bar_graph_risk_score(cur, conn)

main()
