#!/usr/bin/python3
import sys
import argparse #arguments management
from bitarray import bitarray
from collections import deque
 
            




#arguments management
parser = argparse.ArgumentParser("compresor y descompresor lempel ziv")
parser.add_argument(
    '-a',
    '--action',
    required=True,
    help='Comprimir(c) o Descomprimir(u)',
    choices=('c', 'u'),
)
parser.add_argument(
    '-f',
    '--file',
    type=argparse.FileType('r',encoding='utf-8-sig'),
    default=sys.stdin,
    help='Archivo a comprimir o descomprimir',
)
args = parser.parse_args()

#variables
dictionary = {} 
text = ""
toCompare = ""
toStoreInteger = 257
dq = deque()
binaryFile = bitarray()


#algorithm

#Preload ascii to dictionary
for i in range(256):
  bitString = bin(i)[2:]
  dictionary[chr(i)] = bitarray(bitString) 

#compress algorithm
if args.action == "c":
  text = args.file.read()
  for letter in text:
    
    toCompare += letter
    if toCompare in dictionary:
      inDictionary=dictionary[toCompare]
      continue
    else:
      bitString = bin(toStoreInteger)[2:]
      dictionary[toCompare] = bitarray(bitString)     
      
      dq.append(inDictionary)
      toCompare = toCompare[-1]
      toStoreInteger+=1

  maxBinLenght = len( bin(toStoreInteger) ) - 2 #longitud del ultimo binario almacenado

  for value in dq: 
    #print(value)  
    sizeToFill = maxBinLenght - value.length() 
    zeroFill = bitarray(sizeToFill)
    zeroFill.setall(0)
    value = zeroFill + value 
                   
    binaryFile += value

  fileBin = open('out.bits','wb')
  binaryFile.tofile(fileBin)
  fileBin.close()

#uncompress algoritm
if args.action == "u":
  print("descomprimiendo")