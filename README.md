# router_placement_algorithm
This python algorithm creates a simple house floor plan based on a user-provided CSV file. The algorithm generates possible router placements and evaluates where a signal will be reached in every room of the floor plan. 

# blueprints 
The blueprint CSV file should be be in the order: 
    room name, length of room (verticle), width of room (horizontal), x coordinate, y coordinate 
Note: the x coordinate and y coordinate correspond with the lower left corner of the room. 

Note 2: This algorithm only supports square/rectangular rooms. 
Note 3: This algorithm only tests for signal being reached to the ends of the room. It does not evaulate the signal strength in a room. 
