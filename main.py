import sys  # For accepting command line arguments
import random
from enum import Enum

"""
# Reading Command line arguments
numberOfArgs = len(sys.argv)
nameOfScript = sys.argv[0]

print("Number of arguments passed:", numberOfArgs)
print("\nName of script:", nameOfScript)
print("\nArguments passed:")

arguments = []
for i in range(1, numberOfArgs):
    arguments.append(sys.argv[i])
    print(sys.argv[i])

 """
# ha nara

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
        self.comparisons = 0

    # Recursive function to insert val in subtree rooted with node and returns new root of subtree.
    def insert(self, root, val):

        # Step 1 - Perform normal BST
        if not root:
            return AVLNode(val)
        elif val < root.val:
            root.left = self.insert(root.left, val)
        else:
            root.right = self.insert(root.right, val)

        # Step 2 - Update the height of the ancestor node
        root.height = 1 + max(self.getHeight(root.left),
                              self.getHeight(root.right))

        # Step 3 - Get the balance factor
        # If balance factor is greater than 1, then the current node is unbalanced and rotations must be performed
        balance = self.getBalance(root)

        # Step 4 - If the node is unbalanced, then try out the 4 cases to re-balance

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

    # Recursive function to delete a node with given val from subtree with given root. It returns root of the modified subtree.
    def delete(self, root, val):

        # Step 1 - Perform standard BST delete
        if not root:
            return root

        elif val < root.val:
            root.left = self.delete(root.left, val)

        elif val > root.val:
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

        # If the tree has only one node, simply return it
        if root is None:
            return root

        # Step 2 - Update the height of the ancestor node
        root.height = 1 + max(self.getHeight(root.left),
                              self.getHeight(root.right))

        # Step 3 - Get the balance factor
        balance = self.getBalance(root)

        # Step 4 - If the node is unbalanced, then try out the 4 cases
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
        self.comparisons += 1
        # If no root exists then there is no subtree to search in
        if root is None:
            return False
        # Check if the current root value matches the value we are looking for
        elif root.val == val:
            return True
        # If value we are searching for is larger than the current root value it must mean that the value is in the right subtree
        elif root.val < val:
            return self.search(root.right, val)

        # Otherwise check the left subtree
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

    def getComparisons(self):
        return self.comparisons

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

        print("{0} ".format(root.val), end="")
        self.preOrder(root.left)
        self.preOrder(root.right)

    def inOrder(self, root):

        if not root:
            return

        self.inOrder(root.left)
        print("{0} ".format(root.val), end="")
        self.inOrder(root.right)

    def postOrder(self, root):

        if not root:
            return

        self.postOrder(root.left)
        self.postOrder(root.right)
        print("{0} ".format(root.val), end="")


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

https://www.geeksforgeeks.org/c-program-red-black-tree-insertion/
"""

""" 
class Colour(Enum):
    Black = 1
    Red = 2

class RBNode(object):
    def __init__(self, val):
        self.val = val
        self.parent = None
        self.left = NULL
        self.right = NULL
        self.colour = Colour.Red  # if not red = black


