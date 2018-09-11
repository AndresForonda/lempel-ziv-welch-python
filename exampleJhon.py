#!/usr/bin/python3
import sys
import argparse #arguments management


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
dictionary = {} #store dictionary
text = ""
toCompare = ""
toStoreInteger = 257


#algoritm

#Preload ascii to dictionary
for i in range(256):
  dictionary[chr(i)] = bin(i)

#compress algoritm
if args.action == "c":
  print("comprimiendo")
  text = args.file.read()
  print(text)
  for letter in text:
    toCompare += letter
    if toCompare in dictionary:
      continue
    else:
      dictionary[toCompare] = bin(toStoreInteger)
      toCompare = toCompare[-1]

  for k in dictionary:
    print(k,dictionary[k])



#uncompress algoritm
if args.action == "u":
  print("descomprimiendo")