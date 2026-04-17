# This is a test of network configuration 2
# Each packet will take the shortest path to its destination based on the lookup table data 
#  held in each device
# Each packet will print where it ended, the message in the packet, the path that it took, 
#  and the cost of the path

# imports
from SystemVariables import Router, EndDevice, Link

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
router10 = Router("10")
devices.append(router10)
router11 = Router("11")
devices.append(router11)

# define computers
homeComputerA = EndDevice("Home Computer A")
devices.append(homeComputerA)
homeComputerB = EndDevice("Home Computer B")
devices.append(homeComputerB)
homeComputerC = EndDevice("Home Computer C")
devices.append(homeComputerC)

# define servers
server1 = EndDevice("Server 1")
devices.append(server1)
server2 = EndDevice("Server 2")
devices.append(server2)
server3 = EndDevice("Server 3")
devices.append(server3)
server4 = EndDevice("Server 4")
devices.append(server4)

# define links between devices
Link(router1, router2)
Link(router2, router3)
Link(router3, router7)
Link(router7, router5)
Link(router5, router4)
Link(router4, router1)
Link(router1, router6)
Link(router2, router8)
Link(router8, router9)
Link(router9, router10)
Link(router9, router11)
Link(router8, router11)

Link(homeComputerA, router1)
Link(homeComputerB, router1)
Link(homeComputerC, router11)
Link(server1, router6)
Link(server2, router7)
Link(server3, router5)
Link(server4, router10)

# propagate lookup table data after network is finished
for node in devices:
    node.sendUpdate()

# create packets at end device
homeComputerA.createPacket(server1.getIP(), "Twitter Post")
homeComputerA.createPacket(server4.getIP(), "Request to install minecraft.exe")
homeComputerB.createPacket(server2.getIP(), "Request to install teamFortress2.exe")
homeComputerC.createPacket(server4.getIP(), "Request to install balatro.exe")

# propagate data through network
# depending on info received at servers, will create packets to send back through network
for i in range(100):
    for node in devices:
        info = node.forward()
        if info == "Request to install minecraft.exe":
            node.createPacket(homeComputerA.getIP(), "minecraft.exe")
        if info == "Request to install teamFortress2.exe":
            node.createPacket(homeComputerB.getIP(), "teamFortress2.exe")
        if info == "Request to install balatro.exe":
            node.createPacket(homeComputerC.getIP(), "balatro.exe")

    movePackets(devices)