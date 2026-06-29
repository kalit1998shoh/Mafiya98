players = {}

game_started = False

roles = {}

alive_players = set()

dead_players = set()

day = 1

phase = "lobby"      # lobby, night, discussion, voting

mafia_choice = None

doctor_choice = None

commissioner_choice = None

maniac_choice = None

votes = {}

mafia_target = None
doctor_save = None
commissioner_check = None
