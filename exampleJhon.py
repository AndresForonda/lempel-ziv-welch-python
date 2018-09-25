#!/usr/bin/python3
import sys
import argparse #arguments management
import BitVector
import io  
            




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
    type=argparse.FileType('r'),
    default=sys.stdin,
    help='Archivo a comprimir o descomprimir',
)
args = parser.parse_args()

#variables
dictionary = {} 
text = ""
toCompare = ""
toStoreInteger = 257



#algorithm

#Preload ascii to dictionary
for i in range(256):
  bitString = bin(i)[2:]
  dictionary[chr(i)] = BitVector.BitVector(bitstring = bitString)

#compress algorithm
if args.action == "c":

  


  text = args.file.read()
  for letter in text:

    toCompare += letter
    if toCompare in dictionary:
      continue
    else:
      bitString = bin(toStoreInteger)[2:]
      dictionary[toCompare] = BitVector.BitVector(bitstring = bitString)
      toCompare = toCompare[-1]
      toStoreInteger+=1

  maxBinLenght = len( bin(toStoreInteger) ) - 2 #longitud del ultimo binario almacenado
  print("numero maximo de bits = ",maxBinLenght)

  for key in dictionary:
    value = dictionary[key]
    sizeToFill = maxBinLenght - value.length() 
    zeroFill = BitVector.BitVector(size = sizeToFill )
    value = zeroFill + value 
    print(key,"\t\t:",value )

#Restricciones importantes: longitud de bitstring multiplo de 8.
# bv  =  BitVector.BitVector(bitstring = '000011') 
# print( str(bv) )
# FILEOUT = open('output.bits', 'wb')
# bv.write_to_file(FILEOUT)
# FILEOUT.close()

# bv1  =  BitVector.BitVector(filename = 'output.bits')
# BitVector.BitVector()
# bis = bv1.length()
# bv1 =  bv1.read_bits_from_file(bis)
# print(bv1)



#uncompress algoritm
if args.action == "u":
  print("descomprimiendo")