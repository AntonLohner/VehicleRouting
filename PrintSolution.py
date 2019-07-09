from key import key1
tempdata = {"0": '35.051069,-89.793136',  # depot
        "1": '35.093329,-90.019905',
        "2": '35.142712,-90.051908',
        "3": '35.103362,-89.919856',
        "4": '35.138493,-90.010147',
        "5": '35.139243,-90.037901',
        "6": '35.122205,-89.941882',
        "7": '35.115733,-90.031246',
        "8": '35.106397,-89.916895',
        "9": '35.115978,-89.962308',
        "10": '35.152830,-89.992562',
        "11": '35.153515,-90.043538',
        "12": '35.149093,-90.053132',
        "13": '35.098201,-89.864823',
        "14": '35.154906,-89.965071',
        "15": '35.159571,-89.959866'
        }


# Prints solution to console
def print_solution(data, manager, routing, solution):
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
                paths = paths + "&path=color:0x0000ff%7Cweight:5"
                new_path = False
            paths = paths + "%7C{}\n".format(tempdata[str(manager.IndexToNode(index))])
            # We create the paths here.
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
