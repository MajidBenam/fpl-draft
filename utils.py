from base64 import encode
from termios import TIOCPKT_FLUSHREAD
from matplotlib.textpath import text_to_path
import requests
import pandas as pd
import json
import pprint
import time

from all_vars import all_managers_dic, element_type_mapper, good_flags, good_flags_2, German_leagues_ids, My_german_managers, German_leagues_ids_dic

# from IPython.display import Markdown, display
# def printmd(string):
#     display(Markdown(string))
my_tops = []

base_url_draft = "https://draft.premierleague.com/api/bootstrap-static"
base_url_fantasy = "https://fantasy.premierleague.com/api/bootstrap-static"
base_dynamic_url = "https://fantasy.premierleague.com/api/event/4/live/"
majid_leage_url = "https://draft.premierleague.com/api/draft/59081/choices"
milad_leage_url = "https://draft.premierleague.com/api/draft/58924/choices"

#German_leagues_ids = [56490, 56760, 57026, 58512, 58924, 59081, 59219, 60061, 60068, 60279, 60283]

def league_managers_finder(league_ids):
    managers = {}
    for i in league_ids:
        league_url = f"https://draft.premierleague.com/api/draft/{i}/choices"
        response = requests.get(league_url)
        my_league_data = json.loads(response.text)
        managers[i] = {}
        for index, team in enumerate(my_league_data["choices"][0:16]):
            managers[i][index] = {}
            managers[i][index]["first_name"] = team["player_first_name"].lower().capitalize()
            managers[i][index]["last_name"] = team["player_last_name"].lower().capitalize()
            managers[i][index]["team_id"] = team["entry"]
            managers[i][index]["golds"] = 0
            managers[i][index]["silvers"] = 0
            managers[i][index]["bronzes"] = 0
            managers[i][index]["fourths"] = 0
            managers[i][index]["fifths"] = 0
            if "zealand" in team["entry_name"].lower():
                managers[i][index]["country"] = 'New Zealand 🇳🇿'
            elif "taly" in team["entry_name"].lower():
                managers[i][index]["country"] = 'Italy 🇮🇹'
            elif "apan" in team["entry_name"].lower():
                managers[i][index]["country"] = 'Japan 🇯🇵'
            elif "outh" in team["entry_name"].lower():
                managers[i][index]["country"] = 'South Korea 🇰🇷'
            elif "anada" in team["entry_name"].lower():
                managers[i][index]["country"] = 'Canada 🇨🇦'
            elif "ungar" in team["entry_name"].lower():
                managers[i][index]["country"] = 'Hungary 🇭🇺'
            elif "therland" in team["entry_name"].lower():
                managers[i][index]["country"] = 'Netherlands 🇳🇱'
            elif "rgenti" in team["entry_name"].lower():
                managers[i][index]["country"] = 'Argentina 🇦🇷'
            elif "chin" in team["entry_name"].lower():
                managers[i][index]["country"] = 'China 🇨🇳'
            elif "ermany" in team["entry_name"].lower():
                managers[i][index]["country"] = 'Germany 🇩🇪'
            elif "ritain" in team["entry_name"].lower():
                managers[i][index]["country"] = 'Great Britain 🇬🇧'
            elif "ustralia" in team["entry_name"].lower():
                managers[i][index]["country"] = 'Australia 🇦🇺'
            elif "oviet" in team["entry_name"].lower():
                managers[i][index]["country"] = 'The Soviet Union ☭'
            elif "rance" in team["entry_name"].lower():
                managers[i][index]["country"] = 'France 🇫🇷'
            elif "usa" in team["entry_name"].lower() or "nited" in team["entry_name"] :
                managers[i][index]["country"] = 'United States 🇺🇲'
            # elif good_flag in team["entry_name"] or good_flag in team["entry_name"]:
            #     #print(index+1, good_flag, team["entry_name"])
            #     managers[i]["country"] = good_name
    return managers    


def league_managers_finder_slim(league_ids_dic):
    managers = {}
    for city_code, city_name in league_ids_dic.items():
        league_url = f"https://draft.premierleague.com/api/draft/{city_code}/choices"
        response = requests.get(league_url)
        my_league_data = json.loads(response.text)
        this_league_id = {}
        for index, team in enumerate(my_league_data["choices"][0:16]):
            #managers[i][index] = {}
            #managers[i][index]["first_name"] = team["player_first_name"].lower().capitalize()
            #managers[i][index]["last_name"] = team["player_last_name"].lower().capitalize()
            #managers[i][index]["team_id"] = team["entry"]
            if "zealand" in team["entry_name"].lower():
                this_league_id[team["entry"]] = 'New Zealand 🇳🇿'
            elif "taly" in team["entry_name"].lower():
                this_league_id[team["entry"]] = 'Italy 🇮🇹'
            elif "apan" in team["entry_name"].lower():
                this_league_id[team["entry"]] = 'Japan 🇯🇵'
            elif "outh" in team["entry_name"].lower():
                this_league_id[team["entry"]] = 'South Korea 🇰🇷'
            elif "anada" in team["entry_name"].lower():
                this_league_id[team["entry"]] = 'Canada 🇨🇦'
            elif "ungar" in team["entry_name"].lower():
                this_league_id[team["entry"]] = 'Hungary 🇭🇺'
            elif "therland" in team["entry_name"].lower():
                this_league_id[team["entry"]] = 'Netherlands 🇳🇱'
            elif "rgenti" in team["entry_name"].lower():
                this_league_id[team["entry"]] = 'Argentina 🇦🇷'
            elif "chin" in team["entry_name"].lower():
                this_league_id[team["entry"]] = 'China 🇨🇳'
            elif "ermany" in team["entry_name"].lower():
                this_league_id[team["entry"]] = 'Germany 🇩🇪'
            elif "ritain" in team["entry_name"].lower():
                this_league_id[team["entry"]] = 'Great Britain 🇬🇧'
            elif "ustralia" in team["entry_name"].lower():
                this_league_id[team["entry"]] = 'Australia 🇦🇺'
            elif "oviet" in team["entry_name"].lower():
                this_league_id[team["entry"]] = 'The Soviet Union ☭'
            elif "rance" in team["entry_name"].lower():
                this_league_id[team["entry"]] = 'France 🇫🇷'
            elif "usa" in team["entry_name"].lower() or "nited" in team["entry_name"] :
                this_league_id[team["entry"]] = 'United States 🇺🇲'
            # elif good_flag in team["entry_name"] or good_flag in team["entry_name"]:
            #     #print(index+1, good_flag, team["entry_name"])
            #     managers[i]["country"] = good_name
        managers[city_name] = this_league_id
    return managers  

def league_code_finder():
    for i in range(59080,59220):
        league_url = f"https://draft.premierleague.com/api/draft/{i}/choices"
        response = requests.get(league_url)
        if i%100 == 0:
            print(i)
        try:
            my_league_data = json.loads(response.text)
            number_of_flags = 0
            for index, team in enumerate(my_league_data["choices"][0:16]):
                for good_flag, flag_image in good_flags_2.items():
                    if flag_image in team["entry_name"] or good_flag in team["entry_name"]:
                        #print(good_flag)
                        number_of_flags+=1
            if number_of_flags>=1:
                print(i, " ***************", number_of_flags)
        except:
            continue

