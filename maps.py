import maps as map_dir
import os

names = []
maps = []
orders = []

def import_map(name):
    file = open('maps/' + name, 'r')
    content = []
    for line in file:
        if line[0] != '[':
            orders.append(int(line.strip()))
        content.append(line.strip())
    maps.append(content)
    name = list(name)
    for i in range(4):
        name.pop(-1)
    name = ''.join(name)
    names.append(name)

def starting_map_load():
    global maps
    global orders
    global names
    for file in os.listdir('maps'):
        import_map(file)
    tempmaps, tempnames = [0 for i in range(len(maps))], [0 for i in range(len(names))]
    for i in range(len(maps)):
        o = orders[i]
        tempmaps[o] = maps[i]
        tempnames[o] = names[i]
    maps, names = tempmaps, tempnames

def delete(i):
    os.remove(names[i])
    names.pop(i)
    maps.pop(i)
    orders.pop(i)

def add(mapName, map):
    newMap = open('maps/' + mapName + '.txt', 'w')
    for row in map:
        newMap.write(' '.join(str(row)))
        newMap.write('\n')
    names.append(mapName)
    maps.append(newMap)
    orders.append(len(maps))
