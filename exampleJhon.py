#!/usr/bin/python3
import sys

dictionary = {}
print()
if len(sys.argv) == 1:
    print('Parametros:\nUse -c para comprimir\nUse -u para descomprimir.')

else:
  if sys.argv[1] == "-c":
    print('comprimiendo')

  if sys.argv[1] == "-u":
    print('descomprimiendo')  