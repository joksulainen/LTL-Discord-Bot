from dataclasses import dataclass


@dataclass(frozen=True)
class LeaderboardEntry:
    user_id: int
    eliminated_at: float
