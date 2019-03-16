# Laboratorio de sistemas de telecomunicaciones II
Desarrollo de laboratorio de sistemas de telecomunicaciones, aplicación que implementa el algoritmo LZW y Huffman para compresión de archivos de texto en python.

# Lempel Ziv Welch

## Proceso de compresión:

Solo se admiten documentos de texto (txt) para hacer el proceso de compresión. Al comprimir un archivo la salida del proceso entrega un archivo con el nombre out.bits.

Para correr el compresor es necesario usar la siguiente sintaxis:

```
# python lzw.py --compress file.txt
```

  * Se puede usar -c como abreviación de --compress

## Proceso de descompresión:

Solo se admiten archivos que hayan pasado por el proceso de compresión, es decir con extensión .bits, para hacer el proceso de descompresión. Al descomprimir un archivo la salida del proceso entrega un archivo con el nombre result.txt.

Para correr el descompresor es necesario usar la siguiente sintaxis:

```
# python lzw.py --descompress file.bits
```

  * Se puede usar -d como abreviación de --descompress

