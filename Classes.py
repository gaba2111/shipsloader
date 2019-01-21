import random

import pygame
import datetime
import math

WHITE = (255, 255, 255)
BASE_COLOR = {0, 0, 0}


class ShipLoader:
    @staticmethod
    def LoadShip(ship, container_list, merges_number, by_date,method = "greedy"):
        if method == "greedy":
            if by_date:
                container_list.sort(key=lambda x: x.timestamp.date_to_number_of_days(), reverse=False)
            if not by_date:
                container_list.sort(key=lambda x: x.volume, reverse=True)

            containers_to_remove = []
            for contain in container_list:
                if ship.load_container(contain) == 0:
                    containers_to_remove.append(contain)

            for contain in containers_to_remove:
                container_list.remove(contain)

            for j in range(0, merges_number):
                for i in range(0, len(ship.decks)):
                    ship.merge_deck()
                print("merge decks used \n")

                containers_to_remove = []
                for contain in container_list:
                    if ship.load_container(contain) == 0:
                        containers_to_remove.append(contain)

                for contain in containers_to_remove:
                    container_list.remove(contain)

            if len(container_list) == 0:
                print("loaded all the containers")
            else:
                print("couldn't load all the containers")

        if method == "genetic":
            if by_date:
                container_list.sort(key=lambda x: x.timestamp.date_to_number_of_days(), reverse=False)
            if not by_date:
                container_list.sort(key=lambda x: x.volume, reverse=True)
            z = 0
            best = []
            best_fitness = 0
            while z < 3:
                if by_date:
                    container_list.sort(key=lambda x: x.timestamp.date_to_number_of_days(), reverse=False)
                if not by_date:
                    container_list.sort(key=lambda x: x.volume, reverse=True)
                solution = [random.randint(0, ship.x), random.randint(0 , ship.y)]
                best = solution
                while ship.load_container_on_deck_at_coordinates(ship.decks[0], container_list[0], solution[0],
                                                           solution[1]) == 1:
                    solution = [random.randint(0, ship.x), random.randint(0, ship.y)]
                containers_to_remove = []

                containers_to_remove.append(container_list[0])
                i = 1
                if len(container_list) >= 6:
                    for j in range(1, 5):
                        if ship.load_container_on_deck_at_coordinates(ship.decks[i], container_list[j],0, 0) == 1:
                            i -= 1
                            continue
                        containers_to_remove.append(container_list[j])
                        i += 1
                    for contain in containers_to_remove:
                        container_list.remove(contain)

                containers_to_remove = []
                for contain in container_list:
                    if ship.load_container(contain) == 0:
                        containers_to_remove.append(contain)

                for contain in containers_to_remove:
                    container_list.remove(contain)

                if len(container_list) == 0:
                    print("loaded all the containers")
                else:
                    print("couldn't load all the containers")

                if len(ship.containers) > best_fitness:
                    best = solution

                container_list.extend(ship.unload_ship())
                ship.reset()
                z += 1

            solution =  best
            if by_date:
                container_list.sort(key=lambda x: x.timestamp.date_to_number_of_days(), reverse=False)
            if not by_date:
                container_list.sort(key=lambda x: x.volume, reverse=True)

            containers_to_remove = []
            ship.load_container_on_deck_at_coordinates(ship.decks[0], container_list[0], solution[0],
                                                       solution[1])
            containers_to_remove.append(container_list[0])
            i = 1
            if len(container_list) >= 6:
                for j in range(1, 5):
                    if ship.load_container_on_deck_at_coordinates(ship.decks[i], container_list[j],0, 0) == 1:
                        i -= 1
                        continue
                    containers_to_remove.append(container_list[j])
                    i += 1
                for contain in containers_to_remove:
                    container_list.remove(contain)

            containers_to_remove = []
            for contain in container_list:
                if ship.load_container(contain) == 0:
                    containers_to_remove.append(contain)

            for contain in containers_to_remove:
                container_list.remove(contain)

            if len(container_list) == 0:
                print("loaded all the containers")
            else:
                print("couldn't load all the containers")

            if len(ship.containers) > best_fitness:
                best = solution

        if method == "random":
            if by_date:
                container_list.sort(key=lambda x: x.timestamp.date_to_number_of_days(), reverse=False)
            if not by_date:
                container_list.sort(key=lambda x: x.volume, reverse=True)

            containers_to_remove = []

            solution = [random.randint(0, ship.x), random.randint(0, ship.y)]

            ship.load_container_on_deck_at_coordinates(ship.decks[0], container_list[0], solution[0],
                                                             solution[1])
            containers_to_remove.append(container_list[0])
            container_list.remove(containers_to_remove[0])
            containers_to_remove = []

            for contain in container_list:
                if ship.load_container(contain,True) == 0:
                    containers_to_remove.append(contain)

            for contain in containers_to_remove:
                container_list.remove(contain)

            for j in range(0, merges_number):
                for i in range(0, len(ship.decks)):
                    ship.merge_deck()
                print("merge decks used \n")

                containers_to_remove = []
                for contain in container_list:
                    if ship.load_container(contain) == 0:
                        containers_to_remove.append(contain)

                for contain in containers_to_remove:
                    container_list.remove(contain)

            if len(container_list) == 0:
                print("loaded all the containers")
            else:
                print("couldn't load all the containers")


        return ship.containers


