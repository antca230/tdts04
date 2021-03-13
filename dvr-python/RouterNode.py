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
               # distanceTable = self.minC[self.route[node]] + self.distanceTable[self.route[node]][node]
                #print(str(node) + " " + str(cost))
                # if self.route[node] != self.sim.INFINITY and self.minC[node] != distanceTable:
                #     print("kommer vi någonsin in i den här koden?")
                #     # I know a hop for route to i, but old cost info does not align with new info, update
                #     self.minC[node] = distanceTable
                
                if node == self.myID:
                    self.route[node] = self.myID 
                    continue 
               
                for j in range(len(self.costs)):
                    if self.distanceTable[self.myID][j] > self.distanceTable[self.myID][node] + self.distanceTable[node][j]:
                       #print(str(self.distanceTable[self.myID][j]) + " " + str(self.distanceTable[self.myID][node]) + " "+ str(self.distanceTable[node][j]))
                        self.distanceTable[self.myID][j] = self.distanceTable[self.myID][node] + self.distanceTable[node][j]
                            
                        self.minC[j] = self.distanceTable[self.myID][node] + self.distanceTable[node][j] # sätter värde till minCost
                        if(self.route[node] != self.myID):
                            self.route[j] = self.route[node]
                        else:    
                            self.route[j] = node
                        print ("my id is = " + str(self.myID))
                        print("update" + str(self.minC[j]) +"\t"+ str(self.route[j])+"\n")
                        
                                                       
                        for k in range(len(self.costs)):
                            if k != self.myID:
                                #print (str(self.myID) + " = " + str(k))
                                self.sendUpdate(RouterPacket.RouterPacket(self.myID,k,self.distanceTable[self.myID]))

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

#-------------------------------------------SOOOOOOOLCOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOODE


#!/usr/bin/env python
# import GuiTextArea, RouterPacket, F
# from copy import deepcopy

# class RouterNode():
#     myID = None
#     myGUI = None
#     sim = None
#     costs = None

#     formatter = F.F()
#     neighCosts = None   # The neighbours' costs
#     minCosts = None     # The minimum cost to reach node i is minCosts[i].
#     nextHops = None     # The next hop to reach node i is nextHops[i].
#     poisonReverse = None
#     ######

#     # --------------------------------------------------
#     def __init__(self, ID, sim, costs):
#         self.myID = ID
#         self.sim = sim
#         self.neighCosts = [ [0]*sim.NUM_NODES for i in range(self.sim.NUM_NODES) ]
#         self.minCosts = [0]*self.sim.NUM_NODES
#         self.nextHops = [0]*self.sim.NUM_NODES

#         self.myGUI = GuiTextArea.GuiTextArea("  Output window for Router #" + str(ID) + "  ")

#         self.costs = deepcopy(costs)

#         #ADDED SOLUTION
#         formatter = F.F()
#         self.poisonReverse = self.sim.POISONREVERSE
#         self.initRouteTable(self.costs)
#         self.propagate()

#     def initRouteTable(self, costs):
#         for i in range (self.sim.NUM_NODES):
#             # In the beginning, my neighbours have infinite cost to each other router.
#             # This will change when I get updates from my neghbour routers.
#             # Any router have 0 cost to itself.
#             for j in range (self.sim.NUM_NODES):
#                 self.neighCosts[i][j] = self.sim.INFINITY if i != j else 0

#             # If I have a cost to a node that is not INFINITY, then it is a neighbour and
#             # I will set my next hop to it directly until I find a route with less cost.
#             # If not a neighbour, set to infinity until a hop is known.
#             self.nextHops[i] = i if costs[i] < self.sim.INFINITY else self.sim.INFINITY

#         # the direct cost is the cheapest we know so far
#         self.minCosts = deepcopy(costs)

#     # --------------------------------------------------
#     def recvUpdate(self, pkt):
#         self.myGUI.println("Got an update from " + str(pkt.sourceid) + " with the cost to me set to: " + str(self.neighCosts[pkt.sourceid][self.myID]))
#         self.myGUI.println("Mincosts in packet are: " + str(pkt.mincost))

#         changed_table = False

#         # If changed_table sets to true when i is 1 but then to false when i is 2, do we have a bug?
#         # ans: changed_table could be overwritten for every iteration. it should no longer be the case.
#         for i in range (self.sim.NUM_NODES):
#             if self.neighCosts[pkt.sourceid][i] != pkt.mincost[i]:
#                 # got new information from source
#                 changed_table = True
#                 self.neighCosts[pkt.sourceid][i] = pkt.mincost[i]
#                 self.myGUI.println("We have updated our minCosts: " + str(self.minCosts))

#         if changed_table:
#             for i in range (self.sim.NUM_NODES):
#                 if i == self.myID:
#                     continue # we always have 0 cost to ourself, skip