class RB_Tree(object):
    def __init__(self):
        self.root = None
        self.size = 0
 """


class Node():
    def __init__(self, val=None, color='red'):
        self.right = None
        self.left = None
        self.parent = None
        self.val = val
        self.color = color


class RedBlackTree:

    def __init__(self):
        self.NULL = Node(val=None, color='black')
        self.root = self.NULL
        self.size = 0
        self.rotations = 0
        self.comparisons = 0
        self.ordered = []
        self.height = 0
        pass

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

    def insert(self, z):
        new_node = Node(val=z)
        self._insert(new_node)
        self.size += 1

    def _insert(self, z):
        y = self.NULL
        x = self.root
        while x != self.NULL:
            y = x
            if z.val < x.val:
                x = x.left
            else:
                x = x.right
        z.parent = y
        if y == self.NULL:
            self.root = z
        elif z.val < y.val:
            y.left = z
        else:
            y.right = z
        z.left = self.NULL
        z.right = self.NULL
        z.color = "red"
        self.rb_insert_fixup(z)

    def rb_insert_fixup(self, z):
        i = 0
        while z.parent.color == "red":
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right
                if y.color == 'red':
                    z.parent.color = "black"
                    y.color = "black"
                    z.parent.parent.color = "red"
                    z = z.parent.parent
                else:
                    if z == z.parent.right:
                        z = z.parent
                        self.left_rotate(z)
                    z.parent.color = 'black'
                    z.parent.parent.color = 'red'
                    self.right_rotate(z.parent.parent)
            else:
                y = z.parent.parent.left
                if y.color == 'red':
                    z.parent.color = "black"
                    y.color = "black"
                    z.parent.parent.color = "red"
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self.right_rotate(z)
                    z.parent.color = 'black'
                    z.parent.parent.color = 'red'
                    self.left_rotate(z.parent.parent)
            i += 1
        self.root.color = 'black'

    def transplant(self, u, v):
        if u.parent == self.NULL:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def delete(self, z):
        if self.size == 0:
            print("TreeError")
            return
        our_node = self.key_search(z)
        if our_node == None:
            return
        self._delete(our_node)
        self.size -= 1

    def _delete(self, z):
        y = z
        original_color = y.color
        if z.left == self.NULL:
            x = z.right
            self.transplant(z, z.right)
        elif z.right == self.NULL:
            x = z.left
            self.transplant(z, z.right)
        else:
            y = self._min_node(z.right)
            original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self.transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if original_color == 'black':
            self.rb_delete_fixup(x)

    def rb_delete_fixup(self, x):
        while x != self.root and x.color == 'black':
            if x == x.parent.left:
                w = x.parent.right
                if w.color == 'red':
                    w.color = 'black'
                    x.parent.color = 'red'
                    self.left_rotate(x.parent)
                    w = x.parent.right
                if w.left.color == 'black' and w.right.color == 'black':
                    w.color = 'red'
                    x = x.parent
                else:
                    if w.right.color == 'black':
                        w.left.color = 'black'
                        w.color = 'red'
                        self.right_rotate(w)
                        w = x.parent.right
                    w.color = x.parent.color
                    x.parent.color = 'black'
                    w.right.color = 'black'
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                if w.color == 'red':
                    w.color = 'black'
                    x.parent.color = 'red'
                    self.right_rotate(x.parent)
                    w = x.parent.left
                if w.right.color == 'black' and w.left.color == 'black':
                    w.color = 'red'
                    x = x.parent
                else:
                    if w.left.color == 'black':
                        w.right.color = 'black'
                        w.color = 'red'
                        self.left_rotate(w)
                        w = x.parent.left
                    w.color = x.parent.color
                    x.parent.color = 'black'
                    w.left.color = 'black'
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = 'black'

    def search(self, x):
        return self._search(self.root, x)

    def _search(self, current_node, target):
        self.comparisons += 1
        if current_node == self.NULL:
            return "NotFound"
        elif target == current_node.val:
            return "Found"
        elif target < current_node.val:
            return self._search(current_node.left, target)
        else:
            return self._search(current_node.right, target)

    def getRotations(self):
        return self.rotations

    def getComparisons(self):
        return self.comparisons

    def key_search(self, target):
        return self._key_search(self.root, target)

    def _key_search(self, current_node, target):
        self.comparisons += 1
        if current_node == self.NULL:
            return None
        elif target == current_node.val:
            return current_node
        elif target < current_node.val:
            return self._key_search(current_node.left, target)
        else:
            return self._key_search(current_node.right, target)

    def getHeight(self, root):

        heightLeft = 0
        heightRight = 0

        if not root:
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
        return self._maximum(self.root)

    def _maximum(self, x):
        while x.right != self.NULL:
            x = x.right
        return x.val

    def minimum(self):
        if self.size == 0:
            return "Empty"
        return self._minimum(self.root)

    def _minimum(self, x):
        while x.left != self.NULL:
            x = x.left
        return x.val

    def _min_node(self, x):
        while x.left != self.NULL:
            x = x.left
        return x

    def inprint(self):
        if self.size == 0:
            print("Empty")
            return
        self._inprint(self.root)
        for i in range(len(self.ordered)-1):
            print(self.ordered[i], end=' ')
        print(self.ordered[-1])
        self.ordered = []

    def _inprint(self, x):
        if x != self.NULL and x.val != None:
            self._inprint(x.left)
            self.ordered.append(x.val)
            self._inprint(x.right)



# Runner Program

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
print("AVL {} total rotations required, height is {}".format(AVLTree.getRotations(), AVLTree.getHeight(AVLroot)))  # add number of nodes
print("RB {} total rotations required, height is {}".format(RBTree.getRotations(), RBTree.getHeight(RBTree.root)))  # add number of nodes

# print("In order traversal of the constructed AVL tree is:\n")
# AVLTree.inOrder(AVLroot)
# print("In order traversal of the constructed RB tree is:\n")
# RBTree.inprint()

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
print("AVL {} total rotations required, height is {}".format(AVLTree.getRotations(), AVLTree.getHeight(AVLroot)))  # add number of nodes
print("RB {} total rotations required, height is {}".format(RBTree.getRotations(), RBTree.getHeight(RBTree.root)))  # add number of nodes

# print("In order traversal of the constructed AVL tree after deleting items is:\n")
# AVLTree.inOrder(AVLroot)
# RBTree.inprint()

# printTree(AVLroot, 0)
#printTree(RBTree.root, 0)

"""
# Search
"""
for elem in Z:
    AVLTree.search(AVLroot, elem)

for elem in Z:
    RBTree.search(elem)

print("\nSearch")
print("k is ", k)
print("AVL: {} total comparisons required".format(AVLTree.getComparisons()))
print("RB: {} total comparisons required".format(RBTree.getComparisons()))
