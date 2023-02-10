from json import *

from stats import *
from stats.stats import *
from combat_resolution import *
import dearpygui.dearpygui as dpg
from copy import deepcopy

#
#
# dpg.create_context()
#
#
# def calculate_callback(sender, data):
#     first = stats.blocks2[dpg.get_value('combo_a')]
#     second = stats.blocks2[dpg.get_value('combo_b')]
#     if first == second:
#         second = deepcopy(first)
#     trial(first, second)
#
#
# with dpg.window(tag="Primary Window"):
#     dpg.add_text("Welcome to the Warhammer Armies Project battle calculator!")
#     dpg.add_text('Choose your fighters!')
#     dpg.add_combo(["Skeleton warrior", "Tomb King", "Tomb Swarm"], label='Attacker', tag='combo_a')
#     dpg.add_combo(["Skeleton warrior", "Tomb King", "Tomb Swarm"], label='Defender', tag='combo_b')
#     dpg.add_button(label="Calculate", callback=calculate_callback)
#     dpg.add_text(tag='result')
#
# dpg.create_viewport(title='WAP Calc', width=800, height=600)
# dpg.setup_dearpygui()
# dpg.show_viewport()
# dpg.set_primary_window("Primary Window", True)
# dpg.start_dearpygui()


blocks = {"1": skeleton_warrior, "2": tomb_king, "3": tomb_swarm}
print("Choose the first fighter")
print("1. Skeleton warrior", "2. Tomb King", "3. Tomb Swarm", sep='\n')
first = blocks[input()]
print("Choose the second fighter")
print("1. Skeleton warrior", "2. Tomb King", "3. Tomb Swarm", sep='\n')
second = blocks[input()]
if first == second:
    second = deepcopy(first)
print("Options for the first fighter:")
if not first.character:
    print('Enter the unit size of the first unit')
    first.unit_strength = int(input())*first.unit_strength
if len(first.weapon)>1:
    print(f"Choose weapons from the following: {first.weapon}")
    first.weapon = first.weapon[int(input())]
if first.wargear:
    print("Pick the wargear for ")
stats = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
# print(f'Name: {first.name}', f'Unit strength: {first.unit_strength}', f'Stats: {first.stats}',
#       f'Troop type: {first.troop_type}', f'Character: {first.character}', f'Command: {first.command}',
#       f'Weapon: {first.weapon}', f'Rules: {first.rules}', f'Wargear: {first.wargear}')
trial(first, second)

# Failed to hit, failed to wound, successful armor save, successful ward, actual wounds, combat won by

#
# dpg.destroy_context()

# a, b = first.stats.i + 1, second.stats.i
#
# if a > b:
#     combat(first, second, stats)
#     original_strength[1] = second.unit_strength
# else:
#     combat(second, first, stats)
#     original_strength[0] = second.unit_strength
# hp = second.w
# for j in range(first.a):
#     result = attack(first.ws, second.ws, first.s, second.t, second.save, second.ward)
#     if result[0]:
#         hp -= result[0]
#         if hp == 0:
#             stats[4] += 1
#             break
#     else:
#         stats[result[1]] += 1
# print("Attacker scores:")
# print(f"Failed to hit: {100 * stats[0][0] / (first.stats.a * original_strength[0] * trials)}%",
#       f"Failed to wound: {100 * stats[0][1] / (first.stats.a * original_strength[0] * trials)}%",
#       f"Failed to penetrate: {100 * stats[0][2] / (first.stats.a * original_strength[0] * trials)}%",
#       f"Warded away: {100 * stats[0][3] / (first.stats.a * original_strength[0] * trials)}%",
#       f"Successful wounds: {100 * stats[0][4] / (first.stats.a * original_strength[0] * trials)}%", sep='\n')
# print()
# print("Defender scores:")
# print(f"Failed to hit: {100 * stats[1][0] / (second.stats.a * original_strength[1] * trials)}%",
#       f"Failed to wound: {100 * stats[1][1] / (second.stats.a * original_strength[1] * trials)}%",
#       f"Failed to penetrate: {100 * stats[1][2] / (second.stats.a * original_strength[1] * trials)}%",
#       f"Warded away: {100 * stats[1][3] / (second.stats.a * original_strength[1] * trials)}%",
#       f"Successful wounds: {100 * stats[1][4] / (second.stats.a * original_strength[1] * trials)}%", sep='\n')
# print()
# if stats[0][5] > stats[1][5]:
#     print(f'Attacker won by {stats[0][5] - stats[1][5]}')
# elif [0][5] < stats[1][5]:
#     print(f'Defender won by {stats[0][5] - stats[1][5]}')
# else:
#     print("Draw")
