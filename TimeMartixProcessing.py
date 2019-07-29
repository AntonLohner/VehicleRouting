from __future__ import print_function
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from CreateDataModel import create_data_model
from PrintSolution import print_solution


def main(data_model, coords):
    """Solve the problem."""
    # Create the data for the problem.
    if coords[0] != [25.7473953, -100.4032065]:
        coords.insert(0, [25.7473953, -100.4032065])
    data = data_model
    print(data)
    print(coords)
    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(
        len(data['time_matrix']), data['num_vehicles'], data['depot'])
    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    def demand_callback(from_index):
        """Returns the demand of the node."""
        # Convert from routing variable Index to demands NodeIndex.
        from_node = manager.IndexToNode(from_index)
        return data['demands'][from_node]

    def time_callback(from_index, to_index):
        """Returns the travel time between the two nodes."""
        # Convert from routing variable Index to time matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['time_matrix'][from_node][to_node]
    transit_callback_index = routing.RegisterTransitCallback(time_callback)
    demand_callback_index = routing.RegisterUnaryTransitCallback(
        demand_callback)
    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
    # Add Capacity constraint
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # no slack
        data['vehicle_capacities'],  # vehicle maximum capacities
        True,  # start cumul to zero
        'Capacity')
    # Lets the solution drop nodes if necessary.
    penalty = 900000
    for node in range(1, len(data['time_matrix'])):
        routing.AddDisjunction([manager.NodeToIndex(node)], penalty)
    routing.AddDimension(
        transit_callback_index,
        30000,  # allow waiting time
        30000,  # maximum time per vehicle
        False,  # Don't force start cumul to zero.
        'Time')
    time_dimension = routing.GetDimensionOrDie('Time')
    # Add time window constraints for each location except depot.
    for location_idx, time_window in enumerate(data['time_windows']):
        if location_idx == 0:
            continue
        index = manager.NodeToIndex(location_idx)
        time_dimension.CumulVar(index).SetRange(time_window[0], time_window[1])
    # Add time window constraints for each vehicle start node.
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        time_dimension.CumulVar(index).SetRange(data['time_windows'][0][0],
                                                data['time_windows'][0][1])
    for i in range(data['num_vehicles']):
        routing.AddVariableMinimizedByFinalizer(
            time_dimension.CumulVar(routing.Start(i)))
        routing.AddVariableMinimizedByFinalizer(
            time_dimension.CumulVar(routing.End(i)))

    # This constraint isn't  important, as it is overshadowed by both truck capacity and delivery timing.
    '''# Add Time constraint.
    dimension_name = 'Time'
    routing.AddDimension(
        transit_callback_index,
        0,  # no slack
        3000,  # vehicle maximum travel time
        True,  # start cumul to zero
        dimension_name)

    distance_dimension = routing.GetDimensionOrDie(dimension_name)
    distance_dimension.SetGlobalSpanCostCoefficient(100)
    '''
    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        print_solution(data, manager, routing, solution, coords)






