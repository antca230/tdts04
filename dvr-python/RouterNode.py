#!/usr/bin/env python
import GuiTextArea, RouterPacket, F
from copy import deepcopy

class RouterNode():
    myID = None
    myGUI = None
    sim = None
    costs = None
    distanceTable = []
    # Access simulator variables with:
    # self.sim.POISONREVERSE, self.sim.NUM_NODES, etc.

    # --------------------------------------------------
    def __init__(self, ID, sim, costs):
        self.myID = ID
        self.sim = sim
        self.myGUI = GuiTextArea.GuiTextArea("  Output window for Router #" + str(ID) + "  ")

        self.distanceTable = [[0 for i in range(self.sim.NUM_NODES)] for j in range(self.sim.NUM_NODES)]

        self.costs = deepcopy(costs)
        for i in range (len(self.costs)) : 
            for j in range (len(self.costs)) : 
                if i == j : 
                    self.distanceTable[i][j] = 0
                elif i == self.myID :    
                    self.distanceTable[self.myID][j] = self.costs[j]  
                else :
                    self.distanceTable[i][j] = self.sim.INFINITY  

           
        
#        print(str(self.distanceTable))

        for node, cost in enumerate(costs):
            if cost != self.sim.INFINITY and node != self.myID:
                self.sendUpdate(RouterPacket.RouterPacket(self.myID, node, costs)) 

    

    # --------------------------------------------------
    def recvUpdate(self, pkt):
        #self.distanceTable[pkt.sourceid] = pkt.mincost
        pass


    # --------------------------------------------------
    def sendUpdate(self, pkt):

        self.sim.toLayer2(pkt)


    # --------------------------------------------------
    def printDistanceTable(self):
        self.myGUI.println("\nCurrent table for " + str(self.myID) +
                           "  at time " + str(self.sim.getClocktime())+"\n")
        
        self.myGUI.println("DistanceTable:")
        for i in range (len(self.costs)):
            if self.costs[i] != self.sim.INFINITY:        #THIS CODE IS TO SEE THAT WE CAN PRINT LINES ACCORDING TO THE TOTAL CONNECTIONS
                self.myGUI.print("\n nbr  "+ str(i) + "| \t") 
                for j in range (len(self.costs)): 
                    self.myGUI.print("\t" + str(self.distanceTable[i][j]))
                    
        
        self.myGUI.print("\n Our distance vector and routes:\n \tdst |")
        for i in range (len(self.costs)):
            self.myGUI.print("\t" + str(i))
                

    # --------------------------------------------------
    def updateLinkCost(self, dest, newcost):

        pass 
    def Bellman():
        pass
