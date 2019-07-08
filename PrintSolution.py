

# Prints solution to console
def print_solution(data, manager, routing, solution):
    # Dropped Nodes
    dropped_nodes = 'Dropped nodes:'
    for node in range(routing.Size()):
        if routing.IsStart(node) or routing.IsEnd(node):
            continue
        if solution.Value(routing.NextVar(node)) == node:
            dropped_nodes += ' {}'.format(manager.IndexToNode(node))
    print(dropped_nodes)
    # Routes
    time_dimension = routing.GetDimensionOrDie('Time')
    total_time = 0
    total_load = 0
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_time = 0
        route_load = 0
        while not routing.IsEnd(index):
            time_var = time_dimension.CumulVar(index)
            node_index = manager.IndexToNode(index)
            route_load += data['demands'][node_index]
            plan_output += '{0} Time({1},{2}) -> '.format(
                manager.IndexToNode(index), solution.Min(time_var),
                solution.Max(time_var))
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_time += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        time_var = time_dimension.CumulVar(index)
        plan_output += '{0} Time({1},{2})\n'.format(
            manager.IndexToNode(index), solution.Min(time_var),
            solution.Max(time_var))
        plan_output += 'Time of the route: {}hr\n'.format(
            solution.Min(time_var))
        plan_output += ' {0} Load({1})\n'.format(
            manager.IndexToNode(index), route_load)
        plan_output += 'Load of the route: {}\n'.format(route_load)
        print(plan_output)
        total_time += solution.Min(time_var)
        total_load += route_load
    print('Sum of the route Times: {}hr'.format(total_time))
