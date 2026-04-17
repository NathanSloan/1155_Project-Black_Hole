# Black Hole Routing Objects

# imports
from SystemVariables import Router

# Black Hole Router Object
class BlackHoleRouter(Router):
    def sendUpdate(self):
        fakeTable = {}

        # claim best route for everything, lowest possible cost
        for dest in self.lookupTable:
            fakeTable[dest] = ([self], None, 0)

        for link in self.links:
            otherNode = link.getOtherNode(self)
            otherNode.receiveUpdate(self, fakeTable)

    # define when packet is consumed by router, print to terminal
    def forward(self):
        for packet in self.packets:
            print(f"Packet has been claimed by Black Hole Router with message: {packet.information}")
            print(f"Path took: {packet.path}")
            print(f"Cost of Path: {self.lookupTable[packet.sourceIP][2]}")
            self.packets.remove(packet)
            return None

# Advanced Black Hole Router Object
class AdvancedBlackHoleRouter(Router):
    def __init__(self, name, cost):
        self.cost = cost
        super().__init__(name)
    def sendUpdate(self):
        fakeTable = {}

        # claim a low cost route that will not be picked up by the defensive routers
        for dest in self.lookupTable:
            fakeTable[dest] = ([self], None, self.cost)

        for link in self.links:
            otherNode = link.getOtherNode(self)
            otherNode.receiveUpdate(self, fakeTable)

    # define when packet is consumed by router, print to terminal
    def forward(self):
        for packet in self.packets:
            print(f"Packet has been claimed by Black Hole Router with message: {packet.information}")
            print(f"Path took: {packet.path}")
            print(f"Cost of Path: {self.lookupTable[packet.sourceIP][2]}")
            self.packets.remove(packet)
            return None