class Ship:
    def __init__(self, _id, _x, _y, _z, _capacity):
        self.ID = _id
        self.x = _x
        self.y = _y
        self.z = _z
        self.capacity = _capacity
        self.volume = self.x * self.y * self.z
        self.current_capacity = _capacity
        self.current_volume = self.volume
        self.containers = []
        self.decks = []
        self.decks.append(Deck(self.x, self.y, 0, 0))
        self.fuel_consumption = 0

    def reset(self):
        self.current_capacity = self.capacity
        self.current_volume = self.volume
        for deck in self.decks:
            self.decks.remove(deck)
        self.decks = []
        self.decks.append(Deck(self.x, self.y, 0, 0))

    def get_free_space(self):
        free_space = 0
        for deck in self.decks:
            free_space += deck.x * deck.y
        return free_space

    def merge_deck(self):
        for deck_1 in self.decks:
            for deck_2 in self.decks:
                if deck_1 != deck_2:
                    if deck_2.origin_y >= deck_1.origin_y:

                        if deck_1.origin_y + deck_1.y >= deck_2.origin_y and deck_2.origin_x == deck_1.origin_x + deck_1.x and deck_2.origin_y + deck_2.y >= deck_1.origin_y + deck_1.y:
                            size_of_new_deck = (deck_1.origin_y + deck_1.y - deck_2.origin_y) * (deck_1.x + deck_2.x)
                            if size_of_new_deck > deck_1.size and size_of_new_deck > deck_2.size:
                                new_deck1 = Deck(deck_1.x, deck_2.origin_y - deck_1.origin_y, deck_1.origin_x,
                                                 deck_1.origin_y)
                                new_deck2 = Deck(deck_1.x + deck_2.x, deck_1.origin_y + deck_1.y - deck_2.origin_y,
                                                 deck_1.origin_x, deck_2.origin_y, )
                                new_deck3 = Deck(deck_2.x, deck_2.origin_y + deck_2.y - deck_1.y - deck_1.origin_y,
                                                 deck_2.origin_x, deck_1.origin_y + deck_1.y)
                                self.decks.remove(deck_1)
                                self.decks.remove(deck_2)
                                if new_deck1.size > 0:
                                    self.decks.append(new_deck1)
                                if new_deck2.size > 0:
                                    self.decks.append(new_deck2)
                                if new_deck3.size > 0:
                                    self.decks.append(new_deck3)
                                return 0

                    else:
                        if deck_2.origin_y + deck_2.y >= deck_1.origin_y and deck_2.origin_x == deck_1.origin_x + deck_1.x and deck_2.origin_y + deck_2.y <= deck_1.origin_y + deck_1.y:
                            size_of_new_deck = (deck_2.origin_y + deck_2.y - deck_1.origin_y) * (deck_1.x + deck_2.x)
                            if size_of_new_deck > deck_1.size and size_of_new_deck > deck_2.size:
                                new_deck1 = Deck(deck_2.x, deck_1.origin_y - deck_2.origin_y, deck_2.origin_x,
                                                 deck_2.origin_y)
                                new_deck2 = Deck(deck_1.x + deck_2.x, deck_2.origin_y + deck_2.y - deck_1.origin_y,
                                                 deck_1.origin_x, deck_1.origin_y)
                                new_deck3 = Deck(deck_1.x, deck_1.origin_y + deck_1.y - deck_2.y - deck_2.origin_y,
                                                 deck_1.origin_x, deck_2.origin_y + deck_2.y)
                                self.decks.remove(deck_1)
                                self.decks.remove(deck_2)
                                if new_deck1.size > 0:
                                    self.decks.append(new_deck1)
                                if new_deck2.size > 0:
                                    self.decks.append(new_deck2)
                                if new_deck3.size > 0:
                                    self.decks.append(new_deck3)
                                return 0

        return 1

    def load_container(self, container, Random = False):
        loaded = 0
        for deck in self.decks:
            if loaded == 0:
                if not Random:
                    if self.load_container_on_deck(deck, container) == 0:
                        loaded = 1
                else:
                    if self.load_container_on_deck_at_coordinates(deck,container,random.randint(0,deck.x),random.randint(0,deck.y)) == 0:
                        loaded = 1

        if loaded == 1:
            # print("container loaded successfully \n")
            return 0
        else:
            # print("cannot load the container \n")
            return 1


    def unload_ship(self):
        unloaded_containers = self.containers
        self.containers = []
        self.current_volume = self.volume

        return unloaded_containers

    def get_ship_information(self):

        id_and_sizes = "Ship ID: " + str(self.ID) + " Sizes(x,y,z): " + str(self.x) + ", " + str(self.y) + ", " + str(
            self.z) + "\n"
        capacity_volume_current_capacity_volume = "Capacity: " + str(self.capacity) + " Volume: " + str(
            self.volume) + " Current Capacity: " + str(self.current_capacity) + " Current Volume: " + str(
            self.current_volume) + "\n"
        print(id_and_sizes + capacity_volume_current_capacity_volume)
        return id_and_sizes + capacity_volume_current_capacity_volume

    def load_container_on_deck(self, deck, container):
        if self.current_capacity == 0:
            print("Ship is full(capacity left = 0")
            return 1
        if container.x <= deck.x and container.y <= deck.y:
            load = 1
        elif container.y <= deck.x and container.x <= deck.y:
            temp = container.x
            container.x = container.y
            container.y = temp
            load = 1
        else:
            load = 0

        if load == 1:
            new_deck1 = Deck(deck.x - container.x, container.y, deck.origin_x + container.x, deck.origin_y)
            new_deck2 = Deck(container.x, deck.y - container.y, deck.origin_x, deck.origin_y + container.y)
            new_deck3 = Deck(deck.x - container.x, deck.y - container.y, deck.origin_x + container.x,
                             deck.origin_y + container.y)
            self.decks.remove(deck)
            if new_deck2.size > 0:
                self.decks.append(new_deck2)
            if new_deck1.size > 0:
                self.decks.append(new_deck1)
            if new_deck3.size > 0:
                self.decks.append(new_deck3)
            container.position_x = deck.origin_x
            container.position_y = deck.origin_y
            self.containers.append(container)
            self.current_volume = self.current_volume - container.volume
            self.current_capacity = self.current_capacity - 1

            return 0
        else:
            return 1

    def load_container_on_deck_at_coordinates(self, deck, container, x, y):
        if self.current_capacity == 0:
            print("Ship is full(capacity left = 0")
            return 1
        if x + container.x <= deck.x and container.y + y <= deck.y:
            load = 1
        elif container.y + y <= deck.x and container.x + x <= deck.y:
            temp = container.x
            container.x = container.y
            container.y = temp
            temp = x
            x = y
            y = temp
            load = 1
        else:
            load = 0

        if load == 1:
            new_deck3 = Deck(deck.x - container.x-x, container.y, deck.origin_x + x + container.x, deck.origin_y + y)
            new_deck1 = Deck(container.x, deck.y - container.y - y, deck.origin_x + x, deck.origin_y + y + container.y)
            new_deck2 = Deck(deck.x - container.x - x, deck.y - container.y - y, deck.origin_x + x + container.x,
                             deck.origin_y + y + container.y)
            new_deck4 = Deck(deck.x - x - container.x, y, deck.origin_x + x + container.x,
                             deck.origin_y + deck.origin_y)
            new_deck5 = Deck(container.x, y, deck.origin_x + x, deck.origin_y)
            new_deck6 = Deck(x, y, deck.origin_x, deck.origin_y)
            new_deck7 = Deck(x, container.y, deck.origin_x, deck.origin_y + y)
            new_deck8 = Deck(x, deck.y - y - container.y, deck.origin_x, deck.origin_y + container.y + y)
            self.decks.remove(deck)
            if new_deck1.size > 0:
                self.decks.append(new_deck1)
            if new_deck2.size > 0:
                self.decks.append(new_deck2)
            if new_deck3.size > 0:
                self.decks.append(new_deck3)
            if new_deck4.size > 0:
                self.decks.append(new_deck4)
            if new_deck5.size > 0:
                self.decks.append(new_deck5)
            if new_deck6.size > 0:
                self.decks.append(new_deck6)
            if new_deck7.size > 0:
                self.decks.append(new_deck7)
            if new_deck8.size > 0:
                self.decks.append(new_deck8)
            container.position_x = deck.origin_x + x
            container.position_y = deck.origin_y + y
            self.containers.append(container)
            self.current_volume = self.current_volume - container.volume
            self.current_capacity = self.current_capacity - 1

            return 0
        else:
            return 1

    def display_ship(self, current_destination):
        pygame.init()
        monitor_fullness = 0.8
        monitor_h = pygame.display.Info().current_h

        scale = monitor_fullness / ((self.y + math.floor(300 / 700 * self.y)) / monitor_h)

        screen = pygame.display.set_mode(
            (math.floor(scale * self.x), math.floor(scale * (self.y + math.floor(300 / 700 * self.y)))))
        font_size = math.floor(scale * 10)

        myfont = pygame.font.SysFont("monospace", font_size)
        clock = pygame.time.Clock()
        background = pygame.image.load("background.jpg").convert()
        background = pygame.transform.rotate(background, 90)
        background = pygame.transform.scale(background, [math.floor(scale * self.x),
                                                         math.floor(scale * (self.y + math.floor(300 / 700 * self.y)))])
        running = True
        if(len(self.containers)!=0):
            pygame.display.set_caption(
                str(self.ID) + " Destination " + str(current_destination) + "->" + str(self.containers[0].destination))

        # main loop
        while running:
            clock.tick(10)
            # event handling, gets all event from the eventqueue
            for event in pygame.event.get():
                # only do something if the event is of type QUIT
                if event.type == pygame.QUIT:
                    # change the value to False, to exit the main loop
                    running = False
            color_loop = 100
            color = 1
            screen.blit(background, [0, 0])

            for container in self.containers:

                if color == 1:
                    color_to_print = [color_loop, 0, 0]
                elif color == 2:
                    color_to_print = [0, color_loop, 0]
                else:
                    color_to_print = [0, 0, color_loop]
                pygame.draw.rect(screen, color_to_print, [math.floor(scale * container.position_x),
                                                          math.floor(scale * (container.position_y + math.floor(
                                                              220 / 1011 * (self.y + math.floor(300 / 700 * self.y))))),
                                                          math.floor(scale * container.x),
                                                          math.floor(scale * container.y)],
                                 0)
                color_loop = color_loop + 10
                color = color + 1
                if color_loop >= 255:
                    color_loop = 100
                if color == 4:
                    color = 1
                label_id = myfont.render(str(container.ID), 1, (0, 0, 0))
                label_month = myfont.render(str(container.timestamp.month), 1, (0, 0, 0))
                label_day = myfont.render(str(container.timestamp.day), 1, (0, 0, 0))
                label_year = myfont.render(str(container.timestamp.year), 1, (0, 0, 0))
                label_one_line = myfont.render(
                    str(container.timestamp.month) + "-" + str(container.timestamp.day) + "-" + str(
                        container.timestamp.year), 1, (0, 0, 0))
                if container.y > container.x:
                    screen.blit(label_id, (
                        math.floor(scale * container.position_x), math.floor(scale * (container.position_y + math.floor(
                            220 / 1011 * (self.y + math.floor(300 / 700 * self.y)))))))
                    screen.blit(label_month, (math.floor(scale * container.position_x),
                                              math.floor(scale * (container.position_y + font_size + math.floor(
                                                  220 / 1011 * (self.y + math.floor(300 / 700 * self.y)))))))
                    screen.blit(label_day, (math.floor(scale * container.position_x),
                                            math.floor(scale * (container.position_y + 2 * font_size + math.floor(
                                                220 / 1011 * (self.y + math.floor(300 / 700 * self.y)))))))
                    screen.blit(label_year, (math.floor(scale * container.position_x),
                                             math.floor(scale * (container.position_y + 3 * font_size + math.floor(
                                                 220 / 1011 * (self.y + math.floor(300 / 700 * self.y)))))))
                else:
                    screen.blit(label_id, (
                        math.floor(scale * container.position_x), math.floor(scale * (container.position_y + math.floor(
                            220 / 1011 * (self.y + math.floor(300 / 700 * self.y)))))))
                    screen.blit(label_one_line, (math.floor(scale * container.position_x),
                                                 math.floor(scale * (container.position_y + font_size + math.floor(
                                                     220 / 1011 * (self.y + math.floor(300 / 700 * self.y)))))))

            pygame.display.flip()

        pygame.quit()