#                 # determine cost to i via neighbour using new info
#                 neighCost = self.minCosts[self.nextHops[i]] + self.neighCosts[self.nextHops[i]][i]

#                 if self.nextHops[i] != self.sim.INFINITY and self.minCosts[i] != neighCost:
#                     # I know a hop for route to i, but old cost info does not align with new info, update
#                     self.minCosts[i] = neighCost

#                 # is the direct path to i shorter than our current min?
#                 if self.costs[i] < self.minCosts[i]:
#                     self.minCosts[i] = self.costs[i]
#                     self.nextHops[i] = i

#                 # check if we have new cheaper path for each node
#                 for j in range (self.sim.NUM_NODES):
#                     if self.minCosts[i] + self.neighCosts[i][j] < self.minCosts[j]:
#                         # found a cheaper path to j
#                         self.minCosts[j] = self.minCosts[i] + self.neighCosts[i][j]
#                         self.nextHops[j] = self.nextHops[i]

#             self.propagate()


#     def propagate(self):
#         pCosts = [0]*self.sim.NUM_NODES
#         pCosts = deepcopy(self.minCosts)

#         for i in range (self.sim.NUM_NODES):
#             if self.costs[i] != 0 and self.costs[i] != self.sim.INFINITY:
#                 # i is a direct neighbour
#                 if self.poisonReverse:
#                     for j in range (self.sim.NUM_NODES):
#                         # if I am using i to get to j, tell i that my cost to j is infinity
#                         # also, no need to poison if i == j
#                         pCosts[j] = self.sim.INFINITY if (self.nextHops[j] == i and i != j) else self.minCosts[j]

#                 self.sendUpdate(RouterPacket.RouterPacket(self.myID, i, pCosts))


#     # --------------------------------------------------
#     def sendUpdate(self, pkt):
#         self.sim.toLayer2(pkt)

#     # --------------------------------------------------
#     def printDistanceTable(self):
#         self.myGUI.println("Current table for " + str(self.myID) +
#                            "  at time " + str(self.sim.getClocktime()))
#         self.myGUI.println("")

#         self.myGUI.println("DistanceTable:")
#         line = "    dst |"
#         for i in range(self.sim.NUM_NODES):
#             line += self.formatter.format(str(i), 5)
#         self.myGUI.println(line)

#         dashStr = "-" * (9+5*self.sim.NUM_NODES)
#         self.myGUI.println(dashStr)

#         for i in range(self.sim.NUM_NODES):
#             if self.costs[i] != 0 and self.costs[i] != self.sim.INFINITY:
#                 line = " nbr" + self.formatter.format(i, 3) + " |"
#                 for j in range(self.sim.NUM_NODES):
#                     line += self.formatter.format(self.neighCosts[i][j], 5);
#                 self.myGUI.println(line)

#         self.myGUI.println("")
#         self.myGUI.println("Our distance vector and routes:")
#         line = "    dst |"
#         for i in range(self.sim.NUM_NODES):
#             line += self.formatter.format(i, 5)
#         self.myGUI.println(line)

#         self.myGUI.println(dashStr)

#         line = " cost   |"
#         for i in range(self.sim.NUM_NODES):
#             line += self.formatter.format(self.minCosts[i], 5)
#         self.myGUI.println(line)

#         line = " route  |"
#         for i in range(self.sim.NUM_NODES):
#             if self.minCosts[i] == self.sim.INFINITY:
#                 line += self.formatter.format("-", 5)
#             else:
#                 line += self.formatter.format(self.nextHops[i], 5)
#         self.myGUI.println(line)


#     # --------------------------------------------------
#     def updateLinkCost(self, dest, newcost):
#         self.myGUI.println("Got an updated link cost to " + str(dest) + "(" + str(newcost) + ")")
#         self.myGUI.println("My minCosts before: " + str(self.minCosts))

#         # Update link costs for every route that has next hop set to dest.
#         for i in range (self.sim.NUM_NODES):
#             if self.nextHops[i] == dest:
#                 self.minCosts[i] += (newcost - self.costs[dest])

#         self.myGUI.println("My minCosts after: " + str(self.minCosts))
#         self.costs[dest] = newcost

#         # Check if we have another route that is less costly.
#         for i in range (self.sim.NUM_NODES):
#             for j in range (self.sim.NUM_NODES):
#                 # Check the cost on neighbour j for destination dest
#                 if self.neighCosts[j][i] + self.costs[j] < newcost and i != self.myID:
#                     # We have a new lowest cost route
#                     self.minCosts[i] = self.neighCosts[j][i] + self.costs[j]
#                     self.nextHops[i] = j
#                     self.myGUI.println("Setting cost to " + str(i) + " to " + str(self.minCosts[i]) + " with next hop set to " + str(self.nextHops[i]))

#         self.myGUI.println("My minCosts after recalc: " + str(self.minCosts))
#         self.propagate()

