import sys
sys.path.append(".")
from Graph import MyGraph
from Checker import Checker

graphName = sys.argv[1]
n_star = int(1e9) if len(sys.argv)<3 else int(sys.argv[2])
cent_method = 'PageRank' if len(sys.argv)<4 else sys.argv[3]
GRAPH = MyGraph(graphName)
GRAPH.getSubgraph(n_star, cent_method)

best, bestpos, bestdrop, bestpos2 = int(1e9), {}, set(), {}
for i in range(30) :
    GRAPH.getPos()
    drop = set(Checker.getOverlaps(GRAPH.G2, GRAPH.POS))
    if len(drop)<best :
        best = len(drop)
        bestpos = GRAPH.POS.copy()
        bestpos2 = GRAPH.POS2.copy()
        bestdrop = drop.copy()
GRAPH.POS = bestpos
GRAPH.POS2 = bestpos2
GRAPH.adjust(bestdrop)
GRAPH.draw()