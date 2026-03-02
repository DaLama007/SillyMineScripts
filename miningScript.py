from minescript import *
import sys
import time
import collections
import data as d

#def on_command():

#func to calc time in s for specfic block with specific tool
def timePerBlock(tool_enchantlevel):
    #todo: maybe add some set tick speed setting

    #get required values for calc
    items = player_hand_items()
    tool = items.main_hand['item']
    block = player_get_targeted_block()
    block = block.type
    #calculate intermediate values
    
    hardness = d.BLOCK_HARDNESS[block]*1.5
    speed = d.TOOL_SPEEDS[tool][0]
    efficiency_multiplier = 1 + (tool_enchantlevel**2+1)/5
    #calculate full time
    echo(f"Block key: {block}")
    echo(f"Block hardness lookup: {d.BLOCK_HARDNESS.get(block)}")
    result = hardness/(speed*1.3**tool_enchantlevel)
    echo(result)
    efficiency_bonus = enchant_level**2 + 1   # e.g. Efficiency V → 26
    effective_speed = d.TOOL_SPEEDS[tool][0] + efficiency_bonus

    ticks_to_break = (d.BLOCK_HARDNESS.get(block)* 1.5 * 30 / effective_speed)
    ticks_to_break = max(ticks_to_break, 4)   # minimum 4 tick “softcap”

    seconds_to_break = ticks_to_break / 20
    return seconds_to_break

# function for one mining iteration
def mine(tool_enchantlevel):
    #look at first block at top 
    player_set_orientation(0, 0)
    mine_time = timePerBlock(tool_enchantlevel)
    player_press_attack(True)
    time.sleep(mine_time)
    player_press_attack(False)
    #look at second block at bottom
    player_set_orientation(0, 45)
    mine_time = timePerBlock(tool_enchantlevel)
    time.sleep(0.3)
    player_press_attack(True)
    time.sleep(mine_time+0.2)
    player_press_attack(False)
    #look at y-1 block with +1 in the facing direction
    player_set_orientation(0,75)
    block = player_get_targeted_block()
    if block != "lava":
        player_press_forward(True)
        time.sleep(0.5)
        player_press_forward(False)   

enchant_level =3 
# Get the player's position, rounded to the nearest integer:
x, y, z = [round(p) for p in player().position]

# todo: ask the efficiency level of players tool

#efficiency = echo("Enter efficiency level of your tool:")
# add_event_listener(ChatEventListener,on_command)

# main loop
while True:
    for i in range(3):
        echo(i)
        mine(enchant_level)
    break