class Deck:
    def __init__(self, _x, _y, _origin_x, _origin_y):
        self.x = _x
        self.y = _y
        self.origin_x = _origin_x
        self.origin_y = _origin_y
        self.size = self.x * self.y


class Container:
    def __init__(self, _id, _x, _y, _z, _timestamp, _destination):
        self.timestamp = _timestamp
        self.x = _x
        self.y = _y
        self.z = _z
        self.volume = self.x * self.y * self.z
        self.ID = _id
        self.mass = self.x * self.y * self.z * 1000
        self.position_x = 0
        self.position_y = 0
        self.destination = _destination

    def show_timestamp(self):
        print(str(self.timestamp.month) + "-" + str(self.timestamp.day) + "-" + str(self.timestamp.year) + "\n")

    def get_container_information(self):
        id_and_sizes = "Container ID: " + str(self.ID) + " Sizes(x,y,z): " + str(self.x) + ", " + str(
            self.y) + ", " + str(
            self.z) + "\n"
        volume = "Volume: " + str(self.volume) + "\n"
        print(id_and_sizes + volume)
        return id_and_sizes + volume


class Timestamp:
    def __init__(self, _month, _day, _year):
        self.month = _month
        self.day = _day
        self.year = _year

    def date_to_number_of_days(self):
        return self.year * 365 + self.month * 31 + self.day

    def get_string(self):
        return str(self.month) + "-" + str(self.day) + "-" + str(self.year)


