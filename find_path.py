from dis import dis
import math
import time
from turtle import st
import csv
from typing import final
import map

# Returns list which is a row fom the csv

facilities = {
    'waste': [],
    'local_sorting_facility': [],
    'regional_sorting_facility': [],
    'regional_recycling_facility': []
}


def read_from_csv(file_name):
    res = []
    with open(file_name + ".csv") as csv_file:
        node = [line.split(",") for line in csv_file]
        for i, info in enumerate(node):
            #print ("line{0} = {1}".format(i, info))
            # print(type(info))

            info = (int(info[0]), float(info[1]), float(
                info[2]), info[3], float(info[4]), float(info[5]))

            res.append(info)
            if info[3] == 'waste':
                facilities['waste'].append(info)
            elif info[3] == 'local_sorting_facility':
                facilities['local_sorting_facility'].append(info)
            elif info[3] == 'regional_sorting_facility':
                facilities['regional_sorting_facility'].append(info)
            else:
                facilities['regional_recycling_facility'].append(info)
    return res


def create_csv():
    f = open("C:\\programming\\OEC2022\\solution.csv", 'w', newline='')
    return (csv.writer(f), f)


def get_delta_distance(latLon1, latLon2):

    R = 6371
    x1_lat, y1_lon = latLon1
    x2_lat, y2_lon = latLon2
    #print(x1_lat, ",", y1_lon)
    latavg = (int(x1_lat) + int(x2_lat))/2

    x1 = R * int(y1_lon) * math.cos(latavg)
    y1 = R * int(x1_lat)

    x2 = R * int(y2_lon) * math.cos(latavg)
    y2 = R * int(x2_lat)

    return (math.hypot(abs(x1-x2), abs(y1-y2))/1000)


# CALCULATION OF WASTES PICKUPS
def x_val_node(node):
    return node[1]


def y_val_node(node):
    return node[2]


def grid_hasher(node, grid_stats, raw=False):
    # hash coords to step
    if raw:
        x = node[0]
        y = node[1]
    else:
        x = node[1]
        y = node[2]
    x_step = grid_stats[-2]
    y_step = grid_stats[-1]
    x_hash = x//x_step
    y_hash = y//y_step
    hashedStr = str(round(x_hash, 2)) + '|' + str(round(y_hash, 2))
    return hashedStr


grid = dict()
grid_sq_coords = []


def make_grid(step=0.01):
    x_vals = [x_val_node(x) for x in facilities['waste']]
    grid_x_min = min(x_vals)
    grid_x_max = max(x_vals)

    y_vals = [y_val_node(y) for y in facilities['waste']]
    grid_y_min = min(y_vals)
    grid_y_max = max(y_vals)

    print("Bound are: {} -> {} and {} -> {}".format(grid_x_min,
          grid_x_max, grid_y_min, grid_y_max))

    #step = 0.01
    width = grid_x_max - grid_x_min
    height = grid_y_max - grid_y_min
    x_step = step*width
    y_step = step*height

    print(y_step)

    for node in facilities['waste']:
        x = node[1]
        y = node[2]
        # hash coords to step
        x_hash = x//x_step
        y_hash = y//y_step
        hashedStr = str(round(x_hash, 2)) + '|' + str(round(y_hash, 2))
        if hashedStr not in grid.keys():
            grid[hashedStr] = []
            grid_sq_coords.append((round(x_hash, 2), round(y_hash, 2)))
        grid[hashedStr].append(node)

    return (grid_x_min, grid_x_max, grid_y_min, grid_y_max, x_step, y_step)


def nearest_square(hashStr, gridstats):
    mindist = None
    nearest_square = (None, None)
    hash_coords = (tuple(hashStr.split('|')))
    hashPosX, hashPosY = (float(hash_coords[0]), float(hash_coords[1]))

    for sq in grid.keys():
        sq_coords = (tuple(sq.split('|')))
        sqPosX, sqPosY = (float(sq_coords[0]), float(sq_coords[1]))

        dist = get_delta_distance((hashPosX, hashPosY), (sqPosX, sqPosY))
        if (hashPosX, hashPosY) == (sqPosX, sqPosY):
            continue
        if (mindist == None) or (mindist > dist):
            mindist = dist
            nearest_square = (sqPosX, sqPosY)

    #print((sqPosX, sqPosY))
    if mindist == None:
        # print(len(grid.keys()))
        return ""
    return (str(nearest_square[0])+'|'+str(nearest_square[1]))


def deplete_square(hashStr, init_pos, total_dist, out):
    nodes = grid[hashStr]
    final_node = None
    for node in nodes:
        dist = get_delta_distance((init_pos), (node[1], node[2]))
        if dist > 0:
            total_dist = total_dist + dist
            final_node = node
            out.writerow(node)
    return total_dist, final_node


