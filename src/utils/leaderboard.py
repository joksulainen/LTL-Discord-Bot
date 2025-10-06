import datetime
from dataclasses import dataclass


@dataclass(frozen=True)
class LeaderboardEntry:
    user_id: int
    eliminated_at: float


def strftdelta(tdelta: datetime.timedelta) -> str:
    # get the individual time components
    total = tdelta.total_seconds()
    hours = total // 3600
    minutes, seconds = divmod(hours % 3600, 60)
    
    # build the final string
    # this is ugly but it does what i need it to do
    string = ""
    if hours > 0:
        string += f"{int(hours)}h {int(minutes)}m "
    elif minutes > 0:
        string += f"{int(minutes)}m "
    string += f"{int(seconds)}s"
    
    return string

def format_lb_entry(entry: LeaderboardEntry, start_time: float) -> str:
    delta = datetime.datetime.fromtimestamp(entry.eliminated_at, datetime.UTC) - datetime.datetime.fromtimestamp(start_time, datetime.UTC)
    return f"<@{entry.user_id}> - `{strftdelta(delta)}`"
