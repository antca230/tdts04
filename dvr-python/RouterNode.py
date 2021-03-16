#!/usr/bin/env python
import GuiTextArea, RouterPacket, F
from typing import NamedTuple
from copy import deepcopy

class RouterNode():
    myID = None
    myGUI = None
    sim = None
    costs = None
    minC = None
    distanceTable = None
    route = None
    # Access simulator variables with:
    # self.sim.POISONREVERSE, self.sim.NUM_NODES, etc.

    # --------------------------------------------------
    def __init__(self, ID, sim, costs):
        self.myID = ID
        self.sim = sim
        self.myGUI = GuiTextArea.GuiTextArea("  Output window for Router #" + str(ID) + "  ")

        self.distanceTable = [[0 for i in range(self.sim.NUM_NODES)] for j in range(self.sim.NUM_NODES)]
        self.route = [0 for i in range(self.sim.NUM_NODES)]
        self.minC = [0 for i in range(self.sim.NUM_NODES)]
        

        self.costs = deepcopy(costs)
        self.minC = deepcopy(costs)

        for i in range (len(self.costs)) : 
            for j in range (len(self.costs)) : 
                if i == j : 
                    self.distanceTable[i][j] = 0
                elif i == self.myID :    
                    self.distanceTable[self.myID][j] = self.costs[j]  
                else :
                    self.distanceTable[i][j] = self.sim.INFINITY  
            if costs[i] < self.sim.INFINITY: 
                self.route[i] = i 
            else :
                self.route[i] = self.sim.INFINITY
         
#        print(str(self.distanceTable[0][-2]))
        
#        print(str(self.distanceTable))

        for node, cost in enumerate(costs):
            if cost != self.sim.INFINITY and node != self.myID:
                self.sendUpdate(RouterPacket.RouterPacket(self.myID, node, costs)) 

    # --------------------------------------------------
    def recvUpdate(self, pkt):
        self.myGUI.println(f"\nReceived packet - Source: {pkt.sourceid} Data: {pkt.mincost}")
        if self.distanceTable[pkt.sourceid] == pkt.mincost:
            return

        # Update distance table with data from paket
        self.distanceTable[pkt.sourceid] = pkt.mincost

        # Run Bellman-Ford algorithm and if changes were made send update to neighbours
        if self.bellman():
            self.sendpacket(self.distanceTable[self.myID])

    def sendUpdate(self, pkt):
        self.sim.toLayer2(pkt)

    # --------------------------------------------------
    def printDistanceTable(self):
        self.myGUI.println("\nCurrent table for " + str(self.myID) +
                           "  at time " + str(self.sim.getClocktime())+"\n")
        dstrow = "   dst |\t"
        lines = "------------"

        self.myGUI.println("DistanceTable:")
        self.myGUI.print(dstrow)
        for i in range(self.sim.NUM_NODES):
            self.myGUI.print("\t" + str(i))
        self.myGUI.println("")
        for i in range(self.sim.NUM_NODES):
            self.myGUI.print(lines)


        for i in range (len(self.costs)):
            if self.costs[i] != self.sim.INFINITY and self.myID != i :        #THIS CODE IS TO SEE THAT WE CAN PRINT LINES ACCORDING TO THE TOTAL CONNECTIONS
                self.myGUI.print("\n nbr  "+ str(i) + "| \t")
                for j in range (len(self.costs)): 
                    self.myGUI.print("\t" + str(self.distanceTable[i][j]))
                    
        
        self.myGUI.print("\n\n Our distance vector and routes:\n   dst |\t")
        for i in range (len(self.costs)):
            self.myGUI.print("\t" + str(i))
        self.myGUI.println("")

        for i in range(self.sim.NUM_NODES):
            self.myGUI.print(lines)        
        self.myGUI.println("")

        self.myGUI.print(" cost  | \t")
        for i in range(self.sim.NUM_NODES):
            self.myGUI.print("\t" + str(self.distanceTable[self.myID][i])) 
        self.myGUI.println("")
        
        self.myGUI.print(" route | \t")
        for i in range(self.sim.NUM_NODES):
           # if 
                self.myGUI.print("\t" + str(self.route[i])) 

    # --------------------------------------------------
    def updateLinkCost(self, dest, newcost):
        self.costs[dest] = newcost
        
        if self.bellman():
            if self.sim.POISONREVERSE:
                poison = deepcopy(self.distanceTable[self.myID])
                poison[dest] = self.sim.INFINITY
                for neighbour in range(self.sim.NUM_NODES):
                    if neighbour != self.myID and neighbour != self.sim.INFINITY and neighbour != dest:
                        self.sendUpdate(RouterPacket.RouterPacket(self.myID, neighbour, poison))
            else:
                self.sendpacket(self.distanceTable[self.myID])
# ------------------------------------------------------
    def bellman(self):
        newValue = False
        for target in range(self.sim.NUM_NODES):
            if target != self.myID:
                routes = []
                for neighbour in range(self.sim.NUM_NODES):
                    if neighbour != self.myID:
                        # Calculate total distance from this node via neighbour node to target node
                        routes.append((self.costs[neighbour] + self.distanceTable[neighbour][target], neighbour))

                # Find best route
                bestRoute = min(routes, key = lambda r: r[0])
                # Update distance table and routing table
                if bestRoute[0] <= self.costs[target]:
                    self.distanceTable[self.myID][target] = bestRoute[0]
                    self.route[target] = bestRoute[1]
                    newValue = True
        return newValue

    def sendpacket(self, pkt):
        for target in range(len(self.costs)):
            if target != self.myID and target != self.sim.INFINITY:
                self.sendUpdate(RouterPacket.RouterPacket(self.myID,target, pkt)) 
