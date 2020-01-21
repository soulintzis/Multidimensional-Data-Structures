from random import shuffle
import murmurhash
import bitarray 
import hashlib 
import array
import hmac
import math
import time

results = list()
imported_data = list()
#Hash Functions
#We use sha256 for the best uniformity, but it is quite costly
hash_functions = [hashlib.sha256]

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

class BloomFilter:
    def __init__(self, prop_false_positive = None, number_of_items = None, number_of_bits = None, number_of_hf = None):
        if prop_false_positive is None and number_of_bits is not None and number_of_hf is not None:
            self.number_of_items = number_of_items
            self.number_of_bits = number_of_bits
            self.number_of_hf = number_of_hf
            self.calc_prop_false_positive()
        elif prop_false_positive is not None:
            self.prop_false_positive = prop_false_positive
            self.number_of_items = number_of_items
            self.calc_number_of_bits()
            self.calc_number_of_hf()
        else:
            self.number_of_items = number_of_items
            self.prop_false_positive = prop_false_positive
            self.number_of_hf = number_of_hf
            self.number_of_bits = number_of_bits

    def add_item_to_filter(self, item, hash_function):
        for i in range(1, self.number_of_hf):
            hash_object = hmac.new(str(i).encode(), msg = item.encode(), digestmod = hash_function)
            hex_value = hash_object.hexdigest()
            convert_to_base10 = int(hex_value, base=16)
            position = convert_to_base10 % int(self.number_of_bits)
            self.bit_array[position] = 1

    def check_item(self, item, hash_function):
        for i in range(1, self.number_of_hf):
            hash_object = hmac.new(str(i).encode(), msg = item.encode(), digestmod = hash_function)
            hex_value = hash_object.hexdigest()
            convert_to_base10 = int(hex_value, base=16)
            position = convert_to_base10 % int(self.number_of_bits)
            if self.bit_array[position] == 0:
                return False
        return True

    def create_bit_array(self):
        self.bit_array = bitarray.bitarray(int(self.number_of_bits))
        self.bit_array.setall(0)

    def exportBitArray(self, name):
        self.name = name + '.bin'
        with open(self.name, 'wb') as f:
            self.bit_array.tofile(f)
        f.close()

    def import_bit_array(self, file_name):
        self.bit_array = bitarray.bitarray()
        while True:
            try:
                with open(file_name, 'rb') as f:
                    self.bit_array.fromfile(f)
                f.close()
            except FileNotFoundError:
                print("Wrong file or file path")
                file_name = input('Please type in the path to your binary file and press "Enter":')
            else:
                break
        self.number_of_bits = len(self.bit_array)
        self.calc_prop_false_positive()

    def calc_number_of_bits(self):
        self.number_of_bits = math.ceil((self.number_of_items * math.log(self.prop_false_positive))/math.log(1/math.pow(2,math.log(2))))

    def calc_prop_false_positive(self):
        self.prop_false_positive = round(math.pow(1 - math.exp(0-self.number_of_hf/(self.number_of_bits/self.number_of_items)), self.number_of_hf), 9)

    def calc_number_of_hf(self):
        self.number_of_hf = round((self.number_of_bits / self.number_of_items) * math.log(2))

        
print('---------------------------------------------------------------------------------------------')
exists_bit_array = input('Do you want to import an already existed Bit Array?(y/n)')
if exists_bit_array == 'y' or exists_bit_array == 'Y':
    file_name = input('Please type in the path to your binary file and press "Enter":')
    num_items = input('Give the number of items you initially intended to import to the BF:')
    num_of_hf = input('How many times you want to hash each item?')
    print()
    new_filter = BloomFilter(None, int(num_items), None, int(num_of_hf))
    BloomFilter.import_bit_array(new_filter, file_name)
