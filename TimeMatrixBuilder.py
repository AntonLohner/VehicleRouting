from DataMatrix import create_distance_matrix


def main():
    # I'm going to assume response and json help us parse the data, and add it to a simple matrix. '''
    # TODO: REPLACE with actual data
    # origin=41.43206,-81.38992
    # vs origin=24+Sussex+Drive+Ottawa+ON
    data = ['3610+Hacks+Cross+Rd+Memphis+TN',  # depot
            '1921+Elvis+Presley+Blvd+Memphis+TN',
            '149+Union+Avenue+Memphis+TN',
            '1034+Audubon+Drive+Memphis+TN',
            '1532+Madison+Ave+Memphis+TN',
            '706+Union+Ave+Memphis+TN',
            '3641+Central+Ave+Memphis+TN',
            '926+E+McLemore+Ave+Memphis+TN',
            '4339+Park+Ave+Memphis+TN',
            '600+Goodwyn+St+Memphis+TN',
            '2000+North+Pkwy+Memphis+TN',
            '262+Danny+Thomas+Pl+Memphis+TN',
            '125+N+Front+St+Memphis+TN',
            '5959+Park+Ave+Memphis+TN',
            '814+Scott+St+Memphis+TN',
            '1005+Tillman+St+Memphis+TN'
            ]
    addresses = data
    distance_matrix = create_distance_matrix(data)
    print(distance_matrix)


if __name__ == '__main__':
    main()