# CALCULATION OF FACILITIES
def pseudoQoR(ls, prevNode):
    dist = abs(get_delta_distance((ls[1], ls[2]), (prevNode[1], prevNode[2])))
    return dist + (ls[-1] * dist * 1000)


def mergeSort(ar, prevNode):
    if len(ar) > 1:

        # Finding the midpoint of the aray
        mid = len(ar)//2
        # Dividing the array elements
        L = ar[:mid]
        R = ar[mid:]
        # Sorting each half
        mergeSort(L, prevNode)
        mergeSort(R, prevNode)
        i = j = k = 0

        # Copy data to temp arays L[] and R[]
        while i < len(L) and j < len(R):
            if pseudoQoR(L[i], prevNode) < pseudoQoR(R[j], prevNode):
                ar[k] = L[i]
                i += 1
            else:
                ar[k] = R[j]
                j += 1
            k += 1
        # Checking if any element was left
        while i < len(L):
            ar[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            ar[k] = R[j]
            j += 1
            k += 1


def printList(arr):
    for i in range(len(arr)):
        print(arr[i], '  -  ', pseudoQoR(arr[i],
              facilities['local_sorting_facility'][2]))


def printListNormal(arr):
    for i in range(len(arr)):
        print(arr[i])


def find_triplet(waste_node, out):

    mergeSort(facilities['local_sorting_facility'], waste_node)
    mergeSort(facilities['regional_sorting_facility'],
              facilities['local_sorting_facility'][0])
    mergeSort(facilities['regional_recycling_facility'],
              facilities['regional_sorting_facility'][0])

    print()

    init_weight = 1000
    init_distance = 0

    wastes = waste_node
    local_sort = facilities['local_sorting_facility'][0]
    regional_sort = facilities['regional_sorting_facility'][0]
    regional_recycling = facilities['regional_recycling_facility'][0]

    wastes_to_localSort = get_delta_distance(
        (wastes[1], wastes[2]), (local_sort[1], local_sort[2]))
    localSort_loss = local_sort[-1] * wastes_to_localSort * init_weight

    localSort_to_regionalSort = get_delta_distance(
        (local_sort[1], local_sort[2]), (regional_sort[1], regional_sort[2]))
    regionalSort_loss = regional_sort[-1] * \
        localSort_to_regionalSort * (init_weight - localSort_loss)

    regionalSort_to_recycle = get_delta_distance(
        (regional_sort[1], regional_sort[2]), (regional_recycling[1], regional_recycling[2]))
    regionalRecycling_loss = regional_recycling[-1] * regionalSort_to_recycle * (
        init_weight - localSort_loss - regionalSort_loss)
    # Now find QoR
    final_loss = localSort_loss + regionalSort_loss + regionalRecycling_loss
    final_distance = init_distance + wastes_to_localSort + \
        localSort_to_regionalSort + regionalSort_to_recycle
    this_QoR = final_loss + final_distance

    print('I think QoR is : ', this_QoR)

    print()

    print(facilities['local_sorting_facility'][0])
    print(facilities['regional_sorting_facility'][0])
    print(facilities['regional_recycling_facility'][0])

    out.writerow(facilities['local_sorting_facility'][0])
    out.writerow(facilities['regional_sorting_facility'][0])
    out.writerow(facilities['regional_recycling_facility'][0])

    return (facilities['local_sorting_facility'][0], facilities['regional_sorting_facility'][0], facilities['regional_recycling_facility'][0])


def collect_waste(out):
    grid_stats = make_grid(step=0.0125)
    # printListNormal((list(grid.keys())))
    # printListNormal(grid_sq_coords)
    print(len(list(grid.keys())))
    print(len(grid_sq_coords))
    total_dist = 0

    waste_node = facilities['waste'][0]
    hash = grid_hasher(waste_node, grid_stats)
    while len(grid.keys()) > 1:
        #print("Working on hash: " + hash)
        total_dist, last = (deplete_square(
            hash, (grid[hash][0][1], grid[hash][0][2]), total_dist, out))
        #hash_coords = (tuple(hash.split('|')))

        #grid_sq_coords.remove( ( float(hash_coords[0]) , float(hash_coords[1]) ) )
        del grid[hash]
        #print("-->Finding sq next to {}".format(hash))
        hash = nearest_square(hash, grid_stats)
        #print("-->Found sq at  {}".format(hash))

    total_dist, final_node = (deplete_square(
        hash, (grid[hash][0][1], grid[hash][0][2]), total_dist, out))
    del grid[hash]

    print(total_dist)
    print(len(grid.keys()))
    print(final_node)

    return final_node


def run(filepath_noextextenion):
    start_time = time.time()

    out, f = create_csv()

    all = read_from_csv(filepath_noextextenion)

    last_node = collect_waste(out)

    find_triplet(last_node, out)

    f.close()

    print("--- %s seconds ---" % (time.time() - start_time))

    map.map('solution.csv')
