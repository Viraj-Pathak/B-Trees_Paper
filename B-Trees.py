class BTreeNode:
    def __init__(self, leaf=True):
        self.keys = []
        self.children = []
        self.leaf = leaf

    def split_child(self, i, child):
        new_child = BTreeNode(leaf=child.leaf)
        self.children.insert(i + 1, new_child)
        self.keys.insert(i, child.keys.pop())

        # Distribute keys and children between the two nodes
        new_child.keys = child.keys[2:]
        child.keys = child.keys[:2]

        if not child.leaf:
            new_child.children = child.children[2:]
            child.children = child.children[:2]

    def insert_non_full(self, key):
        i = len(self.keys) - 1
        if self.leaf:
            self.keys.append(None)
            while i >= 0 and key < self.keys[i]:
                self.keys[i + 1] = self.keys[i]
                i -= 1
            self.keys[i + 1] = key
        else:
            while i >= 0 and key < self.keys[i]:
                i -= 1
            i += 1
            if len(self.children[i].keys) == 3:
                self.split_child(i, self.children[i])
                if key > self.keys[i]:
                    i += 1
            self.children[i].insert_non_full(key)

    def insert(self, key):
        if len(self.keys) == 3:
            new_root = BTreeNode(leaf=False)
            new_root.children.append(self)
            new_root.split_child(0, self)
            new_root.insert_non_full(key)
            return new_root
        else:
            self.insert_non_full(key)
            return self

    def __str__(self):
        if self.leaf:
            return f"Leaf Node with keys: {', '.join(map(str, self.keys))}"
        else:
            return f"Internal Node with keys: {', '.join(map(str, self.keys))}"

def print_b_tree(node, level=0):
    print("  " * level + str(node))
    if not node.leaf:
        for child in node.children:
            print_b_tree(child, level + 1)

# Example usage:
root = BTreeNode()
root = root.insert(10)
root = root.insert(20)
root = root.insert(5)
root = root.insert(6)
root = root.insert(12)
root = root.insert(30)
root = root.insert(7)

print("B-tree:")
print_b_tree(root)
