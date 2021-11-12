# Joshua Miller
# Router Placement and Testing Algorithm

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
import shapely
from shapely.geometry import LineString

# get user input of blueprint max sizes (used in fig setup)
max_X = int(input("Enter the max width (horizontal) of the blueprint."))
max_Y = int(input("Enter the max length (vertical) of the blueprint. "))
watch = input("If you would like to watch the work enter 'y' \n"
              "Warning this takes 10+minutes. \n"
              "To move on press 'Enter'")

tic = time.perf_counter()
if watch == 'y':
    watch = True
    print("True")
else:
    watch = False

# set up the figure
fig = plt.figure(figsize=(10, 5))
ax = fig.add_subplot(1, 1, 1)   # ax plot holds the rectangles
x_ticks = np.arange(0, max_X + 1, 1)
y_ticks = np.arange(0, max_Y + 1, 1)
plt.xticks(x_ticks)
plt.xlim([0, max_X])
plt.yticks(y_ticks)
plt.ylim([0, max_Y])
plt.grid(alpha=0.4)

# read blueprint
blueprint = pd.read_csv("blueprint_inputs.csv", sep=',')
print(blueprint)
bp_nRows = blueprint['name'].count()

vertexes = []
sqr_ft = 0
Pts = []

# graph the blueprint
for x in range(0, bp_nRows):
    width = blueprint.loc[x, 'width']
    height = blueprint.loc[x, 'length']
    # LL
    LL_tuple = (blueprint.loc[x, 'xPos'], blueprint.loc[x, 'yPos'])
    vertexes.append(LL_tuple)
    # LR
    LR_tuple = (blueprint.loc[x, 'xPos'] + width, blueprint.loc[x, 'yPos'])
    vertexes.append(LR_tuple)
    # UL
    UL_tuple = (blueprint.loc[x, 'xPos'], blueprint.loc[x, 'yPos'] + height)
    vertexes.append(UL_tuple)
    # UR
    UR_tuple = (blueprint.loc[x, 'xPos'] + width,
                blueprint.loc[x, 'yPos'] + height)
    vertexes.append(UR_tuple)

    # manually plot the rectangle to have lines
    plt.plot([LL_tuple[0], LR_tuple[0]], [LL_tuple[1], LR_tuple[1]], lw=2, c='black', gid='wall')
    plt.plot([UL_tuple[0], UR_tuple[0]], [UL_tuple[1], UR_tuple[1]], lw=2, c='black', gid='wall')
    plt.plot([LL_tuple[0], UL_tuple[0]], [LL_tuple[1], UL_tuple[1]], lw=2, c='black', gid='wall')
    plt.plot([LR_tuple[0], UR_tuple[0]], [LR_tuple[1], UR_tuple[1]], lw=2, c='black', gid='wall')

    # sum the square ft after each room is created
    sqr_ft += (height * width)

    # calculate possible router placements / filter out rooms
    if blueprint.loc[x, 'name'] == 'bathroom':
        pass
    elif blueprint.loc[x, 'name'] == 'door':
        pass
    else:
        for idx in range(1, width):
            Pts.append((((blueprint.loc[x, 'xPos'])+idx), (blueprint.loc[x, 'yPos']+height-1)))
            Pts.append((((blueprint.loc[x, 'xPos'])+idx), (blueprint.loc[x, 'yPos']+1)))

        for idx2 in range(2, height-1):
            Pts.append((((blueprint.loc[x, 'xPos'])+1), (blueprint.loc[x, 'yPos']+idx2)))
            Pts.append((((blueprint.loc[x, 'xPos'])+width-1), (blueprint.loc[x, 'yPos']+idx2)))


# unique vertexes
unique_vertexes = list(set(vertexes))
nVertexes = len(unique_vertexes)

print()
print("Number of vertexes: ", nVertexes)
print("Total Square Feet: ", sqr_ft)
if not watch:
    print("Please wait: working ... ")


# test router points & number of Pts
nPts = len(Pts)
max_signal_strength = 150

