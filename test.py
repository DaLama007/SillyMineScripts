from minescript import *
import sys

# Get the player's position, rounded to the nearest integer:
x, y, z = [round(p) for p in player().position]

print(x,y,z)
block = getblock(x,y-1,z)
print(block)
players = execute("list")
player_look_at(x,y-1,z)
echo(players)
data = execute("data get entity Nobody259")
#lines = data.split("\n")
lines = data.split("\n")

for line in lines:
    echo(line)
echo(data)
