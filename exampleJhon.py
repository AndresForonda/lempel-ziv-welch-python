#!/usr/bin/python3
import sys
import argparse #arguments management

dictionary = {} #store dictionary

parser = argparse.ArgumentParser("compresor y descompresor lempel ziv")
parser.add_argument(
    '-a',
    '--action',
    required=True,
    help='Comprimir(c) o Descomprimir(u)',
    choices=('c', 'u'),
)
args = parser.parse_args()

if args.action == "c":
  print("comprimiendo")

if args.action == "u":
  print("descomprimiendo")