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
        else:
            content.append(line.strip())
    maps.append(content)

    name = list(name)
    for i in range(4):
        name.pop(-1)
    name = ''.join(name)
    names.append(name)

def startup_map_load():
    global maps
    global orders
    global names
    for file in os.listdir('maps'):
        import_map(file)
    tempmaps, tempnames = [0 for i in range(2*len(maps))], [0 for i in range(2*len(names))]
    for i in range(len(maps)):
        o = orders[i]
        while o < len(tempmaps):
            if tempmaps[o] == 0:
                tempmaps[o] = maps[i]
                tempnames[o] = names[i]
                break
            else:
                o += 1

    maps, names = tempmaps, tempnames
    while maps.__contains__(0):
        maps.remove(0)
        names.remove(0)
    for map in range(len(maps)):
        newmap = []
        for t in maps[map]:
            s = t.strip()
            newline = []
            for letter in s:
                if letter in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
                    newline.append(int(letter))
            newmap.append(newline)
        maps[map] = newmap
def delete(i):
    os.remove('maps/' + names[i] + '.txt')
    names.pop(i)
    maps.pop(i)
    orders.pop(i)

def add(mapName, map):
    newMap = open('maps/' + mapName + '.txt', 'w')
    newMap.write(' '.join(str(len(maps))))
    newMap.write('\n')

    for row in map:
        newMap.write(' '.join(str(row)))
        newMap.write('\n')
    names.append(mapName)
    maps.append(map)
    orders.append(len(maps) - 1)