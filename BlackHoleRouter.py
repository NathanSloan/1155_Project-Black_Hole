from systemVariables import Router

class BlackHoleRouter(Router):
    def sendUpdate(self):
        fakeTable = {}

        # claim best route for everything, lowest possible cost
        for dest in self.lookupTable:
            fakeTable[dest] = ([self], None, 0)

        for link in self.links:
            otherNode = link.getOtherNode(self)
            otherNode.receiveUpdate(self, fakeTable)

    def forward(self):
        for packet in self.packets:
                print(f"Packet has been claimed by Black Hole Router with message: {packet.information}")
                print(f"Path took: {packet.path}")
                print(f"Cost of Path: {self.lookupTable[packet.sourceIP][2]}")
                self.packets.remove(packet)