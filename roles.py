import random

def give_roles(players):
    players = list(players)
    random.shuffle(players)

    count = len(players)
    roles_list = []

    # Asosiy rollar
    if count < 5:
        raise ValueError("O'yin boshlanishi uchun kamida 5 nafar o'yinchi kerak.")

    if 5 <= count <= 9:
        roles_list = [
            "🔫 Mafiya",
            "👮 Komissar",
            "💉 Doktor",
        ]

    elif 10 <= count <= 14:
        roles_list = [
            "🔫 Mafiya",
            "🔫 Mafiya",
            "👮 Komissar",
            "💉 Doktor",
            "🔪 Manyak",
        ]

    else:  # 15+
        roles_list = [
            "🔫 Mafiya",
            "🔫 Mafiya",
            "🔫 Mafiya",
            "👮 Komissar",
            "🛡 Komissar Yordamchisi",
            "💉 Doktor",
            "🔪 Manyak",
        ]

    # Qolganlarga Oddiy Aholi
    while len(roles_list) < count:
        roles_list.append("🙂 Oddiy Aholi")

    random.shuffle(roles_list)

    roles = {}
    for player, role in zip(players, roles_list):
        roles[player] = role

    return roles
