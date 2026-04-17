# System Objects

# imports
import random as rn

# ensure generated IP does not match any other IPs in network
ipAddresses = []
def generateIP():
    ip = ".".join(str(rn.randint(0, 255)) for _ in range(4))
    ipAddresses.append(ip)
    while not ip in ipAddresses:
        ipAddresses.pop()
        ip = ".".join(str(rn.randint(0, 255)) for _ in range(4))
        ipAddresses.append(ip)

    return ip

# Represents any abstract device in the network
class Node:
    def __init__(self, name):
        # name of node
        self.name = name
        # links to node
        self.links = []
        # IP address of node (generated randomly on startup)
        self.ip = generateIP()
        # packets currently held by node
        self.packets = []
        # lookup table propagated on startup
        self.lookupTable = {}
    
    # add link between two nodes
    def addLink(self, link):
        self.links.append(link)

        otherNode = link.getOtherNode(self)
        if isinstance(otherNode, EndDevice):
            self.lookupTable[otherNode.getIP()] = ([self, otherNode], otherNode, link.cost)

    # get cost of link to neighbor
    def getLinkCost(self, neighbor):
        for link in self.links:
            if (link.a == self and link.b == neighbor) or (link.b == self and link.a == neighbor):
                return link.cost
        return float('inf')  # no direct link

    # propagate other node's lookup table with location of end devices in network
    def sendUpdate(self):
        for link in self.links:
            otherNode = link.getOtherNode(self)
            otherNode.receiveUpdate(self, self.lookupTable)

    # receive location of end device in network to propagate own lookup table
    def receiveUpdate(self, otherNode, otherLookupTable):
        updated = False

        linkCost = self.getLinkCost(otherNode)

        for dest, (path, _, otherCost) in otherLookupTable.items():
            # loop prevention (very important)
            if self in path:
                continue
            newPath = [self] + path
            newCost = otherCost + linkCost
            # determine if location is new or if new route is more efficient
            if dest not in self.lookupTable or newCost < self.lookupTable[dest][2]:
                self.lookupTable[dest] = (newPath, otherNode, newCost)
                updated = True
        
        if updated:
            self.sendUpdate()
    
    # forward packet in network
    def forward(self):
        for packet in self.packets:
            # check if packet is at destination
            if packet.destinationIP == self.ip:
                print(f"Packet arrived at {self} with message: {packet.information}")
                print(f"Path took: {packet.path}")
                print(f"Cost of Path: {self.lookupTable[packet.sourceIP][2]}")
                self.packets.remove(packet)
                return packet.information
            # check if packet cannot be routed to destination
            elif packet.destinationIP not in self.lookupTable:
                print("No route, dropping")
                return None
            # determine next node for packet to visit based on lookup table
            else:
                next_hop = self.lookupTable[packet.destinationIP][1]
                packet.path.append(next_hop)
                packet.nextLocation = next_hop
                return None

    def getIP(self):
        return self.ip

class Router(Node):
    def __repr__(self):
        return f"Router({self.name})"

class EndDevice(Node):
    def __repr__(self):
        return f"End Device({self.name})"

    # create packet at end device
    def createPacket(self, destinationIP, information=None):
        self.packets.append(Packet(self, destinationIP, information))

# Represents connection between devices in network
class Link:
    def __init__(self, a, b, cost=1):
        self.cost = cost
        self.a = a
        self.b = b
        a.addLink(self)
        b.addLink(self)

    # get other node connected to link based on node calling function
    def getOtherNode(self, node):
        if self.a == node:
            return self.b
        elif self.b == node:
            return self.a

# Represents data in the network
class Packet:
    def __init__(self, startNode, destinationIP, information):
        self.currentLocation = startNode
        self.nextLocation = None
        self.sourceIP = startNode.getIP()
        self.destinationIP = destinationIP
        self.information = information
        self.path = [startNode.name]