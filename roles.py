import random

def give_roles(players):
    players = list(players)
    random.shuffle(players)

    roles = {}

    roles[players[0]] = "🔴 Mafiya"
    roles[players[1]] = "🟢 Doktor"
    roles[players[2]] = "🔍 Komissar"

    for player in players[3:]:
        roles[player] = "👤 Oddiy aholi"

    return roles
