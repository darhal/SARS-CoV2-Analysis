import numpy as np

from src.stats import *

###### Test de la fonction mediane_nucleotide ######

print(mediane_nucleotide(fasta_to_genome("./genome/dix_sequences.fasta")))

####################################################

###### Test de la fonction mediane_nucleotide ######

print(variance_nucleotide(fasta_to_genome("./genome/dix_sequences.fasta")))

####################################################

def add(a, b):
    return a + b

def mult(a, b):
    return a * b

def apply_math(fnc, a, b):
    return fnc(a, b)

print(apply_math(add, 5, 3))
print(apply_math(mult, 5, 3))

def fnct_generatrice(convert, analyse_stat, param):
    return analyse_stat(convert(param))

def convert_arn_to_nuermicals(arnm):
    pass
