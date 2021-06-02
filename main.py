import random
from enum import Enum

# Set X
n = random.randint(1000, 3000)
print("\nn:", n)

X = set(random.sample(range(-3000, 3000), n))
print("Set X contains %d elements" % len(X))

# Set Y
m = random.randint(500, 1000)
print("\nm:", m)

Y = set(random.sample(range(-3000, 3000), m))
print("Set Y contains %d elements" % len(Y))

# Set Z
k = random.randint(1000, 2000)
print("\nk:", k)

Z = set(random.sample(range(-3000, 3000), k))
print("Set Z contains %d elements" % len(Z))


intersection = X.intersection(Y)
print("\nSets X and Y have %d elements in common" % len(intersection))


"""
AVL Tree

https://www.geeksforgeeks.org/avl-tree-set-1-insertion/
https://www.geeksforgeeks.org/avl-tree-set-2-deletion/
"""


class AVLNode(object):
    def __init__(self, val):
        self.val = val
        self.height = 1
        self.left = None
        self.right = None


# AVL tree class
class AVL_Tree(object):
    def __init__(self):
        self.rotations = 0
        self.searchComparisons = 0
        self.comparisons = 0
        self.numNodes = 0

    # Recursive function to insert a value in a tree rooted with a node and returns new root of the subtree.
    def insert(self, root, val):
        # Inserting node like normally done in a bst
        self.comparisons += 1
        if not root:
            return AVLNode(val)
        elif val < root.val:
            root.left = self.insert(root.left, val)
        else:
            root.right = self.insert(root.right, val)

        # Updating the parent height
        root.height = 1 + max(self.getHeight(root.left),
                              self.getHeight(root.right))

        # Getting the balance factor. If this is greater than 1, rotations are needed since the tree is unbalanced
        balance = self.getBalance(root)

        # Re-balancing the tree
        # Case 1 - Left Left
        if balance > 1 and val < root.left.val:
            return self.rightRotate(root)

        # Case 2 - Right Right
        if balance < -1 and val > root.right.val:
            return self.leftRotate(root)

        # Case 3 - Left Right
        if balance > 1 and val > root.left.val:
            root.left = self.leftRotate(root.left)
            return self.rightRotate(root)

        # Case 4 - Right Left
        if balance < -1 and val < root.right.val:
            root.right = self.rightRotate(root.right)
            return self.leftRotate(root)
        return root

    # Recursive function to delete a node with given value from subtree with given root. It returns root of the modified subtree.
    def delete(self, root, val):

        # Deleting node like normally done in a bst
        if not root:
            return root
        elif val < root.val:
            self.comparisons += 1
            root.left = self.delete(root.left, val)

        elif val > root.val:
            self.comparisons += 1
            root.right = self.delete(root.right, val)

        else:
            if root.left is None:
                temp = root.right
                root = None
                return temp

            elif root.right is None:
                temp = root.left
                root = None
                return temp

            temp = self.getMinValueNode(root.right)
            root.val = temp.val
            root.right = self.delete(root.right, temp.val)

        # If only one node is present in the tree, simply return it
        if root is None:
            return root

        # Updating the parent height
        root.height = 1 + max(self.getHeight(root.left),
                              self.getHeight(root.right))

        # Getting the balance factor. If this is greater than 1, rotations are needed since the tree is unbalanced
        balance = self.getBalance(root)

        # Re-balancing the tree
        # Case 1 - Left Left
        if balance > 1 and self.getBalance(root.left) >= 0:
            return self.rightRotate(root)

        # Case 2 - Right Right
        if balance < -1 and self.getBalance(root.right) <= 0:
            return self.leftRotate(root)

        # Case 3 - Left Right
        if balance > 1 and self.getBalance(root.left) < 0:
            root.left = self.leftRotate(root.left)
            return self.rightRotate(root)

        # Case 4 - Right Left
        if balance < -1 and self.getBalance(root.right) > 0:
            root.right = self.rightRotate(root.right)
            return self.leftRotate(root)

        return root

    def search(self, root, val):
        self.searchComparisons += 1
        # If no root exists then there is no subtree to search in
        if root is None:
            return False
        # If the current root value matches the value we are looking for, it means we are done searching
        elif root.val == val:
            return True
        # If value we are searching for is larger than the current root value it must mean that the value is in the right subtree
        elif root.val < val:
            return self.search(root.right, val)

        # Otherwise, if the value we are searching for is smaller than the current root, check the left subtree
        return self.search(root.left, val)

    def leftRotate(self, z):

        self.rotations += 1

        y = z.right
        T2 = y.left

        # Perform rotation
        y.left = z
        z.right = T2

        # Update heights
        z.height = 1 + max(self.getHeight(z.left), self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left), self.getHeight(y.right))

        # Return the new root
        return y

    def rightRotate(self, z):

        self.rotations += 1

        y = z.left
        T3 = y.right

        # Perform rotation
        y.right = z
        z.left = T3

        # Update heights
        z.height = 1 + max(self.getHeight(z.left), self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left), self.getHeight(y.right))

        # Return the new root
        return y

    def getHeight(self, root):
        if not root:
            return 0

        return root.height

    def getRotations(self):
        return self.rotations

    def getsearchComparisons(self):
        return self.searchComparisons

    def getcomparisons(self):
        return self.comparisons

    def countNodes(self, root):

        if not root:
            return

        self.countNodes(root.left)
        self.numNodes += 1
        self.countNodes(root.right)

    def getNumNodes(self, root):
        self.numNodes = 0
        self.countNodes(root)
        return self.numNodes

    # Left subtree height – right subtree height
    def getBalance(self, root):
        if not root:
            return 0

        return self.getHeight(root.left) - self.getHeight(root.right)

    def getMinValueNode(self, root):
        if root is None or root.left is None:
            return root

        return self.getMinValueNode(root.left)

    def preOrder(self, root):

        if not root:
            return

        print(root.val," ")
        self.preOrder(root.left)
        self.preOrder(root.right)

    def inOrder(self, root):

        if not root:
            return

        self.inOrder(root.left)
        print(root.val," ", end="")
        self.inOrder(root.right)

    def postOrder(self, root):

        if not root:
            return

        self.postOrder(root.left)
        self.postOrder(root.right)
        print(root.val," ", end="")


