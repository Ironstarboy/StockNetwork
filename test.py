import numpy as np

class Edge:
    def __init__(self, u, v, w):
        self.u = u
        self.v = v
        self.w = w

    def __str__(self):
        return str(self.u) + str(self.v) + str(self.w)


def zhuliu(edges, n, m, root):
    res = 0
    while True:
        pre = [-1]*n
        visited = [-1] * n
        circle = []
        inderee = [INF] * n
        # 寻找最小入边
        inderee[root] = 0
        for i in range(m):
            if edges[i].u != edges[i].v and edges[i].w < inderee[edges[i].v]:
                pre[edges[i].v] = edges[i].u
                inderee[edges[i].v] = edges[i].w
        # 有孤立点，不存在最小树形图
        for i in range(n):
            if i != root and inderee[i] == INF:
                return -1
        # 找有向h环
        tn = 0  # 记录环的个数
        circle = [-1] * n
        for i in range(n):
            res += inderee[i]
            v = i
            # 向前遍历找环，中止情况有：
            # 1. 出现带有相同标记的点，成环
            # 2. 节点属于其他环，说明进了其他环
            # 3. 遍历到root了
            while visited[v] != i and circle[v] == -1 and v != root:
                visited[v] = i
                v = pre[v]
            # 如果成环了才会进下面的循环，把环内的点的circle进行标记
            if v != root and circle[v] == -1:
                while circle[v] != tn:
                    circle[v] = tn
                    v = pre[v]
                tn += 1
        # 如果没有环了，说明一定已经找到了
        if tn == 0:
            break
        # 否则把孤立点都看作自环看待
        for i in range(n):
            if circle[i] == -1:
                circle[i] = tn
                tn += 1
        # 进行缩点，把点号用环号替代
        for i in range(m):
            v = edges[i].v
            edges[i].u = circle[edges[i].u]
            edges[i].v = circle[edges[i].v]
            # 如果边不属于同一个环
            if edges[i].u != edges[i].v:
                edges[i].w -= inderee[v]
        n = tn
        root = circle[root]
    return res


INF = 9999999999
if __name__ == '__main__':
    n, m, root = list(map(int, input().split()))
    edges = []
    for i in range(m):
        u, v, w = list(map(int, input().split()))
        # 输入的点是1开始的，-1改为0开始的
        edges.append(Edge(u-1, v-1, w))
    print(zhuliu(edges, n, m, root-1),end = "")