else:
    file_name = input('Please type in the path to your file and press "Enter":')
    dataset = importData(file_name)
    num_items = input('How many items do you want to insert on the Bloom Filter?')
    if len(dataset) > int(num_items):
        print('The dataset that you imported is greater than the number of items you have declare that the BF possibly can handle.')
        num_items = input('Please enter the number of items again(take into consideration that the file \n that you imported containes {} items): '.format(len(dataset)))
    print('\n1-- Do you want to give the Probability of false positives and take the optimal number of hash functions and size of bit array?')
    print('2-- Do you want to insert custom values for the Bloom Filter?')
    print()
    optim_values = None
    while optim_values is None:
        optim_values = input('Choose one from the above:')
        if optim_values == '1':
            optim_values = True
        elif optim_values == '2':
            optim_values = False
        else:
            optim_values = None
            print('Please try again!')

    if optim_values:
        prop_fp = input('Give the Probability of false positives(fraction between 0 and 1):')
        print()
        new_filter = BloomFilter(float(prop_fp), int(num_items), None, None)
        new_filter.create_bit_array()
        print('Number of items: {}'.format(new_filter.number_of_items))
        print('Bit array size: {}'.format(new_filter.number_of_bits))
        print('Number of hash functions: {}'.format(new_filter.number_of_hf))
        print('Probability of false positives: {} \n'.format(new_filter.prop_false_positive))
    else:
        size_bit_array = input('Give the the size of the bit array:')
        num_of_hf = input('How many times you want to hash each item?')
        print()
        new_filter = BloomFilter(None, int(num_items), int(size_bit_array), int(num_of_hf))
        print('Number of items: {}'.format(new_filter.number_of_items))
        print('Bit array size: {}'.format(new_filter.number_of_bits))
        print('Number of hash functions: {}'.format(new_filter.number_of_hf))
        print('Probability of false positives: {} \n'.format(new_filter.prop_false_positive))
while True:
    print('1-- Add item to the Bloom filter.')
    print('2-- Check if an item exists')
    print('3-- Exit')
    add_or_check = None
    while add_or_check is None:
        add_or_check = input()
        if add_or_check == '1':
            add_or_check = True
        elif add_or_check == '2':
            add_or_check = False
        elif add_or_check == '3':
            exit(0)
        else:
            add_or_check = None
            print('Please try again!')
    print()
    if add_or_check:
        print('1-- Insert the items of the {} file into to the Bloom Filter.'.format(file_name))
        print('2-- Add only one item.')
        prompt = None
        while prompt is None:
            prompt = input()
            if prompt == '1':
                prompt = True
            elif prompt == '2':
                prompt = False
            else:
                prompt = None
                print('Please try again!')
        print()
        if prompt:
            # Initial call to print 0% progress
            printProgressBar(0, len(dataset), prefix = 'Progress:', suffix = 'Complete', length = 50)
            add_start = time.time()
            for i, item in enumerate(dataset):
                new_filter.add_item_to_filter(item, hash_functions[0])
                # Update Progress Bar
                printProgressBar(i + 1, len(dataset), prefix = 'Progress:', suffix = 'Complete', length = 50)
            add_end = time.time()
            print('Total time: {}s.'.format(round(add_end - add_start, 5)))
        else:
            input_item = input('Give the item that you want to insert: ')
            add_start = time.time()
            new_filter.add_item_to_filter(input_item, hash_functions[0])
            add_end = time.time()
            print('Total time: {}s.'.format(round(add_end - add_start, 5)))
    else:
        print('1-- Insert a file and check how many items are contained into the Bloom Filter')
        print('2-- Check for one item')
        prompt = None
        while prompt is None:
            prompt = input()
            if prompt == '1':
                prompt = True
            elif prompt == '2':
                prompt = False
            else:
                prompt = None
                print('Please try again!')
        print()
        if prompt:
            file_name = input('Please type in the path to your file and press "Enter":')
            test_dataset = importData(file_name)
            # Initial call to print 0% progress
            printProgressBar(0, len(test_dataset), prefix = 'Progress:', suffix = 'Complete', length = 50)
            counter = 0
            check_start = time.time()
            for i, item in enumerate(test_dataset):
                if new_filter.check_item(item, hash_functions[0]):
                    counter += 1
                # Update Progress Bar
                printProgressBar(i + 1, len(test_dataset), prefix = 'Progress:', suffix = 'Complete', length = 50)
            check_end = time.time()
            print('Total time: {}s'.format(check_end - check_start))
            print('{} items were inside the Bloom Filter out of the {}.'.format(counter, len(test_dataset)))
            print()
        else:
            input_item = input('Give the item that you want to check: ')
            add_start = time.time()
            if new_filter.check_item(input_item, hash_functions[0]):
                print('The item was inside the Bloom Filter.')
            else:
                print('The item was not inside the Bloom Filter.')
            add_end = time.time()
            print('Total time: {}s'.format(round(add_end - add_start, 5)))
            print()