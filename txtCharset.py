#!/usr/bin/python3
import argparse #arguments management

#arguments management
parser = argparse.ArgumentParser("verificar ")
parser.add_argument(
    '-f',
    '--file',
    type=argparse.FileType('r',encoding='utf-8-sig'),    
    help='Archivo a observar charset ',
    required=True
)
args = parser.parse_args()
listCodes = []

text = args.file.read()
#text = text.encode('iso-8859-1')
#text = text.encode('latin1')
#8221
for letter in text:
    code = ord(letter)
    if code in listCodes:
        continue
    else:
        listCodes.append(code)
    #print(listCodes)

listCodes.sort()
print( listCodes )

