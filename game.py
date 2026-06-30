players = {}

game_started = False

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
