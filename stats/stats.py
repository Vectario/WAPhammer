import json


class StatBlock:
    def __init__(self, ws, bs, s, t, w, i, a, ld, save, ward):
        self.ws = ws
        self.bs = bs
        self.s = s
        self.t = t
        self.w = w
        self.i = i
        self.a = a
        self.ld = ld
        self.save = save
        self.ward = ward


class UnitStats:
    def __init__(self, name, unit_strength, stats, troop_type, character, command, weapon, rules, wargear):
        self.name = name
        self.unit_strength = unit_strength
        self.stats = stats
        self.troop_type = troop_type
        self.character = character
        self.command = command
        self.weapon = weapon
        self.rules = rules
        self.wargear = wargear


with open('C:\\Users\\Aleksander\\PycharmProjects\\WAPcalc\\stats\\skeleton_warrior.json') as file:
    data = json.load(file)
    skeleton_warrior = UnitStats(data['name'], data['unit_strength'], StatBlock(*data['stats'].values()),
                                 data['troop_type'], data['character'], data['command'], data['weapon'], data['rules'],
                                 data['wargear'])

with open('C:\\Users\\Aleksander\\PycharmProjects\\WAPcalc\\stats\\tomb_king.json') as file:
    data = json.load(file)

    tomb_king = UnitStats(data['name'], data['unit_strength'], StatBlock(*data['stats'].values()),
                          data['troop_type'], data['character'], data['command'], data['weapon'], data['rules'],
                          data['wargear'])

with open('C:\\Users\\Aleksander\\PycharmProjects\\WAPcalc\\stats\\tomb_swarm.json') as file:
    data = json.load(file)
    tomb_swarm = UnitStats(data['name'], data['unit_strength'], StatBlock(*data['stats'].values()),
                           data['troop_type'], data['character'], data['command'], data['weapon'], data['rules'],
                           data['wargear'])
