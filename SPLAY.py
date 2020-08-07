from random import shuffle
import sys, time
from math import log

sys.setrecursionlimit(100000)

class Node:
    def __init__(self, key):
        self.key = key
        self.left = self.right = None

class SplayTree:
    def __init__(self):
        self.root = None
    
    def subTreeSize(self, key, x, found = False):
        global depth
        depth = 1
        if (x is not None):
            if not found:
                if key == x.key:
                    self.subTreeSize(key, x, True)
                else:
                    if key < x.key:
                        if x.left is not None:
                            self.subTreeSize(key, x.left, False)
                    else:
                        if x.right is not None:                
                            self.subTreeSize(key, x.right, False)

            else:
                if x.left is not None:
                    depth += self.subTreeSize(key, x.left, True)
                if x.right is not None:
                    depth += self.subTreeSize(key, x.right, True)
        return depth
                
    def calcRank(self, n):
         return log(2, n)

                     
    def parent(self, key):
        n = p = self.root
        while(n.key != key):
            p = n
            if (key < n.key):
                n = n.left
            else:
                n = n.right
        return p


    def insert(self, key, n = None):
        global preRank 
        global postRank 
        r = r1 = 0
        if (n is None):
            n = self.root
        if (n is None):
            self.root = Node(key)
            return 
        if (key < n.key):
            if (n.left is None):
                n.left = Node(key)
                """ SPLAY NEEDS TO RETURN THE CALCUALTION """
                self.splay(n.left, log(self.subTreeSize(key, self.root),2))
                return 
            else:
                self.insert(key, n.left)
                
        if (key > n.key):
            if (n.right is None):
                n.right = Node(key)
                """ SPLAY NEEDS TO RETURN THE CALCUALTION """
                self.splay(n.right, log(self.subTreeSize(key, self.root),2))
                return
            else:
                self.insert(key, n.right)
    
    def find(self, key, n):
        if (n is not None):
            if (key == n.key):
               self.splay(n)
               return
            elif (key < n.key):
                if n.left is not None:
                    self.find(key, n.left)
                else:
                    self.splay(n)
            else:
                if n.right is not None:
                    self.find(key, n.right)
                else:
                    self.splay(n)
        return

    def delete(self, key):
        self.find(key,self.root)
        if ((self.root.left is None) and (self.root.right is not None) and (self.root.right.left is None)):
            self.root = self.root.right
        if ((self.root.right is None) and (self.root.left is not None) and (self.root.left.right is None)):
            self.root = self.root.left
        if ((key == self.root.key) and (self.root.left is not None)):
            n = self.root.left
            while (self.root.right is not None):
                n = n.right
            p = parent(n.key)
            p.right = n.left
            self.root.key = n.key
            return
        if ((key == self.root.key) and (self.root.right is not None)):
            n = self.root.right
            while (self.root.left is not None):
                n = n.left
            p = parent(n.key)
            p.left = n.right
            self.root.key = n.key
            return
        if (key == root.key):
            self.root = None
        else:
            return
    """
    SPLAY NEEDS TO RETURN THE CALCUALTION:
        Simple rotation: Compute 1+r′(x)−r(x)+r'(p)−r(p).
        Zig Zig: Compute 2 + r′(x)− r(x) + r′(p)− r(p) + r′(g)− r(g)
        Zig Zag: 2 + r′(x) − r(x) + r′(p) − r(p) + r′(g) − r(g)
    """
    def splay(self, n, rank = 0):
        
        p = self.parent(n.key)
        g = self.parent(p.key)

        if (n.key == self.root.key):
            return
       

        if (p.key != n.key) and (g.key == p.key):
            if (n.key < p.key):
                p.left = n.right
                n.right = p
            if (n.key > p.key):
                p.right = n.left
                n.left = p
            self.root = n
            self.splay(n)
            return

        q = self.parent(g.key)
        
        if ((n.key < p.key < g.key)):
            g.left = p.right
            p.left = n.right
            p.right = g
            n.right = p

            if (g.key == self.root.key):
                self.root = n
            elif (q.key > n.key):
                q.left = n
            else:
                q.right = n
            self.splay(n)
            return

        if(n.key > p.key > g.key):
            g.right = p.left
            p.right = n.left
            p.left = g
            n.left = p

            if (g.key == self.root.key):
                self.root = n
            elif (q.key > n.key):
                q.left = n
            else:
                q.right = n
            self.splay(n)
            return

        if ((p.key < n.key < g.key)):
            p.right = n.left
            g.left = n.right
            n.left = p
            n.right = g

            if (g.key == self.root.key):
                self.root = n
            elif (q.key > n.key):
                q.left = n
            else:
                q.right = n
            self.splay(n)
            return

        if ((g.key < n.key < p.key)):
            p.left = n.right
            g.right = n.left
            n.left = g
            n.right = p

            if (g.key == self.root.key):
                self.root = n
            elif (q.key > n.key):
                q.left = n
            else:
                q.right = n
            self.splay(n)
            return
    
                

def testTreeSmall(size = 5):
    tSmall = SplayTree()
    d = [i for i in range(1, size + 1)]
    shuffle(d)
    for x in d:
        tSmall.insert(x, tSmall.root)

def testTree(size = 100000):           
    t = SplayTree()
    t.insert(0)
    d = [i for i in range(1, size+2)]
    t1 = time.time()
    shuffle(d)
    for x in d:
        t.insert(x, t.root)
    t2 = time.time()
    print("Finished in: %f seconds" % (t2-t1))
    t3 = time.time()
    t.insert(200000)
    print("Inserted and Splayed 200,000 in: %f seconds" % (t3-t1))
    return
testTreeSmall()
#testTree()

