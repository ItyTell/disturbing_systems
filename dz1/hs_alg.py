# Description: This file contains the implementation of the HS algorithm.


class Node:
    def __init__(self, UID, left=None, right=None):
        self.UID = UID
        self.left = left
        self.right = right
        self.leader = None
    
    def __str__(self):
        return str(self.UID)
    
    def __repr__(self):
        return str(self.UID)

    def recieve(self, msg):
        if msg["type"] == 'ELECT':
            self.elect(msg["UID"], msg["direction"])
        elif msg["type"] == 'LEADER':
            if self.leader is None:
                self.leader = msg["UID"]
                self.send({"type": "LEADER", "UID": msg["UID"], "direction": "right"}, "right")
                self.send({"type": "LEADER", "UID": msg["UID"], "direction": "left"}, "left")
    
    def elect(self, UID, direction):
        if UID > self.UID:
            self.send({"type": "ELECT", "UID": UID, "direction": direction}, direction)
        elif UID < self.UID:
            return
        else:
            self.send({"type": "LEADER", "UID": self.UID, "direction": direction}, direction)

    def send(self, msg, direction):
        if direction == "right":
            self.right.recieve(msg)
        elif direction == "left":
            self.left.recieve(msg)
    
    def start_election(self):
        self.right.recieve({"type": "ELECT", "UID": self.UID, "direction": "right"})
        self.left.recieve({"type": "ELECT", "UID": self.UID, "direction": "left"})

def init_node_circle():
    n = 10
    uids = [5, 8, 3, 1, 7, 19, 2, 4, 6, 10]
    nodes = [Node(uids[i]) for i in range(n)]
    for i in range(n):
        nodes[i].left = nodes[(i-1)%n]
        nodes[i].right = nodes[(i+1)%n]
    return nodes


def hs(nodes):
    for node in nodes:
        node.start_election()
    return nodes

nodes = init_node_circle()
hs(nodes)

print([node.leader for node in nodes])