import bitarray 
from random import shuffle
import os.path
from os import path
import hashlib 
import murmurhash
import array
import math
import time
import hmac

results = list()
imported_data = list()
#Hash Functions
#We use sha256 for the best uniformity, but it is quite costly
hash_functions = [hashlib.sha256]

def importData():
    while True:
        file_name = input('Please type in the path to your file and press "Enter":')
        try:
            with open(file_name, 'r') as f:
                return f.read().split('\n')
            f.close()
        except FileNotFoundError:
            print('Wrong file or file path')
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
    new_filter = BloomFilter(None, int(num_items), None, int(num_of_hf))
    BloomFilter.import_bit_array(new_filter, file_name)
else:
    dataset = importData()
    num_items = input('How many items do you want to insert on the Bloom Filter?')
    if len(dataset) > int(num_items):
        print('The dataset that you imported is greater than the number of items you have declare that the BF possibly can handle.')
        num_items = input('Please enter the number of items again(take into consideration that the file \n that you imported containes {} items): '.format(len(dataset)))
    print('1-- Do you want to give the Probability of false positives and take the optimal number of hash functions and size of bit array?')
    print('2-- Do you want to insert custom values for the Bloom Filter?')
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
        new_filter = BloomFilter(float(prop_fp), int(num_items), None, None)
        new_filter.create_bit_array()
        print('Number of items: {}'.format(new_filter.number_of_items))
        print('Bit array size: {}'.format(new_filter.number_of_bits))
        print('Number of hash functions: {}'.format(new_filter.number_of_hf))
        print('Probability of false positives: {}'.format(new_filter.prop_false_positive))
    else:
        size_bit_array = input('Give the the size of the bit array:')
        num_of_hf = input('How many times you want to hash each item?')
        new_filter = BloomFilter(None, int(num_items), int(size_bit_array), int(num_of_hf))
        print('Number of items: {}'.format(new_filter.number_of_items))
        print('Bit array size: {}'.format(new_filter.number_of_bits))
        print('Number of hash functions: {}'.format(new_filter.number_of_hf))
        print('Probability of false positives: {}'.format(new_filter.prop_false_positive))
            
    # Initial call to print 0% progress
    printProgressBar(0, len(dataset), prefix = 'Progress:', suffix = 'Complete', length = 50)
    add_start = time.time()
    for i, item in enumerate(dataset):
        new_filter.add_item_to_filter(item, hash_functions[0])
        # Update Progress Bar
        printProgressBar(i + 1, len(dataset), prefix = 'Progress:', suffix = 'Complete', length = 50)
    add_end = time.time()

    print('Total time: {}s'.format(add_end - add_start))


# print('1-- Give the size of the BF and the Probability of false positives(fraction between 0 and 1).')
# print('2-- Give the size of the BF, the ')
# dataset = importData('../Datasets/ips.txt')
# l = len(dataset)

# test_count = 0
# test_dataset = importData('../Datasets/test_ips.txt')
# for i in range(0,100000):
#     test_dataset.append(dataset[i])
# test_dataset1 = test_dataset

# shuffle(test_dataset)
# shuffle(test_dataset)
# for size in range(1000000, 30000000, 1000000):
#     bit_array = bitarray(int(size))
#     bit_array.setall(0)
#     for count in range(1,20):
#         for func in hash_functions:
#             print(str(size) + ", " + str(count) + ", " + str(func))
#             # Initial call to print 0% progress
#             printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
#             curr_res = []
#             true_positive = 0
#             false_positive = 0
#             # Add all the items to the bloom filter
#             add_start = time.time()
#             for i, item in enumerate(dataset):
#                 add_item_to_filter(item, count, func, size)
#                 # Update Progress Bar
#                 printProgressBar(i + 1, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
#             add_end = time.time()
#             # Check which items are inside 
#             check_start = time.time()
#             for i, item in enumerate(test_dataset):
#                 if check_item(item, count, func, size) and item in test_dataset1:
#                         true_positive = true_positive + 1
#                 # Update Progress Bar
#                 printProgressBar(i + 1, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
#             check_end = time.time()
#             curr_res.append(str(size))
#             curr_res.append(count)
#             curr_res.append(func)
#             curr_res.append(add_end - add_start)
#             curr_res.append(check_end - check_start)
#             curr_res.append(true_positive)
#             curr_res.append(false_positive)
#             results.append(curr_res)
#             print(results)

# results.append(test_count)
# print(results)
# exportData('results.txt', results)
