import json


def read_from_file(data):
    return UnitStats(data['name'], data['unit_strength'], StatBlock(*data['stats'].values()),
                     data['troop_type'], data['character'], data['command'], data['equipped'],
                     data['weapon'], data['rules'], data['wargear'])


class GearCheck:
    def __init__(self, unit):
        self.unit = unit

    def stat_change(self):
        if self.unit.weapon == 'Polearm':
            self.unit.stats.s += 1
            self.unit.rules.append('Two-handed weapon')
        elif self.unit.weapon == 'Great Weapon':
            self.unit.stats.s += 1
            if self.unit.stats.i <= 2:
                self.unit.stats.i = 1
            else:
                self.unit.stats.i -= 2
            self.unit.rules.append('Two-handed weapon')
            self.unit.rules.append('Great weapon')
        elif self.unit.weapon == 'Flail':
            self.unit.stats.s += 2
            self.unit.rules.append('Two-handed weapon')
        elif self.unit.weapon == 'Spears' and self.unit.troop_type not in ['Cavalry', 'Monstrous cavalry', 'Monster']:
            self.unit.rules.append('Spears on foot')
            self.unit.rules.append('Fight in extra ranks: 1')
        elif self.unit.weapon == 'Pikes':
            self.unit.rules.append('Fight in extra ranks: 3')
            self.unit.rules.append('Two-handed weapon')
            self.unit.rules.append('Pikes')
        elif self.unit.weapon == 'Spears' and self.unit.troop_type in ['Cavalry', 'Monstrous cavalry', 'Monster']:
            self.unit.rules.append('Spears mounted')
        elif self.unit.weapon == 'Lance':
            self.unit.rules.append('Lance')
        elif self.unit.weapon == 'Two hand weapons':
            self.unit.stats.a += 1
            self.unit.rules.append('Two-handed weapon')
            self.unit.rules.append('Parry 6')
        else:
            if 'Shield' in self.unit.equipped:
                self.unit.rules.append('Parry 6')
        if 'Shield' in self.unit.equipped and 'Two-handed weapon' not in self.unit.rules:
            self.unit.stats.save -= 1
        if 'Light armor' in self.unit.equipped:
            self.unit.stats.save -= 1


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
    def __init__(self, name, unit_strength, stats, troop_type, character, command, equipped, weapon, rules,
                 wargear, split_profile=False):
        self.name = name
        self.unit_strength = unit_strength
        self.stats = stats
        self.troop_type = troop_type
        self.character = character
        self.command = command
        self.equipped = equipped
        self.weapon = weapon
        self.rules = rules
        self.wargear = wargear

    def set_split(self, data):
        self.split_profile = data('Crew WS')


with open('C:\\Users\\Aleksander\\PycharmProjects\\WAPcalc\\stats\\skeleton_warrior.json') as file:
    skeleton_warrior = read_from_file(json.load(file))

with open('C:\\Users\\Aleksander\\PycharmProjects\\WAPcalc\\stats\\tomb_king.json') as file:
    tomb_king = read_from_file(json.load(file))

with open('C:\\Users\\Aleksander\\PycharmProjects\\WAPcalc\\stats\\tomb_swarm.json') as file:
    tomb_swarm = read_from_file(json.load(file))

with open('C:\\Users\\Aleksander\\PycharmProjects\\WAPcalc\\stats\\skeleton_chariot.json') as file:
    skeleton_chariot = read_from_file(json.load(file))
