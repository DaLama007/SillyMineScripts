from minescript import *
import sys
import time

# Get the player's position, rounded to the nearest integer:
x, y, z = [round(p) for p in player().position]

print(x,y,z)
block = getblock(x,y-1,z)
print(block)
players = execute("list")
player_look_at(x,y,z)
echo(players)
count=0
while True:
    #look at first block at top 
    player_set_orientation(0, 0)
    player_press_attack(True)
    time.sleep(1)
    player_press_attack(False)
    player_set_orientation(0, 45)
    echo(getblock(x,y-1,z+1))
#look at second block at bottom

    player_press_attack(True)
    time.sleep(1)
    player_press_attack(False)
    #look at y-1 block with +1 in the facing direction
    player_set_orientation(0,75)
    block = player_get_targeted_block()
    if block != "lava":
        player_press_forward(True)
        time.sleep(1)
        player_press_forward(False)   #if not lava then go to straight then repeat
    else:
        break
    count+=1
    if count ==10:
        break
