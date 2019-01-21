import re
from Classes import Port, Ship, Container, Timestamp



def ParseLine(line, rx):
    for key, rx in rx.items():
        match = rx.search(line)
        if match:
            return key, match

    return None, None


class FileExchange:

    @staticmethod
    def LoadAllDataFromFile(path):
        port_list = []
        data = []
        rx_dict = {
            'port': re.compile(r'Port (?P<PortID>\d+) Capacity: (?P<Capacity>\d+)'),
            'ship': re.compile(
                r'Ship ID: (?P<ShipID>\d+) X: (?P<X>\d+) Y: (?P<Y>\d+) Z: (?P<Z>\d+) Capacity: (?P<Capacity>\d+)\n'),
            'container': re.compile(
                r'Container ID: (?P<ContainerID>\d+) X: (?P<X>\d+) Y: (?P<Y>\d+) Z: (?P<Z>\d+) Timestamp:(?P<Month>\d+)-(?P<Day>\d+)-(?P<Year>\d+) DestinationID: (?P<DestinationID>\d+)')
        }
        with open(path, "r") as file_object:
            line = file_object.readline()
            while line:

                key, match = ParseLine(line, rx_dict)
                if key == 'port':
                    port_id = int(match.group('PortID'))
                    port_capacity = int(match.group('Capacity'))
                    # print("PORT ID: " + str(port_id))
                    port_object = Port(port_id, port_capacity)
                    line = file_object.readline()
                    while line.strip():
                        key, match = ParseLine(line, rx_dict)
                        if key == 'ship':
                            ship = int(match.group('ShipID'))
                            x = int(match.group('X'))
                            y = int(match.group('Y'))
                            z = int(match.group('Z'))
                            ship_capacity = int(match.group('Capacity'))
                            ship_ID = int(ship)
                            # print("SHIP ID: " + str(ship_ID) + " X: " + str(x) + " Y: " + str(y) + " Z: " + str(
                            #    z) + " Capacity: " + str(ship_capacity))
                            ship_object = Ship(ship, x, y, z, ship_capacity)
                            port_object.add_ship(ship_object)

                        if key == 'container':
                            container = int(match.group('ContainerID'))
                            x = int(match.group('X'))
                            y = int(match.group('Y'))
                            z = int(match.group('Z'))
                            month = int(match.group('Month'))
                            day = int(match.group('Day'))
                            year = int(match.group('Year'))
                            destination = int(match.group('DestinationID'))
                            timestamp = Timestamp(month, day, year)
                            # print("CONTAINER ID: " + str(container) + " X: " + str(x) + " Y: " + str(y) + " Z: " + str(
                            #    z) + " Date: " + str(month) + "-" + str(day) + "-" + str(year) + " Destination: " + str(
                            #    destination))
                            container_object = Container(container, x, y, z, timestamp, destination)
                            port_object.add_container(container_object)
                        line = file_object.readline()

                    port_list.append(port_object)
                line = file_object.readline()
        for port in port_list:
            handles_list = port_list
            # handles_list.remove(port)
            port.ports_list = handles_list

        if (port_list != None):
            print("\nSucesfully loaded " + str(len(port_list)) + " ports from file\n")
            for port in port_list:
                print("PORT " + str(port.ID))
                print(str(len(port.containers)) + " containers")
                print(str(len(port.ships)) + " ships\n")
        return port_list

    @staticmethod
    def SaveAllDataToFile(path, port_list):
        file = open(path, "w")
        for port in port_list:
            file.write("Port " + str(port.ID) + " Capacity: " + str(port.ship_capacity) + "\n")
            file.write("Ships:\n")
            for ship in port.ships:
                file.write("Ship ID: " + str(ship.ID) + " X: " + str(ship.x) + " Y: " + str(ship.y) + " Z: " + str(
                    ship.z) + " Capacity: " + str(ship.capacity) + "\n")
            file.write("Containers:\n")
            for container in port.containers:
                file.write("Container ID: " + str(container.ID) + " X: " + str(container.x) + " Y: " + str(
                    container.y) + " Z: " + str(
                    container.z) + " Timestamp:" + container.timestamp.get_string() + " DestinationID: " + str(
                    container.destination) + "\n")
            file.write("\n")

    @staticmethod
    def SaveShip(path, ship):
        file = open(path, 'w')
        string = "Ship ID: " + str(ship.ID) + " X: " + str(ship.x) + " Y: " + str(ship.y) + " Z: " + str(
            ship.z) + " Capacity: " + str(ship.capacity) + " Number of containers: " + str(len(ship.containers)) + '\n'
        file.write(string)
        for container in ship.containers:
            string2 = "Container ID: " + str(container.ID) + " X: " + str(container.x) + " Y: " + str(
                container.y) + " Z: " + str(
                container.z) + " Position X: " + str(container.position_x) + " Position Y: " + str(
                container.position_y) + " Timestamp:" + container.timestamp.get_string() + " DestinationID: " + str(
                container.destination) + "\n"
            string = string + string2
            file.write(string2)
        file.write('\n')
        return string

    @staticmethod
    def LoadShipFromFile(path):
        rx_dict = {
            'ship': re.compile(
                r'Ship ID: (?P<ShipID>\d+) X: (?P<X>\d+) Y: (?P<Y>\d+) Z: (?P<Z>\d+) Capacity: (?P<Capacity>\d+)'),
            'container': re.compile(
                r'Container ID: (?P<ContainerID>\d+) X: (?P<X>\d+) Y: (?P<Y>\d+) Z: (?P<Z>\d+) Position X: (?P<PositionX>\d+) Position Y: (?P<PositionY>\d+) Timestamp:(?P<Month>\d+)-(?P<Day>\d+)-(?P<Year>\d+) DestinationID: (?P<DestinationID>\d+)')
        }

        with open(path, "r") as file_object:
            line = file_object.readline()
            ships = []
            while line:
                key, match = ParseLine(line, rx_dict)
                if key == 'ship':

                    ship = int(match.group('ShipID'))
                    x = int(match.group('X'))
                    y = int(match.group('Y'))
                    z = int(match.group('Z'))
                    ship_capacity = int(match.group('Capacity'))
                    ship_ID = int(ship)
                    #print("SHIP ID: " + str(ship_ID))
                    ship_object = Ship(ship, x, y, z, ship_capacity)

                    line = file_object.readline()
                    while line.strip():
                        key, match = ParseLine(line, rx_dict)
                        if key == 'container':
                            container = int(match.group('ContainerID'))
                            x = int(match.group('X'))
                            y = int(match.group('Y'))
                            z = int(match.group('Z'))
                            position_x = int(match.group('PositionX'))
                            position_y = int(match.group('PositionY'))
                            month = int(match.group('Month'))
                            day = int(match.group('Day'))
                            year = int(match.group('Year'))
                            destination = int(match.group('DestinationID'))
                            timestamp = Timestamp(month, day, year)
                            # print("CONTAINER ID: " + str(container) + " X: " + str(x) + " Y: " + str(y) + " Z: " + str(
                            #    z) + " Position X: " + str(position_x) + " Position Y: " + str(
                            #    position_y) + " Date: " + str(month) + "-" + str(day) + "-" + str(
                            #    year) + " Destination: " + str(
                            #    destination))
                            container_object = Container(container, x, y, z, timestamp, destination)
                            container_object.position_x = position_x
                            container_object.position_y = position_y
                            ship_object.containers.append(container_object)
                            ship_object.current_volume = ship_object.current_volume - container_object.volume
                            ship_object.current_capacity = ship_object.current_capacity - 1
                        line = file_object.readline()

                line = file_object.readline()
        try:
            print("Sucesfully loaded ship\n")
            print(str(len(ship_object.containers)) + " containers\n")
            return ship_object
        except:
            print("can't find ship in file")
            return None


def ship_containers(path, output_path, use_inf_ships = True,generate_trip_reports=True,method = "greedy"):
    """

    :param path - path to data that requires solving:
    :param output_path - path to export data:
    :param generate_trip_reports - boolean to generate_trip_reports:
    :return:
    """
    ports = FileExchange.LoadAllDataFromFile(path)

    if use_inf_ships == False:
        not_resolved_ports = 0
        for port in ports:
            not_resolved_ports = not_resolved_ports + port.not_resolved
        while not_resolved_ports > 0:
            not_resolved_ports = 0
            for port in ports:
                not_resolved_ports = not_resolved_ports + port.not_resolved
            for port in ports:
                port.resolve_port(generate_trip_reports)
    else:
        not_resolved_ports = 0
        for port in ports:
            not_resolved_ports = not_resolved_ports + port.not_resolved
        while not_resolved_ports > 0:
            not_resolved_ports = 0
            for port in ports:
                not_resolved_ports = not_resolved_ports + port.not_resolved
            for port in ports:
                port.resolve_port_with_inf_ships(generate_trip_reports,method)


    FileExchange.SaveAllDataToFile(output_path, ports)
    for port in ports:
        print(str(len(port.containers)) + " containers in port " + str(port.ID) + "\n")
