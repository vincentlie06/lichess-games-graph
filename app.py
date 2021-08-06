import requests as req
import matplotlib.pyplot as plt
import csv
import os

from itertools import count
from matplotlib.animation import FuncAnimation
from bs4 import BeautifulSoup

URL = "https://lichess.org/"
UPDATE_RATE = 30 # seconds
PLAYERS_EL_ID = "nb_connected_players"
GAMES_EL_ID = "nb_games_in_play"
SAVE_FILE = "data.csv" # .csv file
CSV_DELIM = ','

x_vals = []
expected_games_ls = []
current_games_ls = []
index = count()

plt.style.use('dark_background')

def update(i):
    x = next(index)
    x_vals.append(x)

    response = req.get(URL)
    print(response)

    html_text = response.text
    html_parsed = BeautifulSoup(html_text, 'html.parser')

    games_link = html_parsed.find("a", {"id": GAMES_EL_ID})
    games_data = games_link.findChild("strong")
    current_games = int(games_data.get("data-count"))

    players_link = html_parsed.find("a", {"id": PLAYERS_EL_ID})
    players_data = players_link.findChild("strong")
    current_players = int(players_data.get("data-count"))
    
    expected_games = current_players // 2

    current_games_ls.append(current_games)
    expected_games_ls.append(expected_games)

    render_graph()

    print(f"{x}:\nNumber of Players: {current_players}\nExpected Games: {expected_games}\nCurrent Games:{current_games}\n")

    save_data()

def save_data():
    with open(SAVE_FILE, 'w') as f:
        w = csv.writer(f, delimiter=CSV_DELIM)
        for x in x_vals:
            w.writerow([x, expected_games_ls[x], current_games_ls[x]])

def load_data():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, 'r') as f:
            r = csv.reader(f, delimiter=CSV_DELIM)
            data = list(r)
            
            for line in data:
                x = next(index)
                x_vals.append(x)

                expected_games_ls.append(int(line[1]))
                current_games_ls.append(int(line[2]))

    print("Data Loaded!")

def render_graph():
    plt.cla()
    plt.plot(x_vals, expected_games_ls, label='Expected Games', color='blue')
    plt.plot(x_vals, current_games_ls, label='Current Games', color='green')

    plt.title("Number of Current Games on Lichess vs Expected Games")
    plt.xlabel(f"Time ({UPDATE_RATE}s interval)")
    plt.ylabel("Number of Games")
    plt.legend()


load_data()
render_graph()

ani = FuncAnimation(plt.gcf(), update, interval=UPDATE_RATE * 1000)

plt.show()
