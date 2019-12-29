from bitarray import bitarray 
import array
import hashlib 

imported_data = list()
hash_functions = [hashlib.md5, hashlib.sha256]

# Number of bits in the filter
size_of_filter = input("Specify the number of bits in the filter: ")

bit_array = bitarray(int(size_of_filter))
bit_array.setall(0)

def exportBitArray(input_array):
    with open('bit_array.bin', 'wb') as f:
        input_array.tofile(f)
    f.close()

def importBitArray(output_array):
    with open('bit_array.bin', 'rb') as f:
        output_array.fromfile(f)
    f.close()

def importData(input_filename):
    with open(input_filename, 'r') as f:
        return f.read().split('\n')

def exportData(output_filename, output_data):
    with open(output_filename, 'w') as f:
        for items in output_data:
            f.write("%s\n" %items)
    print('The data exported successfully')

def add_item_to_filter(item):
    for i in range(len(hash_functions)):
        hash_object = hash_functions[i](item.encode())
        hex_value = hash_object.hexdigest()
        convert_to_base10 = int(hex_value, base=16)
        position = convert_to_base10 % int(size_of_filter)
        print(position)
        bit_array[position] = 1

def check_item(item):
    for i in range(len(hash_functions)):
        hash_object = hash_functions[i](item.encode())
        hex_value = hash_object.hexdigest()
        convert_to_base10 = int(hex_value, base=16)
        position = convert_to_base10 % int(size_of_filter)
        if bit_array[position] == 0:
            return False
    return True