colors = []
signal_distances = []
for pts_index in range(0, nPts):
    remaining_signal_strength = max_signal_strength
    plt.scatter(Pts[pts_index][0], Pts[pts_index][1], s=20, c='yellow')
    print("Current Router Point: X: ", Pts[pts_index][0], " Y: ", Pts[pts_index][1])
    coverage = 0
    dead_zone = 0
    for vertex_index in range(0, nVertexes):
        print("Signal from Current Router Point to End Point: X: ", unique_vertexes[vertex_index][0],
              " Y: ", unique_vertexes[vertex_index][1])

        # label for the legend
        # str_label = 'Point: ', unique_vertexes[vertex_index], 'Distance: ', distance

        # plt plot in form (x1,x2) , (y1, y2)

        ax.plot((Pts[pts_index][0], unique_vertexes[vertex_index][0]),
                (Pts[pts_index][1], unique_vertexes[vertex_index][1]),
                lw=0.6, c='red', gid="router_test")  # removed label=str_label,

        # calculations based on distance
        # for all lines
        intersections = []
        for walls in ax.get_lines():
            # select lines labeled as walls
            if walls.get_gid() == "wall":
                # print(walls.get_data())
                temp_wall_pt1 = (walls.get_data()[0][0], walls.get_data()[1][0])
                temp_wall_pt2 = (walls.get_data()[0][1], walls.get_data()[1][1])

                if temp_wall_pt1 == (unique_vertexes[vertex_index][0], unique_vertexes[vertex_index][1]) or \
                        temp_wall_pt2 == (unique_vertexes[vertex_index][0], unique_vertexes[vertex_index][1]):
                    pass
                else:
                    temp_wall = LineString([(walls.get_data()[0][0], walls.get_data()[1][0]),
                                            (walls.get_data()[0][1], walls.get_data()[1][1])])

                    router_signal = LineString([(Pts[pts_index][0], Pts[pts_index][1]),
                                                (unique_vertexes[vertex_index][0], unique_vertexes[vertex_index][1])])
                    int_pt = router_signal.intersection(temp_wall)
                    # print(int_pt)
                    if int_pt:
                        if isinstance(int_pt, shapely.geometry.linestring.LineString):
                            print("Object Type Error Here")
                        else:
                            # print(type(int_pt))
                            i_cord = int(int_pt.x), int(int_pt.y)
                            intersections.append(i_cord)
                            intersections = list(set(intersections))
                    int_pt = []
        print("Intersection Points: ", intersections)
        for dividers in intersections:
            # distance calculation!
            # start pts - end points
            xVal = Pts[pts_index][0] - dividers[0]
            yVal = Pts[pts_index][1] - dividers[1]
            distance_to_pt = round((np.sqrt((xVal * xVal) + (yVal * yVal))), 2)
            signal_distances.append(distance_to_pt)

        if len(intersections) == 0:
            no_walls_x = Pts[pts_index][0] - unique_vertexes[vertex_index][0]
            no_walls_y = Pts[pts_index][1] - unique_vertexes[vertex_index][1]
            signal_distances.append(round((np.sqrt((no_walls_x * no_walls_x) + (no_walls_y * no_walls_y))), 2))

        print("Distance from end point to signal intersection point: ", signal_distances)

        total_distance = 0
        for each in signal_distances:
            print("remaining signal length", remaining_signal_strength)
            print("next distance to remove", each)
            remaining_signal_strength = remaining_signal_strength - each
            remaining_signal_strength = remaining_signal_strength/2
            total_distance = total_distance + each

        print("Total Distance from router to end pt: ", total_distance)

        if total_distance <= max_signal_strength:
            coverage = coverage + 1
        elif total_distance > max_signal_strength:
            dead_zone = dead_zone + 1

        remaining_signal_strength = 150
        signal_distances.clear()

    print("Dead zone for point: Router: ", Pts[pts_index][0], Pts[pts_index][1], "End Point: ",
          unique_vertexes[vertex_index][0], unique_vertexes[vertex_index][1], "Dead zone value:", dead_zone)
    if dead_zone > 0:
        plt.scatter(Pts[pts_index][0], Pts[pts_index][1], s=15, c='red')
    else:
        plt.scatter(Pts[pts_index][0], Pts[pts_index][1], s=15, c='blue')

        # watch work being done or not based on user input
        if watch:
            plt.pause(2)

        # delete router line
    for line in ax.get_lines():
        if line.get_gid() == "router_test":
            line.remove()
    int_pt = []  # clear and delete intercept points
    signal_distances = []


# plt.legend(bbox_to_anchor=(1, 1.05), loc=2)    # legend for understanding
toc = time.perf_counter()
print("This program took ", toc-tic, " seconds.")
plt.show()
