# This class represents a Node of the tree
# A Node can be either a leaf node or not
def importData(file_name):
    while True:
        try:
            with open(file_name, 'r') as f:
                return f.read().split('\n')
            f.close()
        except FileNotFoundError:
            print('Wrong file or file path')
            file_name = input('Please type in the path to your file and press "Enter":')
        else:
            break

def exportData(output_filename, output_data):
    with open(output_filename, 'w') as f:
        for items in output_data:
            f.write("%s\n" %items)
    f.close()
    print('The data exported successfully')

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()




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
        self.values = list()
        self.leafNode = True

    def add(self, key, value):
        if not self.keys:
            self.keys.append(key)
            self.values.append([value])
            return None

        for item in self.keys:
            index = self.keys.index(item)
            if key == item:
                self.values[index].append(value)
                break

            elif key < item:
                self.keys = self.keys[:index] + [key] + self.keys[index:]
                self.values = self.values[:index] + [[value]] + self.values[index:]
                break

            elif index + 1 == len(self.keys):
                self.keys.append(key)
                self.values.append([value])
                break

    def splitNode(self):
        left = Node(self.size)
        right = Node(self.size)

        self.leafNode = False
        middle = int(self.size / 2)

        right.keys = self.keys[middle:]
        right.values = self.values[middle:]
        
        left.keys = self.keys[:middle]
        left.values = self.values[:middle]

        self.keys = [right.keys[0]]
        self.values = [left, right]

    def printNode(self, level=0):
        '''
        Prints the keys at each level.
        '''
        print('Level: {}, Keys: {}'.format(level, str(self.keys)))

        if self.leafNode != True:
            if self.values[0] is not str and self.values[1] is not str:
                print(self.values[0].printNode(level + 1))
                print(self.values[1].printNode(level + 1))
            else:
                print()

    def isNodeFull(self):
        if len(self.keys) == self.size:
            return True
        else:
            return False
    
    class BPlusTree(object):
        def __init__(self,order=8):
            self.root= Node(self)

        def _search(self, node, key):
            for i, item in enumarate(node.keys):
                if key < item:
                    return node.values[i], i
            return node.values[i+1],i+1

def merge(self, parent, child, index):
    parent.values.pop(index)
    pivot = child.keys[0]

    for i,item in enumerate(parent.keys):
        if pivot<item:
            parent.keys = parent.values[:i] + child.values + parent.values[:i]
            break
        
        elif i+1 == len(parent.)

