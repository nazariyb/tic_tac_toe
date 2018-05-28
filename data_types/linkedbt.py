"""
File: linkedbst.py
Author: Ken Lambert
"""

from data_types.abstractcollection import AbstractCollection
from data_types.btnode import BTNode
from data_types.linkedstack import LinkedStack
from math import log2, ceil


class LinkedBT(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = sourceCollection
        # AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            s = ""
            if node != None:
                s += recurse(node.right, level + 1)
                s += "| " * level
                s += str(node.data) + "\n"
                s += recurse(node.left, level + 1)
            return s

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def get_root(self):
        return self._root

    def children(self, node):
        """
        return children of node
        """
        if node.left != None:
            yield node.left
        if node.right != None:
            yield node.right

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        lyst = []

        def recurse(node):
            if node != None:
                lyst.append(node.data)
                recurse(node.left)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        lyst = []

        def recurse(node):
            if node != None:
                recurse(node.left)
                recurse(node.right)
                lyst.append(node.data)

        recurse(self._root)
        return iter(lyst)

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        lyst = []

        def recurse(node):
            if node != None:
                for c in self.children(node):
                    lyst.append(c.data)
                recurse(node.left)
                recurse(node.right)

            # if node != None:
            #     recurse(node.left)
            #     recurse(node.right)
            #     lyst.append(node.data)

        lyst.append(self._root.data)
        recurse(self._root)
        return iter(lyst)

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left == None:
                    node.left = BTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right == None:
                node.right = BTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def insert_left(self, item, node=None):
        if node is None:
            node = self._root
        node.left = BTNode(item)

    def insert_right(self, item, node=None):
        if node is None:
            node = self._root
        node.right = BTNode(item)

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if item not in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def liftMaxInLeftSubtreeToTop(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            currentNode = top.left
            while not currentNode.right == None:
                parent = currentNode
                currentNode = currentNode.right
            top.data = currentNode.data
            if parent == top:
                top.left = currentNode.left
            else:
                parent.right = currentNode.left

        # Begin main part of the method
        if self.isEmpty():
            return None

        # Attempt to locate the node containing the item
        itemRemoved = None
        preRoot = BTNode(None)
        preRoot.left = self._root
        parent = preRoot
        direction = 'L'
        currentNode = self._root
        while not currentNode == None:
            if currentNode.data == item:
                itemRemoved = currentNode.data
                break
            parent = currentNode
            if currentNode.data > item:
                direction = 'L'
                currentNode = currentNode.left
            else:
                direction = 'R'
                currentNode = currentNode.right

        # Return None if the item is absent
        if itemRemoved == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not currentNode.left == None \
                and not currentNode.right == None:
            liftMaxInLeftSubtreeToTop(currentNode)
        else:

            # Case 2: The node has no left child
            if currentNode.left == None:
                newChild = currentNode.right

                # Case 3: The node has no right child
            else:
                newChild = currentNode.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = newChild
            else:
                parent.right = newChild

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = preRoot.left
        return itemRemoved

    def replace(self, item, newItem):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                oldData = probe.data
                probe.data = newItem
                return oldData
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def _height1(self, top):
        '''
        Helper function
        :param top:
        :return:
        '''

        if self.is_leaf(top):
            return 0
        else:
            return 1 + max([self._height1(c) for c in self.children(top)])

    def height(self, top=None):
        '''
        Return the height of tree
        :return: int
        '''
        if top is None:
            top = self._root
        return self._height1(top)

    def is_leaf(self, node):
        """
        check whether node is a leaf or not
        """
        return node.right is None and node.left is None

    def _leaf_number(self):
        """
        count number of leaves in tree
        :return:
        """
        leaves = []

        def recurse(node):
            if node != None:
                for c in self.children(node):
                    leaves.append(int(self.is_leaf(c)))
                recurse(node.left)
                recurse(node.right)

        recurse(self._root)
        return sum(leaves)

    def isBalanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        l = self._leaf_number()
        return self.height() <= ceil(log2(l)) + 1

    def rangeFind(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        range_list = []
        for item in self:
            if low <= item <= high:
                range_list.append(item)
        return range_list

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        tree_list = []
        for node in self.inorder():
            tree_list.append(node)
        self.clear()
        tree_list.sort()

        def insert(tree_list, left=True):
            if len(tree_list) > 1:
                ind = len(tree_list) // 2
                self.add(tree_list[ind])
                # print('added', tree_list[ind])
                if left:
                    insert(tree_list[ind:], True)
                    insert(tree_list[:ind], False)
                else:
                    insert(tree_list[:ind], False)
                    insert(tree_list[ind:], True)

        insert(tree_list)

    def _dif(self, item, sign):
        differs = []
        for item_in_tree in self:
            if eval('%s%s%s' % (item_in_tree, sign, item)):
                differs.append(item_in_tree)
        return differs

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        return min(self._dif(item, '>'))

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        return max(self._dif(item, '<'))
