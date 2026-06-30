players = {}

game_started = False
group_id = None
lobby_owner = None

roles = {}

alive_players = set()
dead_players = set()

day = 1
phase = "lobby"

# Tun tanlovlari
mafia_target = None
doctor_save = None
commissioner_check = None
commissioner_action = None
commissioner_shot = None
commissioner_used_shot = False
maniac_target = None

# Doktor
doctor_last_save = None

# Ovoz berish
votes = {}


def check_winner():
    mafia_count = 0
    citizen_count = 0

    for player_id in alive_players:
        role = roles.get(player_id)

        if role == "🔫 mafia":
            mafia_count += 1
        else:
            citizen_count += 1

    if mafia_count == 0:
        return "citizens"

    if mafia_count >= citizen_count:
        return "🔫 mafia"

    return None


def reset_game():
    global game_started
    global day
    global phase
    global mafia_target
    global doctor_save
    global commissioner_check
    global commissioner_action
    global commissioner_shot
    global commissioner_used_shot
    global maniac_target
    global doctor_last_save

    players.clear()
    roles.clear()
    alive_players.clear()
    dead_players.clear()
    votes.clear()

    game_started = False
    day = 1
    phase = "lobby"

    mafia_target = None
    doctor_save = None
    commissioner_check = None
    commissioner_action = None
    commissioner_shot = None
    commissioner_used_shot = False
    maniac_target = None
    doctor_last_save = None
