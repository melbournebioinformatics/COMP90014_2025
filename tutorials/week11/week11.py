##############
# Exercise 1 #
##############

def get_neighbours(all_points: list[Datapoint], point: Datapoint, eps: float):
    """
    Find all data points that occur within a maximum of eps distance of point p.
    Return as list of index positions corresponding to each neighbour in the input data point list.
    """
    ### BEGIN SOLUTION
    neighbours = list()
    for new_point in all_points:
        if euclidean_distance(new_point, point) < eps:
            neighbours.append(new_point)
    return neighbours
    ### END SOLUTION


##############
# Exercise 2 #
##############

def get_point_type(all_points: list[Datapoint], point: Datapoint, min_pts: int, eps: float) -> str:
    """
    Identifies the 'type' of a given Datapoint. 
    
    Return point label as: 
    - 'core' if number of points within eps radius >= min_pts, including self.
    - 'border' if within eps distance of a core point
    - 'noise' if not within eps distance of a core point

    Use your 'get_neighbours()' function to help. 
    """
    ### BEGIN SOLUTION
    # get neighbours  
    neighbours = get_neighbours(all_points, point, eps)
    # is this a core point? 
    if len(neighbours) +1 >= min_pts: 
        return 'core'
    # is this a border point?
    for p in neighbours:
        p_neighbours = get_neighbours(all_points, p, eps) 
        if len(p_neighbours) + 1 >= min_pts:
            return 'border'
    # if haven't returned yet, this point is noise. 
    return 'noise'
    ### END SOLUTION


##############
# Exercise 3 #
##############

def traverse(all_points: list[Datapoint], point: Datapoint, eps: float, cluster_id: int) -> None:
    """
    Assigns cluster_id to point.cluster.
    Handles neighbouring points in the following manner: 
        - If the neighbour point already has a valid 'cluster' assigned, ignore.
        - If the neighbour point is 'noise', ignore. 
        - If the neighbour point is 'core', <small>`traverse()`</small> from this next core node. 
        - If the neighbour point is 'border', update its 'cluster' attribute and continue.  
    """
    ### BEGIN SOLUTION
    # Check if the starting point is core
    if point.ptype != 'core':
        return None
    # Assign current cluster ID
    point.cluster = cluster_id
    # Get all neighbours
    neighbours = get_neighbours(all_points, point, eps)
    for neighbour_point in neighbours:
        # Skip assigned points and noise points
        if neighbour_point.cluster != None or neighbour_point.ptype == 'noise':
            continue
        # Recursively traverse core points
        if neighbour_point.ptype == 'core':
            traverse(all_points, neighbour_point, eps, cluster_id)
        # Add border points to the cluster without further traverse
        elif neighbour_point.ptype == 'border':
            neighbour_point.cluster = cluster_id
    ### END SOLUTION


##############
# Exercise 4 #
##############

def dbscan(datapoints: list[Datapoint], min_pts: int, eps: float) -> None:
    """
    performs DBSCAN clustering. 
    """
    for point in datapoints:
        point.ptype = get_point_type(datapoints, point, min_pts, eps)

    ### BEGIN SOLUTION
    # Sequentially naming cluster ID
    cluster_id = 0
    for point in datapoints:
        # Skip border points and assigned points
        if point.ptype == 'border' or point.cluster != None:
            continue
        # Assign -1 cluster ID to noise points
        if point.ptype == 'noise':
            point.cluster = -1
        elif point.ptype == 'core':
            traverse(datapoints, point, eps, cluster_id)
            cluster_id += 1
    ### END SOLUTION
    
    
