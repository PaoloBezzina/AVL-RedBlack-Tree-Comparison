import sys  #For accepting command line arguments
import random

""" 
#Reading Command line arguments
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
#Set X
n = random.randint(1000, 3000)
print("\nn:", n)

X = set(random.sample(range(-3000,3000), n))
print("Set X contains %d elements" %len(X))

#Set Y
m = random.randint(500, 1000)
print("\nm:", m)

Y = set(random.sample(range(-3000,3000), m))
print("Set Y contains %d elements" %len(Y))

#Set Z
k = random.randint(1000, 2000)
print("\nk:", k)

Z = set(random.sample(range(-3000,3000), k))
print("Set Z contains %d elements" %len(Z))


intersection = X.intersection(Y)
print("\nSets X and Y have %d elements in common" %len(intersection))


class Node(object):
    def __init__(self, val):
        self.val = val
        self.height = 1
        self.left = None
        self.right = None

#https://www.geeksforgeeks.org/avl-tree-set-1-insertion/
#https://www.geeksforgeeks.org/avl-tree-set-2-deletion/
#
# AVL tree class which supports the 
# Insert operation
class AVL_Tree(object):

    def __init__(self):
        self.rotations = 0
        self.comparisons = 0
 
    # Recursive function to insert key in subtree rooted with node and returns new root of subtree.
    def insert(self, root, key):
     
        # Step 1 - Perform normal BST
        if not root:
            return Node(key)
        elif key < root.val:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)
 
        # Step 2 - Update the height of the ancestor node
        root.height = 1 + max(self.getHeight(root.left), self.getHeight(root.right))
 
        # Step 3 - Get the balance factor
        #If balance factor is greater than 1, then the current node is unbalanced and rotations must be performed
        balance = self.getBalance(root)
 
        # Step 4 - If the node is unbalanced, then try out the 4 cases to re-balance

        # Case 1 - Left Left
        if balance > 1 and key < root.left.val:
            return self.rightRotate(root)
 
        # Case 2 - Right Right
        if balance < -1 and key > root.right.val:
            return self.leftRotate(root)
 
        # Case 3 - Left Right
        if balance > 1 and key > root.left.val:
            root.left = self.leftRotate(root.left)
            return self.rightRotate(root)
 
        # Case 4 - Right Left
        if balance < -1 and key < root.right.val:
            root.right = self.rightRotate(root.right)
            return self.leftRotate(root)
 
        return root


    # Recursive function to delete a node with given key from subtree with given root. It returns root of the modified subtree. 
    def delete(self, root, key): 
  
        # Step 1 - Perform standard BST delete 
        if not root: 
            return root 
  
        elif key < root.val: 
            root.left = self.delete(root.left, key) 
  
        elif key > root.val: 
            root.right = self.delete(root.right, key) 
  
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
        root.height = 1 + max(self.getHeight(root.left), self.getHeight(root.right)) 
  
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
        #if no root exists then there is no subtree to search in
        if (root is None):
            return False
        #check if the current root value matches the value we are looking for
        elif (root.val == val):
            return True
        #if value we are searching for is larger than the current root value it must mean that the value is in the right subtree
        elif(root.val < val):
            return self.search(root.right,val)

        #otherwise check the left subtree
        return self.search(root.left,val)


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
 
    #left subtree height – right subtree height
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


#Printing the tree
def printTree(root, indent):
    
    space = 4

    if root is None:
        return

    indent = indent + space

    #process right side
    printTree(root.right, indent)

    #process root
    for i in range(space, indent):
        print(end = " ")
    print(root.val)

    #process left side
    printTree(root.left, indent)


# Driver program to test above function
myTree = AVL_Tree()
root = None

"""
Insert
"""
for elem in X:
    root =  myTree.insert(root, elem)

print("\nInsert")
print("AVL %d total rotations required, height is " %myTree.getRotations(), myTree.getHeight(root))

#print("In order traversal of the constructed AVL tree is:\n")
#myTree.inOrder(root)
#printTree(root, 0)

""" 
Delete 
"""
for elem in Y:
    myTree.delete(root, elem)

print("\nDelete")
print("AVL %d total rotations required, height is " %myTree.getRotations(), myTree.getHeight(root))

#print("In order traversal of the constructed AVL tree after deleting items is:\n")
#myTree.inOrder(root)
#printTree(root, 0)

"""
Search
"""
for elem in Z:
    myTree.search(root, elem)

print("\nSearch")
print("k is ", k)
print("AVL: %d total comparisons required" %myTree.getComparisons())