# Creating the base dictionary
word = "Andres"
dictionary = {}
for i in range(256):
  dictionary[chr(i)] = bin(i)
