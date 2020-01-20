# This class represents a Node of the tree
# A Node can be either a leaf node or not
class Node():
    ''''Attributes:
        size(int): The maximum number of keys a node can have
        keys[]: A list of pointers to other nodes 
        values[]: A list of values that the node has
        leafNode(boolean): Indicates if a node is a leaf node.
    '''
    def __init__(self, size):
        self.size = size 
        self.keys= list()
        self.childerns = list()
        self.leafNode = True

    def add(self, key):
        if not self.keys:
            self.keys.append(key)
            # self.values.append([value])
            return None

        for item in self.keys:
            index = self.keys.index(item)
            if key == item:
                print('The item already exists into the node')
                break

            elif key < item:
                self.keys = self.keys[:index] + [key] + self.keys[index:]
                # self.values = self.values[:index] + [[value]] + self.values[index:]
                break

            elif index + 1 == len(self.keys):
                self.keys.append(key)
                # self.values.append([value])
                break

    def splitNode(self):
        left = Node(self.size)
        right = Node(self.size)

        self.leafNode = False
        middle = int(self.size / 2)

        right.keys = self.keys[middle:]
        # right.values = self.values[middle:]
        
        left.keys = self.keys[:middle]
        # left.values = self.values[:middle]

        self.keys = [right.keys[0]]
        self.childerns = [left, right]


    def printNode(self, level=0):
        '''
        Prints the keys at each level.
        '''
        print('Level: {}, Keys: {}'.format(level, str(self.keys)))

        if self.leafNode != True:
            if self.childerns[0] is not None and self.childerns[1] is not None:
                print(self.childerns[0].printNode(level + 1))
                print(self.childerns[1].printNode(level + 1))
            else:
                print()

    def isNodeFull(self):
        if len(self.keys) == self.size:
            return True
        else:
            return False

node = Node(3)
node.add("a")
node.add("b")
node.add("c")
node.splitNode()
node.printNode()
node.add("d")

