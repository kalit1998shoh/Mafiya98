import random

def give_roles(players):
    players = list(players)
    random.shuffle(players)

    roles = {}

    roles[players[0]] = "🔫 Mafiya"
    roles[players[1]] = "👮 Komissar"
    roles[players[2]] = "💉 Doktor"

    for player in players[3:]:
        roles[player] = "🙂 Oddiy Aholi"

    return roles
