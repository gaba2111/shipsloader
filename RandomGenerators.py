from random import randint
from Classes import Timestamp, Ship, Container
import math


class ContainerGenerator:

    @staticmethod
    def GenerateContainer(ID, size_x, size_y, size_z, deviation, destination):
        deviation_random = randint(-deviation, deviation)
        deviation_percentage = deviation_random / 100
        container_size_x = math.floor(size_x + size_x * deviation_percentage)
        container_size_y = math.floor(size_y + size_y * deviation_percentage)
        container_size_z = size_z

        container = Container(ID, container_size_x, container_size_y, container_size_z,
                              Timestamp(randint(1, 12), randint(1, 30), randint(2019, 2022)), destination)
        return container

    @staticmethod
    def GenerateShip(ID, size_x, size_y, size_z, deviation, capacity, capacity_deviation):
        deviation_random = randint(-deviation, deviation)
        capacity_deviation_random = randint(-capacity_deviation, capacity_deviation)
        capacity_deviation_percentage = capacity_deviation_random / 100
        deviation_percentage = deviation_random / 100
        ship_size_x = math.floor(size_x + size_x * deviation_percentage)
        ship_size_y = math.floor(size_y + size_y * deviation_percentage)
        ship_capacity = math.floor(capacity + capacity_deviation_percentage * capacity)
        ship = Ship(ID, ship_size_x, ship_size_y, size_z, ship_capacity)
        return ship

