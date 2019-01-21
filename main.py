from FileExchange import ship_containers
from Classes import Port
from Classes import Ship
from RandomGenerators import ContainerGenerator
from FileExchange import FileExchange
ship_containers('ExampleContainerList.txt', 'ExampleResults.txt', True, True, "random")

ship = ContainerGenerator.GenerateShip(1,70,200,10,50,100,10)
ship2 = ContainerGenerator.GenerateShip(1,70,200,10,50,100,10)

ports = [Port(1,5),Port(2,6)]
ports[0].ships = [ship,ship2]
container_list = []
for i in range(0,100):
    container_list.append(ContainerGenerator.GenerateContainer(i,50,50,10,20,2))

ports[0].containers = container_list
FileExchange.SaveAllDataToFile("cos.txt",ports)