# Printing the tree
def printTree(root, indent):

    space = 4

    if root is None:
        return

    indent = indent + space

    # process right side
    printTree(root.right, indent)

    # process root
    for i in range(space, indent):
        print(end=" ")
    print(root.val)

    # process left side
    printTree(root.left, indent)


"""
RBT Tree

https://www.geeksforgeeks.org/red-black-tree-set-1-introduction-2/
https://www.geeksforgeeks.org/red-black-tree-set-2-insert/
https://www.geeksforgeeks.org/red-black-tree-set-3-delete-2/
"""


class Colour(Enum):
    Black = 1
    Red = 2


class Node():
    def __init__(self, val=None, colour=Colour.Red):
        self.right = None
        self.left = None
        self.parent = None
        self.val = val
        self.colour = colour


class RedBlackTree:

    def __init__(self):
        self.NULL = Node(val=None, colour=Colour.Black)
        self.root = self.NULL
        self.size = 0
        self.rotations = 0
        self.comparisons = 0
        self.searchComparisons = 0
        self.height = 0

    def insert(self, z):
        new_node = Node(val=z)

        # self._insert(new_node)
        y = self.NULL
        x = self.root
        while x != self.NULL:
            y = x
            self.comparisons += 1
            if new_node.val < x.val:
                x = x.left
            else:
                x = x.right
        new_node.parent = y
        if y == self.NULL:
            self.root = new_node
        elif new_node.val < y.val:
            y.left = new_node
        else:
            y.right = new_node
        new_node.left = self.NULL
        new_node.right = self.NULL
        new_node.colour = Colour.Red
        self.insert_fix(new_node)

        self.size += 1

    def insert_fix(self, z):
        i = 0
        while z.parent.colour == Colour.Red:
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right
                if y.colour == Colour.Red:
                    z.parent.colour = Colour.Black
                    y.colour = Colour.Black
                    z.parent.parent.colour = Colour.Red
                    z = z.parent.parent
                else:
                    if z == z.parent.right:
                        z = z.parent
                        self.left_rotate(z)
                    z.parent.colour = Colour.Black
                    z.parent.parent.colour = Colour.Red
                    self.right_rotate(z.parent.parent)
            else:
                y = z.parent.parent.left
                if y.colour == Colour.Red:
                    z.parent.colour = Colour.Black
                    y.colour = Colour.Black
                    z.parent.parent.colour = Colour.Red
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self.right_rotate(z)
                    z.parent.colour = Colour.Black
                    z.parent.parent.colour = Colour.Red
                    self.left_rotate(z.parent.parent)
            i += 1
        self.root.colour = Colour.Black

    def delete(self, z):
        if self.size == 0:
            print("Error")
            return

        node_del = self.key_search(self.root, z)
        if node_del == None:
            return

        y = node_del
        original_color = y.colour
        if node_del.left == self.NULL:
            x = node_del.right
            self.transplant(node_del, node_del.right)
        elif node_del.right == self.NULL:
            x = node_del.left
            self.transplant(node_del, node_del.right)
        else:
            y = self.min_node(node_del.right)
            original_color = y.colour
            x = y.right
            if y.parent == node_del:
                x.parent = y
            else:
                self.transplant(y, y.right)
                y.right = node_del.right
                y.right.parent = y
            self.transplant(node_del, y)
            y.left = node_del.left
            y.left.parent = y
            y.colour = node_del.colour
        if original_color == Colour.Black:
            self.delete_fix(x)

        self.size -= 1

    def delete_fix(self, x):
        while x != self.root and x.colour == Colour.Black:
            if x == x.parent.left:
                w = x.parent.right
                if w.colour == Colour.Red:
                    w.colour = Colour.Black
                    x.parent.colour = Colour.Red
                    self.left_rotate(x.parent)
                    w = x.parent.right
                if w.left.colour == Colour.Black and w.right.colour == Colour.Black:
                    w.colour = Colour.Red
                    x = x.parent
                else:
                    if w.right.colour == Colour.Black:
                        w.left.colour = Colour.Black
                        w.colour = Colour.Red
                        self.right_rotate(w)
                        w = x.parent.right
                    w.colour = x.parent.colour
                    x.parent.colour = Colour.Black
                    w.right.colour = Colour.Black
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                if w.colour == Colour.Red:
                    w.colour = Colour.Black
                    x.parent.colour = Colour.Red
                    self.right_rotate(x.parent)
                    w = x.parent.left
                if w.right.colour == Colour.Black and w.left.colour == Colour.Black:
                    w.colour = Colour.Red
                    x = x.parent
                else:
                    if w.left.colour == Colour.Black:
                        w.right.colour = Colour.Black
                        w.colour = Colour.Red
                        self.left_rotate(w)
                        w = x.parent.left
                    w.colour = x.parent.colour
                    x.parent.colour = Colour.Black
                    w.left.colour = Colour.Black
                    self.right_rotate(x.parent)
                    x = self.root
        x.colour = Colour.Black

    def transplant(self, u, v):
        if u.parent == self.NULL:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def search(self, root, target):
        self.searchComparisons += 1

        if root == self.NULL:
            return "NotFound"
        elif target == root.val:
            return "Found"
        elif target < root.val:
            return self.search(root.left, target)
        else:
            return self.search(root.right, target)

    def key_search(self, root, target):
        self.comparisons += 1
        if root == self.NULL:
            return None
        elif target == root.val:
            return self.root
        elif target < root.val:
            return self.key_search(root.left, target)
        else:
            return self.key_search(root.right, target)

    def left_rotate(self, x):
        self.rotations += 1

        y = x.right
        x.right = y.left
        if y.left != self.NULL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == self.NULL:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, x):
        self.rotations += 1

        y = x.left
        x.left = y.right
        if y.right != self.NULL:
            y.right.parent = x
        y.parent = x.parent
        if x.parent == self.NULL:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def getRotations(self):
        return self.rotations

    def getsearchComparisons(self):
        return self.searchComparisons

    def getComparisons(self):
        return self.comparisons

    def getNumNodes(self):
        return self.size

    def getHeight(self, root):

        heightLeft = 0
        heightRight = 0

        if root is None:
            return 0

        while root.right != self.NULL:
            root = root.right
            heightRight += 1

        while root.left != self.NULL:
            root = root.left
            heightLeft += 1

        if heightLeft >= heightRight:
            self.height = heightLeft
        else:
            self.height = heightRight

        return self.height

    def maximum(self):
        if self.size == 0:
            return "Empty"

        while self.root.right != self.NULL:
            self.root = self.root.right
        return self.root.val

    def minimum(self):
        if self.size == 0:
            return "Empty"

        while self.root.left != self.NULL:
            self.root = self.root.left

        return self.root.val

    def min_node(self, x):
        while x.left != self.NULL:
            x = x.left
        return x

    def preOrder(self, root):
        if self.size == 0:
            print("Empty")
            return

        if root != self.NULL and root.val != None:
            print(root.val," ", end="")
            self.preOrder(root.left)
            self.preOrder(root.right)

    def inOrder(self, root):
        if self.size == 0:
            print("Empty")
            return

        if root != self.NULL and root.val != None:
            self.inOrder(root.left)
            print(root.val," ", end="")
            self.inOrder(root.right)

    def postOrder(self, root):
        if self.size == 0:
            print("Empty")
            return

        if root != self.NULL and root.val != None:
            self.postOrder(root.left)
            self.postOrder(root.right)
            print(root.val," ", end="")


