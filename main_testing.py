from dis import dis
import math
import time

#Returns list which is a row fom the csv

facilities = {
    'waste':[],
    'local_sorting_facility':[],
    'regional_sorting_facility':[],
    'regional_recycling_facility':[]
}
def read_from_csv(file_name):
    res = []
    with open(file_name + ".csv") as csv_file:
        node = [line.split(",") for line in csv_file]
        for i, info in enumerate(node):
            #print ("line{0} = {1}".format(i, info))
            #print(type(info))

            info = ( int(info[0]) , float(info[1]) , float(info[2]) , info[3] , float(info[4]) , float(info[5]) )

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

def BAD_find_quartet():
    solution = tuple()
    QoR = None
    init_weight = 1000
    for wastes in [facilities['waste'][0]]:
        for local_sort in facilities['local_sorting_facility']:
            wastes_to_localSort = abs(get_delta_distance( (wastes[1],wastes[2]) , (local_sort[1],local_sort[2]) ))
            localSort_loss = local_sort[-1] * wastes_to_localSort * init_weight
            for regional_sort in facilities['regional_sorting_facility']:
                localSort_to_regionalSort = abs(get_delta_distance( (local_sort[1],local_sort[2]) , (regional_sort[1],regional_sort[2]) ))
                regionalSort_loss = regional_sort[-1] * localSort_to_regionalSort * (init_weight - localSort_loss)
                for regional_recycling in facilities['regional_recycling_facility']:
                    regionalSort_to_recycle = abs(get_delta_distance( (regional_sort[1],regional_sort[2]) , (regional_recycling[1],regional_recycling[2]) ))
                    regionalRecycling_loss = regional_recycling[-1] * regionalSort_to_recycle * (init_weight - localSort_loss - regionalSort_loss)
                    #Now find QoR
                    final_loss = localSort_loss + regionalSort_loss + regionalRecycling_loss
                    final_distance = wastes_to_localSort + localSort_to_regionalSort + regionalSort_to_recycle
                    this_QoR = final_loss + final_distance
                    if (QoR == None) or (QoR > this_QoR):
                        QoR = this_QoR
                        solution = (wastes[0], local_sort[0], regional_sort[0], regional_recycling[0])
                    else:
                        continue
    print([init_weight, localSort_loss, regionalSort_loss, regionalRecycling_loss])
    print("Old QoR is : " , QoR)
    return solution

def pseudoQoR(ls, prevNode):
    dist = abs(get_delta_distance( (ls[1],ls[2]) , (prevNode[1],prevNode[2]) ))
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
        print(arr[i] , '  -  ' , pseudoQoR(arr[i], facilities['local_sorting_facility'][2]))

def printListNormal(arr):
    for i in range(len(arr)):
        print(arr[i])

def find_quartet():
    pass









start_time = time.time()

all = read_from_csv("C:\\programming\\OEC2022\\test cases\\medium\\test_10000_equal")
#printList(facilities['regional_sorting_facility'])


#print(BAD_find_quartet())

mergeSort(facilities['local_sorting_facility'], facilities['waste'][0])
mergeSort(facilities['regional_sorting_facility'], facilities['local_sorting_facility'][0])
mergeSort(facilities['regional_recycling_facility'], facilities['regional_sorting_facility'][0])

print()

init_weight = 1000
wastes = facilities['waste'][0]
local_sort = facilities['local_sorting_facility'][0]
regional_sort = facilities['regional_sorting_facility'][0]
regional_recycling = facilities['regional_recycling_facility'][0]

wastes_to_localSort = get_delta_distance( (wastes[1],wastes[2]) , (local_sort[1],local_sort[2]) )
localSort_loss = local_sort[-1] * wastes_to_localSort * init_weight

localSort_to_regionalSort = get_delta_distance( (local_sort[1],local_sort[2]) , (regional_sort[1],regional_sort[2]) )
regionalSort_loss = regional_sort[-1] * localSort_to_regionalSort * (init_weight - localSort_loss)

regionalSort_to_recycle = get_delta_distance( (regional_sort[1],regional_sort[2]) , (regional_recycling[1],regional_recycling[2]) )
regionalRecycling_loss = regional_recycling[-1] * regionalSort_to_recycle * (init_weight - localSort_loss - regionalSort_loss)
#Now find QoR
final_loss = localSort_loss + regionalSort_loss + regionalRecycling_loss
final_distance = wastes_to_localSort + localSort_to_regionalSort + regionalSort_to_recycle
this_QoR = final_loss + final_distance

print('new QoR is : ' , this_QoR)

print()
print("--- %s seconds ---" % (time.time() - start_time))



print(facilities['local_sorting_facility'][0])
print(facilities['regional_sorting_facility'][0])
print(facilities['regional_recycling_facility'][0])

print()
#printList(facilities['regional_recycling_facility'])


def bullshit(arr):
    if len(arr) > 1:
  
         # Finding the mid of the array
        mid = len(arr)//2
  
        # Dividing the array elements
        L = arr[:mid]
  
        # into 2 halves
        R = arr[mid:]
  
        # Sorting the first half
        mergeSort(L)
  
        # Sorting the second half
        mergeSort(R)
  
        i = j = k = 0
  
        # Copy data to temp arrays L[] and R[]
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
  
        # Checking if any element was left
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
  
        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1
