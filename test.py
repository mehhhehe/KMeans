"""
German University of Technology in Oman
AI 2 102
AI: Representation and Problem-Solving
Aya Kinaan and Mehreen Mansoor
"""

import math
import random
import matplotlib.pyplot as plt
import copy


def points_init():
    """
    This function allows the user to decide whether they want to
    manually enter points or have them randomly generated, and calls the relevant
    functions to do so.
    """

    # ask the user if they would like to manually enter points or not
    option = input("Would you like to enter the points manually? (y/n) ")

    # if the user asks to enter points manually
    if option.lower().strip() == "y":
        # function that allows user to enter points
        # this function returns a 2-d list of points entered by the user
        return enter_points()
    # if the user asks to randomly generate points
    else:
        # function that generates points randomly
        # this function returns a 2-d list of n randomly generated points
        return gen_points()


def enter_points():
    """
    This function allows the user to manually enter points.
    """

    # ask the user how many points they would like to enter
    num = int(input("How many points would you like to enter? "))
    # this banner tells the user what format to use to enter points
    print("***** Please enter points as comma separated integers, e.g. 1, 5 *****")
    # initialise an empty list 'points' to which we will append the points entered by the user
    points = []

    # we will ask the user to enter 'num' points
    for i in range(num):
        # ask the user to enter the i-th point where i is in the range [1, num]
        point = input(f'Please enter point {i + 1}: ')
        # split the input according to the delimiter ','
        # the result would be a list of strings
        # if the user entered 1, 5 it would be split into ["1", "5"]

        x, y = point.split(",")
        # we will then convert both these strings to integers and append the point to 'points' as a list
        # the None value added to the point is the centroid it is associated with
        # initially set to None
        p = [int(x), int(y), None]
        # we will ensure that the user has not already entered the same point,
        # otherwise, this will create problems when removing from the set of points associated with a cluster
        while p in points:
            x, y = input("You have already entered that point before, please try again: ").split(",")
            # converting x and y to integers and setting centroid no. to None
            p = [int(x), int(y), None]
        points.append(p)

    # return the points entered by the user
    return points


def gen_points():
    # ask the user how many points they would like to generate
    num = int(input("How many points would you like to generate? "))
    # ask the user for an upper bound for the points
    # e.g. if they enter 100, then all points would have x,y coordinates <= 100
    ub = int(input("Please enter an upper bound for the points' values: "))
    # ask the user for a lower bound for the points
    # e.g. if they enter 5, then all points would have x,y coordinates >= 5
    lb = int(input("Please enter a lower bound for the points' values: "))
    # it might not be possible to generate enough points depending on the ub and lb
    # in that case, we will ask the user for new ub and lb values
    while (ub-lb+1)**2 <= num:
        print("""The values of upper bound and lower bound entered can not generate the number of points you require.
              Please enter new values such that (ub - lb + 1)^2 >= number of points.""")
        ub = int(input("Please enter an upper bound for the points' values: "))
        lb = int(input("Please enter a lower bound for the points' values: "))
    # initialise an empty list 'points' to which we will append the randomly generated points
    points = []

    # generate 'num' random points
    for i in range(num):
        # we will generate a random point x in the range [lb, ub]
        x = random.randint(lb, ub)
        y = random.randint(lb, ub)
        # we will inform the user that this point has been generated, and print it
        # the None value added to the point is the centroid it is associated with
        # initially set to None
        p = [x, y, None]
        # since these points are being generated randomly, there is a chance that they will be duplicated
        # this will cause issues when removing a point from a cluster and moving it to a different one
        # we will ensure there is no duplication
        while p in points:
            # the same code snippet as seen before in this function to create a point p
            x = random.randint(lb, ub)
            y = random.randint(lb, ub)
            p = [x, y, None]
        # inform the user that point number n has been generated
        print(f"Point {i+1} generated: {p[0], p[1]}")
        # append the randomly generated point to 'points'
        points.append(p)
    # return the randomly generated points
    return points


def cent_init():
    """
    This function allows the user to decide whether they want to
    manually enter the centroids or have them randomly generated, and calls the relevant
    functions to do so.
    """

    # ask the user if they would like to manually enter points or not
    option = input("Would you like to enter the centroids manually? (y/n) ")

    # if the user asks to enter points manually
    if option.lower().strip() == "y":
        # function that allows user to enter points
        # this function returns a 2-d list of points entered by the user
        return enter_cent()
    # if the user asks to randomly generate points
    else:
        # function that generates points randomly
        # this function returns a 2-d list of 'num' randomly generated points
        # num is determined by the user
        return gen_cent()


