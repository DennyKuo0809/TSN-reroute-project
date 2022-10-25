from collections import defaultdict
from copy import copy
from platform import node
import sys
import copy
from typing import List
import pickle
from argparse import ArgumentParser, Namespace


total_cycle_length = 0

class Graph:
    def __init__(self, vertices):
        #No. of vertices
        self.vertex_num= vertices
         
        # default dictionary to store graph (Adjacency list)
        self.Adj = defaultdict(list)
        self.edgeList = []
        self.utilMap = [[0]*vertices for i in range(vertices)]
    
    def addEdge(self, u, v, util):
        self.Adj[u].append(v)
        self.edgeList.append([u, v])
        self.utilMap[u][v] = util
        
    def modifyEdge(self, u, v, delta):
        self.utilMap[u][v] += delta
    
def subGraph(G: Graph, nodeList: List):
    g = Graph(G.vertex_num)
    g.utilMap = copy.deepcopy(G.utilMap)

    for u in nodeList:
        for v in nodeList:
            if u != v and G.utilMap[u][v] > 0:
                g.addEdge(u, v, G.utilMap[u][v])
    return g

#=======================================#
#   Below are for tarjan scc finding    #
#=======================================#
class SCC():
    def __init__(self, G):
        self.graph = G
        
        self.Time = 0
        self.low_val = [-1] * G.vertex_num
        self.discover_time = [-1] * G.vertex_num
        self.stack = []
        
        # output
        self.SCCs = []

        self.tarjan()
        
    def dfs(self, node):
        self.low_val[node] = node
        self.discover_time[node] = self.Time
        self.Time += 1
        self.stack.append(node)
        
        for neighbor in self.graph.Adj[node]:
            if self.discover_time[neighbor] < 0:
                self.dfs(neighbor)
                self.low_val[node] = min(self.low_val[node], self.low_val[neighbor])
            elif neighbor in self.stack: # neighbor is the ancestor of node
                self.low_val[node] = min(self.low_val[node], self.discover_time[neighbor])
        
        if self.low_val[node] == self.discover_time[node]: # Found SCC which contains {node}
            scc = []
            v = -1
            while v != node:
                v = self.stack.pop()
                scc.append(v)
            self.SCCs.append(sorted(scc))
        
    def tarjan(self):
        for node in list(self.graph.Adj.keys()):
            if self.discover_time[node] < 0:
                self.dfs(node)
    
    # def tarjan(self):
    #     for node in range(self.graph.vertex_num):
    #         if self.discover_time[node] < 0:
    #             self.dfs(node)
            
#===================================#
#   Below are for circuit finding   #
#===================================#
class Johnson():
    def __init__(self, G: Graph, constant: float, reserve: float):
        self.ori_graph = G
        self.graph = G
        self.reduceConstant = constant
        self.reservation = reserve
        
        
        self.S = 0
        self.V = G.vertex_num
        self.stack = []
        self.blocked = [False] * self.graph.vertex_num
        self.B = [[] for i in range(self.graph.vertex_num)]
        self.count = 0
        self.allCircuits = []
        self.included = [False] * self.graph.vertex_num

        self.FOUND = False

        self.circuitFinding()
        
    def output(self):
        global total_cycle_length
        # print("[Circuit No.{}]".format(self.count))
        # print("circuit length : {}".format(len(self.stack)))
        self.count += 1
        self.allCircuits.append(copy.deepcopy(self.stack))
        self.allCircuits[-1].append(self.stack[0])

        circuitLen = len(self.stack)
        total_cycle_length += circuitLen
        for i in range(circuitLen):
            print("{} -->".format(self.stack[i]), end="")
            self.included[self.stack[i]] = True
            self.graph.utilMap[self.stack[i]][self.stack[(i+1)%circuitLen]] -= self.reduceConstant
        print(self.stack[0])

    def unblock(self, u):
        self.blocked[u] = False
        while len(self.B[u]) > 0:
            w = self.B[u].pop()
            if self.blocked[w]:
                self.unblock(w)
        return 
        
    def circuit(self, v):
        # print(" circuit : ",c v, self.blocked, self.stack)
        f = False
        self.stack.append(v)
        self.blocked[v] = True

        for w in self.graph.Adj[v]:
            if self.FOUND:
                return True
            if self.graph.utilMap[v][w] > self.reservation:
                if w == self.S:
                    if self.stack + [self.stack[0]] not in self.allCircuits:
                        self.output()
                        self.FOUND = True
                    f = True
                elif not self.blocked[w]:
                    if self.circuit(w):
                        f = True
        
        if f:
            self.unblock(v)
        else:
            for w in self.graph.Adj[v]:
                if v not in self.B[w]:
                    self.B[w].append(v)
        
        self.stack.pop()
        return f

    def Normalcircuit(self, v):
        f = False
        self.stack.append(v)
        self.blocked[v] = True

        for w in self.graph.Adj[v]:
            if self.graph.utilMap[v][w] > 0:
                if w == self.S:
                    self.output()
                    f = True
                elif not self.blocked[w]:
                    if self.Normalcircuit(w):
                        f = True
        
        if f:
            self.unblock(v)
        else:
            for w in self.graph.Adj[v]:
                if v not in self.B[w]:
                    self.B[w].append(v)
        
        self.stack.pop()
        return f


    def circuitFinding(self):
        self.S = 0

        nodeList = [node for node in range(self.graph.vertex_num)]
        
        while self.S < self.V :
            self.graph = subGraph(self.ori_graph, nodeList)
            sccs = SCC(self.graph).SCCs
            # print(f"sccs : {sccs}")

            if len(sccs) > 0:
                self.S = min(sccs[0])

                if self.reduceConstant == 0:
                    self.stack = []
                    for i in range(self.S, self.V):
                        self.blocked[i] = False
                        self.B[i] = []
                    dummy = self.Normalcircuit(self.S)
                else:
                    self.FOUND = True
                    while self.FOUND:
                        self.FOUND = False
                        self.stack = []
                        for i in range(self.S, self.V):
                            self.blocked[i] = False
                            self.B[i] = []
                        dummy = self.circuit(self.S)
                self.S += 1
                nodeList = nodeList[self.S:]
            else:
                self.S = self.V
    
    
