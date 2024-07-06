DEFAULT_SETTINGS = {
    "imposter_count": 3,
    "reveal_role": True,
    "emergency_meetings": 3,
    "discussion_time": 600,
    "emergency_cooldown": 30,
    "kill_cooldown": 30,
    "short_tasks": 2,
    "long_tasks": 2,
    "common_tasks": 1
}


class Game:

    def __init__(self, settings, users):
        self.settings = settings


class Players:

    def __init__(self, user):
        self.user = user
        self.alive = True
        self.role = None
        self.tasks = []

