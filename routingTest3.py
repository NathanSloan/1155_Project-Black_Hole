# This is a test of network configuration 2
# Each packet will take the shortest path to its destination based on the lookup table data 
#  held in each device
# Each packet will print where it ended, the message in the packet, the path that it took, 
#  and the cost of the path

# imports
from systemVariables import Router, EndDevice, Link

# move packets in system
def movePackets(routers):
    for node in routers:
        newPackets = []

        for packet in node.packets:
            if packet.nextLocation:
                packet.currentLocation = packet.nextLocation
                packet.nextLocation.packets.append(packet)
                packet.nextLocation = None
            else:
                newPackets.append(packet)

        node.packets = newPackets

# Starting network
# Define routers
devices = []
router1 = Router("1")
devices.append(router1)
router2 = Router("2")
devices.append(router2)
router3 = Router("3")
devices.append(router3)
router4 = Router("4")
devices.append(router4)
router5 = Router("5")
devices.append(router5)
router6 = Router("6")
devices.append(router6)
router7 = Router("7")
devices.append(router7)
router8 = Router("8")
devices.append(router8)
router9 = Router("9")
devices.append(router9)

# define computers
homeComputerA = EndDevice("Home Computer A")
devices.append(homeComputerA)
homeComputerB = EndDevice("Home Computer B")
devices.append(homeComputerB)

# define servers
server1 = EndDevice("Server 1")
devices.append(server1)
server2 = EndDevice("Server 2")
devices.append(server2)

# define links between devices
Link(router1, router2, 4)
Link(router2, router3, 3)
Link(router3, router4, 6)
Link(router4, router5, 2)
Link(router5, router6, 1)
Link(router6, router7, 8)
Link(router7, router8, 1)
Link(router8, router1, 2)
Link(router1, router9, 2)
Link(router2, router9, 1)
Link(router4, router9, 2)
Link(router6, router9, 4)
Link(router7, router9, 3)

Link(homeComputerA, router6, 1)
Link(homeComputerB, router7, 1)
Link(server1, router3, 2)
Link(server2, router1, 2)

# propagate lookup table data after network is finished
for node in devices:
    node.sendUpdate()

# create packets at end devices
homeComputerA.createPacket(server1.getIP(), "Hello server 1: From Computer A")
homeComputerA.createPacket(server2.getIP(), "Hello server 2: From Computer A")
homeComputerB.createPacket(server1.getIP(), "Hello server 1: From Computer B")
homeComputerB.createPacket(server2.getIP(), "Hello server 2: From Computer B")

# propagate data through network
for i in range(20):
    for node in devices:
        node.forward()

    movePackets(devices)