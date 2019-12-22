#import the libraries that we are going to be used later
import string
from numpy import linalg as la
import numpy as np
import math as m
from collections import OrderedDict

#this function checks if k is smaller than the binomial coefficient 
def binomial_coefficient(n):
    binom = int(m.factorial(n) / (m.factorial(2)*m.factorial(n-2))) #n!/(2!*(n-2)!)
    k = int(input("Give K(must be smaller than " + str(binom) + "):" ))
    if n == 2: #if the number of documents is 2 then we give k the value of 1 because is the only value that k can match with
        return 1
    elif k < binom: #if k is smaller than the binomial coefficient then we return the value of k
        return k
    else: #in any other case we return as k the value of 1 because its the default value
        print("K must be smaller than " + str(binom) + ".")
        print("Default K = 1.")
        return 1

#lists and dictionary that we will be used later
similarity = dict()
dictionary = list()
file_names = list()
doc_count = list()

number_of_docs = int(input("How many documents do you want to insert:"))
while number_of_docs == 1: #if user give only one document then the program ask the user again for the number of bocuments
    number_of_docs = int(input("Give number of documents again:"))

for x in range(number_of_docs):
    print('Give the', x+1, 'document name:')
    name = input() #takes as input the name of the document
    if name.endswith('.txt'):
        file_names.append(name) #add the name to a list
    else: #checks if the document is a txt file
        print('You must insert document with \"txt\" extension!')
        exit()

K = int(binomial_coefficient(number_of_docs)) 

for x in range(number_of_docs): #opens one by one the files 
    file = "Documents/" + file_names[x]  
    with open(file, 'r') as f: 
        for line in f: #reads the lines of the document
            for word in line.split(): #splits the lines into words
                if word in dictionary: #if the word is already into the list ignore the word
                    continue
                else: #add the word to the list without punctuation and in lowercase
                    dictionary.append(word.translate(str.maketrans('', '', string.punctuation)).lower()) 

for x in range(number_of_docs):
    count = list(0 for i in range(len(dictionary))) #initialize the list with zeros
    with open(file_names[x], 'r') as f:
        for line in f:
            for word in line.split(): 
                position = dictionary.index(word.translate(str.maketrans('', '', string.punctuation)).lower()) #searches for the word into the list in order to find the index number
                count[position] = count[position] + 1 #in position of the index, increases the counter by 1
    doc_count.append(count)


for i in range(0, number_of_docs):
    for j in range(i, number_of_docs):
        if i == j:
            continue
        doc1 = doc_count[i]
        doc2 = doc_count[j]

        norm1 = la.norm(doc1, ord=2) #calculates the norm-2 for the first doc
        norm2 = la.norm(doc2, ord=2) #calculates the norm-2 for the first doc

        dot_product = np.dot(doc1,doc2) #calculates the dot product for the documentes
        result = dot_product / (norm1 * norm2) #calculates cosine

        pair_of_docs = file_names[i] + " and " + file_names[j]
        temp = {pair_of_docs:result}
        similarity.update(temp)

sortedDict = (OrderedDict(sorted(similarity.items(), key=lambda x: x[1], reverse = True)[0:K])) #sort the first K results in order to take the most similar documents
print("\nTop K Similar Documents listed below:")

for key in sortedDict: #prints the results in the appropriate format
    print(key + " %.2f" % sortedDict[key] + ", " + str(round(sortedDict[key], 2)*100) + "%")