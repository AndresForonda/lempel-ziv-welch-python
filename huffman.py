

from heapq import heapify, heappush, heappop
from bitarray import bitarray
import argparse  # arguments management
from collections import Counter
from collections import deque
from functools import partial
from itertools import accumulate

# import json


def getProbabilityTable(text):
    counter = Counter(text)
    sumCounter = sum(counter.values())
    probabilityTable = [[num / sumCounter, character, []]
                        for character, num in counter.items()]
    return probabilityTable


def make_tree(probs):
    heapify(probs)
    while len(probs) > 1:

        e1 = heappop(probs)  # El símbolo menos probable
        e2 = heappop(probs)  # El segundo menos probable
        nw_e = [e1[0] + e2[0], "", deque([e1, e2])]
        heappush(probs, nw_e)


def followBranch(branch, dictionary):
    if type(branch[2]) is deque and len(branch[2]) == 2:
        branch0 = branch[2].pop()
        branch0[1] = ''.join([branch0[1], branch[1], "0"])
        branch1 = branch[2].pop()
        branch1[1] = ''.join([branch1[1], branch[1], "1"])

        followBranch(branch0, dictionary)
        followBranch(branch1, dictionary)
        pass
    else:
        dictionary[branch[1][0]] = (branch[1][1:])


def getLetterCompress(dictionary, letter):
    return dictionary[letter]


def mergeLetters(l1, l2):
    return l1 + l2

# arguments management
parser = argparse.ArgumentParser("compresor y descompresor Huffman")
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


if args.compress:
    # print("comprimiendo")
    dictionary = {}
    probabilityTable = {}
    text = args.compress.read()  # texto del archivo a comprimir
    # making probabilityTable
    probabilityTable = getProbabilityTable(text)
    # print(json.dumps(probabilityTable))
    # print(len(probabilityTable))
    make_tree(probabilityTable)
    # print(probabilityTable)
    followBranch(probabilityTable[0], dictionary)
    print(dictionary)

    compressLetter = partial(getLetterCompress, dictionary)

    lettersCom = map(compressLetter, text)
    restString = ''.join(lettersCom)
    binaryFile = bitarray(restString)
    with open('outHuffman.bits', 'wb') as fileBin:
        binaryFile.tofile(fileBin)