def enter_cent():
    """
    This function allows the user to manually enter the cluster heads
    """

    # ask the user how many clusters they would like to create
    num = int(input("How many clusters would you like to create? "))
    # this banner tells the user what format to use to enter coordinates
    print("***** Please enter centroid coordinates as comma separated integers, e.g. 1, 5 *****")
    # initialise an empty list 'centroids' to which we will append the centroids entered by the user
    centroids = []

    # we will ask the user to enter 'num' centroids
    for i in range(1, num+1):
        # ask the user to enter the i-th centroid where i is in the range [1, num]
        point = input(f"Please enter centroid {i}'s coordinates: ")
        # split the input according to the delimiter ','
        # the result would be a list of strings
        # if the user entered "1, 5" it would be split into ["1", " 5"]
        # we will then convert both these strings to integers and append the centroid to 'centroids' as a list
        # the empty set added to the point is the set of points in that particular cluster
        # the set is initially empty
        x, y = point.split(",")
        p = [int(x), int(y), set()]
        # the customer may enter the same centroid coordinates twice
        # we need to ensure there's no duplication
        while p in centroids:
            x, y = input("You have already entered that centroid before, please try again: ").split(",")
            p = [int(x), int(y), set()]
        # we will append this centroid to 'centroids'
        centroids.append([int(x), int(y), set()])

    # return the points entered by the user
    return centroids


def gen_cent():
    # ask the user how many clusters they would like to create
    num = int(input("How many clusters would you like to create? "))
    # ask the user for an upper bound for the centroids
    # e.g. if they enter 100, then all centroids would have x,y coordinates <= 100
    ub = int(input("Please enter an upper bound for the centroids' values: "))
    # ask the user for a lower bound for the centroids
    # e.g. if they enter 5, then all points centroids have x,y coordinates >= 5
    lb = int(input("Please enter a lower bound for the centroids' values: "))
    # initialise an empty list 'points' to which we will append the randomly generated points
    centroids = []

    # generate 'num' random centroids
    for i in range(num):
        # we will generate a random point x in the range [lb, ub]
        x = random.randint(lb, ub)
        y = random.randint(lb, ub)

        p = [x, y, set()]
        while p in centroids:
            x = random.randint(lb, ub)
            y = random.randint(lb, ub)
            p = [x, y, set()]
        # we will inform the user that this point has been generated, and print it
        print(f"Centroid {i + 1} generated: {p[0], p[1]}")
        # the empty set added to the centroid is the set of points associated with it
        # initially empty

        # append the randomly generated centroid to 'centroids'
        centroids.append(p)
    # return the randomly generated centroids
    return centroids


def cluster(points, centroids):
    """
    This function assigns each point to a cluster
    and updates 'points' and 'centroids' accordingly
    """
    # we will iterate over every data point
    for j in range(len(points)):
        # in order to find out which centroid is closest to the point
        # we will set the variable min_dist to infinity in order to progressively find which centroid is closer
        min_dist = float('inf')
        # the centroid which corresponds to min_dist (currently closest to the point) is initially set to None
        cent = None
        # we will iterate over the centroids one by one
        for i in range(len(centroids)):
            # we will calculate the distance from the data point to each centroid, one by one
            dist = euc_dist(points[j][0], points[j][1], centroids[i][0], centroids[i][1])
            # if this centroid is closer to the data point than the previously closest centroid
            # the distance from this centroid to the dp will become min_dist
            # and the closest centroid 'cent' will be set equal to this centroid's index
            if dist <= min_dist:
                min_dist = dist
                cent = i
        # if the centroid this data point is associated with is not the same as the new closest centroid 'cent'
        if points[j][2] != cent:
            # if this data point was already associated with another centroid
            # i.e. we are making sure this is not the first iteration where the centroid this
            # data point is associated with is not None
            if points[j][2] != None:
                # we will remove this data point from the cluster it was previously in since it
                # now belongs to the cluster with a cnetroid that is closer
                centroids[points[j][2]][2].remove((points[j][0], points[j][1]))
            # we will inform the user that this data point is moving to another (closer) cluster 'i' (cluster number)
            # corresponding to the centroid at coordinates (x, y)
            # and print the distance from this point to that centroid
            print(f'{points[j][0], points[j][1]} moving to cluster {cent+1}, centroid = {centroids[cent][0], centroids[cent][1]}, distance = {min_dist}')
        # setting the cluster the data point is in equal to 'cent'
        points[j][2] = cent
        # adding the data point to its new cluster
        centroids[cent][2].add((points[j][0], points[j][1]))