def league_city_collector(league_ids):
    league_city = {}
    for league_id in league_ids:
        league_city[league_id] = German_leagues_ids[league_id]
    return league_city
        

def league_info_collector(league_ids):
    good_dic_of_league_team_names_flags = {}
    german_players = {}
    for league_id in league_ids:
        league_url = f"https://draft.premierleague.com/api/draft/{league_id}/choices"
        response = requests.get(league_url)
        my_league_data = json.loads(response.text)
        good_dic_of_team_names_flags = {}
        
        for index, team in enumerate(my_league_data["choices"][0:16]):
            for good_flag, good_name in good_flags.items():
                if "zealand" in team["entry_name"].lower():
                    good_dic_of_team_names_flags[team["entry"]] = 'New Zealand 🇳🇿'
                elif "taly" in team["entry_name"].lower():
                    good_dic_of_team_names_flags[team["entry"]] = 'Italy 🇮🇹'
                elif "apan" in team["entry_name"].lower():
                    good_dic_of_team_names_flags[team["entry"]] = 'Japan 🇯🇵'
                elif "outh" in team["entry_name"].lower():
                    good_dic_of_team_names_flags[team["entry"]] = 'South Korea 🇰🇷'
                elif "anada" in team["entry_name"].lower():
                    good_dic_of_team_names_flags[team["entry"]] = 'Canada 🇨🇦'
                elif "ungar" in team["entry_name"].lower():
                    good_dic_of_team_names_flags[team["entry"]] = 'Hungary 🇭🇺'
                elif "therland" in team["entry_name"].lower():
                    good_dic_of_team_names_flags[team["entry"]] = 'Netherlands 🇳🇱'
                elif "rgenti" in team["entry_name"].lower():
                    good_dic_of_team_names_flags[team["entry"]] = 'Argentina 🇦🇷'
                elif "chin" in team["entry_name"].lower():
                    good_dic_of_team_names_flags[team["entry"]] = 'China 🇨🇳'
                elif "ermany" in team["entry_name"].lower():
                    good_dic_of_team_names_flags[team["entry"]] = 'Germany 🇩🇪'
                    german_players[team["entry"]] = league_id
                elif "ritain" in team["entry_name"].lower():
                    good_dic_of_team_names_flags[team["entry"]] = 'Great Britain 🇬🇧'
                elif "ustralia" in team["entry_name"].lower():
                    good_dic_of_team_names_flags[team["entry"]] = 'Australia 🇦🇺'
                elif "oviet" in team["entry_name"].lower():
                    good_dic_of_team_names_flags[team["entry"]] = 'The Soviet Union ☭'
                elif "rance" in team["entry_name"].lower():
                    good_dic_of_team_names_flags[team["entry"]] = 'France 🇫🇷'
                elif "usa" in team["entry_name"].lower() or "nited" in team["entry_name"] :
                    good_dic_of_team_names_flags[team["entry"]] = 'United States 🇺🇲'
                elif good_flag in team["entry_name"] or good_flag in team["entry_name"]:
                    #print(index+1, good_flag, team["entry_name"])
                    good_dic_of_team_names_flags[team["entry"]] = good_name

        good_dic_of_league_team_names_flags[league_id] = good_dic_of_team_names_flags
        print(league_id, ": ", str(len(good_dic_of_league_team_names_flags[league_id])))
    return good_dic_of_league_team_names_flags, german_players


def league_info_collector_plus(league_ids):
    good_dic_of_league_team_names_flags = {}
    german_players = {}
    for league_id in league_ids:
        league_url = f"https://draft.premierleague.com/api/draft/{league_id}/choices"
        response = requests.get(league_url)
        my_league_data = json.loads(response.text)
        good_dic_of_team_names_flags = {}
        
        for index, team in enumerate(my_league_data["choices"][0:16]):
            for good_flag, good_name in good_flags.items():
                if "zealand" in team["entry_name"].lower():
                    good_dic_of_team_names_flags[team["entry"]] = 'New Zealand 🇳🇿'
                elif "taly" in team["entry_name"].lower():
                    good_dic_of_team_names_flags[team["entry"]] = 'Italy 🇮🇹'
                elif "apan" in team["entry_name"].lower():
                    good_dic_of_team_names_flags[team["entry"]] = 'Japan 🇯🇵'
                elif "outh" in team["entry_name"].lower():
                    good_dic_of_team_names_flags[team["entry"]] = 'South Korea 🇰🇷'
                elif "anada" in team["entry_name"].lower():
                    good_dic_of_team_names_flags[team["entry"]] = 'Canada 🇨🇦'
                elif "ungar" in team["entry_name"].lower():
                    good_dic_of_team_names_flags[team["entry"]] = 'Hungary 🇭🇺'
                elif "therland" in team["entry_name"].lower():
                    good_dic_of_team_names_flags[team["entry"]] = 'Netherlands 🇳🇱'
                elif "rgenti" in team["entry_name"].lower():
                    good_dic_of_team_names_flags[team["entry"]] = 'Argentina 🇦🇷'
                elif "chin" in team["entry_name"].lower():
                    good_dic_of_team_names_flags[team["entry"]] = 'China 🇨🇳'
                elif "ermany" in team["entry_name"].lower():
                    good_dic_of_team_names_flags[team["entry"]] = 'Germany 🇩🇪'
                    german_players[team["entry"]] = league_id
                elif "ritain" in team["entry_name"].lower():
                    good_dic_of_team_names_flags[team["entry"]] = 'Great Britain 🇬🇧'
                elif "ustralia" in team["entry_name"].lower():
                    good_dic_of_team_names_flags[team["entry"]] = 'Australia 🇦🇺'
                elif "oviet" in team["entry_name"].lower():
                    good_dic_of_team_names_flags[team["entry"]] = 'The Soviet Union ☭'
                elif "rance" in team["entry_name"].lower():
                    good_dic_of_team_names_flags[team["entry"]] = 'France 🇫🇷'
                elif "usa" in team["entry_name"].lower() or "nited" in team["entry_name"] :
                    good_dic_of_team_names_flags[team["entry"]] = 'United States 🇺🇲'
                elif good_flag in team["entry_name"] or good_flag in team["entry_name"]:
                    #print(index+1, good_flag, team["entry_name"])
                    good_dic_of_team_names_flags[team["entry"]] = good_name

        good_dic_of_league_team_names_flags[league_id] = good_dic_of_team_names_flags
        print(league_id, ": ", str(len(good_dic_of_league_team_names_flags[league_id])))
    return good_dic_of_league_team_names_flags, german_players



base_response = requests.get(base_url_draft)
base_data = json.loads(base_response.text)

