import requests
import os
import sqlite3
import matplotlib.pyplot as plt 

def write_txt(data,filename):
    with open(filename, "w") as file:
        file.write(data)

def get_color_for_risk_score(score):
    if score >= 0 and score <= 2.5:
        return 'green'
    elif score > 2.5 and score <= 3.5:
        return 'yellow'
    elif score > 3.5 and score <= 4.5:
        return 'orange'
    elif score > 4.5 and score <= 5:
        return 'red'
    else:
        return 'black' 

def risk_level_avg_refugees(cur):
    cur.execute("SELECT risk_score, AVG(num_refugees) FROM country_data GROUP BY risk_score") 
    data = cur.fetchall()
    risk_score = []
    num_refugees = []

    for tup in data:
        risk_score.append(tup[0])
        num_refugees.append(tup[1])

    colors = [get_color_for_risk_score(score) for score in risk_score]

    plt.scatter(risk_score, num_refugees, c=colors, label="Num Refugees")
    plt.xlabel("Risk Scores")
    plt.ylabel("Average Number of Refugees")
    plt.title("Average Number of Refugees by Risk Scores")
    plt.legend()
    plt.show()

   
    content = "Risk Score, Average Number of Refugees\n"
    for score, avg_refugees in zip(risk_score, num_refugees):
        content += f"{score}, {avg_refugees}\n"

    write_txt(content, 'risk_level_avg_refugees.txt')


def risk_level_avg_gdp(cur):
    cur.execute("SELECT risk_score, AVG(gdp) FROM country_data GROUP BY risk_score") 
    data = cur.fetchall()
    risk_score = []
    gdp = []

    for tup in data:
        risk_score.append(tup[0])
        gdp.append(tup[1])

    colors = [get_color_for_risk_score(score) for score in risk_score]

    plt.scatter(risk_score, gdp, c=colors, label="GDP")
    plt.xlabel("Risk Scores")
    plt.ylabel("Average GDP")
    plt.title("Average GDP by Risk Scores")
    plt.legend()
    plt.show()

    content = "Risk Score, Average GDP\n"
    for score, avg_gdp in zip(risk_score, gdp):
        content += f"{score}, {avg_gdp}\n"

    write_txt(content, 'risk_level_avg_gdp.txt')

def main():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + '/'+ "final_data.db")
    cur = conn.cursor()
    risk_level_avg_refugees(cur)
    risk_level_avg_gdp(cur)

main()




