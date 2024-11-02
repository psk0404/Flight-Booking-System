class Graph:
    def __init__(self, a, b):
        self.N = 200
        self.e = [0] * self.N
        self.ne = [-1] * self.N
        self.h = [-1] * self.N
        self.idx = 0
        self.flag = 0
        self.s1 = []    # main stack
        self.s2 = []    # auxiliary
        self.backup = []

        # compute
        self.init()
        self.getpath(a, b)

    def add(self, a, b):
        self.e[self.idx] = b
        self.ne[self.idx] = self.h[a]
        self.h[a] = self.idx
        self.idx += 1

    def init(self):
        # Initialize
        self.add(1, 2), self.add(1, 8)
        self.add(2, 1)
        self.add(3, 5), self.add(3, 11), self.add(3, 9), self.add(3, 16)
        self.add(4, 12), self.add(4, 15), self.add(4, 14)
        self.add(5, 14), self.add(5, 3)
        self.add(6, 11), self.add(6, 7)
        self.add(7, 6), self.add(7, 11)
        self.add(8, 12), self.add(8, 1)
        self.add(9, 3), self.add(9, 11), self.add(9, 10)
        self.add(10, 9), self.add(10, 11), self.add(10, 15)
        self.add(11, 3), self.add(11, 9), self.add(11, 10), self.add(11, 13), self.add(11, 6), self.add(11, 7)
        self.add(12, 15), self.add(12, 4), self.add(12, 8)
        self.add(13, 11), self.add(13, 5)
        self.add(14, 5), self.add(14, 16), self.add(14, 4)
        self.add(15, 12), self.add(15, 10), self.add(15, 4)
        self.add(16, 3), self.add(16, 14), self.add(16, 4)

    def exists_s(self, s, ele):
        return ele in s

    def create_stack(self):
        element0 = self.s2[-1][-1]
        self.s2[-1].pop()
        u = element0

        if not self.exists_s(self.s1, element0):
            self.s1.append(element0)
            self.flag = 1
        else:
            while self.s2[-1]:
                element1 = self.s2[-1][-1]
                self.s2[-1].pop()
                if not self.exists_s(self.s1, element1):
                    self.flag = 1
                    u = element0
                    self.s1.append(element1)

        if not self.flag:
            self.s2.append([])

        ts = []
        i = self.h[u]
        while i != -1:
            ele = self.e[i]
            if not self.exists_s(self.s1, ele):
                ts.append(ele)
            i = self.ne[i]
        self.s2.append(ts)
        self.flag = 0

    def delete_stack(self):
        self.s2.pop()
        self.s1.pop()

    def storage(self):
        self.backup.append(self.s1.copy())

    def outputs(self, s):
        print(s)

    def getpath(self, a, b):
        self.s1.append(a)  # Start with the node a
        lst = []
        i = self.h[a]
        while i != -1:
            lst.append(self.e[i])
            i = self.ne[i]
        self.s2.append(lst)

        while self.s1 and self.s2:
            if not self.s2[-1]:
                self.delete_stack()
                continue
            self.create_stack()

            if self.s1[-1] == b:
                self.storage()
                self.delete_stack()
                continue

