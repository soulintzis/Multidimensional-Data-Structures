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

class Node:
    '''Nodes stores keys and values and values are stored as a a linked list under each key'''
    def __init__(self, order):
        self.order = order
        self.keys = []
        self.values = []
        self.leaf = True

    def add(self, key, value):
        '''Adds a key-value pair to the node'''
        if not self.keys:
            self.keys.append(key)
            self.values.append([value])
            return None

        for i, item in enumerate(self.keys):
            if key == item:
                self.values[i].append(value)
                break

            elif key < item:
                self.keys = self.keys[:i] + [key] + self.keys[i:]
                self.values = self.values[:i] + [[value]] + self.values[i:]
                break

            elif i + 1 == len(self.keys):
                self.keys.append(key)
                self.values.append([value])
                break

    def split(self):
        '''Splits  node into two and stores them as child nodes'''
        left = Node(self.order)
        right = Node(self.order)
        mid = self.order / 2

        left.keys = self.keys[:mid]
        left.values = self.values[:mid]

        right.keys = self.keys[mid:]
        right.values = self.values[mid:]

        self.keys = [right.keys[0]]
        self.values = [left, right]
        self.leaf = False

    def is_full(self):
        '''Checks if the node is full and return s true'''
        return len(self.keys) == self.order

    def show(self, counter=0):
        '''Prints the keys at each level'''
        print(counter, str(self.keys))

        if not self.leaf:
            for item in self.values:
                item.show(counter + 1)

class BPlusTree(object):
    '''Creating B+ tree object, consisting of nodes.
    Nodes will split in two when it is full. When a split
    occurs, a key will 'float' upwards and be inserted into the parent node to
    act as a pivot'''
    def __init__(self, order=8):
        self.root = Node(order)

    def _find(self, node, key):
        '''Returns the index where the key should be
        inserted and the list of values at that index'''
        for i, item in enumerate(node.keys):
            if key < item:
                return node.values[i], i

        return node.values[i + 1], i + 1

    def _merge(self, parent, child, index):
        '''For a parent and child node, extract a pivot from the child to be
        inserted into the keys of the parent. Insert the values from the child
        into the values of the parent'''
        parent.values.pop(index)
        pivot = child.keys[0]

        for i, item in enumerate(parent.keys):
            if pivot < item:
                parent.keys = parent.keys[:i] + [pivot] + parent.keys[i:]
                parent.values = parent.values[:i] + child.values + parent.values[i:]
                break

            elif i + 1 == len(parent.keys):
                parent.keys += [pivot]
                parent.values += child.values
                break

    def insert(self, key, value):
        '''Inserts a key-value pair after traversing to a leaf node. If the leaf
        node is full, split the leaf node into two'''
        parent = None
        child = self.root

        while not child.leaf:
            parent = child
            child, index = self._find(child, key)

        child.add(key, value)

        if child.is_full():
            child.split()

            if parent and not parent.is_full():
                self._merge(parent, child, index)

    def retrieve(self, key):
        '''Returns a value for a given key, and None if the key does not exist'''
        child = self.root

        while not child.leaf:
            child, index = self._find(child, key)

        for i, item in enumerate(child.keys):
            if key == item:
                return child.values[i]

        return None

    def show(self):
        '''Prints the keys at each level'''
        self.root.show()
    
    def delete(self, key, value):
        if node==null:
            

if __name__ == '__main__':
    demo_node()
    print '\n'
    demo_bplustree()

