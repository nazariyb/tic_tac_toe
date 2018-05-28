class LinkedBinaryTree:
    def __init__(self, root):
        self.key = root
        self.left_child = None
        self.right_child = None

    def insert_left(self, new_node):
        if self.left_child == None:
            self.left_child = LinkedBinaryTree(new_node)
        else:
            t = LinkedBinaryTree(new_node)
            t.left_child = self.left_child
            self.left_child = t

    def insert_right(self, new_node):
        if self.right_child == None:
            self.right_child = LinkedBinaryTree(new_node)
        else:
            t = LinkedBinaryTree(new_node)
            t.right_child = self.right_child
            self.right_child = t

    def get_right_child(self):
        return self.right_child

    def get_left_child(self):
        return self.left_child

    # def num_children(self, node):
    #     return node.get_left_child

    def set_root_val(self, obj):
        self.key = obj

    def get_root_val(self):
        return self.key

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        lyst = []

        def recurse(node):
            if node != None:
                if node.left_child != None and node.right_child != None:
                    lyst.append(node.left_child.key)
                    lyst.append(node.right_child.key)
                    print(node.left_child.key, node.right_child.key)
                    recurse(node.left_child)
                    recurse(node.right_child)

            # if node != None:
            #     recurse(node.left)
            #     recurse(node.right)
            #     lyst.append(node.data)

        lyst.append(self.key)
        print(self.key)
        recurse(self)
        return iter(lyst)
