import pandas as pd
import cv2
import pgeocode
import time
import ast

fulldists = pd.read_csv("fulldists.csv", index_col=0, dtype={0:str})
fullroutes = pd.read_csv("fullroutes.csv", index_col=0, dtype={0:str})

def irrelevant_node(relevantroutes, routes):
    #currentroute = [node, dist, remainingdests, availabledests] of latest node
    currentroute = routes[-1]
    #node = {to : [[route1], [route2]]} for current node
    node = relevantroutes[currentroute[0]]
    #change to set, because quicker for large lists
    s = set(currentroute[2])
    for dest in s:
        broken = False
        #every shortest path from the current node to an available node
        for i in node[dest]:
            for x in i:
                if (x in s and x != dest):
                    currentroute[3].remove(dest)
                    broken = True
                    break
            if (broken):
                break
    
    routes[-1] = currentroute
    return (routes)

#root = int, postal code
#distances = dataframe of shortest dists distances[from][to] = dist
#droutes = dataframe of shortests routes
#destinations = list of postal codes
def multi_node(root, distances, droutes, destinations):
    #create list with root included
    tempdests = list(destinations)
    tempdests.append(root)
    tempdests.sort()
    #get only relevant dists + how to get there
    #same format as distances and droutes
    df = distances.filter(tempdests)
    relevantdists = df.filter(tempdests, axis=0)
    df2 = droutes.filter(tempdests)
    relevantroutes = df2.filter(tempdests, axis=0)
    
    #shortest distance and path
    totdistmin = 0
    notablepath = []
    #non visted nodes
    nvisited = list(destinations)

    #for baseline calcs
    #shortestnode = next closest node
    currentnode = root

    while(len(nvisited) > 0):
        relevantsearch = relevantdists[currentnode].filter(nvisited)
        currentnode = relevantsearch.idxmin()
        totdistmin += relevantsearch.min()
        notablepath.append(currentnode)
        nvisited.remove(currentnode)
    
    #go back to root
    totdistmin += relevantdists[currentnode][root]
    notablepath.append(root)
    
    #remainingdests = every remaining dest
    remainingdests = list(destinations)
    #availabledests is the list of destinations relevant to the then current node
    availabledests = list(remainingdests)
    routes = [[root, 0, remainingdests, availabledests]]

    routes = irrelevant_node(relevantroutes, routes)

    #while there still is an available destination
    while(len(routes) != 0):
        #go to next available dest if it exists
        latestroute = routes[-1]
        if (len(latestroute[3]) == 0):
            #if there are no more available dests pop the latest route
            routes.pop(-1)
        else:
            #check if going into the first available node + returning to root is shorter then the current min dist
            #relevantdists[from][to] = distance between nodes
            lfrom = latestroute[0]
            lto = latestroute[3][0]
            #remove the first element from available because it will be longer then the shortest route or it will be appended to routes making it the latestroute
            latestroute[3].pop(0)
            if((latestroute[1] + relevantdists[lfrom][lto] + relevantdists[lto][root]) < totdistmin):
                remainingdests = list(latestroute[2])
                remainingdests.remove(lto)
                #check if every destination has been reached
                if (len(remainingdests) == 0):
                    #if it every destination has been reached it is the new shortest route as shown by the if before
                    totdistmin = latestroute[1] + relevantdists[lfrom][lto] + relevantdists[lto][root]
                    #find notable path
                    notablepath = []
                    for i in range(1, len(routes)):
                        notablepath.append(routes[i][0])
                    notablepath.append(lto)
                    notablepath.append(root)
                else:
                    #if not the last destination add it as the new latest route
                    availabledests = list(remainingdests)
                    currentdist = latestroute[1] + relevantdists[lfrom][lto]
                    currentroute = [lto, currentdist, remainingdests, availabledests]
                    routes.append(currentroute)
                    routes = irrelevant_node(relevantroutes, routes)
    
    absolutepath = [root]
    for i in notablepath:
        #finds the path + removes none values
        currentpath = ast.literal_eval(relevantroutes[absolutepath[-1]][i])[0]
        absolutepath.extend(currentpath)
    
    return (totdistmin, notablepath, absolutepath)