# Runner Program
if __name__ == '__main__':
    # Driver program to test AVL functions
    AVLTree = AVL_Tree()
    AVLroot = None

    RBTree = RedBlackTree()

    """
    # Insert
    """
    for elem in X:
        AVLroot = AVLTree.insert(AVLroot, elem)

    for elem in X:
        RBTree.insert(elem)

    print("\nInsert")
    print("AVL {} total rotations required, height is {}, number of nodes is {}, total number of comparisons is {}".format(
        AVLTree.getRotations(), AVLTree.getHeight(AVLroot), AVLTree.getNumNodes(AVLroot), AVLTree.getcomparisons()))
    print("RB {} total rotations required, height is {}, number of nodes is {}, total number of comparisons is {}".format(
        RBTree.getRotations(), RBTree.getHeight(RBTree.root), RBTree.getNumNodes(), RBTree.getComparisons()))

    # print("In order traversal of the constructed AVL tree is:\n")
    # AVLTree.inOrder(AVLroot)
    # print("In order traversal of the constructed RB tree is:\n")
    # RBTree.inOrder(RBTree.root)

    # printTree(AVLroot, 0)
    # printTree(RBTree.root, 0)

    """
    # Delete
    """
    for elem in Y:
        AVLTree.delete(AVLroot, elem)

    for elem in Y:
        RBTree.delete(elem)

    print("\nDelete")
    print("AVL {} total rotations required, height is {}, number of nodes is {}, total number of comparisons is {}".format(
        AVLTree.getRotations(), AVLTree.getHeight(AVLroot), AVLTree.getNumNodes(AVLroot), AVLTree.getcomparisons()))
    print("RB {} total rotations required, height is {}, number of nodes is {}, total number of comparisons is {}".format(
        RBTree.getRotations(), RBTree.getHeight(RBTree.root), RBTree.getNumNodes(), RBTree.getComparisons()))

    # print("In order traversal of the constructed AVL tree after deleting items is:\n")
    # AVLTree.inOrder(AVLroot)
    # RBTree.inOrder(RBTree.root)

    # printTree(AVLroot, 0)
    #printTree(RBTree.root, 0)

    """
    # Search
    """
    for elem in Z:
        AVLTree.search(AVLroot, elem)

    for elem in Z:
        RBTree.search(RBTree.root, elem)

    print("\nSearch")
    print("k is ", k)
    print("AVL: {} total Comparisons required".format(AVLTree.getsearchComparisons()))
    print("RB: {} total Comparisons required".format(RBTree.getsearchComparisons()))