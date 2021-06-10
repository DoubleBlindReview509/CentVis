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
        S = set()
        self.POS = {}
        self.POS2 = {}

        def find(x, y) :
            dxy = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            Q = collections.deque()
            SS = set()
            SS.add((x,y))
            Q.append((x,y))
            while Q :
                x0,y0 = Q.popleft()
                for dx,dy in dxy :
                    x1,y1 = x0+dx,y0+dy
                    if 0<=x1<self.MAXN and 0<=y1<self.MAXN :
                        if (x1,y1) not in S :
                            return x1,y1
                        if (x1,y1) not in SS :
                            SS.add((x1,y1))
                            Q.append((x1,y1))
            return -1,-1

        for u in self.NodeList :
            [x0,y0] = pos[u]
            self.POS2[u] = ((x0+1)*LEN, (y0+1)*LEN)
            x,y = int((x0+1)*LEN+0.5), int((y0+1)*LEN+0.5)
            if (x,y) in S :
                x,y = find(x,y)
            S.add((x,y))
            self.POS[u] = (x,y)

    def findRoute(self, st, ed) :
        self.dxy = [(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1)]
        cost = []
        cost.append([0,50,100,10000,10000,10000,100,50])
        cost.append([50,0,50,100,10000,10000,10000,100])
        cost.append([100,50,0,50,100,10000,10000,10000])
        cost.append([10000,100,50,0,50,100,10000,10000])
        cost.append([10000,10000,100,50,0,50,100,10000])
        cost.append([10000,10000,10000,100,50,0,50,100])
        cost.append([100,10000,10000,10000,100,50,0,50])
        cost.append([50,100,10000,10000,10000,100,50,0])
        N = 2*self.MAXN
        dist = [[[int(1e9) for _ in range(8)] for i in range(N)] for j in range(N)]
        predir = [[[int(0) for _ in range(8)] for i in range(N)] for j in range(N)]
        Q = []
        for i,(dx,dy) in enumerate(self.dxy) :
            x1,y1 = st[0]+dx,st[1]+dy
            if 0<=x1<N and 0<=y1<N and self.map[x1][y1] :
                dist[x1][y1][i] = 1
                heapq.heappush(Q, (1,x1,y1,i))
        self.map[ed[0]][ed[1]] = True
        finald = -1
        while Q :
            dd,x,y,d = heapq.heappop(Q)
            if dist[x][y][d]!=dd : 
                continue
            if x==ed[0] and y==ed[1] :
                finald = d
                break
            for i,(dx,dy) in enumerate(self.dxy) :
                x1,y1 = x+dx,y+dy
                if (0<=x1<N) and (0<=y1<N) and self.map[x1][y1] :
                    cst = dd+cost[d][i]+1
                    if cst<dist[x1][y1][i] :
                        dist[x1][y1][i] = cst
                        predir[x1][y1][i] = d
                        heapq.heappush(Q, (cst,x1,y1,i))
        self.map[ed[0]][ed[1]] = False
        if finald==-1 : return None
        ret = [(ed[0],ed[1])]
        cntx,cnty,cntd,predi = ed[0],ed[1],finald,-1
        while cntx!=st[0] or cnty!=st[1] :
            tmp = predir[cntx][cnty][cntd]
            cntx,cnty = cntx-self.dxy[cntd][0],cnty-self.dxy[cntd][1]
            if cntd==predi :
                ret[-1] = (cntx,cnty)
            else :
                ret.append((cntx,cnty))
                predi = cntd
            cntd = tmp
        return ret

    def adjust(self, drop) :
        self.restLink = []
        for u,v in self.G2.edges :
            if (u,v) not in drop :
                self.restLink.append((u, v))
        EC = nx.edge_betweenness_centrality(self.G)
        templ = list(EC.keys())
        for (u,v) in templ :
            EC[v,u] = EC[u,v]
        A = [(-EC[x], x) for x in drop]
        A.sort()
        self.map = [[True] * (2*self.MAXN) for i in range(2*self.MAXN)]
        for u in self.G2.nodes :
            self.map[self.POS[u][0]*2][self.POS[u][1]*2] = False
        self.drops = 0
        self.addLink = []
        for _,(u,v) in A :
            x0,y0 = self.POS[u][0]*2,self.POS[u][1]*2
            x1,y1 = self.POS[v][0]*2,self.POS[v][1]*2
            route = self.findRoute((x0,y0), (x1,y1))
            if route==None :
                self.drops += 1
            else :
                self.addLink.append(route)

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
        f.close()
        f = open("../log/NodePos2.txt", "w")
        for u in self.NodeList :
            f.write(str(self.POS2[u][0])+'\n')
            f.write(str(self.POS2[u][1])+'\n')
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
        f = open("../log/Edges2.txt", "w")
        for u,v in self.G2.edges :
            f.write(str(self.POS2[u][0])+'\n')
            f.write(str(self.POS2[u][1])+'\n')
            f.write(str(self.POS2[v][0])+'\n')
            f.write(str(self.POS2[v][1])+'\n')
        f.close()
        f = open("../log/StraightEdges.txt", "w")
        f.write(str(len(self.restLink))+'\n')
        for u,v in self.restLink :
            f.write(str(self.POS[u][0])+'\n')
            f.write(str(self.POS[u][1])+'\n')
            f.write(str(self.POS[v][0])+'\n')
            f.write(str(self.POS[v][1])+'\n')
        f.close()
        f = open("../log/PolyEdges.txt", "w")
        f.write(str(len(self.addLink))+'\n')
        for lst in self.addLink :
            f.write(str(len(lst))+'\n')
            for x,y in lst :
                f.write(str(x/2)+'\n')
                f.write(str(y/2)+'\n')
        f.close()
        system("mpost DrawGraph.mp")
        runcmd = "mv DrawGraph-1.eps ../pictures/" + self.NAME + ".eps"
        system(runcmd)
        system("rm DrawGraph.log")


