#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 02:25:45 2019

@author: selenachow
"""

# initialize
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from matplotlib.collections import PolyCollection, LineCollection
import seaborn as sns
from scipy.spatial import Delaunay
from scipy.spatial import distance
import datetime
import time

# static data points
# data points for pre-determined meeting points
meetname = ["Orange Circles", "Hearst Ave @ Arch Bus Stop", "North Gate", "Sutardja Dai",
            "Anthropology Library Fountain", "Hearst Field Annex", "Amazon Lockers at Sather Lane",
            "Haas Pavilion", "South Edge of Crescent Lawn", "North Edge of Crescent Lawn"]
meetlong = [-122.26489, -122.26412, -122.26012, -122.25853, -122.25487, -122.25746, -122.2593,
            -122.26155, -122.26563, -122.26564]
meetlat = [37.87297, 37.87434, 37.87489, 37.87512, 37.86963, 37.86933, 37.86919, 37.86872,
           37.87092, 37.87226]
meetlonglatarray = np.vstack((meetlong, meetlat)).T
meetdata = {"Meeting Point Name": meetname, "Longitude": meetlong, "Latitude": meetlat}
meet = pd.DataFrame(data=meetdata)

# data points for cardinal directions used to calculate total bounds
cardinalname = ["Center", "North", "East", "South", "West"]
centerlong = -122.25986
centerlat = 37.87146
center = np.vstack((centerlong, centerlat)).T
diff = 0.01446
cardinallong = [centerlong, centerlong, (centerlong+diff), centerlong, (centerlong-diff)]
cardinallat = [centerlat,  (centerlat + diff), centerlat, (centerlat-diff), centerlat]
cardinallonglatarray = np.vstack((cardinallong, cardinallat)).T
cardinaldata = {"Cardinal Point Name": cardinalname, "Longitude": cardinallong, "Latitude": cardinallat}
cardinal = pd.DataFrame(data=cardinaldata)

# data points used to calculate bounds of UC Berkeley campus
boundname = ["NW", "NE", "Mid E", "SE", "SW"]
boundlong = [-122.26612, -122.25689, -122.25294, -122.25241, -122.26548]
boundlat = [37.87408, 37.87538, 37.87181, 37.86963, 37.86799]
boundlonglatarray = np.vstack((boundlong, boundlat)).T
bounddata = {"Bounds Point Name": boundname, "Longitude": boundlong, "Latitude": boundlat}
bound = pd.DataFrame(data=bounddata)

# functions
def out_hull(p, hull):
    """
    Test if points in `p` are outside `hull`

    `p` should be a `NxK` coordinates of `N` points in `K` dimensions
    `hull` is either a scipy.spatial.Delaunay object or the `MxK` array of the
    coordinates of `M` points in `K`dimensions for which Delaunay triangulation
    will be computed
    """

    if not isinstance(hull,Delaunay):
        hull = Delaunay(hull)

    return hull.find_simplex(p)<0

def plot_out_hull(p, hull, showmap, extrapoints):
    """
    plot relative to `out_hull` for 2d data and returns test points within bounds
    can choose to show entire map or show minimum points
    """

    if not isinstance(hull,Delaunay):
        hull = Delaunay(hull)

    # plot tested points `p` - red are outside hull, green outside, x if beyond cardinal bounds
    outside = out_hull(p,hull)
    #distance of points in p from center
    dst = distance.cdist(center, p,'euclidean')
    # boolean to know if point is within cardinal circle counds
    outcardinalbool = (dst>diff).reshape((len(p),))
    # plot points outside of campus & within cardinal circle bounds
    withinbounds = outside&~outcardinalbool
    if showmap:
        # plot triangulation
        poly = PolyCollection(hull.points[hull.vertices], facecolors='w', edgecolors='w')
        plt.clf()
        sns.set_style("darkgrid")
        plt.title('Berkeley Map')
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.gca().add_collection(poly)
        plt.plot(hull.points[:,0], hull.points[:,1], 'o')

        # plot the convex hull
        edges = set()
        edge_points = []

        def add_edge(i, j):
            """Add a line between the i-th and j-th points, if not in the list already"""
            if (i, j) in edges or (j, i) in edges:
                # already added
                return
            edges.add( (i, j) )
            edge_points.append(hull.points[ [i, j] ])

        for ia, ib in hull.convex_hull:
            add_edge(ia, ib)

        lines = LineCollection(edge_points, color='b')
        plt.gca().add_collection(lines)
        # plot good points in green
        plt.plot(p[withinbounds,0],p[ withinbounds,1],'.g')
        if extrapoints:
            # plot points inside Berkeley campus
            plt.plot(p[~outside,0],p[~outside,1],'xr')
            # plot points outside of cardinal circle bounds
            plt.plot(p[outcardinalbool,0],p[outcardinalbool,1],'xr')
            plt.plot(center[0,0],center[0,1],"^y")
            plt.plot(meetlonglatarray[:,0],meetlonglatarray[:,1],'om')
    return p[withinbounds],withinbounds

def getkNN(point, points, n, df):
    # distance from center to point
    pointcentdist = distance.cdist(center, [point],'euclidean')[0]
    # calculate euclidean distances
    distances = distance.cdist(point.reshape(1,-1), points,'euclidean')
    # sorted euclidean distances
    sorteddistances = np.sort(distances)
    # index of sorted distances
    order = np.argsort(distances)[0]
    # n nearest neighbors and self (if there aren't multiples of the same points)
    sortednotfar = ((distances<=pointcentdist))[0][order]
    sortednotfar[n:] = False
    nearestpoints = points[order][sortednotfar]
    restofpoints = points[order][~sortednotfar]
    nearestnames = df[["Last","First"]].iloc[order,:].iloc[sortednotfar,:].values.tolist()
    restofnamesdf = df[["Last","First"]].iloc[order,:].iloc[~sortednotfar,:]
    return sorteddistances, order, nearestpoints,restofpoints, nearestnames, restofnamesdf

def plotmapandkNN(point, p, hull, n, showmap,extrapoints, df):
    goodpoints,withinbounds = plot_out_hull(p,hull,showmap,extrapoints)
    sorteddistances, order, nearestpoints,restofpoints, nearestnames, restofnames = getkNN(point,goodpoints,n,df)
    # find closest meetpoint
    meanpoint = np.mean(nearestpoints,axis=0)
    closestmeetindex = np.argmin(distance.cdist(meanpoint.reshape(1,-1), meetlonglatarray, 'euclidean'))
    closestmeetname = meet.iloc[closestmeetindex,:]["Meeting Point Name"]
    closestmeetpoint = np.vstack((meet.iloc[closestmeetindex,:]["Longitude"],meet.iloc[closestmeetindex,:]["Latitude"])).T

    if showmap:
        plt.plot(nearestpoints[:,0],nearestpoints[:,1],'oc')
        plt.plot(point[0],point[1],'Dc')
        plt.plot(closestmeetpoint[0][0],closestmeetpoint[0][1],'om')
        #legend
        greendot = mlines.Line2D([], [], color='green', marker='o', linestyle='None', markersize=5, label='Viable Points')
        cyandiamond = mlines.Line2D([], [], color='cyan', marker='D', linestyle='None', markersize=5, label='Group Main Point')
        cyandot =  mlines.Line2D([], [], color='cyan', marker='o', linestyle='None', markersize=5, label='Group Points (kNN)')
        magentapoint = mlines.Line2D([], [], color='magenta', marker='o', linestyle='None', markersize=5, label='Meeting Point')
        blueline = mlines.Line2D([], [], color='blue', marker='o', linestyle='solid', markersize=5, label='Bounds')
#        redx = mlines.Line2D([], [], color='red', marker='x', linestyle='None', markersize=5, label='Out of Bounds Points')
#        yellowtriangle = mlines.Line2D([], [], color='yellow', marker='^', linestyle='None', markersize=5, label='Center')
#       full legend
#        plt.legend(handles=[greendot, cyandiamond, cyandot,magentapoint,blueline,redx,yellowtriangle],loc=(1.04,0))
        plt.legend(handles=[greendot, cyandiamond, cyandot,magentapoint,blueline],loc=(1.04,0))
        plt.show()
        
    return nearestpoints, restofpoints, closestmeetpoint, closestmeetname, nearestnames, restofnames



'''
# test data points
testname = ["Point 1", "Point 2", "Point 3", "Point 4", "Point 5", "Point 6",
            "Point 7", "Point 8", "Point 9", "Point 10", "Point 11", "Point 12",
            "Point 13", "Point 14", "Point 15", "Point 16"]
testlong = [-122.26392,-122.26242,-122.26049	,-122.25834,-122.25648,-122.25264,-122.25972,
            -122.26618,-122.27121,-122.26361,-122.26876,-122.25868,-122.26885,-122.25571,-122.25374,-122.27745]
testlat = [37.86771,37.86696,37.87013,37.86768,37.86688,37.86876,37.86437,37.86451,37.87347,
           37.87784,37.87586,37.87793,37.86951,	37.86382, 37.86609,37.86061]


testlonglatarray = np.vstack((testlong, testlat)).T
'''

grouparray = []
grouplenarray= []
meetarray = []
namesarray = []
grouptime = []

weboutput = [['Shaaaaa', 'John',  '3','30', "PM", "37.86061","-122.27745"],
            ["Steinbecka",'John', '3','30', "PM", '37.86609','-122.25374'],
            ["Miltonaaaaa","John",'3','40', "PM","37.86382","-122.25571"],
            ["Oliveraaaaa","John",'3','40', "PM", "37.86951","-122.26885"],
            ["Williams", "John",  '3','30', "PM","37.87793","-122.25868"]]
df = pd.DataFrame.from_records(weboutput,columns = ["Last","First","Hour","Minute","AM/PM","Latitude","Longitude"])
if (df["AM/PM"]=="PM").any():
    df["Hour"]=pd.to_numeric(df["Hour"]) + 12
else:
    df["Hour"]=df["Hour"]=pd.to_numeric(df["Hour"])
df["Minute"]=pd.to_numeric(df["Minute"])
df["Latitude"]=pd.to_numeric(df["Latitude"])
df["Longitude"]=pd.to_numeric(df["Longitude"])
#in10 = datetime.datetime.now() + datetime.timedelta(minutes = 10)

#change hour and minutehere
testtime = [3,40,"PM"]

if testtime[2] == "PM":
    testtime[0]=testtime[0]+12
bool1 = df["Hour"]== testtime[0]
bool2 = df["Minute"]== testtime[1]
pointswithin10 = df[bool1 & bool2]

pointswithin10array = np.vstack((pointswithin10["Longitude"], pointswithin10["Latitude"])).T
if len(pointswithin10array) != 0:
    if testtime[0] > 12:
        grouphour = testtime[0] - 12
        AMPM = "PM"
    else:
        grouphour = testtime[0]
        AMPM = "AM"
    grouptime = np.array([grouphour, testtime[0], AMPM])
    grouparray = []
    meetarray = []
    namesarray = []
    points10bounded,points10boundedbool = plot_out_hull(pointswithin10array, boundlonglatarray, showmap=True, extrapoints=False)
    nearestpoints,restofpoints, closestmeetpoint, closestmeetname,nearestnames,restofnamesdf = plotmapandkNN(points10bounded[0], pointswithin10array, boundlonglatarray, 5, True, False, pointswithin10[points10boundedbool])
    grouparray.append(nearestpoints)
    meetarray.append(closestmeetname)
    namesarray.append(nearestnames)
    while len(restofpoints) != 0:
        nearestpoints, restofpoints, closestmeetpoint, closestmeetname,nearestnames,restofnamesdf = plotmapandkNN(restofpoints[0], restofpoints, boundlonglatarray, 5, True, False, restofnamesdf)
        grouparray.append(nearestpoints)
        meetarray.append(closestmeetname)
        namesarray.append(nearestnames)
grouplenarray = [len(grouparray[i]) for i in range(len(grouparray))]
print(grouparray)
print(grouplenarray)
print(meetarray)
print(namesarray)
print(grouptime)
