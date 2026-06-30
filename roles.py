import random

def give_roles(players):
    players = list(players)
    random.shuffle(players)

    count = len(players)
    roles = {}

    role_list = []

    if count < 5:
        raise ValueError("Kamida 5 ta o'yinchi kerak.")

    if 5 <= count <= 9:
        role_list = [
            "🔫 Mafiya",
            "👮 Komissar",
            "💉 Doktor",
        ]

    elif 10 <= count <= 14:
        role_list = [
            "🔫 Mafiya",
            "🔫 Mafiya",
            "👮 Komissar",
            "💉 Doktor",
            "🔪 Manyak",
        ]

    else:
        role_list = [
            "🔫 Mafiya",
            "🔫 Mafiya",
            "🔫 Mafiya",
            "👮 Komissar",
            "🛡 Komissar Yordamchisi",
            "💉 Doktor",
            "🔪 Manyak",
        ]

    while len(role_list) < count:
        role_list.append("🙂 Oddiy Aholi")

    random.shuffle(role_list)

    for player, role in zip(players, role_list):
        roles[player] = role

    return roles