def parseGraph(inputFile: str, routeFile: str):
    g = None
    with open(inputFile, "r") as input_file:
        num_vertex = int(input_file.readline().strip())
        g = Graph(num_vertex)

        for i in range(num_vertex):
            start_vertex, neighbor_util = input_file.readline().strip().split(",")
            neighbor_util = neighbor_util.split(" ")
            j = 0
            for end_vertex, util in zip(neighbor_util[0::2], neighbor_util[1::2]):
                g.addEdge(int(start_vertex), int(end_vertex), int(util))
    ### Load type1 route
    with open(routeFile, "rb") as route_file:
        type1_route = pickle.load(route_file)
        for r in type1_route:
            for i in range(len(r[0]) - 1):
                g.modifyEdge(r[0][i], r[0][i+1], -r[1])
    return g
    
def cycleSelection(vertex_num: int, cycles: List[List[int]]):
    result = cycles[0]
    unCover = set([v for v in range(vertex_num) if v not in result])
    selected = set([0])

    while unCover and len(list(selected)) < vertex_num:
        print(unCover)
        coverMost_idx = -1
        coverMost_num = -1
        for i, c in enumerate(cycles):
            if i == 0 or i in selected:
                continue
            num_cover = len(list(unCover & set(c)))
            print(f"{unCover} & {c} num : {num_cover}")
            if num_cover >= coverMost_num:
                coverMost_idx = i
                coverMost_num = num_cover
        if coverMost_num <= 0:
            break
        common_node = list(set(cycles[coverMost_idx]) & set(result))[1]
        unCover = unCover - set(cycles[coverMost_idx])
        selected.update([coverMost_idx])
        # print(common_node)
        print(result, "\n", cycles[coverMost_idx])
        print(f"{result[:result.index(common_node)]} {cycles[coverMost_idx][cycles[coverMost_idx].index(common_node):]} {cycles[coverMost_idx][1:cycles[coverMost_idx].index(common_node)]} {result[result.index(common_node) : ]}")
        
        result_ = result[:-1]
        select_cycle = cycles[coverMost_idx][:-1]
        result = result_[:result_.index(common_node) + 1] + \
            select_cycle[select_cycle.index(common_node)+1:] + \
                select_cycle[1:select_cycle.index(common_node)] + \
                    result_[result_.index(common_node) : ] + [result[0]]
        # print(result)
    return result



def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument(
        "--scenario",
        type=str,
        help="Path to input data."
    )
    parser.add_argument(
        "--trim",
        type=float,
        help="When ther any new-found cycle, take this constant away from the capacity of all edges in the cycle.\n \
                Default: 0.0, which means the cycle finding alrorithm will return all cycles in the graph.",
        default=0.0
    )
    parser.add_argument(
        "--reserve",
        type=float,
        help="Reserve partial of capacity for all edge to avoid run out of bandwidth of network.",
        default=0.0
    )
    parser.add_argument(
        "--type1_route",
        type=str,
        help="Path to the pickle file which stores the route of type1 streams"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Path to the pickle file which stores the result of johnson algorithm.",
        default="type2_route.pickle"
    )
    args = parser.parse_args()
    return args

def main(args):
    g = parseGraph(args.scenario, args.type1_route)
    j = Johnson(g, args.trim, args.reserve)
    cycles = sorted(j.allCircuits, key=lambda c: len(c), reverse=True)
    route = cycleSelection(g.vertex_num, cycles)
    with open(args.output, "wb") as f:
        pickle.dump(route, f)
    print(route)

if __name__ == "__main__":
    args = parse_args()
    main(args)
