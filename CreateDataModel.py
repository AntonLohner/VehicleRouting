from DataModelMaker import DataModelInput


def create_data_model(time_matrix, total_num_vehicles):
    data = DataModelInput(time_matrix, total_num_vehicles)
    return data

# num_vehicles: len(time_matrix)
# no demands or vehicle capacities?
# TODO: Capacities as an input. demands as an input, time windows as an input.
# Vehicle_Handler
# Time windows and demands are inbuilt into the API handler.
