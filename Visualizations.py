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


def get_risk_color(avg_risk_score):
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

    colors = [get_risk_color(score) for score in avg_risk_scores]
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

def calc_avg_population_per_income_level(cur):
    lvl_one_total_pop = 0
    lvl_two_total_pop = 0
    lvl_three_total_pop = 0
    lvl_four_total_pop = 0

    coutries_in_lvl_1 =0
    coutries_in_lvl_2 =0
    coutries_in_lvl_3 =0
    coutries_in_lvl_4 =0

    cur.execute("SELECT name, population, income_level, risk_score FROM country_data")
    data = cur.fetchall()
    #print(data)
    #Find average population by income level
    for items in data :
        if (items[2] == 1):
            lvl_one_total_pop += float(items[1])
            coutries_in_lvl_1 += 1
        elif(items[2] == 2):
            lvl_two_total_pop += float(items[1])
            coutries_in_lvl_2 += 1
        elif (items[2] == 3):
            lvl_three_total_pop += float(items[1])
            coutries_in_lvl_3 += 1
        else:
            lvl_four_total_pop += float(items[1])

            coutries_in_lvl_4 += 1

    avg_pop_one = lvl_one_total_pop/coutries_in_lvl_1
    avg_pop_two = lvl_two_total_pop/coutries_in_lvl_2
    avg_pop_three = lvl_three_total_pop/coutries_in_lvl_3
    avg_pop_four = lvl_four_total_pop/coutries_in_lvl_4
  
    
#Found average pop and risk score by income level 
    #print((avg_pop_one,round(avg_risk_score_one,3)),(avg_pop_two,round(avg_risk_score_two,3)),(avg_pop_three,round(avg_risk_score_three,3)),(avg_pop_four,round(avg_risk_score_four,3)))
    return (avg_pop_one, avg_pop_two,avg_pop_three, avg_pop_four)

def bar_graph_pop_risk_score_by_income_lvl(cur, conn):
    avg_populations = calc_avg_population_per_income_level(cur) #returns a list of the calc avg of population from each income_level
    avg_risk_scores = calc_avg_risk_score_per_income_level(cur) #return a list of risk sore by income level 
    cur.execute("SELECT DISTINCT income_level from country_data")
    income_level = cur.fetchall()
    income_level_num = []
    for tup in income_level:
        income_level_num.append(int(tup[0]))

    #colors = [get_risk_color(score) for score in avg_risk_scores]
    # Creating the bar plot
    fig, ax = plt.subplots()
    bars = ax.bar(income_level_num, avg_populations)

    # Adding color legend
   # legend_labels = ["0-2.5 (Safe)", "2.5-3.5 (Medium Risk)", "3.5-4.5 (High Risk)", "4.5-5 (Extreme Warning)"]
  #  legend = ax.legend(bars, legend_labels, loc = "upper left", bbox_to_anchor=(1, 1), title="Risk Category")
    ax.set_xticks(income_level_num)
    #ax.set_yticks(40000000,60000000,80000000,100000000)

    ax.set_xlabel("Income Level")
    ax.set_ylabel("Average Population")
    ax.set_title("Average Population to Country Income Level")
    plt.subplots_adjust(right=0.7)
    plt.show()

def risk_level_avg_refugees(cur):
    cur.execute("SELECT risk_score, AVG(num_refugees) FROM country_data GROUP BY risk_score") 
    data = cur.fetchall()
    risk_score = []
    num_refugees = []

    for tup in data:
        risk_score.append(tup[0])
        num_refugees.append(tup[1])

    plt.bar(risk_score, num_refugees, label = "Num Refugees")
    plt.xticks(risk_score)
    plt.xlabel("Risk Scores")
    plt.ylabel("Average Number of Refugees")
    plt.title("Average Number of Refugees by Risk Scores")
    plt.show()

def risk_level_avg_gdp(cur):
    cur.execute("SELECT risk_score, AVG(gdp) FROM country_data GROUP BY risk_score") 
    data = cur.fetchall()
    risk_score = []
    gdp = []

    for tup in data:
        risk_score.append(tup[0])
        gdp.append(tup[1])

    plt.bar(risk_score, gdp, label = "GDP")
    plt.xticks(risk_score)
    plt.xlabel("Risk Scores")
    plt.ylabel("Average GDP")
    plt.title("Average GDP by Risk Scores")
    plt.show()




def main():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + '/'+ "final_data.db")
    cur = conn.cursor()
    #calc_avg_risk_score_per_income_level(cur)
    #calc_avg_population_per_income_level(cur)
    #bar_graph_risk_score(cur, conn)
    #bar_graph_pop_risk_score_by_income_lvl(cur,conn)
    risk_level_avg_refugees(cur)
    risk_level_avg_gdp(cur)


main()

#The number of refugees, to GDP, to travel risk
#Determine which countries are in the extreme risk, high risk, medium risk, low risk 
#Compare with mean number of refugees
#And average GDP 





