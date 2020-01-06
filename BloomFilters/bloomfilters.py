import bitarray 
from random import shuffle
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

# bit_array = bitarray(int(size_of_filter))
# bit_array.setall(0)

def importData(input_filename):
    with open(input_filename, 'r') as f:
        return f.read().split('\n')

def exportData(output_filename, output_data):
    with open(output_filename, 'w') as f:
        for items in output_data:
            f.write("%s\n" %items)
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
            self.prop_false_positive =  self.calc_prop_false_positive
        elif prop_false_positive is not None:
            self.number_of_items = number_of_items
            self.number_of_bits = self.calc_number_of_bits
            self.number_of_hf = self.calc_number_of_hf
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

    def create_bit_array(self, number_of_bits):
        self.bit_array = bitarray.bitarray(int(number_of_bits))
        self.bit_array.setall(0)

    def exportBitArray(self, name):
        self.name = name + '.bin'
        with open(self.name, 'wb') as f:
            self.bit_array.tofile(f)
        f.close()

    def import_bit_array(self, name):
        self.name = name + '.bin'
        self.bit_array = bitarray.bitarray()
        with open('bit_array.bin', 'rb') as f:
            self.bit_array.fromfile(f)
        f.close()
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
    file_name = input('Give the name of the file(without extension):') 
    items = input('Give the number of items you initially intended to import to the BF:')
    num_of_hf = input('Give the number of hash functions you initially intended to use:')
    new_filter = BloomFilter(None, int(items), None, int(num_of_hf))
    BloomFilter.import_bit_array(new_filter, file_name)

# num_items = input('How many items do you want to insert on the Bloom Filter?')

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
