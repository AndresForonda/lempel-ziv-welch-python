#!/usr/bin/python3
import sys
import argparse #arguments management
from bitarray import bitarray
from collections import deque
 

#arguments management
parser = argparse.ArgumentParser("compresor y descompresor lempel ziv")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument(
    '-d',
    '--decompress',
    type=argparse.FileType('rb'),
    help='Archivo a descomprimir',
)
group.add_argument(
    '-c',
    '--compress',
    type=argparse.FileType('r',encoding='utf-8-sig'),    
    help='Archivo a comprimir ',
    required=False,
)
args = parser.parse_args()





#variables




#compress algorithm
if args.compress:
  dictionary = {}
  print("comprimiendo")
  #variables
  text = ""
  toCompare = ""
  toStoreInteger = 257
  dq = deque()
  binaryFile = bitarray()
  lenghtBinary = 0


  #Preload ascii to dictionary
  for i in range(256):
    bitString = bin(i)[2:]
    dictionary[chr(i)] = bitarray(bitString) 

  #algorithm
  text = args.compress.read()
  print( text.isprintable() )
  print( type(text) )
  for letter in text:
    toCompare += letter
    #print(str(toCompare in dictionary)+":"+toCompare+":"+toCompare[:-1]) 
    if toCompare in dictionary:
      continue
    else:
      
      bitString = bin(toStoreInteger)[2:]
      dictionary[toCompare] = bitarray(bitString)    
      inDictionary=dictionary[toCompare[:-1] ]
      
      dq.append(inDictionary)
      #print(inDictionary)
      toCompare = toCompare[-1]
      toStoreInteger+=1

  maxBinLenght = len( bin(toStoreInteger) ) - 2 #longitud del ultimo binario almacenado
  
  lenghtBinary = bin(maxBinLenght)[2:]
  lengtFill = 8 - len(lenghtBinary)
  aleatoryToFill =  bitarray(lengtFill)
  aleatoryToFill.setall(0)
  binaryLenghFile = aleatoryToFill + bitarray(lenghtBinary)
  binaryFile += binaryLenghFile

  for value in dq: 
    #print(value)  
    sizeToFill = maxBinLenght - value.length() 
    #print(maxBinLenght,value.length() )
    zeroFill = bitarray(sizeToFill)
    zeroFill.setall(0)
    value = zeroFill + value 
                   
    binaryFile += value

  # for i in dictionary:
  #   print(i,dictionary[i])
  
  

  fileBin = open('out.bits','wb')
  binaryFile.tofile(fileBin)
  fileBin.close()
  for i in dictionary:
    print( i,dictionary[i] )

#uncompress algoritm
if args.decompress:
  dictionary = {}
  
  #variables
  binaryFile = bitarray()
  binaryFile.fromfile(args.decompress) #Contiene el stream de bits
  lenghtCodes = {'binary':bitarray(),'number':0} #Longitud de todos los codigos en binaryFile
  code = {'chainBits':'','str':''} #Codigo indivitual(binario,numero,cadena)
  textUncompress = ''

  #lenghtBynary = binaryFile[0:8]
  lenghtCodes["binary"] = binaryFile[0:8]
  #lengtInt = ord( lenghtBynary.tostring() )
  lenghtCodes["number"] = ord( lenghtCodes["binary"].tostring() )


  #Preload ascii to dictionary int,character
  for i in range(256): 
    bitString = bin(i)[2:]
    numberZeros = lenghtCodes["number"] - len( bitString )
    bitString = '0'*numberZeros + bitString
    dictionary[ bitString ] =  chr(i) #diccionario (bits en string, cadena)


  
  for i in range(8, binaryFile.length() - lenghtCodes["number"] ,lenghtCodes["number"]):
    code["chainBits"] = binaryFile[i:i+lenghtCodes["number"]].to01()
    if code["chainBits"] in dictionary:
      code["str"] = dictionary[ code["chainBits"] ]
      textUncompress += code["str"]

  print(textUncompress)