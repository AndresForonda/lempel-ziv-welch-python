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
args = parser.parse_args()

#variables
dictionary = {} #store dictionary


#algoritm
if args.action == "c":
  print("comprimiendo")

if args.action == "u":
  print("descomprimiendo")