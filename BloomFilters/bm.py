import bitarray
import hashlib 
import random
import hmac
import math
import time

hash_functions = [hashlib.sha256]
dataset = list()
testing_dataset = dict()

class BloomFilter:
    def __init__(self, prop_false_positive=None, number_of_items=None, number_of_bits=None, number_of_hf=None):
        if prop_false_positive is not None and number_of_bits is not None and number_of_hf is not None:
            self.number_of_items = number_of_items
            self.number_of_bits = number_of_bits
            self.number_of_hf = number_of_hf
            self.prop_false_positive = prop_false_positive
            self.create_bit_array()
            print('BloomFilter created successfully...')

    def create_bit_array(self):
        self.bit_array = bitarray.bitarray(int(self.number_of_bits))
        self.bit_array.setall(0)

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

    def add_list_to_filter(self, list_name, hash_function):
        # Initial call to print 0% progress
        self.printProgressBar(0, len(dataset), prefix = 'Progress:', suffix = 'Complete', length = 50)
        add_start = time.time()
        for i, item in enumerate(list_name):
            self.add_item_to_filter(item, hash_function)
            # Update Progress Bar
            self.printProgressBar(i + 1, len(dataset), prefix = 'Progress:', suffix = 'Complete', length = 50)
        add_end = time.time()
        print('Total time: {}s.'.format(round(add_end - add_start, 5)))

    @staticmethod
    def culc_optimal_params(fp_prop, bm_size):
        try:
            bit_array_size = math.ceil((bm_size * math.log(fp_prop)) / math.log(1 / pow(2, math.log(2))))
            hash_functions = round((bit_array_size / bm_size) * math.log(2))
            return (bit_array_size, hash_functions)
        except:
              print("Something went wrong")

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



def importData(file_name):
    while True:
        try:
            with open(file_name, 'r') as f:
                dataset = f.read().split('\n')
                return dataset
            f.close()
        except FileNotFoundError:
            print('Wrong file or file path')
            file_name = input('Please type in the path to your file and press "Enter":')

# 0:Ask the user if he wants to import an existed bit array
# 1:Import a file DONE
# 2:Ask if the number of items in the BM would be the same as the imported file DONE
# 3:If not ask for the final number of items DONE
# 4:Ask the user if he want to enter manual the parameters for the BM
# 5:If yes ask for the values and calculate the false positive propability
# 6:If not ask for the false positive propability and calculate the size of the bit array and the number of hash function
# 7:Create the BM with the above values
# 8:Insert the items from the list
# 9:Ask the user if he wants to enter a value manualy or check if a value exists in the BM
# 10:Ask the user if he wants to export the bit array on file for use on the next session 

exists_bit_array = input('Do you want to import an already existed Bit Array?(y/n)\n')
if exists_bit_array == 'y' or exists_bit_array == 'Y':
    pass
else: 
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
    
    size = input('Do you want to keep the size of the BM as the size of the file you inserted or your you want to make it larger for future use?(y/n)\n')
    if size == 'y' or size == 'Y':
        bm_size = int(dataset_size) #keep the initial size for the bm
    else:
        bm_size = int(input('Give the size of the Bloom Filter: \n')) #make the bm larger from the initial dataset

    parameters = input('Do you want to enter manualy the parameters for the Bloom Filter(y/n)?\n')
    if parameters == 'y' or parameters == 'Y':
        bit_array_size = input('Give the size of the bit array: \n')
        num_of_hf = input('Give the number of hash functions: \n')
    else:
        prop_false_positive = float(input('Give the propabilty of false positive: \n'))
        bit_array_size, num_of_hf = BloomFilter.culc_optimal_params(prop_false_positive, dataset_size)
    # Create Filter
    b_filter = BloomFilter(int(prop_false_positive), int(bm_size), int(bit_array_size), int(num_of_hf))
    b_filter.add_list_to_filter(dataset, hash_functions[0])
    while True:
        print('1-- Add item to the Bloom filter.')
        print('2-- Check if an item exists')
        print('3-- Test the BM using the testing dataset')
        print('4-- Exit')
        choise = None
        while choise is None:
            choise = input('Pick an option: ')
            if choise == '1':
                choise = 1
            elif choise == '2':
                choise = 2
            elif choise == '3':
                choise = 3
            elif choise == '4':
                exit(0)
            else:
                choise = None
                print('Please try again!')
        if choise == 1:
           value = input('Give the item that you want top insert: \n')
           b_filter.add_item_to_filter(value, hash_functions[0])
           print('The item was inserted successfully')