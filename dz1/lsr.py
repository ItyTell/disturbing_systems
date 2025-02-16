# Description: This file contains the implementation of the LCR algorithm.


class Node:
    def __init__(self, UID, right=None):
        self.UID = UID
        self.right = right
        self.leader = None
    
    def __str__(self):
        return str(self.UID)
    
    def __repr__(self):
        return str(self.UID)
    
    def recieve(self, msg):
        if msg["type"] == 'ELECT':
            self.elect(msg["UID"])
        elif msg["type"] == 'LEADER':
            if self.leader is None:
                self.leader = msg["UID"]
                self.send({"type": "LEADER", "UID": msg["UID"]})
    
    def elect(self, UID):
        if UID > self.UID:
            self.send({"type": "ELECT", "UID": UID})
        elif UID < self.UID:
            self.send({"type": "ELECT", "UID": self.UID})
        else:
            self.send({"type": "LEADER", "UID": self.UID})
    
    def send(self, msg):
        self.right.recieve(msg)

    def start_election(self):
        self.send({"type": "ELECT", "UID": self.UID})


def init_node_circle():
    n = 10
    uids = [5, 8, 3, 1, 7, 9, 2, 4, 6, 10]
    nodes = [Node(uids[i]) for i in range(n)]
    for i in range(n):
        nodes[i].right = nodes[(i+1)%n]
    return nodes


def lcr(nodes):
    for node in nodes:
        node.start_election()
    return nodes

nodes = init_node_circle()
lcr(nodes)
print([node.leader for node in nodes])