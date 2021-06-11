import sys
sys.path.append(".")
from Graph import MyGraph

graphName = sys.argv[1]
n_star = int(1e9) if len(sys.argv)<3 else int(sys.argv[2])
cent_method = 'PageRank' if len(sys.argv)<4 else sys.argv[3]
GRAPH = MyGraph(graphName)
GRAPH.getSubgraph(n_star, cent_method)
GRAPH.getPos()
GRAPH.draw()