def euc_dist(x1, y1, x2, y2):
    """
    This function calculates the euclidean distance
    between points p1 (x1, y1) and p2 (x2, y2)
    """
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def update_cent(centroids):
    """
    This function updates the centroids' positions
    based on the mean of the points in the cluster associated with this centroid
    """
    # iterating over the cnetroids one by one
    for i in range(len(centroids)):
        # decomposing each row of 'centroids' into
        # the x coord, y coord, and the set of corresponding points
        x, y, points = centroids[i]
        # total_x and total_y are the sums of the x and y values
        # these will be used later to calculate the mean value
        # to which we will move the centroid
        # we will initialise both to 0
        total_x = 0
        total_y = 0
        # iterating over the points present in the cluster associated with this centroid
        for j in points:
            # adding x coord of the point to total_x and
            # y coord to total_y
            total_x += j[0]
            total_y += j[1]
        # it is possible that there are no points in this cluster
        # in that case, the program will raise a ZeroDivisionErrror
        # additionally, if there are no points in this cluster, the centroid will not move anyways
        if len(points) != 0:
            # calculating the mean x and y coords
            mean_x = total_x/len(points)
            mean_y = total_y/len(points)
            # changing the coordinates of the centroid to mean_x, mean_y, the new coordinates
            centroids[i][0], centroids[i][1] = mean_x, mean_y


def visualise(centroids, colours):
    """
    This function will generate the figure required
    for us to visualise the cluster-point-centroid movement.
    It takes the list of centroids and colours (generated in main()) as arguments.
    """
    # we will iterate over the centroids
    for i in range(len(centroids)):
        # creating two empty lists x and y for the x and y coords of the data points to plot
        x = []
        y = []
        # iterating over the data points in each cluster
        for a, b in centroids[i][2]:
            # appending the x coords to x and y coords to y
            x.append(a)
            y.append(b)
        # we will plot the centroid, size = 100, colour = the i-th colour in colours, shape = star
        plt.scatter(centroids[i][0], centroids[i][1], s = 100, c = colours[i], marker = '*')
        # we will plot the data points, size = 4, colour = the i-th colour in colours, shape = the default dot
        plt.scatter(x, y, s = 4, c = colours[i])
    # we will show the figure and set block = False so the user does not have to
    # close the matplotlib window for the next figure to appear
    plt.show(block = False)
    # we will wait on this figure for 3 seconds to allow the user to look at the figure
    plt.pause(5)
    # we will clear this figure so the next figure can appear
    plt.clf()


def main():
    # we will initialise the points, whichever way the user prefers
    # manually or randomly
    points = points_init()
    # initialise the centroids
    centroids = cent_init()
    # these are all the characters/numbers used in hexadecimal representation
    # we will use this string to generate 'n' random colours where n is the number of clusters
    hex = 'ABCDEF123456789'
    # creating list 'colours' to append the colours to
    colours = []
    # generating len(centroids) number of colours
    for i in range(len(centroids)):
        # we will choose 6 characters from 'hex' and join them together as a string
        colour = f'#{"".join(random.choices(hex, k= 6))}'
        # to ensure that we have unique colours and that the colour is not white (because the bg is white)
        while colour in colours or colour == "#FFFFFF":
            colour = f'#{"".join(random.choices(hex, k= 6))}'
        # we will append the colour to colours
        colours.append(colour)

    # to visualise the data points and centroids before we begin clustering
    # create the lists of x and y coords of the data points
    x = [points[i][0] for i in range(len(points))]
    y = [points[i][1] for i in range(len(points))]
    # plot the data points, size = 4, colour = black
    plt.scatter(x, y, s = 4, c = 'black')
    # iterate over the centroids
    for i in range(len(centroids)):
        # plot the centroids one by one
        # size = 100, colour = i-th colour from colours, marker = star
        plt.scatter(centroids[i][0], centroids[i][1], s = 100, c = colours[i], marker = '*')
    # show the figure
    plt.show(block = False)
    # keep the figure on the screen for 5 seconds
    plt.pause(5)
    # close the figure
    plt.clf()
    # before we start clustering, we will create a variable n
    # to keep track of the number of iterations
    # we will initialise it to 1
    n = 1
    # while the algorithm has not converged
    while True:
        # tell the user which iteration this is
        print(f"Iteration {n}: ")
        # make a deep copy of the points to compare to later
        # the comparison will tell us whether the points have changed their clusters or not
        # in order to determine whether the algorithm has converged
        temp = copy.deepcopy(points)
        # call the cluster function, which will cluster each data point and update 'points'
        # and 'centroids'
        cluster(points, centroids)
        # call the visualise function to visualise the clusters
        visualise(centroids, colours)
        # increment the iteration tracker by 1
        n += 1
        # check if any points have changed their clusters
        # if not, this means that the points in each cluster are the same
        # the centroid's position will not change anymore
        # this means that the algorithm has converged
        if points == temp:
            print('The algorithm has converged.')
            # close all figure windows
            plt.close('all')
            # break out of the loop, iteration is over
            break
        # if any of the data points have changed clusters, update the
        # positions of the centroids
        update_cent(centroids)


if __name__ == "__main__":
    main()
