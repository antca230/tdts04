#!/usr/bin/env python
import GuiTextArea, RouterPacket, F
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
        
        if self.distanceTable[pkt.sourceid] != pkt.mincost: 
            self.distanceTable[pkt.sourceid] = pkt.mincost
        #    print("source: "+str(pkt.sourceid) +"  myID: " +  str(self.myID)+ "  mincost: "+ str(pkt.mincost))
          

            #---sudo code
            for node, cost in enumerate(self.distanceTable):
#                print(str(self.minC[self.route[node]]) +" "+str(self.distanceTable[self.route[node]][node]) )
                distanceTable = self.minC[self.route[node]] + self.distanceTable[self.route[node]][node]
                #print(str(node) + " " + str(cost))
                # if self.route[node] != self.sim.INFINITY and self.minC[node] != distanceTable:
                #     print("kommer vi någonsin in i den här koden?")
                #     # I know a hop for route to i, but old cost info does not align with new info, update
                #     self.minC[node] = distanceTable
                if node == self.myID:
                    continue
                for j in range(len(self.costs)):
                    if self.distanceTable[self.myID][j] > self.distanceTable[self.myID][node] + self.distanceTable[node][j]:
                       # print(str(self.distanceTable[self.myID][j]) + " " + str(self.distanceTable[self.myID][node]) + " "+ str(self.distanceTable[node][j]))
                        self.distanceTable[self.myID][j] = self.distanceTable[self.myID][node] + self.distanceTable[node][j]
                        self.minC[self.myID] = self.distanceTable[self.myID][j]
                        self.route[j] = node
                        for k in range(len(self.costs)):
                            if k != self.myID:
                                self.sendUpdate(RouterPacket.RouterPacket(self.myID,k,self.distanceTable[self.myID]))
                    else :
                       self.route[j] = self.myID 
        
        


        
    # --------------------------------------------------
    def sendUpdate(self, pkt):
        self.sim.toLayer2(pkt)


    # --------------------------------------------------
    def printDistanceTable(self):
        self.myGUI.println("\nCurrent table for " + str(self.myID) +
                           "  at time " + str(self.sim.getClocktime())+"\n")
        dstrow = "   dst |\t"
        lines = "------------"
        space = "\t"

        self.myGUI.println("DistanceTable:")
        self.myGUI.print(dstrow)
        for i in range(self.sim.NUM_NODES):
            self.myGUI.print(space + str(i))
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
            self.myGUI.print("\t" + str(self.minC[i])) 
        self.myGUI.println("")
        
        self.myGUI.print(" route | \t")
        for i in range(self.sim.NUM_NODES):
           # if 
                self.myGUI.print("\t" + str(self.route[i])) 

    # --------------------------------------------------
    def updateLinkCost(self, dest, newcost):
       pass 

    def Bellman():
        pass
