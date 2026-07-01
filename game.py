import asyncio
players = {}

game_started = False
group_id = None
lobby_owner = None

roles = {}

alive_players = set()
dead_players = set()
started_users = set()

day = 1
phase = "lobby"

# Taymerlar
night_task = None

NIGHT_TIME = 60
DISCUSSION_TIME = 90
VOTE_TIME = 45

# Tun tanlovlari
# 👑 Mafiya Otasi
mafia_father = None

# Mafiyalarning tanlovlari
mafia_votes = {}

# Kim o'ldirdi
killer_role = None
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
        role = players[player_id]["role"]

        if role == "🔫 Mafiya":
            mafia_count += 1
        else:
            citizen_count += 1

    if mafia_count == 0:
        return "👨‍🌾 Aholi"

    if mafia_count >= citizen_count:
        return "🔫 Mafiya"

    return None


def reset_game():
    global mafia_father
    global mafia_votes
    global killer_role
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
    global group_id
    global lobby_owner
    global votes
    
    players.clear()
    roles.clear()
    alive_players.clear()
    dead_players.clear()
    votes.clear()

    game_started = False
    group_id = None
    lobby_owner = None
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
    mafia_father = None
    mafia_votes.clear()
    killer_role = None
