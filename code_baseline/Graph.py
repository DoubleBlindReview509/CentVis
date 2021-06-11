import collections
import heapq
import networkx as nx
import math
from os import system

class MyGraph :
    def __init__(self, na) :
        self.NAME = na
        fileName = "../data/" + na + ".txt"
        self.G = nx.read_edgelist(fileName, nodetype=int)
        self.CentFuncDict = {}
        self.CentFuncDict["Degree"] = nx.degree_centrality
        self.CentFuncDict["Betweenness"] = nx.betweenness_centrality
        self.CentFuncDict["Closeness"] = nx.closeness_centrality
        self.CentFuncDict["Eigenvector"] = nx.eigenvector_centrality
        self.CentFuncDict["Katz"] = nx.katz_centrality
        self.CentFuncDict["Information"] = nx.information_centrality
        self.CentFuncDict["Harmonic"] = nx.harmonic_centrality
        self.CentFuncDict["Subgraph"] = nx.subgraph_centrality
        self.CentFuncDict["PageRank"] = nx.pagerank
        self.CentFuncDict["SecondOrder"] = nx.second_order_centrality
    
    def getSubgraph(self, n_star, centName) :
        C = self.CentFuncDict[centName](self.G)
        NC = [(-C[u], u) for u in self.G.nodes]
        NC.sort()
        S = [x[1] for x in NC[:n_star]]
        others = [x[1] for x in NC[n_star:]]
        L = dict(nx.shortest_path_length(self.G))
        S_add = []
        for u in others :
            flag = False
            for v0 in S :
                if flag : break
                for v1 in S :
                    if flag : break
                    if L[u].get(v0)==None or L[u].get(v1)==None or L[v0].get(v1)==None : continue
                    if L[u][v0]+L[u][v1]==L[v0][v1] :
                        flag = True
                        break
            if flag : S_add.append(u)
        S = S + S_add
        self.G2 = nx.subgraph(self.G, S)
        self.NodeList = S
        self.RANK = [0.0]
        for i in range(1, len(S)) :
            if abs(C[S[i]]-C[S[i-1]])<1e-9 :
                self.RANK.append(self.RANK[-1])
            else :
                self.RANK.append(self.RANK[-1]+1)
        if max(self.RANK)>0 :
            self.RANK = [x/max(self.RANK) for x in self.RANK]

    def getPos(self) :
        pos = nx.spring_layout(self.G2)
        LEN = int(2.0 * math.sqrt(len(self.G2.nodes)) + 0.5)
        self.MAXN = LEN * 2 + 1
        self.POS = {}

        for u in self.NodeList :
            [x0,y0] = pos[u]
            self.POS[u] = ((x0+1)*LEN, (y0+1)*LEN)

    def draw(self) :
        f = open("../log/GraphInformation.txt", "w")
        f.write(str(len(self.G2.nodes))+'\n')
        f.write(str(len(self.G2.edges))+'\n')
        f.close()
        f = open("../log/NodeLabels.txt", "w")
        for u in self.NodeList :
            f.write(str(u)+'\n')
        f.close()
        f = open("../log/NodePos.txt", "w")
        for u in self.NodeList :
            f.write(str(self.POS[u][0])+'\n')
            f.write(str(self.POS[u][1])+'\n')
        f.close()
        f = open("../log/NodeRank.txt", "w")
        for x in self.RANK :
            f.write(str(x)+'\n')
        f.close()
        f = open("../log/Edges.txt", "w")
        for u,v in self.G2.edges :
            f.write(str(self.POS[u][0])+'\n')
            f.write(str(self.POS[u][1])+'\n')
            f.write(str(self.POS[v][0])+'\n')
            f.write(str(self.POS[v][1])+'\n')
        f.close()
        system("mpost -numbersystem=binary DrawGraph.mp")
        runcmd = "mv DrawGraph-1.eps ../pictures_baseline/" + self.NAME + ".eps"
        system(runcmd)
        system("rm DrawGraph.log")