def rootcoordinates(stad, steden):
    stadje = steden.loc[steden['place_name'] == stad]
    latitudes = list(stadje['latitude'])[0]
    longitudes = list(stadje['longitude'])[0]
    return longitudes, latitudes

def coordinates(stad, steden, latitudes, longitudes):
    stadje = steden.loc[steden['place_name'] == stad]
    latitudes.append(list(stadje['latitude'])[0])
    longitudes.append(list(stadje['longitude'])[0])

def image(root, notablepath, absolutepath):
    bel = pgeocode.Nominatim(country="BE")
    steden = pd.DataFrame(bel._data)
    
    rootlong, rootlat = rootcoordinates(root, steden)
    notablelong = []
    notablelat = []
    absolutelong = []
    absolutelat = []

    for i in notablepath:
        coordinates(i, steden, notablelat, notablelong)
    
    for j in absolutepath:
        coordinates(j, steden, absolutelat, absolutelong)

    Directory = "map_belgie.png" 
    img = cv2.imread(Directory)

    resizescale = 44/100

    nwidth = int(img.shape[1] * resizescale)
    nheight = int(img.shape[0] * resizescale)
    dim = (nwidth, nheight)

    #pixel measurements of distance between extremities in the photo
    width = 1938 * resizescale
    height = 1586  * resizescale

    #pixel measurements of the extra space outside of belgium
    extrawidth = int(174 * resizescale)
    extraheight = int(232 * resizescale)

    #extremities of longitude and lattitude belgium
    nmostpoint = 51.504940
    smostpoint = 49.497082
    cheight = nmostpoint - smostpoint

    wmostpoint = 2.545777
    emostpoint = 6.408037
    cwidth = emostpoint - wmostpoint
    
    img = cv2.resize(img, dim)
    
    for i in range(len(absolutelong)):
        plongpoint = int(((absolutelong[i] - wmostpoint) / cwidth) * width) + extrawidth
        platpoint = int(((nmostpoint - absolutelat[i]) / cheight) * height) + extraheight
        cv2.circle(img, (plongpoint, platpoint), 3, (0, 0, 0), -1)
        if i != 0:
            p0longpoint = int(((absolutelong[i - 1] - wmostpoint) / cwidth) * width) + extrawidth
            p0latpoint = int(((nmostpoint - absolutelat[i - 1]) / cheight) * height) + extraheight
            cv2.line(img, (p0longpoint, p0latpoint), (plongpoint, platpoint), (0, 0, 0), 1)
    
    for i in range(len(notablelong)):
        plongpoint = int(((notablelong[i] - wmostpoint) / cwidth) * width) + extrawidth
        platpoint = int(((nmostpoint - notablelat[i]) / cheight) * height) + extraheight
        cv2.circle(img, (plongpoint, platpoint), 3, (0, 255, 0), -1)
    
    plongpoint = int(((rootlong - wmostpoint) / cwidth) * width) + extrawidth
    platpoint = int(((nmostpoint - rootlat) / cheight) * height) + extraheight
    cv2.circle(img, (plongpoint, platpoint), 3, (0, 0, 255), -1)

    cv2.imshow('Map Belgium',img)
    cv2.waitKey(0)

start_time = time.time()

root = "Zaventem"

Capitals = ["Bruxelles", "Antwerpen", "Gent", "Brugge", "Mons", "Namur", "Hasselt", "Liège", "Arlon", "Leuven", "Wavre"]
Destinations = ["Maaseik", "Bilzen", "Bocholt", "Tongeren", "Halen", "Hasselt", "Genk", "Lommel", "Brugge", "Kortrijk", "Oostende", "Waregem", "Ieper", "Roeselare", "Oudenburg", "Poperinge", "Leuven", "Tienen", "Halle", "Vilvoorde", "Aarschot", "Landen", "Tervuren"]

totdistmin, notablepath, absolutepath = multi_node(root, fulldists, fullroutes, Destinations)

totaltime = time.time() - start_time

print(totaltime)
print(totdistmin)
print(absolutepath)
print(notablepath)

image(root, notablepath, absolutepath)

#cv2.destroyAllWindows()