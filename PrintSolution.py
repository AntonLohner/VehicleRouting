from key import key1


# Prints solution to console
def print_solution(data, manager, routing, solution, coords):
    Coords = coords
    tempdata = {}
    for i in data['location_names']:
        if i == 'depot':
            i = "0"
            tempdata[i] = '25.680723,-100.365837'
        else:
            tempdata[i] = Coords[int(i)]


    node_dropped = False
    paths = ""
    link = "https://maps.googleapis.com/maps/api/staticmap?size=400x400&key={}\n".format(key1)
    markers = ""
    # Dropped Nodes
    dropped_nodes = 'Dropped nodes:'
    for node in range(routing.Size()):
        if routing.IsStart(node) or routing.IsEnd(node):
            continue
        if solution.Value(routing.NextVar(node)) == node:
            if not node_dropped:
                markers = markers + "&markers=color:blue%7ClabelD:"
            markers = markers + "%7C{}\n".format(tempdata[str(manager.IndexToNode(node))])
            # This is where we add the dropped nodes as pins to the map
            dropped_nodes += ' {}'.format(manager.IndexToNode(node))
    print(dropped_nodes)
    # Routes
    time_dimension = routing.GetDimensionOrDie('Time')
    total_time = 0
    total_load = 0
    i = 0
    color = ["0xFF0000FF", "0x666666FF", "0x38761DFF", "0x674EA7FF", "0x783F04FF", "0x0000FFFF", "0xFFFF00FF",
             "0x134F5CFF"]
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_time = 0
        route_load = 0
        new_path = True
        while not routing.IsEnd(index):
            time_var = time_dimension.CumulVar(index)
            node_index = manager.IndexToNode(index)
            route_load += data['demands'][node_index]
            plan_output += '{0} Time({1},{2}) -> '.format(
                manager.IndexToNode(index), solution.Min(time_var),
                solution.Max(time_var))
            if new_path is True:
                paths = paths + "&path=color:{}%7Cweight:5\n".format(color[i])
                i = i + 1
                if i == 8:
                    i = 0
                new_path = False
            paths = paths + "%7C{}\n".format(tempdata[str(manager.IndexToNode(index))])
            # We create the paths here.
            # TODO: Consider adding the final return to the hub. Better colour? Transparency? They might want a dynamic
            # map instead.
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_time += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        time_var = time_dimension.CumulVar(index)
        plan_output += '{0} Time({1},{2})\n'.format(
            manager.IndexToNode(index), solution.Min(time_var),
            solution.Max(time_var))
        plan_output += 'Time of the route: {}sec\n'.format(
            solution.Min(time_var))
        plan_output += ' {0} Load({1})\n'.format(
            manager.IndexToNode(index), route_load)
        plan_output += 'Load of the route: {}\n'.format(route_load)
        print(plan_output)
        total_time += solution.Min(time_var)
        total_load += route_load
    link = link + paths + markers
    print('Sum of the route Times: {}sec'.format(total_time))
    print(link)