def gw_dic_reporter(all_managers_dic, gw_number):
    managers_points = {}
    for manager, manager_name in all_managers_dic.items():
        url = f"https://draft.premierleague.com/api/entry/{manager}/event/{gw_number}"
        response = requests.get(url)
        data = json.loads(response.text)
        #if manager == 263589:
        #    pprint.pprint(data)
        players = {}
        for player in data["picks"]:
            for index, a_player in enumerate(base_data["elements"]):
                if player['element'] == a_player['id']:
                    player_name = base_data["elements"][index]['web_name']
                    player_id = base_data["elements"][index]['id']
                    player_selection_rank = player["position"]
                    # event_points = base_data["elements"][index]['event_points']
                    # element_type = base_data["elements"][index]['element_type']
                    # # player['element'] is exactly the id in the bootsrap static and detailed pages
                    # player_details_url = f"https://fantasy.premierleague.com/api/element-summary/{player['element']}/"
                    # player_details_response = requests.get(player_details_url)
                    # player_details = json.loads(player_details_response.text)
                    # if player['element'] == 428:
                    #     print("index: ", index, "    ", "player_id: ", player['element'])
                    #     pprint.pprint(player_details["history"])
                    # minutes = player_details["history"][-1]["minutes"]

                    
                    # my_player_info = {
                    #     "event_points": event_points,
                    #     "element_type": element_type,
                    #     "minutes": minutes,
                    #     "player_name": player_name
                    # }
                    players[player_id] = [player_name, player_selection_rank]
                    break
        managers_points[manager_name] = players
    return managers_points
    pprint.pprint(managers_points)

def top_players_revealer(all_managers_full_up_to_gw_x):
    dic_of_all_players ={}
    for league_id, value in all_managers_full_up_to_gw_x.items():
        for value_num, main_dic in value.items():
            try:
                team_name = main_dic["country"] + " (" +  main_dic["first_name"] + " " + main_dic["last_name"] + ") " + f"[{German_leagues_ids_dic[league_id]}]"
                medals= (main_dic["golds"], main_dic["silvers"], main_dic["bronzes"], 
                    main_dic["fourths"], main_dic["fifths"])
            except:
                team_name = "Referee"
                medals= (0,0,0,0,0)
            dic_of_all_players[team_name] = medals
    sort_players = sorted(dic_of_all_players.items(), key=lambda x: (x[1][0], x[1][1], x[1][2], x[1][3], x[1][4]), reverse=True)
    return sort_players
    
def top_players_table_maker(bunch_of_sorted_players):
    line_str = "-"*99
    gw_str = "|" + "°°° Up to GW: 8 °°°".center(97) + "|"
    headers_str = f"| ## | ** Manager: [CITY] ** {'':<35} |  " + u"\U0001F947" + "  |  " + u"\U0001F948" + "  |  " + u"\U0001F949" +  "  | 4th | 5th |"
    #subheaders_str = f"| {'':<59} | " + u"\U0001F947" + " | " + u"\U0001F948" + " | " + u"\U0001F949" +  " | 3rd | 4th |"
    table_report = []
    table_report.append(line_str)
    table_report.append(gw_str)
    table_report.append(line_str)
    table_report.append(headers_str)
    #table_report.append(subheaders_str)
    table_report.append(line_str)

    for index, team_details in enumerate(bunch_of_sorted_players):
        #print(team_details)
        manager_rank_str = f"|{str(index+1):>3} | {team_details[0]:<58}|{str(team_details[1][0]).center(6)}|{str(team_details[1][1]).center(6)}|{str(team_details[1][2]).center(6)}|{str(team_details[1][3]).center(5)}|{str(team_details[1][4]).center(5)}|"
        #print(index+1, team_details)
        table_report.append(manager_rank_str)
        table_report.append(line_str)
    table_report_str = "\n".join(table_report)
    return table_report_str



def table_maker(all_managers_dic, gw_number):
    managers_points = gw_dic_reporter(all_managers_dic, gw_number)
    final_points_dic = {}
    for manager, players in managers_points.items():
        manager_lineup_points = 0
        manager_lineup_goals = 0
        manager_lineup_assists = 0
        manager_bench_points = 0
        manager_bench_goals = 0
        manager_bench_assists = 0
        for player_id, player_name_pos in players.items():
            player_details = get_player_live_details(player_id, gw_number)
            player_total_points =  player_details["total_points"]
            player_total_goals = player_details["goals"]
            player_total_assists = player_details["assists"]
            if player_name_pos[1] <= 11:
                manager_lineup_points = manager_lineup_points + player_total_points
                manager_lineup_goals = manager_lineup_goals + player_total_goals
                manager_lineup_assists = manager_lineup_assists + player_total_assists
            else:
                manager_bench_points = manager_bench_points + player_total_points
                manager_bench_goals = manager_bench_goals + player_total_goals
                manager_bench_assists = manager_bench_assists + player_total_assists
        final_points_dic[manager] = (manager_lineup_points, manager_bench_points, 
                                    manager_lineup_goals, manager_bench_goals,
                                    manager_lineup_assists, manager_bench_assists,)

    sort_managers = sorted(final_points_dic.items(), key=lambda x: (x[1][0], x[1][2], x[1][4]), reverse=True)
    return sort_managers

def manager_players_info_maker(all_managers_dic, gw_number):
    managers_points = gw_dic_reporter(all_managers_dic, gw_number)
    final_report_dic = {}
    for manager, players in managers_points.items():
        players_details = {}
        for player_id, player_name_pos in players.items():
            player_details = get_player_live_details(player_id, gw_number)
            players_details[player_id] = player_details
        final_report_dic[manager] = players_details

    return final_report_dic

def player_analysis(players_dic, player_id):
    player_info = players_dic[player_id]
    player_name = player_info['player_name']
    player_position = player_info['player_position']
    team_status = player_info["team_of_player_has_played"]
    player_status = player_info["player_has_played"]
    player_length = len(player_name)
    points = '.'*(30-player_length)
    if team_status == 'PLAYED' and player_status == 'PLAYED':
        player_report = f"PLAYED   ({player_position}): {player_name:.<30} {player_info['total_points']: >2} point(s)"
        return player_report
    elif team_status == 'PLAYED' and player_status == 'DIDNOTPLAY':
        player_report = f"BENCHED  ({player_position}): {player_name:.<42}"
        return player_report
    elif team_status == 'ONGOING' and player_status == 'DIDNOTPLAY':
        player_report = f"Benched  ({player_position}): {player_name} was benched and has got no point(s) yet."
        return player_report
    elif team_status == 'ONGOING' and player_status == 'PLAYING':
        player_report = f"PLAYING  ({player_position}): {player_name:.<30} {player_info['total_points']: >2} point(s)"
        return player_report
    elif team_status == 'ONGOING' and player_status == 'BENCHING':
        player_report = f"BENCHING ({player_position}): {player_name:.<30} 0 point(s)"
        return player_report
    elif team_status == 'UNDONE':
        player_report = f"WAITING  ({player_position}): {player_name:.<30}          "
        return player_report
    else:
        pprint.pprint(player_info)
        return f"NO_GAME  ({player_position}): {player_name:.<30}..... X ...."

