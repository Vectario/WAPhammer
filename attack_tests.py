import random

type_strength = {'Infantry': 1, 'Chariots': 3}
models_per_rank = {'Infantry': 5, 'Swarm': 5, 'Chariot': 3}


def roll():
    k = random.randint(1, 6)
    return k


def chance_to_hit(ws_attacker, ws_defender):
    if ws_attacker >= ws_defender * 2:
        return 2
    elif ws_attacker > ws_defender:
        return 3
    elif ws_attacker * 2 + 3 <= ws_defender:
        return 6
    elif ws_attacker * 2 <= ws_defender:
        return 5
    else:
        return 4


def chance_to_wound(s, t):
    if s == t:
        return 4
    elif s == t + 1:
        return 3
    elif s == t - 1:
        return 5
    elif s <= t - 2:
        return 6
    else:
        return 2


def model_attack(attacker, defender, first_round, charger):
    tmp_ward = 0
    if 'Great weapon' in attacker.rules and first_round:
        tmp_s = 1
    elif 'Spears mounted' in attacker.rules and first_round and charger:
        tmp_s = 2
    elif 'Spears on foot' in attacker.rules and first_round and not charger and defender.troop_type in ['Warbeast',
                                                                                                        'Cavalry',
                                                                                                        'Monstrous infantry',
                                                                                                        'Monster',
                                                                                                        'Chariot']:
        tmp_s = 1
    elif 'Pikes' in attacker.rules and first_round and not charger and defender.troop_type in ['Warbeast', 'Cavalry',
                                                                                               'Monstrous infantry',
                                                                                               'Monster', 'Chariot']:
        tmp_s = 1
    elif 'Lance' in attacker.rules and first_round and charger:
        tmp_s = 2
    else:
        tmp_s = 0
    if roll() < chance_to_hit(attacker.stats.ws, defender.stats.ws):
        return 0, 0
    roll_to_wound = roll()
    if 'Poison' in attacker.rules and ('AnimatedConstruct' not in defender.rules
                                       and 'ImmunePoison' not in defender.rules):
        roll_to_wound += 1
    if roll_to_wound < chance_to_wound(attacker.stats.s + tmp_s, defender.stats.t):
        return 0, 1
    if roll() >= defender.stats.save + attacker.stats.s + tmp_s - 3:
        return 0, 2
    if 'Parry 6' in defender.rules:
        tmp_ward = 1
    if defender.stats.ward - tmp_ward <= 6 and roll() >= defender.stats.ward - tmp_ward:
        return 0, 3
    return 1, 1
    # if roll >= chance_to_hit(ws_attacker, ws_defender):
    #     print('Hit')
    #     if roll >= chance_to_wound(s, t):
    #         print('Wounded')
    #         if roll < save + (s - 3):
    #             print('Save failed')
    #             if ward:
    #                 if roll < ward:
    #                     print('Ward failed')
    #                     return 1
    #                 else:
    #                     print('Ward successful')
    #                     return 0
    #             else:
    #                 print('Save successful')
    #                 return 1
    #         else:
    #             print('Not wounded')
    #             return 0
    #     else:
    #         print('Missed')
    #         return 0
    # else:
    #     return 0


def crumbles(unit, score, hp):
    if score > hp:
        score -= hp
        unit.unit_strength -= 1 + score // unit.stats.w
        hp -= score % unit.stats.w
    elif score == hp:
        unit.unit_strength -= 1
        hp = unit.stats.w
    else:
        hp -= score
    return unit.unit_strength, hp


def combat_score_calculation(unit1, unit2, wounds1, wounds2, first_round):
    combat_score1 = wounds1 + first_round + unit1.command['banner'] + (
                unit1.unit_strength // type_strength[unit1.troop_type]) // unit1.models_per_rank[unit1.troop_type]
    combat_score2 = wounds2 + unit2.command['banner']
    if unit1.unit_strength > unit2.unit_strength:
        combat_score1 += 1
    elif unit1.unit_strength < unit2.unit_strength:
        combat_score1 -= 1
    if unit1.unit_strength >= 10:
        combat_score1 += 1
    return combat_score1 - combat_score2


def unit_attacks(attacker, defender, hp_def, first_round, charger):
    a = ''
    print(f'Unit attacks: {attacker.unit_strength}->{defender.unit_strength}', end=' ')
    if attacker.unit_strength <= models_per_rank[attacker.troop_type]:
        effective_attacks = attacker.stats.a * attacker.unit_strength + attacker.command['champion']
    else:
        if attacker.unit_strength > models_per_rank[attacker.troop_type] * 2:
            effective_attacks = attacker.stats.a * models_per_rank[attacker.troop_type] + \
                                models_per_rank[attacker.troop_type] + attacker.command['champion']
            if 'Fight in extra ranks: 1' in attacker.rules:
                tmp = attacker.unit_strength - models_per_rank[attacker.troop_type] * 2
                if tmp >= models_per_rank[attacker.troop_type]:
                    effective_attacks += models_per_rank[attacker.troop_type]
                else:
                    effective_attacks += tmp
            else:
                if 'Fight in extra ranks: 3' in attacker.rules:
                    tmp = attacker.unit_strength - models_per_rank[attacker.troop_type] * 2
                    if tmp // models_per_rank[attacker.troop_type] >= 3:
                        effective_attacks += models_per_rank[attacker.troop_type] * 3
                    else:
                        effective_attacks += tmp
        else:
            effective_attacks = attacker.stats.a * models_per_rank[attacker.troop_type] + attacker.unit_strength - \
                                models_per_rank[attacker.troop_type] + attacker.command['champion']
    for _ in range(effective_attacks):
        result = model_attack(attacker, defender, first_round, charger)
        if result[0]:
            if hp_def - 1 == 0:
                defender.unit_strength -= 1
            else:
                hp_def -= 1
                # statistics[0][4] += 1
        # else:
        # statistics[0][result[1]] += 1
        a += str(result)
    print(a)
    return hp_def, defender.unit_strength
