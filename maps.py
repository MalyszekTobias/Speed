import maps as map_dir
import os

names = []
maps = []
orders = []
allowed_chars = []

def import_map(name):
    file = open('maps/' + name, 'r')
    content = []
    for line in file:
        if line[0] != '[':
            l = line.strip()
            if l[0:10] == 'characters':
                l = l.split()
                l.pop(0)
                a = [int(i) for i in l]
                allowed_chars.append(a)
                print('a', a)
            else:
                orders.append(int(l))
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
    global allowed_chars
    for file in os.listdir('maps'):
        import_map(file)
        if len(maps)> len(allowed_chars):
            allowed_chars.append([0,1,2,3])
    tempmaps, tempnames, tempchars = [0 for i in range(2*len(maps))], [0 for i in range(2*len(names))], [0 for i in range(2*len(allowed_chars))]
    for i in range(len(maps)):
        o = orders[i]
        while o < len(tempmaps):
            if tempmaps[o] == 0:
                tempmaps[o] = maps[i]
                tempnames[o] = names[i]
                tempchars[o] = allowed_chars[i]
                break
            else:
                o += 1

    maps, names, allowed_chars = tempmaps, tempnames, tempchars
    while maps.__contains__(0):
        maps.remove(0)
        names.remove(0)
        allowed_chars.remove(0)
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
    orders.sort()
def delete(i):
    os.remove('maps/' + names[i] + '.txt')
    names.pop(i)
    maps.pop(i)
    orders.pop(i)
    allowed_chars.pop(i)

def add(mapName, map, original=None):
    order = str(len(maps))
    if original != None:
        os.rename('maps/' + original + '.txt', 'maps/' + mapName + '.txt')
        mapIndex = names.index(original)
        order = str(orders[mapIndex])
    newMap = open('maps/' + mapName + '.txt', 'w')
    newMap.write(' '.join(order))
    newMap.write('\n')

    for row in map:
        newMap.write(' '.join(str(row)))
        newMap.write('\n')
    if original == None:
        names.append(mapName)
        maps.append(map)
        orders.append(len(maps) - 1)
        allowed_chars.append([0,1,2,3])