def player_analysis_HTML(players_dic, player_id):
    player_info = players_dic[player_id]
    player_name = player_info['player_name']
    player_position = player_info['player_position']
    team_status = player_info["team_of_player_has_played"]
    player_status = player_info["player_has_played"]

    if team_status == 'PLAYED' and player_status == 'PLAYED':
        player_report_cell = f"""
        <span class="text-secondary fw-bold  px-2">{player_name}<sup class="badge py-1 px-2 fw-bold rounded-pill bg-secondary">{player_info['total_points']}</sup>
        """
        return player_report_cell, player_position

    elif team_status == 'PLAYED' and player_status == 'DIDNOTPLAY':
        player_report_cell = f"""
        <span class="text-secondary fw-bold  px-2"><strike>{player_name}</strike><sup class="badge py-1 px-2 fw-bold rounded-pill bg-secondary"><i class="fa-solid fa-xmark"></i></sup>
        """
        return player_report_cell, player_position

    elif team_status == 'ONGOING' and player_status == 'DIDNOTPLAY':
        player_report_cell = f"""
        <span class="text-danger fw-bold px-2">{player_name} 
            <sup><i class="fa-solid fa-ellipsis text-danger"></i></sup>
        </span>
        """
        return player_report_cell, player_position

    elif team_status == 'ONGOING' and player_status == 'PLAYING':
        player_report_cell = f"""
        <span class="text-info fw-bold  px-2">{player_name}<sup class="badge py-1 px-2 fw-bold rounded-pill bg-info">{player_info['total_points']}</sup>
        """
        return player_report_cell, player_position

    elif team_status == 'ONGOING' and player_status == 'BENCHING':
        player_report_cell = f"""
        <span class="text-danger fw-bold px-2">{player_name} 
            <sup><i class="fa-solid fa-ellipsis text-danger"></i></sup>
        </span>
        """
        return player_report_cell, player_position

    elif team_status == 'UNDONE':
        player_report_cell = f"""
        <span class="text-primary fw-bold  px-2">{player_name} 
            <sup><i class="fa-solid fa-circle text-primary"></i></sup>
        </span>
        """
        return player_report_cell, player_position

    else:
        pprint.pprint(player_info)
        player_report_cell = f"""
        <span class="text-primary fw-bold  px-2"><strike>{player_name}</strike>
            <sup><i class="fa-solid fa-umbrella-beach text-secondary"></i></sup>
        </span>
        """
        return player_report_cell, player_position



def report_maker(all_managers_dic, gw_number):
    final_report_dic = manager_players_info_maker(all_managers_dic, gw_number)
    managers_points = gw_dic_reporter(all_managers_dic, gw_number)
    final_team_points_dic = {}
    line_str = "-"*46
    headers_str = f"| TEAM {'':<20} | Points (Bench) |"
    full_report = []
    table_report = []
    table_report.append(line_str)
    table_report.append(headers_str)
    table_report.append(line_str)


    for manager, players in managers_points.items():
        manager_lineup_points = 0
        manager_bench_points = 0
        for player_id, player_name_pos in players.items():
            player_details = get_player_live_details(player_id, gw_number)
            player_total_points =  player_details["total_points"]
            if player_name_pos[1] <= 11:
                manager_lineup_points = manager_lineup_points + player_total_points
            else:
                manager_bench_points = manager_bench_points + player_total_points
        final_team_points_dic[manager] = (manager_lineup_points, manager_bench_points)
    sorted_managers = sorted(final_team_points_dic.items(), key=lambda x: x[1], reverse=True)

    for item in sorted_managers:
        if "Referee" in item[0]:
            continue
        points_bench_str = f"{str(item[1][0])} ({str(item[1][1])})"
        team_rank_str = f"| {item[0]:<25} |{points_bench_str.center(16)}|"
        team_rank_str = f"| {item[0]:<25} |{points_bench_str.center(16)}| {str(item[1][2]).center(9)} | {str(item[1][4]).center(11)}"
        table_report.append(team_rank_str)
        table_report.append(line_str)
    
    table_report_str = "\n".join(table_report)
    full_report.append(table_report_str)

    full_report.append("\n\n******  More Details  ******** \n")

    for manager, players in final_report_dic.items():
        final_report_list = []
        manager_total_pts = final_team_points_dic[manager][0]
        team_title = f"{manager::<52}{manager_total_pts:>3} pts\n"
        final_report_list.append(team_title)
        for index, player in enumerate(players.keys()):
            player_report_str = player_analysis(final_report_dic[manager], player)
            if index == 11:
                final_report_list.append("_"*56)
            final_report_list.append(player_report_str)
        manager_report = "\n    ".join(final_report_list)
        full_report.append(manager_report)
    return f"\n\n{'='*60}\n".join(full_report)

def live_report_maker(all_managers_dic, gw_number):
    final_report_dic = manager_players_info_maker(all_managers_dic, gw_number)
    managers_points = gw_dic_reporter(all_managers_dic, gw_number)
    final_team_points_dic = {}
    line_str = "-"*64
    gw_str = f"| ** GameWeek: {gw_number} **{'':<43} |"
    headers_str = f"| TEAM {'':<20} | Points (Bench) | Goals | Assists |"
    full_report = []
    table_report = []
    table_report.append(line_str)
    table_report.append(gw_str)
    table_report.append(line_str)
    table_report.append(headers_str)
    table_report.append(line_str)
    for manager, players in managers_points.items():
        manager_lineup_points = 0
        manager_lineup_goals = 0
        manager_lineup_assists = 0
        manager_bench_points = 0
        manager_bench_goals = 0
        manager_bench_assists = 0
        for player_id, player_name_pos in players.items():
            player_details = get_player_live_details(player_id, gw_number)
            player_total_points =  player_details["total_points"]
            player_total_goals = player_details["goals"]
            player_total_assists = player_details["assists"]
            if player_name_pos[1] <= 11:
                manager_lineup_points = manager_lineup_points + player_total_points
                manager_lineup_goals = manager_lineup_goals + player_total_goals
                manager_lineup_assists = manager_lineup_assists + player_total_assists
            else:
                manager_bench_points = manager_bench_points + player_total_points
                manager_bench_goals = manager_bench_goals + player_total_goals
                manager_bench_assists = manager_bench_assists + player_total_assists
        final_team_points_dic[manager] = (manager_lineup_points, manager_bench_points, 
                                    manager_lineup_goals, manager_bench_goals,
                                    manager_lineup_assists, manager_bench_assists,)
    sorted_managers = sorted(final_team_points_dic.items(), key=lambda x: (x[1][0], x[1][2], x[1][4]), reverse=True)




    for index, item in enumerate(sorted_managers):
        if "Referee" in item[0]:
            continue
        points_bench_str = f"{str(item[1][0])} ({str(item[1][1])})"
        if index == 0:
            team_name = u"\U0001F947" + " " + item[0]
            team_rank_str = f"| {team_name:<24} |{points_bench_str.center(16)}|{str(item[1][2]).center(7)}|{str(item[1][4]).center(9)}|"
        elif index == 1:
            team_name = u"\U0001F948" + " " + item[0]
            team_rank_str = f"| {team_name:<24} |{points_bench_str.center(16)}|{str(item[1][2]).center(7)}|{str(item[1][4]).center(9)}|"
        elif index == 2:
            team_name = u"\U0001F949" + " " + item[0]
            team_rank_str = f"| {team_name:<24} |{points_bench_str.center(16)}|{str(item[1][2]).center(7)}|{str(item[1][4]).center(9)}|"
        else:
            team_name = item[0]
            team_rank_str = f"| {team_name:<25} |{points_bench_str.center(16)}|{str(item[1][2]).center(7)}|{str(item[1][4]).center(9)}|"

        table_report.append(team_rank_str)
        table_report.append(line_str)
    
    table_report_str = "\n".join(table_report)
    full_report.append(table_report_str)

    full_report.append("\n\n******  More Details  ******** \n")

    for manager, players in final_report_dic.items():
        final_report_list = []
        manager_total_pts = final_team_points_dic[manager][0]
        team_title = f"{manager::<52}{manager_total_pts:>3} pts\n"
        final_report_list.append(team_title)
        for index, player in enumerate(players.keys()):
            player_report_str = player_analysis(final_report_dic[manager], player)
            if index == 11:
                final_report_list.append("_"*56)
            final_report_list.append(player_report_str)
        manager_report = "\n    ".join(final_report_list)
        full_report.append(manager_report)
    return f"\n\n{'='*60}\n".join(full_report)



