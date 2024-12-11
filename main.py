import os

try:
    from pypresence import Presence
    import pytimedinput
    import validators
except ModuleNotFoundError:
    install = input(
        "Some modules that this program uses are not installed. Would you like to install them automatically? [Y/N]: "
    ).strip()
    if install.lower() == "y" or install.lower() == "yes":
        if os.name == "nt":
            os.system("pip install -r requirements.txt")
        elif os.name == "posix":
            os.system("pip3 install -r requirements.txt")
        else:
            input(
                "The current operating software is not supported by FootyRP. Press ENTER to exit..."
            )
    else:
        input(
            "The program cannot run without the required modules. Press ENTER to exit..."
        )
try:
    import information
    import mapper
    import help
except FileNotFoundError:
    pass


def main():
    home_score = 0
    away_score = 0
    firstHalf = True
    lastEvent = ""
    lastEventDetails = ""
    state = ""
    stoppage_time = ""

    os.system("cls")
    information.match_time = input(
        "Enter the match time in the 24h format (HH:MM:SS Ex: 20:30:00): "
    ).strip()
    try:
        try:
            time_check = "".join(information.match_time.split(":"))
        except ValueError:
            pass
        time_check = int(time_check)
    except ValueError:
        pass
    while not isinstance(time_check, int) or len(information.match_time) != 8:
        print("\nInvalid time entered. Please enter a valid time.")
        information.match_time = input(
            "Enter the match time in the 24h format (HH:MM:SS Ex: 20:30:00): "
        ).strip()
        try:
            try:
                time_check = "".join(information.match_time.split(":"))
            except ValueError:
                pass
            time_check = int(time_check)
        except ValueError:
            pass
    while information.tournament.lower() not in mapper.tournaments:
        information.tournament = input("Enter Tournament Name: ")
        if information.tournament == "" or information.tournament.isspace():
            print("\nTournament field can't be leave empty.")
        elif information.tournament.lower() not in mapper.tournaments:
            print("\nFootyRP doesn't support this tournament at the moment")
    information.home_team = input("Enter Home Team Name: ").strip()
    while information.home_team == "" or information.home_team.isspace():
        print("\nInvalid team name. Team name can't be empty")
        information.home_team = input("Enter Home Team Name: ").strip()
    information.away_team = input("Enter Away Team Name: ").strip()
    while information.away_team == "" or information.away_team.isspace():
        print("\nInvalid team name. Team name can't be empty")
        information.away_team = input("Enter Home Team Name: ").strip()
    information.match_stats = input(
        "Enter Match Stats URL (Leave empty for no link): "
    ).strip()
    while (
        information.match_stats != ""
        and validators.url(information.match_stats) is not True
    ):
        print("\nInvalid URL. Please enter a valid URL.")
        information.match_stats = input(
            "Enter Match Stats URL (Leave empty for no link): "
        ).strip()

    RPC = Presence("1262177540907470858")
    RPC.connect()

    while True:
        os.system("cls")
        if firstHalf:
            half = "1st Half"
        else:
            half = "2nd Half"
        previous_state = state
        state = information.get_time_left() if state != "FULL TIME" else "FULL TIME"
        RPC.update(
            large_image=mapper.tournaments.get(f"{information.tournament.lower()}")[0],
            large_text=f"{mapper.tournaments.get(information.tournament.lower())[1]} {information.season}",  # {match_information.year if mapper.tournaments.get(match_information.tournament.lower())[2] == "tournament" else match_information.season}"
            details=f"{information.home_team} {home_score} - {away_score} {information.away_team}",
            state=(
                state
                if previous_state != "KICK OFF!"
                else f"Match Time: {information.get_time_elapsed()} {stoppage_time}"
            ),
            small_image=(mapper.events.get(lastEvent) if lastEvent != "" else None),
            small_text=lastEventDetails if lastEventDetails != "" else None,
            buttons=(
                [{"label": "Match Stats", "url": information.match_stats}]
                if information.match_stats.isalnum()
                else None
            ),
        )
        choice, timedOut = pytimedinput.timedInput(
            prompt="Enter Event (Type help for....help DUH): ",
            timeout=3,
            resetOnInput=True,
        )

        if choice.lower() == "kick off":
            lastEvent = "kick off"
            lastEventDetails = "KICK OFF!"

        elif choice.lower().startswith("goal"):
            try:
                event, team = choice.lower().split(" ")
            except ValueError:
                team = input("Enter [h]ome or [a]way: ").strip()
            if (
                team.lower().strip() == "h"
                or team.lower().strip() == "home"
                or team.lower().strip() == information.home_team.lower()
            ):
                home_score += 1
            elif (
                team.lower().strip() == "a"
                or team.lower().strip() == "away"
                or team.lower().strip() == information.away_team.lower()
            ):
                away_score += 1
            else:
                input(
                    "\nPlease provide whether the goal was scored for the home or away side. Press ENTER to continue..."
                )
            if team.lower() == "h" or team.lower() == "a":
                goalscorer = input("Enter goalscorer (Leave empty for no goalscorer): ")
                lastEvent = "goal" if goalscorer != "" or goalscorer.isspace() else None
                lastEventDetails = (
                    f"GOAL!: {goalscorer}"
                    if goalscorer != "" or goalscorer.isspace()
                    else None
                )

        elif choice.lower().startswith("remove"):
            try:
                event, team = choice.lower().split(" ")
            except ValueError:
                team = input("Enter [h]ome or [a]way: ").strip()
            if (
                team.lower().strip() == "h"
                or team.lower().strip() == "home"
                or team.lower().strip() == information.home_team.lower()
            ):
                home_score -= 1
            elif (
                team.lower().strip() == "a"
                or team.lower().strip() == "away"
                or team.lower().strip() == information.away_team.lower()
            ):
                away_score -= 1
            else:
                input(
                    "\nPlease provide whether the goal was removed for the home or away side. Press ENTER to continue..."
                )

        elif choice.lower() == "half time" and half != "2nd Half":
            RPC.update(
                large_image=mapper.tournaments.get(f"{information.tournament.lower()}")[
                    0
                ],
                large_text=f"{information.tournament} {information.season}",  # {information.year if mapper.tournaments.get(information.tournament.lower())[1] == "tournament" else information.season}"
                details=f"{information.home_team} {home_score} - {away_score} {information.away_team}",
                state=("HALF TIME"),
                buttons=[{"label": "Match Stats", "url": information.match_stats}],
            )
            input("Press ENTER to start timer...")
            information.match_time = input(
                "Enter then match time in the format (HH:MM:SS): "
            )
            lastEventDetails = "2nd Half Kick Off"
            firstHalf = False

        elif choice.lower().startswith("stoppage"):
            try:
                event, stoppage = choice.split(" ", maxsplit=1)
            except ValueError:
                stoppage = input("Enter number of stoppage minutes: ").strip()
            try:
                stoppage = int(stoppage.strip())
            except ValueError:
                pass
            while not isinstance(stoppage, int):
                print("\nInvalid number of minutes. Please enter a number")
                try:
                    stoppage = int(input("Enter number of stoppage minutes: ").strip())
                except ValueError:
                    pass
            stoppage_time = f"+{stoppage}'"

        elif choice.lower().startswith("yellow"):
            try:
                event, player = choice.split(" ", maxsplit=1)
            except ValueError:
                player = input("Enter player name: ")
            while player == "" or player.isspace() or player.isalpha() is False:
                print(
                    "\nInvalid player name (No numbers or symbols). Please provide the correct player name."
                )
                player = input("Enter player name: ")
            lastEvent = "yellow"
            lastEventDetails = f"Yellow card: {player.strip()}"

        elif choice.lower() == "red":
            try:
                event, players = choice.split(" ", maxsplit=1)
            except ValueError:
                player = input("Enter player name: ")
            while player == "" or player.isspace() or player.isalpha is False:
                print(
                    "\nInvalid player name (No numbers or symbols). Please provide the correct player name."
                )
                player = input("Enter player name: ")
            lastEvent = "red"
            lastEventDetails = f"Red card: {player.strip()}"

        elif choice.lower() == "clear":
            lastEvent, lastEventDetails = "", ""

        elif choice.lower() == "end":
            RPC.update(
                large_image=mapper.tournaments.get(f"{information.tournament.lower()}")[
                    0
                ],
                large_text=f"{information.tournament} {information.season}",  # {information.year if mapper.tournaments.get(information.tournament.lower())[1] == "tournament" else information.season}"
                details=f"{information.home_team} {home_score} - {away_score} {information.away_team}",
                state=("FULL TIME"),
                buttons=(
                    [{"label": "Match Stats", "url": information.match_stats}]
                    if information.match_stats.isalnum()
                    else None
                ),
            )
            input()
            break

        elif choice.lower() == "stop":
            break

        elif choice.lower().startswith("help"):
            try:
                choice, command = choice.split(" ", maxsplit=1)
                input(
                    f"\n{command}: {help.commands.get(command)}\n\nPress ENTER to continue..."
                )
            except:
                input(
                    """Command: Usage

• Goal: This command adds a goal to either the home or away side. Usage: goal [h]ome OR goal [a]way

• Remove: This command removes a goal from either the home or away side. Usage: remove [h]ome OR remove [a]way

• Yellow: This command is used to indicate a yellow card given to a player. Usage: yellow <player name> OR yellow

• Red: This command is used to indicate a red card given to a player. Usage: red <player name> OR red

• Clear: This command is used to clear the small image and text in your discord presence.Usage: clear

• Half time: This command is used to stop the timer and indicate half time. Usage: half time

• Stoppage: This command is used to add stoppage time to your discord presence. Usage: stoppage <n> OR stoppage

• Help: This command is used to display the list of commands and their usage. Usage: help

• stop: This command is used to stop the program. Usage: stop

Press ENTER to close this menu..."""
                )
                os.system("cls")


if __name__ == "__main__":
    main()
