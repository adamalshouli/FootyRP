import os
from pypresence import Presence
import pytimedinput
import match_information
import images_mapper

match_information.match_time = input("Enter then match time in the format (HH:MM:SS): ")
match_information.tournament = input("Enter Tournament Name: ")
match_information.home_team = input("Enter Home Team Name: ")
match_information.away_team = input("Enter Away Team Name: ")
match_information.match_stats = input("Enter Match Stats URL: ")
home_score = 0
away_score = 0
firstHalf = True
lastEvent = ""
lastEventDetails = ""
state = ""
stoppage_time = ""

RPC = Presence("1262177540907470858")
RPC.connect()

while True:
    os.system("cls")
    if firstHalf:
        half = "1st Half"
    else:
        half = "2nd Half"
    previous_state = state
    state = match_information.get_time_left() if state != "FULL TIME" else "FULL TIME"
    RPC.update(
        large_image=images_mapper.tournament_images.get(
            f"{match_information.tournament.lower()}"
        )[0],
        large_text=f"{match_information.tournament} {match_information.year if images_mapper.tournament_images.get(match_information.tournament.lower())[1] == "tournament" else match_information.season}",
        details=f"{match_information.home_team} {home_score} - {away_score} {match_information.away_team}",
        state=(
            state
            if previous_state != "KICK OFF!"
            else f"Match Time: {match_information.get_time_elapsed()} {stoppage_time}"
        ),
        small_image=(
            images_mapper.event_images.get(lastEvent) if lastEvent != "" else None
        ),
        small_text=lastEventDetails if lastEventDetails != "" else None,
        buttons=[{"label": "Match Stats", "url": match_information.match_stats}],
    )
    choice, timedOut = pytimedinput.timedInput(
        prompt="Enter Event: ", timeout=1, resetOnInput=True
    )
    if choice.lower() == "kick off":
        lastEvent = "kick off"
        lastEventDetails = "Kick Off"
    elif choice.lower().startswith("goal"):
        event, team = choice.lower().split(" ")
        if team.lower() == "h":
            home_score += 1
            lastEvent = "goal"
            lastEventDetails = f"Goal: {input("Enter goalscorer: ")}"
        elif team.lower() == "a":
            away_score += 1
            lastEvent = "goal"
            lastEventDetails = f"Goal: {input("Enter goalscorer: ")}"
        else:
            pass
    elif choice.lower().startswith("remove"):
        event, team = choice.lower().split(" ")
        if team.lower() == "h":
            home_score -= 1
        elif team.lower() == "a":
            away_score -= 1
        else:
            pass
    elif choice.lower() == "half time":
        RPC.update(
            large_image=images_mapper.tournament_images.get(
                f"{match_information.tournament.lower()}"
            )[0],
            large_text=f"{match_information.tournament} {match_information.year if images_mapper.tournament_images.get(match_information.tournament.lower())[1] == "tournament" else match_information.season}",
            details=f"{match_information.home_team} {home_score} - {away_score} {match_information.away_team}",
            state=("HALF TIME"),
            buttons=[{"label": "Match Stats", "url": match_information.match_stats}],
        )
        input("Press any key to start timer...")
        match_information.match_time = input(
            "Enter then match time in the format (HH:MM:SS): "
        )
        lastEventDetails = "2nd Half Kick Off"
        firstHalf = False
    elif choice.lower() == "stoppage":
        stoppage_time = f"({input("Enter stoppage time in the format (+<n>'): ")})"
    elif choice.lower() == "yellow":
        lastEvent = "yellow"
        lastEventDetails = f"Yellow card: {input("Enter player name: ")}"
    elif choice.lower() == "red":
        lastEvent = "red"
        lastEventDetails = f"Red card: {input("Enter player name: ")}"
    elif choice.lower() == "clear":
        lastEvent, lastEventDetails = "", ""
    elif choice.lower() == "end":
        RPC.update(
            large_image=images_mapper.tournament_images.get(
                f"{match_information.tournament.lower()}"
            )[0],
            large_text=f"{match_information.tournament} {match_information.year if images_mapper.tournament_images.get(match_information.tournament.lower())[1] == "tournament" else match_information.season}",
            details=f"{match_information.home_team} {home_score} - {away_score} {match_information.away_team}",
            state=("FULL TIME"),
            buttons=[{"label": "Match Stats", "url": match_information.match_stats}],
        )
        input()
        break
    elif choice.lower() == "stop":
        break
