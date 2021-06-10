import networkx as nx
import math

class Checker :
    @classmethod
    def dis(cls, p1, p2) :
        ret = math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)
        return ret

    @classmethod
    def getbox(cls, p1, p2) :
        return [min(p1[0], p2[0]), max(p1[0], p2[0]), min(p1[1], p2[1]), max(p1[1], p2[1])]

    @classmethod
    def segNotCross(cls, a1, b1, a2, b2) :
        return (a1>b2 or a2>b1)

    @classmethod
    def crossdot(cls, v1, v2) :
        return v1[0]*v2[1] - v2[0]*v1[1]

    @classmethod
    def nodeEdgeDis(cls, p1, p2, p3) :
        a = Checker.getbox(p1, p2)
        if a[0]<=p3[0]<=a[1] and a[2]<=p3[1]<=a[3] :
            e1, e2, e3 = Checker.dis(p1, p2), Checker.dis(p1, p3), Checker.dis(p2, p3)
            ee = (e1+e2+e3)/2
            s = math.sqrt(max(ee*(ee-e1)*(ee-e2)*(ee-e3), 0.0))
            d = s*2/e1
            return d
        else :
            return 1.0

    @classmethod
    def cross(cls, p1, p2, p3, p4) :
        a = Checker.getbox(p1, p2)
        b = Checker.getbox(p3, p4)
        if Checker.segNotCross(a[0], a[1], b[0], b[1]) : return False
        if Checker.segNotCross(a[2], a[3], b[2], b[3]) : return False
        v1 = [p2[0]-p1[0], p2[1]-p1[1]]
        v2 = [p3[0]-p1[0], p3[1]-p1[1]]
        v3 = [p4[0]-p1[0], p4[1]-p1[1]]
        return Checker.crossdot(v1, v2) * Checker.crossdot(v1, v3) < 0

    @classmethod
    def getNodeNodeDistance(cls, G, pos) :
        ret = 1e10
        for u in G.nodes :
            for v in G.nodes :
                if u!=v :
                    ret = min(ret, Checker.dis(pos[u], pos[v]))
        return ret

    @classmethod
    def getEdgeCrossNumber(cls, G, pos) :
        ret = 0
        for u1,v1 in G.edges :
            for u2,v2 in G.edges :
                if u1!=u2 and u1!=v2 and v1!=u2 and v1!=v2 :
                    if Checker.cross(pos[u1], pos[v1], pos[u2], pos[v2]) :
                        ret += 1
        return ret

    @classmethod
    def getOverlaps(cls, G, pos) :
        ret = []
        for u,v in G.edges :
            for x in G.nodes :
                if x==u or x==v : continue
                d = Checker.nodeEdgeDis(pos[u], pos[v], pos[x])
                if d<0.2 :
                    ret.append((u,v))
                    break
        return ret