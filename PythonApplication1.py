import string
import random
imported_data=''

dataset = list()

def printList(input_list):
    for x in range(len(input_list)):
        print(input_list[x])

try:
    with open("data-lsh.txt", 'r',  encoding='utf-8') as rfile:
        imported_data = rfile.read()
    rfile.close()
except FileNotFoundError:
    print('Something went wrong!')

for line in imported_data.split('\n'):
    if line != '':
        dataset.append(line.strip())

#Ask user to give a value for k
while True:
    try:
        k_value = int(input("Please enter k value for k-shingles: "))
    except ValueError:
        print("Your input is not valid. Give a positive natural number > 0...")
        continue
    if k_value <= 0:
        continue
    else:
        break

num_shingles = 0
document_shingle_sets = dict()

for data in dataset:
    # Split each document into words without punctuation
    words = list()
    for word in data.split():
        words.append(word.translate(str.maketrans('', '', string.punctuation)).lower()) 
    num_docs = 0
    document_id = words[0]
    words.remove(document_id)
    print(document_id)
    if (int(document_id) > num_docs):
        num_docs= document_id
    
    shingle = set()
    shingle_word_sets = set()

    for i in range(0, len(words) - int(k_value) + 1):
        shingle = words[i: i + int(k_value)]
        shingle = ' '.join(shingle)
        num_shingles = num_shingles + 1


        if shingle not in shingle_word_sets:
            shingle_word_sets.add(shingle)
        else:
            del shingle
            num_shingles = num_shingles - 1

    #print(num_shingles)

    document_shingle_sets[document_id] = shingle_word_sets
print("lista me shingles ", document_shingle_sets["1"])
          
matrix = [[0 for i in range(len(dataset )+ 1)] for j in range(num_shingles + 1)]

col_pos = 0
matrix[0][0] = None
for key in document_shingle_sets:
    matrix[0][col_pos + 1] = key
    col_pos = col_pos + 1

row_pos = 0
for key in document_shingle_sets:
    for item in document_shingle_sets[key]:
        matrix[row_pos + 1][0] = item
        row_pos = row_pos + 1
#print(matrix)
for i in range(len(matrix)):
    for y in range(1, len(matrix[i])):
        key = matrix[0][y]
        if matrix[i][0] in document_shingle_sets[key]:
            matrix[i][y] = 1

#printList(matrix)

#Ask user to give a value for hash functions to be used
while True:
    try:
        num_hashes = int(input("\nPlease enter how many permutations functions you want to be used: "))
    except ValueError:
        print("Your input is not valid. Give a positive natural number > 0...")
        continue
    if num_hashes <= 0:
        continue
    else:
        break

def pickPrimeNumber(shingles):
    if shingles % 2 == 0:
        return shingles + 1
    else:
        return shingles + 2
    

prime_num = pickPrimeNumber(num_shingles)

def generateRandomCoeffs(iter):
    coeffs = list()
    random.seed(random.randint(0, num_shingles))
    while iter > 0:
        random_coeff = random.randint(0, num_shingles)

        while random_coeff in coeffs:
            random_coeff = random.randint(0, num_shingles)

        iter = iter - 1
        coeffs.append(random_coeff)

    return coeffs      
     
rand_coeffs_A = generateRandomCoeffs(num_hashes)
rand_coeffs_B = generateRandomCoeffs(num_hashes)

#print('The following are the hash functions that were randomly generated:')
#for i in range(0, num_hashes):
#   print('{}. ({}x + {}) mod {} '.format(i+1, rand_coeffs_A[i], rand_coeffs_B[i], prime_num))

def generatePermutations(prime, num_hash, coeffs_A, coeffs_B):
    permutations = [[0 for i in range(prime - 1)] for j in range(num_hash)]
    
    for col in range(num_hash):
        for row in range(prime-1):
            # print('Row: {}, Col {}'.format(row, col))
            #print('{} ({} + {}) mod {} '.format(row, rand_coeffs_A[col], rand_coeffs_B[col], prime_num))
            permutations[col][row] = (coeffs_A[col]*row + coeffs_B[col])%prime
            # print(permutations[col][row])
    return permutations

permut = generatePermutations(prime_num, num_hashes, rand_coeffs_A, rand_coeffs_B)
#printList(permut)

def generate_signature_matrix(matrix, permutations,perm_number):
    signature_matrix = list()
    #print(permutations[1])
    for col in range(1,len(matrix[0])):
        ones_pos = list()
        for row in range( 1, len(matrix)):
            
            if matrix[row][col] == 1:
                permut_pos = permutations[perm_number][row - 1]
                # print(permut_pos)
                ones_pos.append(permut_pos)
            else:
                continue
        #print(ones_pos)
        signature_matrix.append(min(ones_pos))
    return signature_matrix

def generate_all_signatures(num_hash,matrix , permut):
    all_signatures = list()
    for i in range(num_hash):
        signature =  generate_signature_matrix(matrix, permut,i)
        all_signatures.append(signature)

    return all_signatures




print (" MAtrixes " ,matrix)
signatures = generate_all_signatures(num_hashes, matrix , permut)
printList(signatures)

def create_bands(all_signatures,num_of_bands,num_hash):
    bands = list()
    for i in range(int(num_hashes/num_of_bands)):
        tempband = all_signatures[i*num_of_bands:(i*num_of_bands)+num_of_bands]
        print(i)
        print(tempband)
        bands.append(tempband)

    return bands
num_bandes =int(input("\nPlease enter how many bands functions you want to be used: "))
bands = create_bands(signatures,num_bandes,num_hashes)

margin =int(input("\nPlease enter the margin you want for  comparison: "))
document_1 =int(input("\nPlease enter the first document you want to compare for partition: "))
document_2 =int(input("\nPlease enter the second document you want to compare for partition: "))

def create_hash_for_each_band(doc1,doc2):
    hashes = list()
    success= 0
    for bandie in bands:
        sum1 =0
        sum2 = 0
        hashvalue1=0
        hashvalue2 = 0
        for k in range(len(bandie)):
            sum1 = sum1 + bandie[k][doc1]
            sum2 = sum2 + bandie[k][doc2]
        if sum1%2==0:
            hashvalue1 = sum1/num_bandes
        else:
            hashvalue1 = sum1+1/num_bandes
        if sum2%2==0:
            hashvalue2 = sum2/num_bandes
        else:
            hashvalue2 = sum2+1/num_bandes
        print(hashvalue1,"1")
        print(hashvalue2,"2")
        if 100-((max(hashvalue1,hashvalue2)-min(hashvalue1,hashvalue2))/num_hashes)*100>margin:
            success=1
    if success == 1:
        print("Documents are paired and simillar")




print(create_hash_for_each_band(document_1,document_2))
