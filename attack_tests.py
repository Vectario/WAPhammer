import random


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


def model_attack(ws_attacker, ws_defender, s_attacker, t_defender, save, ward, rules_attacker, rules_defender):
    if roll() < chance_to_hit(ws_attacker, ws_defender):
        return 0, 0
    roll_to_wound = roll()
    if 'Poison' in rules_attacker and ('AnimatedConstruct' not in rules_defender
                                       and 'ImmunePoison' not in rules_defender):
        roll_to_wound += 1
    if roll_to_wound < chance_to_wound(s_attacker, t_defender):
        return 0, 1
    if roll() >= save + s_attacker - 3:
        return 0, 2
    if ward and roll() >= ward:
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
    # while hp - abs(score) < 0:
    #     unit.unit_strength -= 1
    #     score -= unit.stats.w
    # else:
    #     if abs(score) < hp:
    #         hp -= abs(score)
    #     else:
    #         unit.unit_strength -= abs(score)
    return unit.unit_strength, hp


def combat_score_calculation(unit1, unit2, wounds1, wounds2, first_round):
    combat_score1 = wounds1 + first_round + unit1.command['banner']
    combat_score2 = wounds2 + unit2.command['banner']
    if unit1.unit_strength > unit2.unit_strength:
        combat_score1 += 1
    elif unit1.unit_strength < unit2.unit_strength:
        combat_score1 -= 1
    if unit1.unit_strength >= 10:
        combat_score1 += 1
    return combat_score1 - combat_score2


def unit_attacks(attacker, defender, hp_def):
    a = ''
    print(f'Unit attacks: {attacker.unit_strength}->{defender.unit_strength}', end=' ')
    if attacker.unit_strength <= 5:
        effective_attacks = attacker.stats.a * attacker.unit_strength + attacker.command['champion']
    else:
        effective_attacks = attacker.stats.a * 5 + (attacker.unit_strength - 5) + attacker.command['champion']
    for _ in range(effective_attacks):
        result = model_attack(attacker.stats.ws, defender.stats.ws, attacker.stats.s, defender.stats.t,
                                    defender.stats.save, defender.stats.ward,
                                    attacker.rules, defender.rules)
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

# def combat(first, second, stats):
#     hp = second.stats.w
#     first_score, second_score = 0, 0
#     for j in range(first.stats.a * first.unit_strength):
#         result = attack(first.stats.ws, second.stats.ws, first.stats.s, second.stats.t, second.stats.save,
#                         second.stats.ward)
#         if result[0]:
#             if hp - 1 == 0:
#                 second.unit_strength -= 1
#             else:
#                 hp -= 1
#             first_score += 1
#             stats[0][4] += 1
#         else:
#             stats[0][result[1]] += 1
#     if second.unit_strength:
#         hp = first.stats.w
#         for j in range(second.stats.a * second.unit_strength):
#             result = attack(second.stats.ws, first.stats.ws, second.stats.s, first.stats.t, first.stats.save,
#                             first.stats.ward)
#             if result[0]:
#                 if hp - 1 == 0:
#                     first.unit_strength -= 1
#                 else:
#                     hp -= 1
#                 second_score += 1
#                 stats[1][4] += 1
#             else:
#                 stats[1][result[1]] += 1
#         if first_score > second_score:
#             stats[0][5] += 1
#         else:
#             if second_score > first_score:
#                 stats[1][5] += 1
#     else:
#         stats[0][5] += 1
