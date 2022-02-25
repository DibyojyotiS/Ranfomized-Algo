class UnionFind:

    def __init__(self, num_nodes) -> None:
        self.parent = list(range(num_nodes))
        self.size = [1]*num_nodes
        self.num_sets = num_nodes

    def find(self, node):
        t= node
        while t != self.parent[t]:
            self.parent[t] = self.parent[self.parent[t]]
            t = self.parent[t]
        return t
    
    def union(self, a, b):
        root_a = self.find(a)
        root_b = self.find(b)
        if root_a == root_b: return
        if self.size[root_a] < self.size[root_b]:
            self.parent[root_a] = root_b
            self.size[root_b] += self.size[root_a]
        else:
            self.parent[root_b] = root_a
            self.size[root_a] += self.size[root_b]
        self.num_sets -= 1

    def itter_sizes(self):
        for i,p in enumerate(self.parent):
            if i == p:
                yield self.size[i]
                