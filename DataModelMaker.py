

def DataModelInput(time_matrix, vehicles):
    demands = [0]
    vehicle_capacities = []
    location_names = ["depot"]
    x = 0
    i = 0
    while x < vehicles:
        vehicle_capacities.append(20)
        x = x + 1
    time_windows = []
    while i < len(time_matrix):
        time_windows.append((0, 60000))
        if i > 0:
            demands.append(1)
            location_names.append(str(i))
        i = i + 1
    data = {'time_matrix': time_matrix,
            'num_vehicles': vehicles, 'depot': 0, 'demands': demands,
            'time_windows': time_windows,
            'vehicle_capacities': vehicle_capacities,
            'location_names': location_names
            }
    return data