def live_report_maker_aggr(any_managers_dic, gw_number, league_id):
    #final_report_dic = manager_players_info_maker(any_managers_dic, gw_number)
    managers_points = gw_dic_reporter(any_managers_dic, gw_number)
    final_team_points_dic = {}

    for manager, players in managers_points.items():
        manager_lineup_points = 0
        manager_lineup_goals = 0
        manager_lineup_assists = 0
        manager_bench_points = 0
        manager_bench_goals = 0
        manager_bench_assists = 0
        for player_id, player_name_pos in players.items():
            player_details = get_player_live_details(player_id, gw_number)
            player_total_points =  player_details["total_points"]
            player_total_goals = player_details["goals"]
            player_total_assists = player_details["assists"]
            if player_name_pos[1] <= 11:
                manager_lineup_points = manager_lineup_points + player_total_points
                manager_lineup_goals = manager_lineup_goals + player_total_goals
                manager_lineup_assists = manager_lineup_assists + player_total_assists
            else:
                manager_bench_points = manager_bench_points + player_total_points
                manager_bench_goals = manager_bench_goals + player_total_goals
                manager_bench_assists = manager_bench_assists + player_total_assists
        final_team_points_dic[manager] = (manager_lineup_points, manager_bench_points, 
                                    manager_lineup_goals, manager_bench_goals,
                                    manager_lineup_assists, manager_bench_assists,)
    sorted_managers = sorted(final_team_points_dic.items(), key=lambda x: (x[1][0], x[1][2], x[1][4]), reverse=True)
    
    line_str = "-"*64
    city = German_leagues_ids_dic[league_id]
    gw_str = f"| ** GameWeek: {gw_number} **{city:>43} |"
    headers_str = f"| TEAM {'':<20} | Points (Bench) | Goals | Assists |"
    full_report = []
    table_report = []
    table_report.append(line_str)
    table_report.append(gw_str)
    table_report.append(line_str)
    table_report.append(headers_str)
    table_report.append(line_str)

    # medals
    medals = {}
    for index, item in enumerate(sorted_managers):
        if "Referee" in item[0]:
            continue
        points_bench_str = f"{str(item[1][0])} ({str(item[1][1])})"
        if index == 0:
            team_name = u"\U0001F947" + " " + item[0]
            team_rank_str = f"| {team_name:<24} |{points_bench_str.center(16)}|{str(item[1][2]).center(7)}|{str(item[1][4]).center(9)}|"
            medals["gold"] = item[0]
        elif index == 1:
            team_name = u"\U0001F948" + " " + item[0]
            team_rank_str = f"| {team_name:<24} |{points_bench_str.center(16)}|{str(item[1][2]).center(7)}|{str(item[1][4]).center(9)}|"
            medals["silver"] = item[0]
        elif index == 2:
            team_name = u"\U0001F949" + " " + item[0]
            team_rank_str = f"| {team_name:<24} |{points_bench_str.center(16)}|{str(item[1][2]).center(7)}|{str(item[1][4]).center(9)}|"
            medals["bronze"] = item[0]
        elif index == 3:
            team_name = item[0]
            team_rank_str = f"| {team_name:<25} |{points_bench_str.center(16)}|{str(item[1][2]).center(7)}|{str(item[1][4]).center(9)}|"
            medals["fourth"] = item[0]
        elif index == 4:
            team_name = item[0]
            team_rank_str = f"| {team_name:<25} |{points_bench_str.center(16)}|{str(item[1][2]).center(7)}|{str(item[1][4]).center(9)}|"
            medals["fifth"] = item[0]
        elif index == 5:
            team_name = item[0]
            team_rank_str = f"| {team_name:<25} |{points_bench_str.center(16)}|{str(item[1][2]).center(7)}|{str(item[1][4]).center(9)}|"
            medals["sixth"] = item[0]
        elif index == 6:
            team_name = item[0]
            team_rank_str = f"| {team_name:<25} |{points_bench_str.center(16)}|{str(item[1][2]).center(7)}|{str(item[1][4]).center(9)}|"
            medals["seventh"] = item[0]
        elif index == 7:
            team_name = item[0]
            team_rank_str = f"| {team_name:<25} |{points_bench_str.center(16)}|{str(item[1][2]).center(7)}|{str(item[1][4]).center(9)}|"
            medals["eighth"] = item[0]
        elif index == 8:
            team_name = item[0]
            team_rank_str = f"| {team_name:<25} |{points_bench_str.center(16)}|{str(item[1][2]).center(7)}|{str(item[1][4]).center(9)}|"
            medals["ninth"] = item[0]
        elif index == 9:
            team_name = item[0]
            team_rank_str = f"| {team_name:<25} |{points_bench_str.center(16)}|{str(item[1][2]).center(7)}|{str(item[1][4]).center(9)}|"
            medals["tenth"] = item[0]
        elif index == 10:
            team_name = item[0]
            team_rank_str = f"| {team_name:<25} |{points_bench_str.center(16)}|{str(item[1][2]).center(7)}|{str(item[1][4]).center(9)}|"
            medals["eleventh"] = item[0]
        elif index == 11:
            team_name = item[0]
            team_rank_str = f"| {team_name:<25} |{points_bench_str.center(16)}|{str(item[1][2]).center(7)}|{str(item[1][4]).center(9)}|"
            medals["twelfth"] = item[0]
        elif index == 12:
            team_name = item[0]
            team_rank_str = f"| {team_name:<25} |{points_bench_str.center(16)}|{str(item[1][2]).center(7)}|{str(item[1][4]).center(9)}|"
            medals["thirteenth"] = item[0]
        elif index == 13:
            team_name = item[0]
            team_rank_str = f"| {team_name:<25} |{points_bench_str.center(16)}|{str(item[1][2]).center(7)}|{str(item[1][4]).center(9)}|"
            medals["fourteenth"] = item[0]
        elif index == 14:
            team_name = item[0]
            team_rank_str = f"| {team_name:<25} |{points_bench_str.center(16)}|{str(item[1][2]).center(7)}|{str(item[1][4]).center(9)}|"
            medals["fifteenth"] = item[0]
        else:
            team_name = item[0]
            team_rank_str = f"| {team_name:<25} |{points_bench_str.center(16)}|{str(item[1][2]).center(7)}|{str(item[1][4]).center(9)}|"

        table_report.append(team_rank_str)
        table_report.append(line_str)
    
    table_report_str = "\n".join(table_report)
    full_report.append(table_report_str)

    return (f"\n\n{'='*60}\n".join(full_report), medals)


