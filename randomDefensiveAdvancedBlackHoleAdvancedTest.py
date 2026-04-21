# This is random traffic test of black hole advanced vs advanced defense.
import random

from BlackHoleRouter import AdvancedBlackHoleRouter
from defensiveRouter import AdvancedRouter
from systemVariables import Router, EndDevice, Link

TRIALS = 100
PACKETS_PER_TRIAL = 20
STEPS_PER_TRIAL = 100
SEED = 1155
LINK_COST = 2
ADV_TOLERANCE = 1


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


rng = random.Random(SEED)
capturedCount = 0
deliveredCount = 0

for trial in range(TRIALS):
    devices = []
    router1 = AdvancedRouter("1", 1)
    devices.append(router1)
    router2 = AdvancedRouter("2", 1)
    devices.append(router2)
    router3 = AdvancedRouter("3", 1)
    devices.append(router3)
    router4 = AdvancedRouter("4", 1)
    devices.append(router4)
    router5 = AdvancedRouter("5", 1)
    devices.append(router5)
    router6 = AdvancedRouter("6", 1)
    devices.append(router6)
    router7 = AdvancedRouter("7", 1)
    devices.append(router7)
    router8 = AdvancedRouter("8", 1)
    devices.append(router8)
    router9 = AdvancedRouter("9", 1)
    devices.append(router9)
    router10 = AdvancedRouter("10", 1)
    devices.append(router10)
    router11 = AdvancedRouter("11", 1)
    devices.append(router11)

    homeComputerA = EndDevice("Home Computer A")
    devices.append(homeComputerA)
    homeComputerB = EndDevice("Home Computer B")
    devices.append(homeComputerB)
    homeComputerC = EndDevice("Home Computer C")
    devices.append(homeComputerC)

    server1 = EndDevice("Server 1")
    devices.append(server1)
    server2 = EndDevice("Server 2")
    devices.append(server2)
    server3 = EndDevice("Server 3")
    devices.append(server3)
    server4 = EndDevice("Server 4")
    devices.append(server4)

    Link(router1, router2, LINK_COST)
    Link(router2, router3, LINK_COST)
    Link(router3, router7, LINK_COST)
    Link(router7, router5, LINK_COST)
    Link(router5, router4, LINK_COST)
    Link(router4, router1, LINK_COST)
    Link(router1, router6, LINK_COST)
    Link(router2, router8, LINK_COST)
    Link(router8, router9, LINK_COST)
    Link(router9, router10, LINK_COST)
    Link(router9, router11, LINK_COST)
    Link(router8, router11, LINK_COST)

    Link(homeComputerA, router1, LINK_COST)
    Link(homeComputerB, router1, LINK_COST)
    Link(homeComputerC, router11, LINK_COST)
    Link(server1, router6, LINK_COST)
    Link(server2, router7, LINK_COST)
    Link(server3, router5, LINK_COST)
    Link(server4, router10, LINK_COST)

    blackHole = AdvancedBlackHoleRouter("Black Hole", 1)
    devices.append(blackHole)
    attackPoints = [router2, router3, router8, router9]
    Link(blackHole, rng.choice(attackPoints), LINK_COST)

    for node in devices:
        node.sendUpdate()

    sources = [homeComputerA, homeComputerB, homeComputerC]
    destinations = [server1, server2, server3, server4]

    for i in range(PACKETS_PER_TRIAL):
        src = rng.choice(sources)
        dst = rng.choice(destinations)
        src.createPacket(dst.getIP(), f"Trial {trial} Packet {i}")

    for i in range(STEPS_PER_TRIAL):
        for node in devices:
            before = len(blackHole.packets) if node is blackHole else 0
            try:
                info = node.forward()
            except KeyError:
                info = None
            if node is blackHole and len(blackHole.packets) < before:
                capturedCount += 1
            if info is not None:
                deliveredCount += 1

        movePackets(devices)

sentCount = TRIALS * PACKETS_PER_TRIAL
resolvedCount = capturedCount + deliveredCount
droppedCount = sentCount - resolvedCount
captureSentRate = 0.0 if sentCount == 0 else (100.0 * capturedCount / sentCount)
deliverySentRate = 0.0 if sentCount == 0 else (100.0 * deliveredCount / sentCount)
droppedSentRate = 0.0 if sentCount == 0 else (100.0 * droppedCount / sentCount)

print("Random Defensive Test: advanced defense vs advanced black hole")
print(f"Trials: {TRIALS}")
print(f"Packets per Trial: {PACKETS_PER_TRIAL}")
print(f"Total Sent: {sentCount}")
print(f"Captured: {capturedCount} ({captureSentRate:.2f}% of sent)")
print(f"Delivered: {deliveredCount} ({deliverySentRate:.2f}% of sent)")
print(f"Dropped: {droppedCount} ({droppedSentRate:.2f}% of sent)")
