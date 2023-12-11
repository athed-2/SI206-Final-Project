import requests
import os
import sqlite3
import matplotlib.pyplot as plt 


def write_txt(data, filename):
    with open(filename,"w") as file:
        file.write(data)
        file.close()
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

    avg_pop_one = (lvl_one_total_pop/coutries_in_lvl_1)/1000000
    avg_pop_two = (lvl_two_total_pop/coutries_in_lvl_2)/1000000
    avg_pop_three = (lvl_three_total_pop/coutries_in_lvl_3)/1000000
    avg_pop_four = (lvl_four_total_pop/coutries_in_lvl_4)/1000000
    results = f'Average population of incoome level 1:{avg_pop_one},Average population of incoome level 2:{avg_pop_two},Average population of incoome level 3:{avg_pop_three},Average population of incoome level 4:{avg_pop_four}'
    
    write_txt(results,'Average Country Population by Income Level')
    return (avg_pop_one, avg_pop_two,avg_pop_three, avg_pop_four)

def get_pop_color(avg_populations):
    if avg_populations < 38:
        return "blue"
    elif 38 <= avg_populations < 42:
        return "green"
    else:
        return "purple"

def bar_graph_pop_by_income_lvl(cur, conn):
    avg_populations = calc_avg_population_per_income_level(cur) #returns a list of the calc avg of population from each income_level
    cur.execute("SELECT DISTINCT country_data.income_level, IncomeClass.income_class FROM country_data JOIN IncomeClass ON country_data.income_level = IncomeClass.id")
    conn.commit()
    income_level = cur.fetchall()
    income_class = []
    for tup in income_level:
        income_class.append(tup[1])
    colors = [get_pop_color(pop) for pop in avg_populations]
    
    fig, ax = plt.subplots()
    bars = ax.bar(income_class, avg_populations, color=colors)
    #Legend
    colors = {'<38 (Below Average)':'blue', '39-42 (Average)':'green', '>43 (Above Average)':'purple'}         
    labels = list(colors.keys())
    handles = [plt.Rectangle((0,0),1,1, color=colors[label]) for label in labels]
    plt.legend(handles, labels,loc = "upper left", bbox_to_anchor=(1, 1), title="Comparison to Global Average of 40 million")

    ax.set_xticks(income_class)
    ax.set_xlabel("Income Level")
    ax.set_ylabel("Average Population in millions")
    ax.set_title("Average Population to Country Income Level")
    plt.subplots_adjust(right=0.7)
    plt.show()


def main():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + '/'+ "final_data.db")
    cur = conn.cursor()
    calc_avg_population_per_income_level(cur)
    bar_graph_pop_by_income_lvl(cur,conn)

main()

