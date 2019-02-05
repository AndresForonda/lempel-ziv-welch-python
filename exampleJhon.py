#!/usr/bin/python3
import sys
import argparse  # arguments management
from bitarray import bitarray
from collections import deque


# arguments management
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
    type=argparse.FileType('r', encoding='utf-8-sig'),
    help='Archivo a comprimir ',
    required=False,
)
args = parser.parse_args()


# variables


# compress algorithm
if args.compress:
    dictionary = {}
    print("comprimiendo")
    # variables
    text = ""
    toCompare = ""
    toStoreInteger = 257
    dq = deque()
    binaryFile = bitarray()
    lenghtBinary = 0

    # Preload ascii to dictionary
    for i in range(256):
        bitString = bin(i)[2:]
        dictionary[chr(i)] = bitarray(bitString)

    # algorithm
    text = args.compress.read()
    # print( text.isprintable() )
    # print( type(text) )
    for letter in text:
        toCompare += letter
        #print(str(toCompare in dictionary)+":"+toCompare+":"+toCompare[:-1])
        if toCompare in dictionary:
            continue
        else:

            bitString = bin(toStoreInteger)[2:]
            dictionary[toCompare] = bitarray(bitString)
            inDictionary = dictionary[toCompare[:-1]]

            dq.append(inDictionary)
            # print(inDictionary)
            toCompare = toCompare[-1]
            toStoreInteger += 1

    # longitud del ultimo binario almacenado
    maxBinLenght = len(bin(toStoreInteger)) - 2

    lenghtBinary = bin(maxBinLenght)[2:]
    lengtFill = 8 - len(lenghtBinary)
    aleatoryToFill = bitarray(lengtFill)
    aleatoryToFill.setall(0)
    binaryLenghFile = aleatoryToFill + bitarray(lenghtBinary)
    binaryFile += binaryLenghFile

    for value in dq:
        # print(value)
        sizeToFill = maxBinLenght - value.length()
        #print(maxBinLenght,value.length() )
        zeroFill = bitarray(sizeToFill)
        zeroFill.setall(0)
        value = zeroFill + value

        binaryFile += value

    # for i in dictionary:
    #   print(i,dictionary[i])

    fileBin = open('out.bits', 'wb')
    binaryFile.tofile(fileBin)
    fileBin.close()
    # for i in dictionary:
    #   print(i,dictionary[i] )

# uncompress algoritm
if args.decompress:
    # variables
    dictionary = {}
    binaryFile.fromfile(args.decompress)  # Archivo binario a descomprimir
    lenghtCode = int(binaryFile[0:8].to01(), 2)  # longitud de los codigo
    decompressed = ''
    key = 257

    codeBefore = dictionary[binaryFile[8:8 + lenghtCode].to01()]
    overfit = (binaryFile.length() - 8) % 9
    decompressed += codeBefore

    for i in range(8 + lenghtCode, binaryFile.length() - overfit, lenghtCode):
        codeNow = dictionary[binaryFile[i:i + lenghtCode].to01()]
        if codeNow is None:
            break
        keyBits = bin(key)[2:]
        numberZeros = lenghtCode - len(keyBits)
        keyString = '0' * numberZeros + keyBits
        dictionary[keyString] = codeBefore + codeNow[0]
        decompressed += codeNow
        key += 1
        codeBefore = codeNow

    with open('result', 'w') as file:
        file.write(decompressed)