def test_reading_tables_from_json(filename):
    with open(filename, 'r') as f:
        my_tables = json.load(f)
    return(my_tables)


def live_reports_all(German_leagues_ids, gws):
    my_league_data, my_germans = league_info_collector(German_leagues_ids)
    table_gws = {}
    all_medals = {}
    with open('table_dics_for_all_9.json', 'r') as f:
        table_gws = json.load(f)
    with open('medal_dics_for_all_9.json', 'r') as f1:
        all_medals = json.load(f1)

    for gw in gws:
        if str(gw) in table_gws.keys() and str(gw) in all_medals.keys():
            print(f"GameWeek {gw} is already ", "Done...")
            continue
        st = time.time()
        table_league = {}
        medals_league = {}

        for league_id, league_teams in my_league_data.items():
            # league_team is a good managers_dic
            table_league[league_id], medals_this_gw = live_report_maker_aggr(league_teams, gw, league_id)
            golds = {}
            silvers = {}
            bronzes = {}
            fourths = {}
            fifths = {}
            sixths = {}
            sevenths = {}    
            eighths = {}
            ninths = {}    
            tenths = {}
            elevenths = {}    
            twelfths = {}
            thirteenths = {}    
            fourteenths = {}
            fifteenths = {}
            for medal, country_name in medals_this_gw.items():
                if medal == "gold":
                    golds = country_name
                elif medal == "silver":
                    silvers = country_name
                elif medal == "bronze":
                    bronzes = country_name
                elif medal == "fourth":
                    fourths = country_name
                elif medal == "fifth":
                    fifths = country_name
                elif medal == "sixth":
                    sixths = country_name
                elif medal == "seventh":
                    sevenths = country_name
                elif medal == "eighth":
                    eighths = country_name
                elif medal == "ninth":
                    ninths = country_name
                elif medal == "tenth":
                    tenths = country_name
                elif medal == "eleventh":
                    elevenths = country_name
                elif medal == "twelfth":
                    twelfths = country_name
                elif medal == "thirteenth":
                    thirteenths = country_name
                elif medal == "fourteenth":
                    fourteenths = country_name
                elif medal == "fifteenth":
                    fifteenths = country_name
                else:
                    pass
            medals_league[league_id] = {
                'gold' : golds,
                'silver' : silvers,
                'bronze' : bronzes,
                'fourth' : fourths,
                'fifth' : fifths,
                'sixth' : sixths,
                'seventh' : sevenths,
                'eighth' : eighths,
                'ninth' : ninths,
                'tenth' : tenths,
                'eleventh' : elevenths, 
                'twelfth' : twelfths,
                'thirteenth' : thirteenths,
                'fourteenth' : fourteenths,
                'fifteenth' : fifteenths,
            }
        table_gws[gw] = table_league
        all_medals[gw] = medals_league
        et = time.time()
        # get the execution time
        elapsed_time = et - st
        print(f"GameWeek {gw} ", "Done..." , end=", ")
        print('Execution time:', elapsed_time, 'seconds')
        with open('table_dics_for_all_9.json', 'w') as fp:
            json.dump(table_gws, fp)
        with open('medal_dics_for_all_9.json', 'w') as fp2:
            json.dump(all_medals, fp2)
    return table_gws, all_medals


element_type_mapper = {
        2: "DF",
        3: "MF",
        4: "FW",
        1: "GK",
    }


def fixture_data(fixture_id):
    fixture_url = "https://fantasy.premierleague.com/api/fixtures/"
    fixture_response = requests.get(fixture_url)
    fixtures = json.loads(fixture_response.text)
    for game in fixtures:
        if game["id"] == fixture_id:
            selected_fixture = game
            return selected_fixture
    return 0

def teams_mapper():
    useful_info = {}
    for team_info in base_data['teams']:
        useful_info[team_info['id']] = team_info['name']
    return useful_info

def team_mapper(team_id):
    useful_info = teams_mapper()
    return useful_info[team_id]

# def game_has_been_played(fixture_id):
#     this_fixture = fixture_data(fixture_id)
#     has_started = this_fixture["started"]
#     has_finished = this_fixture["finished"]
#     if has_started and has_finished:
#         status = "PLAYED"
#     elif has_started and not has_finished:
#         status = "ONGOING"
#     else:
#         status = "UNDONE"
#     return status

# def player_has_played(player_id, fixture_id, gw_number):
#     player_details_url = f"https://fantasy.premierleague.com/api/element-summary/{player_id}/"
#     player_details_response = requests.get(player_details_url)
#     player_details = json.loads(player_details_response.text)
#     player_this_gw_data =  player_details["history"][gw_number -1]
#     player_minutes = player_this_gw_data["minutes"]

#     if player_this_gw_data["fixture"] != fixture_id:
#         return "WRONGGAME"
#     if game_has_been_played(fixture_id) == "UNDONE":
#         return "WAITING"
#     if game_has_been_played(fixture_id) == "PLAYED" and player_minutes == 0:
#         return "DIDNOTPLAY"
#     if game_has_been_played(fixture_id) == "PLAYED" and player_minutes >= 1:
#         return "PLAYED"



