import string

f = open("data.txt","r")
data = f.read()
import re


data.strip()
text2=data.lower()

SplittedData= text2.split()
print(SplittedData)

print("Enter the value of k")
valueK = 3

Shingle=[]
uniqueShingles=[]

for i in range(0,len(SplittedData)-3+1):
      Shingle = SplittedData[i:i+valueK]
      Shingle = ' '.join(Shingle)

      print(Shingle)

      if Shingle not in uniqueShingles:
          uniqueShingles.append(Shingle)
      else:
          del Shingle
print(uniqueShingles)
      
  
        
      
      



   
        
     