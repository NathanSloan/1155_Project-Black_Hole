# This is random traffic test of black hole normal vs no defense.
import random

from BlackHoleRouter import BlackHoleRouter
from systemVariables import Router, EndDevice, Link

TRIALS = 100
PACKETS_PER_TRIAL = 20
STEPS_PER_TRIAL = 100
SEED = 1155


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

    # define black hole router
    blackHole = BlackHoleRouter("Black Hole")
    devices.append(blackHole)

    # Randomize black hole attachment over hotspots.
    attackPoints = [router2, router3, router8, router9]
    Link(blackHole, rng.choice(attackPoints))

    # propagate lookup table data after network is finished
    for node in devices:
        node.sendUpdate()

    # create random packets at end devices
    sources = [homeComputerA, homeComputerB, homeComputerC]
    destinations = [server1, server2, server3, server4]

    for i in range(PACKETS_PER_TRIAL):
        src = rng.choice(sources)
        dst = rng.choice(destinations)
        src.createPacket(dst.getIP(), f"Trial {trial} Packet {i}")

    # propagate data through network
    for i in range(STEPS_PER_TRIAL):
        for node in devices:
            before = len(blackHole.packets) if node is blackHole else 0
            info = node.forward()
            if node is blackHole and len(blackHole.packets) < before:
                capturedCount += 1
            if info is not None:
                deliveredCount += 1

        movePackets(devices)

totalCount = capturedCount + deliveredCount
captureRate = 0.0 if totalCount == 0 else (100.0 * capturedCount / totalCount)
deliveryRate = 0.0 if totalCount == 0 else (100.0 * deliveredCount / totalCount)

print("Random Test: no defense vs black hole")
print(f"Trials: {TRIALS}")
print(f"Packets per Trial: {PACKETS_PER_TRIAL}")
print(f"Total Packets: {totalCount}")
print(f"Captured: {capturedCount} ({captureRate:.2f}%)")
print(f"Delivered: {deliveredCount} ({deliveryRate:.2f}%)")
