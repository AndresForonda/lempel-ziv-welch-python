import heapq
import argparse  # arguments management
from collections import Counter
import json
import threading


def getProbabilityTable(text):
    counter = Counter(text)
    sumCounter = sum(counter.values())
    probabilityTable = [[num / sumCounter, character, []]
                        for character, num in counter.items()]
    return probabilityTable


def make_tree(probs):
    heapq.heapify(probs)
    while len(probs) > 1:

        e1 = heapq.heappop(probs)  # El símbolo menos probable
        e2 = heapq.heappop(probs)  # El segundo menos probable
        nw_e = [e1[0] + e2[0], "", [e1, e2]]
        heapq.heappush(probs, nw_e)


def followBranch(branch):
    if type(branch[2]) is list and len(branch[2]) == 2:
        branch0 = branch[2].pop()
        branch0[1] = ''.join([branch[1], "0"])
        branch1 = branch[2].pop()
        branch1[1] = ''.join([branch[1], "1"])

        followBranch(branch0)
        followBranch(branch1)
        pass
    else:
        print(branch, branch[1])


def makeDictionary(tree):
    pass


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
    print("comprimiendo")
    probabilityTable = {}
    text = args.compress.read()  # texto del archivo a comprimir
    # making probabilityTable
    probabilityTable = getProbabilityTable(text)
    print(json.dumps(probabilityTable))
    print(len(probabilityTable))
    make_tree(probabilityTable)
    print(json.dumps(probabilityTable))
    followBranch(probabilityTable[0])


# Para recorrer el arbol. Revisando el segundo elemento heapq si es dict,
# tiene hilos
