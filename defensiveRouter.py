# Defensive Router Object

# imports
from systemVariables import Router

# Advanced Router Object
class AdvancedRouter(Router):
    def __init__(self, name, tolerance=0):
        # define suspicion tolerance of link cost (default is 0)
        self.tolerance = tolerance
        super().__init__(name)
    def __repr__(self):
        return f"Advanced Router({self.name})"
    
    # receive location of end device in network to propagate own lookup table
    def receiveUpdate(self, otherNode, otherLookupTable):
        updated = False

        linkCost = self.getLinkCost(otherNode)

        for dest, (path, _, otherCost) in otherLookupTable.items():
            # loop prevention (very important)
            if self in path:
                continue

            # DEFENSE AGAINST BLACK HOLE
            # reject links with suspiciously low routes based on tolerance
            if otherCost <= self.tolerance and dest != otherNode.getIP():
                continue

            newPath = [self] + path
            newCost = otherCost + linkCost
            # determine if location is new or if new route is more efficient
            if dest not in self.lookupTable or newCost < self.lookupTable[dest][2]:
                self.lookupTable[dest] = (newPath, otherNode, newCost)
                updated = True
        
        if updated:
            self.sendUpdate()