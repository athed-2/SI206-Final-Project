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
def calc_avg_risk_score_per_language(cur):
    # Select relevant columns and group by language_name
    query = """
        SELECT LanguageTable.language_name, AVG(country_data.risk_score) as avg_risk_score
        FROM country_data
        JOIN LanguageTable ON country_data.language_id = LanguageTable.id
        GROUP BY LanguageTable.language_name
    """
    cur.execute(query)
    data = cur.fetchall()
    # Create a dictionary to store language-wise average risk scores
    avg_scores = {language_name: avg_risk_score for language_name, avg_risk_score in data}

    return avg_scores

def get_color(avg_risk_score):
    if avg_risk_score >= 4.5:
        return "red"
    elif 3.5 <= avg_risk_score < 4.5:
        return "yellow"
    elif 2.5 <= avg_risk_score < 3.5:
        return "blue" 
    elif 0 <= avg_risk_score < 2.5:
        return "green"

def bar_graph_risk_score(cur, conn):
    avg_risk_scores = calc_avg_risk_score_per_income_level(cur)  # returns a list of the calc avg of risk_score from each income_level
    cur.execute("SELECT DISTINCT country_data.income_level, IncomeClass.income_class FROM country_data JOIN IncomeClass ON country_data.income_level = IncomeClass.id")
    conn.commit()
    income_level = cur.fetchall()
    income_class = []
    for tup in income_level:
        income_class.append(tup[1])

    colors = [get_color(score) for score in avg_risk_scores]
    # Creating the bar plot
    fig, ax = plt.subplots()
    bars = ax.bar(income_class, avg_risk_scores, color=colors)

    # Adding color legend
    legend_labels = ["0-2.5 (Safe)", "2.5-3.5 (Medium Risk)", "3.5-4.5 (High Risk)", "4.5-5 (Extreme Warning)"]
    legend_colors = ["green", "blue", "yellow", "red"]  # Match colors with the get_color function
    legend = ax.legend(bars, legend_labels, loc="upper left", bbox_to_anchor=(1, 1), title="Risk Category")
    for i in range(len(legend.legendHandles)):
        legend.legendHandles[i].set_color(legend_colors[i])

    ax.set_xticks(income_class)
    ax.set_xlabel("Income Level")
    ax.set_ylabel("Average Advisory Risk Score")
    ax.set_title("Average Advisory Risk Score to Country Income Level")
    plt.subplots_adjust(right=0.7)
    plt.show()

def plot_top_10_languages_with_lowest_risk_scores(cur):
    # Calculate average risk scores per language
    avg_risk_scores = calc_avg_risk_score_per_language(cur)

    # Sort languages by average risk scores and get the top 10
    top_10_languages = sorted(avg_risk_scores.items(), key=lambda x: x[1])[:10]

    # Extract language names and corresponding average risk scores
    languages, avg_scores = zip(*top_10_languages)
    plt.figure(figsize=(10, 6))
    plt.barh(languages, avg_scores, color='skyblue')
    plt.xlabel('Average Risk Score')
    plt.ylabel('Language')
    plt.title('Top 10 Languages with Lowest Average Risk Scores')
    plt.tight_layout()
    plt.show()


def main():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + '/'+ "final_data.db")
    cur = conn.cursor()
    calc_avg_risk_score_per_income_level(cur)
    calc_avg_risk_score_per_language(cur)
    plot_top_10_languages_with_lowest_risk_scores(cur)
    bar_graph_risk_score(cur, conn)

main()




