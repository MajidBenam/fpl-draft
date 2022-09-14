import requests
import pandas as pd
import json
import pprint
my_tops = []

base_url_draft = "https://draft.premierleague.com/api/bootstrap-static"
base_url_fantasy = "https://fantasy.premierleague.com/api/bootstrap-static"

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


def table_maker(all_managers_dic, gw_number):
    managers_points = gw_dic_reporter(all_managers_dic, gw_number)
    final_points_dic = {}
    for manager, players in managers_points.items():
        manager_lineup_points = 0
        manager_bench_points = 0
        for player_id, player_name_pos in players.items():
            player_details = get_player_history_details(player_id, gw_number)
            player_total_points =  player_details["total_points"]
            if player_name_pos[1] <= 11:
                manager_lineup_points = manager_lineup_points + player_total_points
            else:
                manager_bench_points = manager_bench_points + player_total_points
        final_points_dic[manager] = (manager_lineup_points, manager_bench_points)

    sort_managers = sorted(final_points_dic.items(), key=lambda x: x[1], reverse=True)
    return sort_managers

def manager_players_info_maker(all_managers_dic, gw_number):
    managers_points = gw_dic_reporter(all_managers_dic, gw_number)
    final_report_dic = {}
    for manager, players in managers_points.items():
        players_details = {}
        for player_id, player_name_pos in players.items():
            player_details = get_player_history_details(player_id, gw_number)
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
        player_report = f"PLAYED  ({player_position}): {player_name:.<30} {player_info['total_points']: >2} point(s)"
        return player_report
    if team_status == 'PLAYED' and player_status == 'DIDNOTPLAY':
        player_report = f"Benched ({player_position}): {player_name:.<42}"
        return player_report
    if team_status == 'ONGOING' and player_status == 'DIDNOTPLAY':
        player_report = f"Still Benched ({player_position}): {player_name} was benched and has got no point(s) yet."
        return player_report
    if team_status == 'UNDONE':
        player_report = f"Waiting ({player_position}): {player_name:.<30}???????????"
        return player_report

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
            player_details = get_player_history_details(player_id, gw_number)
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