class Port:
    def __init__(self, _id, _ship_capacity, ):
        self.ships_send = 0
        self.not_resolved = 1
        self.ports_list = []
        self.containers = []
        self.ID = _id
        self.ship_capacity = _ship_capacity
        self.ships = []
        self.destination_list = []
        self.containers_with_destination = []

    def resolve_port(self, generate_trip_reports):
        self.create_destination_list()
        containers_to_remove = []
        ships_to_send = []
        for destination in self.containers_with_destination:
            if len(self.ships) > 0:
                for ship in self.ships:
                    containers_to_remove = self.load_ship(ship.ID, destination, 2, False)
                    if len(containers_to_remove) > 0:
                        ships_to_send.append(ship)
                    for container in containers_to_remove:
                        if container in self.containers:
                            self.containers.remove(container)
                    if len(destination) == 0 and destination in self.containers_with_destination:
                        self.containers_with_destination.remove(destination)

                for ship in ships_to_send:
                    print("sending ship" + str(ship.ID))
                    ship.display_ship(self.ID)
                    self.send_ship(self.ships,ship.ID, ship.containers[0].destination, generate_trip_reports,False)
                for ship in ships_to_send:
                    self.undock_ship(ship)
            else:
                self.request_ship(generate_trip_reports)

        self.create_destination_list()
        if len(self.containers_with_destination) == 0:
            self.not_resolved = 0
        return 0

    def resolve_port_with_inf_ships(self,generate_trip_reports, method):
        self.ships.sort(key=lambda x: x.volume, reverse=False)
        ships_to_send = []
        for destination in self.containers_with_destination:
            while len(destination) > 0:
                sent = 0
                for ship in self.ships:
                    ShipLoader.LoadShip(ship, destination, 2,True, method)
                    if len(destination) > 0 and self.ships.index(ship) != len(self.ships) - 1:
                        destination.extend(ship.containers)
                        ship.containers.clear()
                        ship.reset()
                        continue
                    if len(destination) > 0 and self.ships.index(ship) == len(self.ships) - 1:
                        ships_to_send.append(ship)
                        current_sent_ship = ship
                        sent = 1
                    if len(destination) == 0:
                        self.containers_with_destination.remove(destination)
                        ships_to_send.append(ship)
                        current_sent_ship = ship
                        sent = 1
                        break

                if sent == 1:
                    self.ships.append(Ship(current_sent_ship.ID + 100, current_sent_ship.x, current_sent_ship.y, current_sent_ship.z,
                                      current_sent_ship.capacity))
                    self.ships.remove(current_sent_ship)
                self.ships.sort(key=lambda x: x.volume, reverse=False)

            for ship in ships_to_send:
                for container in ship.containers:
                    self.containers.remove(container)
                print("sending ship" + str(ship.ID))
                ship.display_ship(self.ID)
                self.send_ship(ships_to_send,ship.ID, ship.containers[0].destination, generate_trip_reports, inf = True)

        self.create_destination_list()
        if len(self.containers_with_destination) == 0:
            self.not_resolved = 0
        return 0

    def request_ship(self, generate_trip_reports):
        for port in self.ports_list:
            if port != self:
                port.create_destination_list()
                if len(port.containers_with_destination) == 0 and len(port.ships) > 0:
                    port.send_ship(port.ships[0].ID, self.ID, generate_trip_reports)
                    port.undock_ship(port.ships[0])
        print("cos")

    def create_destination_list(self):
        self.destination_list = []
        self.containers_with_destination = []
        for container in self.containers:
            if not container.destination in self.destination_list and container.destination != self.ID:
                self.destination_list.append(container.destination)

        for destination in self.destination_list:
            containers_to_destination = []
            for container in self.containers:
                if container.destination == destination:
                    containers_to_destination.append(container)
            self.containers_with_destination.append(containers_to_destination)

        self.containers_with_destination.sort(key=lambda x: len(x), reverse=True)

    def add_ship(self, ship):
        self.ships.append(ship)

    def add_container(self, container):
        self.containers.append(container)

    def send_ship(self,ship_list, ship_id, dest_port_id,generate_trip_reports, inf = True):
        for x in self.ports_list:
            if x.ID == dest_port_id:
                for y in ship_list:
                    if y.ID == ship_id:
                        trip_number = 0
                        for port in self.ports_list:
                            trip_number = trip_number + port.ships_send
                        if generate_trip_reports:
                            GenerateSendReport("", y, self.ID, dest_port_id, trip_number)
                        print("docking ship" + str(y.ID))
                        x.dock_ship(y,inf)
                        self.ships_send = self.ships_send + 1

    def unload_ship(self, ship):
        containers_to_remove = []
        for container in ship.containers:
            containers_to_remove.append(container)
            self.containers.append(container)
        for container in containers_to_remove:
            ship.containers.remove(container)
        ship.reset()

    def undock_ship(self, ship):
        self.ships.remove(ship)

    def dock_ship(self, ship,inf = True):
        if len(self.ships) < self.ship_capacity:
            self.unload_ship(ship)
            if not inf:
                self.add_ship(ship)
            return 0
        else:
            return 1

    def get_ships(self):
        return self.ships

    def load_ship(self, ship_id, container_list, merges_number, by_date):
        for x in self.ships:
            if x.ID == ship_id:
                loaded_containers = ShipLoader.LoadShip(x, container_list, merges_number, by_date)
                print("loaded ship")
                return loaded_containers
        else:
            print("couldn't find ship")
            return 1


def GenerateSendReport(path, ship, current_location, destination, travel_number):
    path = path + "Travel " + str(travel_number + 1)
    file = open(path, 'w')
    file.write('Travel number: ' + str(travel_number + 1) + " From port: " + str(current_location) + " To port: " + str(
        destination))
    string = " Ship ID: " + str(ship.ID) + " X: " + str(ship.x) + " Y: " + str(ship.y) + " Z: " + str(
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
