import random
import time
import os

testing_dataset = dict()

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

class Node(object):
    """Each node stores keys and values. Keys are not unique to each value, and as such values are
    stored as a list under each key.
    Attributes:
        order (int): The maximum number of keys each node can hold"""
    def __init__(self, order):
        """Child nodes can be converted into parent nodes by setting self.leaf = False. Parent nodes
        simply act as a medium element in order to traverse the tree"""
        self.order = order
        self.keys = []
        self.values = []
        self.leaf = True

    def add(self, key, value):
        """Adds a key-value pair to the node"""
        # If the node is empty, insert the new key-value pair
        if not self.keys:
            self.keys.append(key)
            self.values.append([value])
            return None

        for i, item in enumerate(self.keys):
            # If new key matches with the existing key, add it to the list of values
            if key == item:
                self.values[i].append(value)
                break

            # If new key is smaller than the existing key, insert new key to the left of the existing key
            elif key < item:
                self.keys = self.keys[:i] + [key] + self.keys[i:]
                self.values = self.values[:i] + [[value]] + self.values[i:]
                break

            # If new key is larger than all the existing keys, insert new key to the right of all existing keys
            elif i + 1 == len(self.keys):
                self.keys.append(key)
                self.values.append([value])

    def split(self):
        """Splits the node into two and stores them as child nodes."""
        left = Node(self.order)
        right = Node(self.order)
        mid = self.order // 2

        left.keys = self.keys[:mid]
        left.values = self.values[:mid]

        right.keys = self.keys[mid:]
        right.values = self.values[mid:]

        # When the node is split, set the parent key to the left-most key of the right child node.
        self.keys = [right.keys[0]]
        self.values = [left, right]
        self.leaf = False

    def is_full(self):
        """Returns True if the node is full."""
        return len(self.keys) == self.order

    def show(self, counter=0):
        """Prints the keys at each level."""
        print(counter, str(self.keys))

        # Recursively print the key of child nodes (if these exist).
        if not self.leaf:
            for item in self.values:
                item.show(counter + 1)

class BPlusTree(object):
    """B+ tree object, consisting of nodes.
    Nodes will automatically be split into two once it is full. When a split occurs, a key will
    'float' upwards and be inserted into the parent node to act as a pivot.
    Attributes:
        order (int): The maximum number of keys each node can hold.
    """
    def __init__(self, order=8):
        self.root = Node(order)

    def _find(self, node, key):
        """ For a given node and key, returns the index where the key should be inserted and the
        list of values at that index."""
        for i, item in enumerate(node.keys):
            if key < item:
                return node.values[i], i

        return node.values[i + 1], i + 1

    def _merge(self, parent, child, index):
        """For a parent and child node, extract a pivot from the child to be inserted into the keys
        of the parent. Insert the values from the child into the values of the parent.
        """
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
        """Inserts a key-value pair after traversing to a leaf node. If the leaf node is full, split
        the leaf node into two.
        """
        parent = None
        child = self.root

        # Traverse tree until leaf node is reached.
        while not child.leaf:
            parent = child
            child, index = self._find(child, key)

        child.add(key, value)

        # If the leaf node is full, split the leaf node into two.
        if child.is_full():
            child.split()

            # Once a leaf node is split, it consists of a internal node and two leaf nodes. These
            # need to be re-inserted back into the tree.
            if parent and not parent.is_full():
                self._merge(parent, child, index)

    def retrieve(self, key):
        """Returns a value for a given key, and None if the key does not exist."""
        child = self.root

        while not child.leaf:
            child, index = self._find(child, key)

        for i, item in enumerate(child.keys):
            if key == item:
                return child.values[i]

        return None

    def show(self):
        """Prints the keys at each level."""
        self.root.show()

    def add_list_to_bplustree(self, data):
        # Initial call to print 0% progress
        self.printProgressBar(0, len(data), prefix = 'Progress:', suffix = 'Complete', length = 50)
        add_start = time.time()
        for i, item in enumerate(data):
            data = item.split('?$')
            if data != '' and len(data) > 1:
                username = data[0].strip()
                article = data[1].strip()
                self.insert(username, article)
            # Update Progress Bar
            self.printProgressBar(i + 1, len(data), prefix = 'Progress:', suffix = 'Complete', length = 50)
        add_end = time.time()
        print('Total time: {}s.'.format(round(add_end - add_start, 5)))

    # Print iterations progress
    @staticmethod
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

if __name__ == '__main__':
    file_name = input('Please type in the path to your file and press "Enter":\n')
    dataset = importData(file_name) #import the dataset
    dataset_size = len(dataset) #get the size of the dataset
    print('You imported {} items'.format(dataset_size))
    save_data_for_testing = input('Do you want to keep some items for later Testing?(y/n)\n')

    if save_data_for_testing == 'y'or save_data_for_testing == 'Y':
        number_of_testing_items = input('How many items do you want to keep?\n')
        random.shuffle(dataset) #shuffle the dataset to enchance the randomness
        c_left_on_ds = 0 #counter for the items that was left on dataset
        c_took_out_from_dt = 0 #counter for the items that was popped from the dataset

        for x in range(int(number_of_testing_items)):
            choise = random.choice([True, False]) #choose if the it item will popped or left on the dataset
            position = random.randint(0, dataset_size-x) #get a random position from dataset
            if choise:
                return_value = dataset.pop(position) #pop item from the dataset
                c_took_out_from_dt += 1 #incease the counter    
                testing_dataset[return_value] = 1 #add the item to the testing dataset
            else:
                return_value = dataset[position] #get the item from the random position
                c_left_on_ds += 1 #increase the counter
                testing_dataset[return_value] = 0 #add the item to the testing dataset
        print('From the {} the {} left on the dataset and the other {} were left out in a new testing dataset.\n'.format(number_of_testing_items, c_left_on_ds, c_took_out_from_dt))
        
    node_size = int(input("Give node size:\n"))
    print('Initializing B+ tree...')
    bplus = BPlusTree(order=node_size)
    #Insert items from the dataset to bplus tree
    bplus.add_list_to_bplustree(dataset)
    # bplus.show()
    start = time.time()
    print(bplus.retrieve('Eatsofast'))
    end = time.time()
    print('Total time: {}s.'.format(round(end - start, 5)))