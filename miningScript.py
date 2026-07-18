from minescript import *
import sys
import time
import collections
import data as d

blocksps = 5.612 
def detectLava():
    yaw, pitch = player_orientation()
    x,y,z = [int(p) for p in player_position()]
    x2,y2,z2 = x,y,z

    rotation = yaw/90
    echo(f"rotation: {rotation}")

    match rotation:
        case 0:
            z+=1
            z2-=1
            x2+=2
        case 1:
            x-=1
            z2+=2 
            x2+=1
        case 2:
            z+=1
            z2-=1
            x2-=2
        case 3:
            x-=1
            z2-=2 
            x2+=1

    region = get_block_region([x,y,z-2], [x2, y2,z2+2])
    minX, minY, minZ = region.min_pos
    maxX, maxY, maxZ= region.max_pos
    for x in range(minX, maxX): 
        for y in range(minY, maxY): 
            for z in range(minZ, maxZ): 
                if region.get_block(x,y,z).type == "minecraft:lava" and region.get_block(x,y,z).type == "minecraft:flowing_lava":
                    return True
    return False
#func to calc time in s for specfic block with specific tool
def timePerBlock(tool_enchantlevel):
    #todo: maybe add some set tick speed setting
    seconds_to_break = 1
    #get required values for calc
    items = player_hand_items()
    tool = items.main_hand['item']
    block = player_get_targeted_block()
    block = block.type
    #calculate intermediate values
    echo(f"{block}")
    echo(f"Block key: {block}")
    echo(f"Block hardness lookup: {d.BLOCK_HARDNESS.get(block)}")
    hardness = d.BLOCK_HARDNESS.get(block)*1.5
    speed = d.TOOL_SPEEDS[tool][0]
    efficiency_multiplier = 1 + (tool_enchantlevel**2+1)/5
    #calculate full time
    result = hardness/(speed*1.3**tool_enchantlevel)
    echo(result)
    efficiency_bonus = enchant_level**2 + 1   # e.g. Efficiency V → 26
    effective_speed = d.TOOL_SPEEDS[tool][0] + efficiency_bonus

    ticks_to_break = (d.BLOCK_HARDNESS.get(block)* 1.5 * 30 / effective_speed)
    ticks_to_break = max(ticks_to_break, 4)   # minimum 4 tick “softcap”

    seconds_to_break = ticks_to_break / 20+0.05
    return seconds_to_break

# function for one mining iteration
def mine(tool_enchantlevel, player_orientation_yaw):
    #look at first block at top 
    player_set_orientation(player_orientation_yaw, 0)
    mine_time = timePerBlock(tool_enchantlevel)
    player_press_attack(True)
    time.sleep(mine_time)
    player_press_attack(False)
    #look at second block at bottom
    player_set_orientation(player_orientation_yaw, 45)
    mine_time = timePerBlock(tool_enchantlevel)
    time.sleep(0.3)
    player_press_attack(True)
    time.sleep(mine_time+0.2)
    player_press_attack(False)
    #look at y-1 block with +1 in the facing direction
    player_set_orientation(player_orientation_yaw,75)
    block = player_get_targeted_block()
    if not detectLava():
        player_press_forward(True)
        time.sleep(0.5)
        player_press_forward(False)
        return True
    else:
        return False

def walk_back(dist, player_orientation_yaw):
    # trun and sprint
    player_set_orientation(player_orientation_yaw+180,0)
    player_press_sprint(True)

    # calculate time needed and use to know how long to run to reach initial position
    timeNeeded = dist/blocksps
    player_press_forward(True)
    time.sleep(timeNeeded)
    player_press_forward(False)

def multiMine(enchant_level, player_orientation_yaw):
    dist = 0
    for i in range(3):
        echo(i)
        result = mine(enchant_level, player_orientation_yaw)
        if not result:
            break
        dist+=1
    return dist
def stripMine(enchant_level):
    yaw, pitch =  player_orientation()
    player_orientation_yaw =yaw
    echo(f"player_orientation: {player_orientation_yaw}")

    # rotate and mine into left
    player_set_orientation(player_orientation_yaw-90, 0)
    yaw, pitch =  player_orientation()
    player_orientation_yaw =yaw
    dist = multiMine(enchant_level, player_orientation_yaw)
    echo(f"player_orientation: {player_orientation_yaw}")
    walk_back(dist, player_orientation_yaw)
    
    # mine right
    yaw, pitch =  player_orientation()
    player_orientation_yaw =yaw
    echo(f"player_orientation: {player_orientation_yaw}")
    dist = multiMine(enchant_level, player_orientation_yaw)
    walk_back(dist, player_orientation_yaw)

    # turn 90 degrees right 
    yaw, pitch =  player_orientation()
    player_orientation_yaw =yaw
    echo(f"player_orientation: {player_orientation_yaw}")
    player_set_orientation(player_orientation_yaw+90, 0)
    yaw, pitch =  player_orientation()
    player_orientation_yaw =yaw
    straightDist = multiMine(enchant_level, player_orientation_yaw)
    if straightDist is not 3:
        return False
    return True
enchant_level =3
# Get the player's position, rounded to the nearest integer:
x, y, z = [round(p) for p in player().position]

# todo: ask the efficiency level of players tool

#efficiency = echo("Enter efficiency level of your tool:")
# add_event_listener(ChatEventListener,on_command)

# main loop
while True:
    res = stripMine(enchant_level)
    if not res:
        break