def get_player_history_details(player_id, gw_number):
    player_details_url = f"https://fantasy.premierleague.com/api/element-summary/{player_id}/"
    player_details_response = requests.get(player_details_url)
    player_details = json.loads(player_details_response.text)

    player_name = base_data["elements"][player_id -1]['web_name']
    element_type = base_data["elements"][player_id -1]['element_type']
    player_this_gw_data =  player_details["history"][gw_number -1]
    this_fixture = player_this_gw_data["fixture"]

    def game_has_been_played(fixture_id):
        this_fixture_data = fixture_data(fixture_id)
        has_started = this_fixture_data["started"]
        has_finished = this_fixture_data["finished"]
        if has_started and has_finished:
            status = "PLAYED"
        elif has_started and not has_finished:
            status = "ONGOING"
        else:
            status = "UNDONE"
        return status

    def player_has_played():
        player_this_gw_data =  player_details["history"][gw_number -1]
        player_minutes = player_this_gw_data["minutes"]

        if player_this_gw_data["fixture"] != this_fixture:
            return "WRONGGAME"
        if game_has_been_played(this_fixture) == "UNDONE":
            return "WAITING"
        if game_has_been_played(this_fixture) == "PLAYED" and player_minutes == 0:
            return "DIDNOTPLAY"
        if game_has_been_played(this_fixture) == "PLAYED" and player_minutes >= 1:
            return "PLAYED"


    useful_details = {
        "player_name": player_name,
        "total_points": player_this_gw_data["total_points"],
        "minutes": player_this_gw_data["minutes"],
        "player_position": element_type_mapper[element_type],
        "player_fixture": this_fixture,
        "opponent_team": team_mapper(player_this_gw_data["opponent_team"]),
        "team_of_player_has_played": game_has_been_played(this_fixture),
        "player_has_played": player_has_played(),
    }
    #print(player_name)
    #return player_details["history"][gw_number -1]
    return useful_details


def get_player_live_details(player_id, gw_number):
    player_details_url = f"https://fantasy.premierleague.com/api/event/{gw_number}/live/"
    #player_details_url = f"https://fantasy.premierleague.com/api/element-summary/{player_id}/"
    player_details_response = requests.get(player_details_url)
    player_details = json.loads(player_details_response.text)

    player_name = base_data["elements"][player_id -1]['web_name']
    element_type = base_data["elements"][player_id -1]['element_type']
    all_players_details = player_details["elements"]
    for player in all_players_details:
        if player_id == player["id"]:
            player_this_gw_data = player["stats"]
            try:
                this_fixture = player["explain"][0]
            except:
                bad_useful_details = {
                    "player_name": player_name,
                    "total_points": 0,
                    "minutes": 0,
                    "player_position": element_type_mapper[element_type],
                    "player_fixture": 0,
                    #"opponent_team": team_mapper(player_this_gw_data["opponent_team"]),
                    "team_of_player_has_played": "OUT_THIS_WEEK",
                    "player_has_played": "OUT_THIS_WEEK_P",
                    "goals": 0,
                    "assists": 0
                }
                return bad_useful_details
            break
    #player_this_gw_data =  player_details["history"][gw_number -1]
    #this_fixture = player_this_gw_data["fixture"]

    fixture_id = this_fixture["fixture"]

    this_fixture_data = fixture_data(fixture_id)
    has_started = this_fixture_data["started"]
    has_finished = this_fixture_data["finished"]
    if has_started and has_finished:
        game_status = "PLAYED"
    elif has_started and not has_finished:
        game_status = "ONGOING"
    else:
        game_status = "UNDONE"

    player_minutes = player_this_gw_data["minutes"]
    player_goals = player_this_gw_data["goals_scored"]
    player_assists = player_this_gw_data["assists"]


    if game_status == "UNDONE":
        player_status =  "WAITING"
    elif game_status == "PLAYED" and player_minutes == 0:
        player_status =  "DIDNOTPLAY"
    elif game_status == "PLAYED" and player_minutes >= 1:
        player_status =  "PLAYED"
    elif game_status == "ONGOING" and player_minutes >= 1:
        player_status =  "PLAYING"
    elif game_status == "ONGOING" and player_minutes == 0:
        player_status =  "BENCHING"
    else:
        player_status =  "OUT_THIS_WEEK"


    useful_details = {
        "player_name": player_name,
        "total_points": player_this_gw_data["total_points"],
        "minutes": player_this_gw_data["minutes"],
        "player_position": element_type_mapper[element_type],
        "player_fixture": this_fixture,
        #"opponent_team": team_mapper(player_this_gw_data["opponent_team"]),
        "team_of_player_has_played": game_status,
        "player_has_played": player_status,
        "goals": player_goals,
        "assists": player_assists
    }
    #print(player_name)
    #return player_details["history"][gw_number -1]
    return useful_details




