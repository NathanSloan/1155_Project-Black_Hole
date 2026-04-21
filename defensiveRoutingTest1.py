# This is a test of the defense against the Black Hole Attack with Advanced Routers using network configuration 1
# The Advanced Routers will detect suspiciously low link costs and will discard that information instead
#  of adding it to other nodes' lookup tables
# The packet arrives at its intended destination with the Advanced Router

# imports
from systemVariables import Router, EndDevice, Link
from BlackHoleRouter import BlackHoleRouter
from DefensiveRouter import AdvancedRouter

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
routerA = Router("A")
devices.append(routerA)
routerB = AdvancedRouter("B")
devices.append(routerB)
routerC = AdvancedRouter("C")
devices.append(routerC)
routerD = Router("D")
devices.append(routerD)

# define computers and servers
homeComputer = EndDevice("Home Computer")
devices.append(homeComputer)
server = EndDevice("Server")
devices.append(server)

# define links between devices
linkHtoA = Link(homeComputer, routerA)
linkAtoB = Link(routerA, routerB)
linkBtoD = Link(routerB, routerD)
linkAtoC = Link(routerA, routerC)
linkCtoD = Link(routerC, routerD)
linkDtoS = Link(routerD, server)

# define black hole router
blackHole = BlackHoleRouter("Black Hole")
devices.append(blackHole)
linkCtoBH = Link(blackHole, routerC)

# propagate lookup table data after network is finished
for node in devices:
    node.sendUpdate()

# create packet at end device
homeComputer.createPacket(server.getIP(), "Hello World!")

# propagate data through network
for i in range(20):
    for node in devices:
        node.forward()

    movePackets(devices)