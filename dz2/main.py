# Maximum Independent Set in Trees

class Node:
    def __init__(self):
        self.children = []
        self.m_size = 0


def mis(node):
    # якщо вузол вже був оброблений
    if node.m_size != 0:
        return node.m_size
    
    # якщо вузол - листок
    if len(node.children) == 0:
        node.m_size = 1
        return 1

    m1 = 1
    for child in node.children:
        for grandchild in child.children:
            m1 += mis(grandchild)

    m0 = 0
    for child in node.children:
        m0 += mis(child)

    node.m_size = max(m0, m1)
    
    return node.m_size



nodes = [Node() for i in range(10)]
nodes[3].children = [nodes[0], nodes[1], nodes[2]]
nodes[4].children = [nodes[3], nodes[5]]
nodes[5].children = [nodes[6], nodes[7], nodes[8]]
nodes[9].children = [nodes[4]]

print(mis(nodes[9]))  # 7