def live_report_maker_HTML(all_managers_dic, gw_number, city_name):
    final_report_dic = manager_players_info_maker(all_managers_dic, gw_number)
    managers_points = gw_dic_reporter(all_managers_dic, gw_number)
    final_team_points_dic = {}
    city_and_gw_str = f"<h1> {city_name}: (GW: {gw_number})</h1>"
    full_report = []
    table_report = []
    for manager, players in managers_points.items():
        manager_lineup_points = 0
        manager_lineup_goals = 0
        manager_lineup_assists = 0
        manager_bench_points = 0
        manager_bench_goals = 0
        manager_bench_assists = 0
        for player_id, player_name_pos in players.items():
            player_details = get_player_live_details(player_id, gw_number)
            player_total_points =  player_details["total_points"]
            player_total_goals = player_details["goals"]
            player_total_assists = player_details["assists"]
            if player_name_pos[1] <= 11:
                manager_lineup_points = manager_lineup_points + player_total_points
                manager_lineup_goals = manager_lineup_goals + player_total_goals
                manager_lineup_assists = manager_lineup_assists + player_total_assists
            else:
                manager_bench_points = manager_bench_points + player_total_points
                manager_bench_goals = manager_bench_goals + player_total_goals
                manager_bench_assists = manager_bench_assists + player_total_assists
        final_team_points_dic[manager] = (manager_lineup_points, manager_bench_points, 
                                    manager_lineup_goals, manager_bench_goals,
                                    manager_lineup_assists, manager_bench_assists,)
    sorted_managers = sorted(final_team_points_dic.items(), key=lambda x: (x[1][0], x[1][2], x[1][4]), reverse=True)

    top_table_str = f"""
<div class="container mt-5">
    {city_and_gw_str}
</div>
<!-- form-row and form-group etc are removed in Bootstrap 5 -->
<div class="container mt-3">
    <div class="table-responsive">
        <table id="table_id" class="table align-middle table-striped table-hover table-bordered" style="padding: 0.25 rem !important; margin:0.05 rem !important;">
            <thead>
              <tr>
                <th scope="col" style="text-align: center">#</th>
                <th scope="col" style="text-align: left" class="fw-light"> Team</th>
                <th scope="col" style="text-align: center" class="fw-light"> Points(s)</th>
                <th scope="col" style="text-align: center" class="fw-light">Goals</th>
                <th scope="col" style="text-align: center" class="fw-light">Assists</th>
                <th scope="col" style="text-align: center" class="fw-light">Players</th>
                <th scope="col" style="text-align: center" class="fw-light">Bench</th>
              </tr>
            </thead>
            <tbody>

    """
    table_report.append(top_table_str)
    bottom_table_str = """
            </tbody>
        </table>
    </div>
</div>
    """

    for index, item in enumerate(sorted_managers):
        if "Referee" in item[0]:
            continue
        print(index, ":", item)
        points_bench_str = f"{str(item[1][0])}"
        a_manager_s_players_report = ""
        for manager, players in final_report_dic.items():
            if manager == item[0]:
                players_report_str = []
                table_header_str = """
                    <div class="table-responsive">
                    <table id="table_id" class="table align-middle table-striped table-hover table-bordered" style="padding: 0.25 rem !important;">
                        <tbody>

                """
                table_footer_str = """
                        </tbody>
                    </table>
                </div>
                """
                gk_in_lineup = []
                defenders_in_lineup = []
                mids_in_lineup = []
                fws_in_lineup = []
                bench_players = []

                for inner_index, player in enumerate(players.keys()):
                    player_report_info, player_pos = player_analysis_HTML(final_report_dic[manager], player)
                    if player_pos == "GK" and inner_index< 4:
                        gk_in_lineup.append(player_report_info)
                    elif player_pos == "DF" and inner_index < 11:
                        defenders_in_lineup.append(player_report_info)
                    elif player_pos == "MF" and inner_index < 11:
                        mids_in_lineup.append(player_report_info)
                    elif player_pos == "FW" and inner_index < 11:
                        fws_in_lineup.append(player_report_info)
                    elif inner_index >= 11:
                        bench_players.append(player_report_info)
                
                    #players_report_str.append(player_report_str)
                goalie_row = "<tr><td class='GK_ROW'>" + "\n".join(gk_in_lineup)  + "</td></tr>"
                defender_row = "<tr><td class='DF_ROW'>" + "\n".join(defenders_in_lineup)  + "</td></tr>"
                midfielder_row = "<tr><td class='MF_ROW'>" + "\n".join(mids_in_lineup)  + "</td></tr>"
                forward_row = "<tr><td class='FW_ROW'>" + "\n".join(fws_in_lineup)  + "</td></tr>"
                for bench_index, bench_player in enumerate(bench_players):
                    if bench_index == 0:
                        bencher_0 = "<tr><td class='B_ROW1'>" + bench_player  + "</td></tr>"
                    if bench_index == 1:
                        bencher_1 = "<tr><td class='B_ROW2'>" + bench_player  + "</td></tr>"
                    if bench_index == 2:
                        bencher_2 = "<tr><td class='B_ROW3'>" + bench_player  + "</td></tr>"
                    if bench_index == 3:
                        bencher_3 = "<tr><td class='B_ROW4'>" + bench_player  + "</td></tr>"
                a_manager_s_lineup_players_report = table_header_str + goalie_row + defender_row + midfielder_row + forward_row + table_footer_str
                a_manager_s_bench_players_report = table_header_str + bencher_0 + bencher_1 + bencher_2 + bencher_3 + table_footer_str
                #a_manager_s_lineup_players_report = "\n    ".join(players_report_str)

        if index == 0:
            team_name = u"\U0001F947" + " " + item[0]
            team_rank_str = f"""
            <tr> 
                <td style="text-align: left">{str(index+1)} </td>
                <td style="text-align: left"><h5>{team_name}</h5> </td>
                <td style="text-align: center"><h5>{points_bench_str}</h5> </td>
                <td style="text-align: center"><h5>{str(item[1][2])}</h5> </td>
                <td style="text-align: center"><h5>{str(item[1][4])}</h5> </td>
                <td style="text-align: center">{a_manager_s_lineup_players_report} </td>
                <td style="text-align: center">{a_manager_s_bench_players_report} </td>
            </tr>
            """
        elif index == 1:
            team_name = u"\U0001F948" + " " + item[0]
            team_rank_str = f"""
            <tr> 
                <td style="text-align: left">{str(index+1)} </td>
                <td style="text-align: left"><h5>{team_name}</h5> </td>
                <td style="text-align: center"><h5>{points_bench_str}</h5> </td>
                <td style="text-align: center"><h5>{str(item[1][2])}</h5> </td>
                <td style="text-align: center"><h5>{str(item[1][4])}</h5> </td>
                <td style="text-align: center">{a_manager_s_lineup_players_report} </td>
                <td style="text-align: center">{a_manager_s_bench_players_report} </td>
            </tr>
            """
        elif index == 2:
            team_name = u"\U0001F949" + " " + item[0]
            team_rank_str = f"""
            <tr> 
                <td style="text-align: left">{str(index+1)} </td>
                <td style="text-align: left"><h5> {team_name}</h5>  </td>
                <td style="text-align: center"><h5>{points_bench_str}</h5> </td>
                <td style="text-align: center"><h5>{str(item[1][2])}</h5> </td>
                <td style="text-align: center"><h5>{str(item[1][4])}</h5> </td>
                <td style="text-align: center">{a_manager_s_lineup_players_report} </td>
                <td style="text-align: center">{a_manager_s_bench_players_report} </td>
            </tr>
            """
        else:
            team_name = item[0]
            team_rank_str = f"""
            <tr> 
                <td style="text-align: left">{str(index+1)} </td>
                <td style="text-align: left"><h5> {team_name}</h5>  </td>
                <td style="text-align: center"><h5> {points_bench_str}</h5> </td>
                <td style="text-align: center"><h5> {str(item[1][2])}</h5> </td>
                <td style="text-align: center"><h5> {str(item[1][4])}</h5> </td>
                <td style="text-align: center">{a_manager_s_lineup_players_report} </td>
                <td style="text-align: center">{a_manager_s_bench_players_report} </td>
            </tr>
            """

        table_report.append(team_rank_str)
    table_report.append(bottom_table_str)
    table_report_str = "\n".join(table_report)
    full_report.append(table_report_str)

    with open(f"fpl_{city_name}.html", "w") as my_file:
        my_file.write(table_report_str)

    print("\n\n******  More Details  ******** \n")
    # for manager, players in final_report_dic.items():
    #     #print(manager, players)
    #     final_report_list = []
    #     manager_total_pts = final_team_points_dic[manager][0]
    #     team_title = f"{manager::<52}{manager_total_pts:>3} pts\n"
    #     final_report_list.append(team_title)
    #     for index, player in enumerate(players.keys()):
    #         player_report_str = player_analysis(final_report_dic[manager], player)
    #         if index == 11:
    #             final_report_list.append("_"*56)
    #         final_report_list.append(player_report_str)
    #     manager_report = "\n    ".join(final_report_list)
    #     full_report.append(manager_report)
    #return  f"\n\n{'='*60}\n".join(full_report)
    return f"\n".join(full_report)

def live_HTML_All(dic_of_all_league_name_cities, gw_number):
    every_thing_all_in_one = []
    toptop_table_str = f"""{{% extends "core/fpl-base.html" %}}
{{% load crispy_forms_tags %}}
{{% block content %}}
"""
    every_thing_all_in_one.append(toptop_table_str)
    bottombottom_table_str = f"""
{{% endblock %}}
"""
    for city_name, all_managers_per_league_dic in dic_of_all_league_name_cities.items():
        new_city = live_report_maker_HTML(all_managers_per_league_dic, gw_number, city_name)
        every_thing_all_in_one.append(new_city)
        # make all teams in one league:
    every_thing_all_in_one.append(bottombottom_table_str)
    with open(f"fpl_all_together.html", "w") as my_file:
        my_file.write("\n".join(every_thing_all_in_one))


