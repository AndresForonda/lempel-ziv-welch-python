
import argparse  # arguments management
from bitarray import bitarray
from collections import deque


def printDictionary(dictionary):

    for key in dictionary:
        value = dictionary[key]
        if type(bitarray("00")) == type(value):
            print(int(value.to01(), 2), ":" + key + ":")
        else:
            print(key, ":" + value + ":")


def getStringFromBeginBinaryCode(begin, lenghtCode, dictionary):
    code = binaryFile[begin:begin + lenghtCode]
    codeInt = int(code.to01(), 2)
    stringFromCode = dictionary.get(codeInt)
    return stringFromCode


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
    text = args.compress.read()  # texto del archivo a comprimir
    for letter in text:
        toCompare += letter
        # print(str(toCompare in dictionary)+":"+toCompare+":"+toCompare[:-1])
        if toCompare in dictionary:
            continue
        else:

            # cadena binaria del nuevo codigo para la nueva palabra
            bitString = bin(toStoreInteger)[2:]
            # agregar al diccionario la palabra y el codigo
            dictionary[toCompare] = bitarray(bitString)
            # extraer del diccionario el codigo para la palabra a
            # comprimir(palabra actual menos ultima letra)
            inDictionary = dictionary[toCompare[:-1]]
            # agregar a la cola el codigo de la palabra comprimida
            dq.append(inDictionary)
            # print(inDictionary)
            # mantener ultima letra de la palabra actual
            toCompare = toCompare[-1]
            # nuevo codigo para la siguiente palabra a agregar al diccionario
            toStoreInteger += 1
    dq.append(dictionary[text[-1]])
    # longitud del ultimo binario almacenado
    maxBinLenght = len(bin(toStoreInteger)) - 2
    print(maxBinLenght)
    # binario de la logitud
    lenghtBinary = bin(maxBinLenght)[2:]
    # tamaño a llenar de ceros para completar 8 bits con el binario de la
    # longitud
    lengtFill = 8 - len(lenghtBinary)
    # armando los ceros
    aleatoryToFill = bitarray(lengtFill)
    aleatoryToFill.setall(0)
    #  binario con la longitud de tamanio 8 bits
    binaryLenghFile = aleatoryToFill + bitarray(lenghtBinary)
    binaryFile += binaryLenghFile

    # armar cadena de ceros
    for value in dq:
        # print(value)
        sizeToFill = maxBinLenght - value.length()
        # print(maxBinLenght,value.length() )
        zeroFill = bitarray(sizeToFill)
        zeroFill.setall(0)
        value = zeroFill + value
        binaryFile += value

    # escribir archivo binario
    fileBin = open('out.bits', 'wb')
    binaryFile.tofile(fileBin)
    fileBin.close()


# uncompress algoritm
if args.decompress:
    print("descomprimiendo")
    # variables
    binaryFile = bitarray()
    dictionary = {}

    # diccionario base
    for i in range(256):
        dictionary[i] = chr(i)

    with open('out.bits', 'rb') as fileBits:
        binaryFile.fromfile(fileBits)
    # Archivo binario a descomprimir
    lenghtCode = int(binaryFile[0:8].to01(), 2)  # longitud de los codigo
    decompressed = ''
    key = 257
    lastString = ''
    lastString = getStringFromBeginBinaryCode(8, lenghtCode, dictionary)
    decompressed += lastString
    for begin in range(8 + lenghtCode, binaryFile.length() - lenghtCode, lenghtCode):
        inputString = getStringFromBeginBinaryCode(
            begin, lenghtCode, dictionary)

        if inputString:
            dictionary[key] = lastString + inputString[0]
            decompressed += inputString
            lastString = inputString
        else:
            dictionary[key] = lastString + lastString[0]
            decompressed += dictionary[key]
            lastString = dictionary[key]
        key += 1
    with open('result', 'w') as file:
        file.write(decompressed)
