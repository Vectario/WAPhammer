from copy import deepcopy

from attack_tests import *


def round_of_combat(attacker, defender):
    first_round = True
    current_round, score = 1, 0
    hp_att, hp_def = attacker.stats.w, defender.stats.w
    while attacker.unit_strength > 0 and defender.unit_strength > 0:
        print(f"Beginning of round {current_round}, initiatives: {attacker.stats.i + first_round}, {defender.stats.i}, "
              f"current strength: {attacker.unit_strength} and {defender.unit_strength}")
        previous_us_att, previous_us_def = attacker.unit_strength, defender.unit_strength
        hp_def_prev, hp_att_prev = hp_def, hp_att
        if attacker.stats.i + first_round > defender.stats.i:
            hp_def, defender.unit_strength = unit_attacks(attacker, defender, hp_def)
            if defender.unit_strength:
                hp_att, attacker.unit_strength = unit_attacks(defender, attacker, hp_att)
        elif attacker.stats.i < defender.stats.i:
            hp_att, attacker.unit_strength = unit_attacks(defender, attacker, hp_att)
            if attacker.unit_strength:
                hp_def, defender.unit_strength = unit_attacks(attacker, defender, hp_def)
        else:
            tmp1 = deepcopy(attacker)
            tmp2 = deepcopy(defender)
            hp_def, tmp2.unit_strength = unit_attacks(tmp1, tmp2, hp_def)
            hp_att, tmp1.unit_strength = unit_attacks(defender, tmp1, hp_att)
            attacker, defender = tmp1, tmp2
            # tmp_att, tmp_def = deepcopy(attacker), deepcopy(defender)
            # hp_def, tmp_def_str = unit_attacks(tmp_att, tmp_def, hp_def)
            # hp_att, tmp_att_str = unit_attacks(attacker, defender, hp_att)
            # print(f'{attacker.unit_strength} -> {tmp_att_str}; {defender.unit_strength} -> {tmp_def_str}')
            # defender.unit_strength = tmp_def_str
            # attacker.unit_strength = tmp_att_str
        if attacker.unit_strength > 0 and defender.unit_strength > 0:
            wounds1 = (previous_us_def - defender.unit_strength) * defender.stats.w + hp_def_prev - hp_def
            wounds2 = (previous_us_att - attacker.unit_strength) * attacker.stats.w + hp_att_prev - hp_att
            score = combat_score_calculation(attacker, defender, wounds1, wounds2, first_round)
            if score == 0:
                if attacker.command['musician'] and not defender.command['musician']:
                    score += 1
                else:
                    if defender.command['musician'] and not attacker.command['musician']:
                        score -= 1
            print(f'Score is {score}, wounds caused: {wounds1}, {wounds2}, current strength: {attacker.unit_strength}, '
                  f'{defender.unit_strength}', end=' ')
            if score > 0 and attacker.unit_strength > 0:
                if 'Unstable' in defender.rules:
                    print('Pre-DC', attacker.unit_strength, defender.unit_strength,  end='->')
                    defender.unit_strength, hp_def = crumbles(defender, abs(score), hp_def)
                    print('DC', attacker.unit_strength, defender.unit_strength)
                else:
                    if 'Unstable' not in defender.rules and roll() > defender.stats.ld - score:
                        print('Defender broke')
                        break
            else:
                if score < 0 and defender.unit_strength > 0:
                    if 'Unstable' in attacker.rules:
                        print('Pre-AC', attacker.unit_strength, defender.unit_strength, end='->')
                        attacker.unit_strength, hp_att = crumbles(attacker, abs(score), hp_att)
                        print('AC', attacker.unit_strength, defender.unit_strength)
                else:
                    if 'Unstable' not in attacker.rules and roll() > attacker.stats.ld - abs(score):
                        print('Attacker broke')
                        break

        print(f'Combat, round {current_round}: attacker has {attacker.unit_strength} unit strength, defender has '
              f'{defender.unit_strength}, {hp_att}/{hp_def}\n')
        current_round += 1
        first_round = False
    return attacker.unit_strength, defender.unit_strength


def trial(first, second):
    trials = 1
    for i in range(trials):
        first.unit_strength, second.unit_strength = round_of_combat(first, second)
        if first.unit_strength > 0 and second.unit_strength <= 0:
            print(f'{first.name} won')
        elif second.unit_strength > 0:
            print(f'{second.name} won')
        else:
            print('Draw')
