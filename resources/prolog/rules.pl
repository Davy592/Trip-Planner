% tells if a variable it's a node
is_node(X):-
    prop(X, type, node).

% tells the coord of a node
get_node_coord(X, Lat, Lon):-
    is_node(X),
    prop(X, lat, Lat),
    prop(X, lon, Lon).

% tells if a variable it's a way
is_way(X):-
    prop(X, type, way).

% gets all the ways from a given node From_node to a given node To_node
get_ways(Way, From_node, To_node):-
    is_way(Way),
    prop(Way, from_node, From_node),
    prop(Way, to_node, To_node).

% gets all the info of all the neighbours of a given From_node (without limitations)
get_neighbours(From_node, To_node, To_node_lat, To_node_lon):-
    get_ways(_, From_node, To_node),
    get_node_coord(To_node, To_node_lat, To_node_lon).

% gets all the info of all the neighbours of a given From_node (with limitations)
% true if exist a way from From_node to To_node
% or if exist a way from To_node to From_node and the way is bidirectional
% or if exist a way between the nodes (besides the direction) and im on foot
get_available_neighbours(From_node, To_node, To_node_lat, To_node_lon):-
    get_ways(_, From_node, To_node),
    get_node_coord(To_node, To_node_lat, To_node_lon);
    get_ways(Way, To_node, From_node),
    get_node_coord(To_node, To_node_lat, To_node_lon),
    prop(Way, bidirectional, true);
    on_foot,
    (get_ways(_, From_node, To_node),
    get_node_coord(To_node, To_node_lat, To_node_lon);
    get_ways(_, To_node, From_node),
    get_node_coord(To_node, To_node_lat, To_node_lon)).

% get all the nodes in KB
get_all_node(Node, Lat, Lon):-
    is_node(Node),
    prop(Node, lat, Lat),
    prop(Node, lon, Lon).

% get all the ways in KB
get_all_ways(Way, From_node, To_node, bidi):-
    is_way(Way),
    prop(Way, from_node, From_node),
    prop(Way, to_node, To_node),
    prop(Way, bidirectional, bidi).


% gets the distance between two nodes
get_distance(From_node, To_node, Distance):-
    get_node_coord(From_node, From_node_lat, From_node_lon),
    get_node_coord(To_node, To_node_lat, To_node_lon),
    Distance is sqrt((From_node_lat - To_node_lat) ** 2 + (From_node_lon - To_node_lon) ** 2).

% haversine distance
% given two nodes returns the distance between them in km
haversine_distance(From_node, To_node):-
    get_node_coord(From_node, Lat1, Lon1),
    get_node_coord(To_node, Lat2, Lon2),
    % Convert latitude and longitude from decimal degree to radians
    Radians1Lat is Lat1 * pi / 180,
    Radians1Lon is Lon1 * pi / 180,
    Radians2Lat is Lat2 * pi / 180,
    Radians2Lon is Lon2 * pi / 180,
    % Calculate the difference between the two longitudes and latitudes
    Dlon is Radians2Lon - Radians1Lon,
    Dlat is Radians2Lat - Radians1Lat,
    % Calculate the half-verse of angular distance
    A is sin(Dlat / 2) ** 2 + cos(Radians1Lat) * cos(Radians2Lat) * sin(Dlon / 2) ** 2,
    % Calculate the distance
    C is 2 * asin(sqrt(A)),
    % Return the distance in km
    Distance is 6371 * C.