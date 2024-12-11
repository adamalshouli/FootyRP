import datetime

match_time = ""
home_team = ""
away_team = ""
tournament = ""
season = "24/25"
match_stats = ""


def get_time_left():
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    hours, minutes, seconds = current_time.split(":")
    match_hours, match_minutes, match_seconds = match_time.split(":")
    seconds = int(seconds) + int(minutes) * 60 + int(hours) * 3600
    match_seconds = (
        int(match_seconds) + int(match_minutes) * 60 + int(match_hours) * 3600
    )
    time_left = match_seconds - seconds - 1
    hours_left = time_left // 3600
    time_left -= hours_left * 3600
    minutes_left = time_left // 60
    time_left -= minutes_left * 60
    total_left = hours_left * 3600 + minutes_left * 60 + time_left
    if total_left > 0:
        if hours_left == 0:
            if minutes_left != 0:
                if minutes_left == 1:
                    return f"Kick off in {minutes_left} minute {time_left} seconds"
                else:
                    return f"Kick off in {minutes_left} minutes {time_left} seconds"
            else:
                if time_left == 1:
                    return f"Kick off in {time_left} second"
                else:
                    return f"Kick off in {time_left} seconds"
        elif hours_left == 1:
            if minutes_left == 1:
                return f"Kick off in {hours_left} hour {minutes_left} minute"
            else:
                return f"Kick off in {hours_left} hour {minutes_left} minutes"
        else:
            if minutes_left == 1:
                return f"Kick off in {hours_left} hours {minutes_left} minute"
            else:
                return f"Kick off in {hours_left} hours {minutes_left} minutes"
    return "KICK OFF!"


def get_time_elapsed():
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    hours, minutes, seconds = current_time.split(":")
    match_hours, match_minutes, match_seconds = match_time.split(":")
    seconds = int(seconds) + int(minutes) * 60 + int(hours) * 3600
    match_seconds = (
        int(match_seconds) + int(match_minutes) * 60 + int(match_hours) * 3600
    )
    time_elapsed = seconds - match_seconds + 1
    minutes_elapsed = time_elapsed // 60
    time_elapsed -= minutes_elapsed * 60
    return f"{minutes_elapsed:02}:{time_elapsed:02}"


def stoppage_elapsed():
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    hours, minutes, seconds = current_time.split(":")
    match_hours, match_minutes, match_seconds = match_time.split(":")
    seconds = int(seconds) + int(minutes) * 60 + int(hours) * 3600
    match_seconds = (
        int(match_seconds) + int(match_minutes) * 60 + int(match_hours) * 3600
    )
    stoppage_time_elapsed = seconds - match_seconds + 1
    stoppage_minutes_elapsed = stoppage_time_elapsed // 60
    stoppage_time_elapsed -= stoppage_minutes_elapsed * 60
    return f"{stoppage_minutes_elapsed:02}:{stoppage_time_elapsed:02}"
