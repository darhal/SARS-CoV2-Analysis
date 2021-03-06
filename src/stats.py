import math

from os import stat
from src.utility import *
from src.codon import *

#####################################
# FONCTION STATS DE BASE            #
#####################################

def moyenne(list):
    ''' La fonction fait la moyenne des valeurs d'une liste

    Args :
        list : liste de valeurs

    Returns :
        la moyenne des valeurs
    '''
    if not list:
        return None
    
    res = 0

    for k in list:
        res += k
    return res / len(list)


def mediane(list):
    ''' La fonction donne la médiane de l'échantillon

    Args :
        list : liste de valeurs

    Returns :
        la médiane de la liste
    '''
    if not list:
        return None

    L = sorted(list)
    n = len(L)

    if n%2 == 0:
        return (L[n//2] + L[n//2-1]) / 2
    else:
        return L[(n-1) // 2]


def quartile(list, n):  # quartile(2,list) est la médiane
    ''' La fonction donne le quartile (1er, 2e, ou 3e) de l'échantillon

    Args :
        list : liste de valeurs

    Returns :
        le quartile (1er, 2e, ou 3e) de la liste
    '''
    if not list:
        return None
    if n not in [1, 2, 3]:
        return None
    if n == 2:  # la médiane
        return mediane(list)

    L = sorted(list)
    t = len(list)

    if t % 4 == 0:
        if n == 1:
            return L[t//4 - 1]
        elif n == 3:
            return L[3*t//4]
    else:
        if n == 1:
            return L[t//4]
        elif n == 3:
            return L[int(3*t/4)]


def intervalle_interquartile(list):
    '''La fonction calcule l'intervalle interquartile (Q3-Q1) d'une liste de valeurs en entrée (list)

    Args:
        list: une liste de valeurs

    Returns:
        la valeur de l'invertalle interquartile (Q3-Q1) de la liste d'entrée
    '''
    if not list:
        return None
    return quartile(list, 3) - quartile(list, 1)


def variance(list):
    ''' La fonction calcule la variance de l'échantillon

    Args :
        list : liste de valeurs

    Returns :
        la variance de la liste
    '''
    if not list:
        return None

    res = 0
    m = moyenne(list)

    for k in list:
        res += (m-k)**2
    return res / len(list)


def ecart_type(list):
    ''' La fonction calcule l'écart-type de l'échantillon

    Args :
        list : liste de valeurs

    Returns :
        l'écart-type de la liste
    '''
    if not list:
        return None
    return math.sqrt(variance(list))

#####################################
# FONCTION SUR LES PROPORTIONS      #
#####################################

def proportions(sequence, sampler):
    '''Retourne un dictionaire contenant les proportions des différents éléments de la séquence.

    Args:
        sequence : The ARNm or codons sequence (type : string)
        sampler : The list of elements to sample (ARMm nucleotides or Amino-acids) (type : list)

    Returns:
        dico_proportions : Dictionnaire associant les proportions aux éléments de la séquence
    '''

    dico_nombre_elements = nombre_elements(sequence, sampler)
    taille = len(sequence)
    if taille == 0:
        return {s: 0 for s in sampler}
    
    dico_proportions = {}
    
    for element in dico_nombre_elements:
        dico_proportions[element] = dico_nombre_elements[element] / taille

    return dico_proportions


#####################################
# FONCTIONs BOOTSTRAP               #
#####################################

def call_stat_taille_genome(stat_func, tab, *args):
    '''Fonction generale qui appelle les autres fonctions statistiques sur les tailles de genomes

    Args:
        stat_func:  fonction statistique à appeler
        tab:        tableau des sequances ARN ou Acides aminés
        *args:      arguments supplémentaires optionelle
    
    Returns: 
        les reusltats statistiques
    '''
    tailles = taille_ensemble(tab)
    return stat_func(tailles, *args)


def perform_all_stats_taille(sequences):
    '''Fonction generale qui fait tout l'analyse statistique sur la taille des séquences

    Args:
        sequences:  l'échantillon

    Returns:
        Dictionnaire qui contients les stats
    '''
    # Optimise this function by calling nombre_element_echantillion outside
    # nbr_elm_ech = nombre_element_echantillon(sequences, sampler)
    stats = {}
    stats["moy"] = call_stat_taille_genome(moyenne, sequences)
    stats["med"] = call_stat_taille_genome(mediane, sequences)
    stats["ecartt"] = call_stat_taille_genome(ecart_type, sequences)
    stats["var"] = call_stat_taille_genome(variance, sequences)
    stats["quart1"] = call_stat_taille_genome(quartile, sequences, 1)
    stats["quart3"] = call_stat_taille_genome(quartile, sequences, 3)
    stats["int_quart"] = call_stat_taille_genome(intervalle_interquartile, sequences)
    return stats


def call_stat(stat_func, sequences, sampler, *args):
    '''Fonction general qui appelle les autres fonctions statistiques

    Args:
        stat_func:  fonction statistique à appeler
        sequences:  tableau des sequences ARN, Acides aminés
        sampler:    les valeurs à prendre comme des echantillons
        *args:      arguments supplémentaires optionelle

    Returns: 
        Dictionnaire qui à le retoure de la fonction
    '''
    nbr = nombre_element_echantillon(sequences, sampler)
    return call_stat_on_echantillon(stat_func, nbr, *args)


def call_stat_on_echantillon(stat_func, nb_elm_ech, *args):
    '''Fonction generale qui appelle les autres fonctions statistiques

    Args:
        stat_func:  fonction statistique à appeler
        nb_elm_ech: nombre elements echantillon d'une séquence donnée
        *args:      argument supplémentaire optionelle
    
    Returns: 
        Dictionnaire qui à le retoure de la fonction
    '''
    list_element = list(nb_elm_ech.keys())
    d = {s: 0 for s in list_element}

    for element in list_element:
        d[element] = stat_func(nb_elm_ech[element], *args)

    return d


def call_stat_prop(stat_func, sequences, sampler, *args):
    '''Fonction generale qui appelle les autres fonctions statistiques pour les proportions

    Args:
        stat_func:  fonction statistique à appeler (moyenne, mediane, quartile, intervalle_interquartile, variance, ecart_type)
        sequences:  tableau des sequances ARNm ou d'Acides aminés
        sampler:    les valeurs à prendre comme des echantillons (NUCLEOTIDES ou AMINO_ACIDS)
        *args:      arguments supplémentaires optionel (notamment n pour l'appel de quartile)

    Returns: 
        Dictionnaire qui à le retoure de la fonction
    '''
    dicos = [proportions(sequence, sampler) for sequence in sequences]
    resultat = {}

    for element in sampler:
        liste = [dico[element] for dico in dicos]
        resultat[element] = stat_func(liste, *args)

    return resultat


def perform_all_stats_prop(sequences, sampler):
    '''Fonction generale qui fait tout l'analyse statistique sur la proportion des nucléotides dans les séquences

    Args:
        sequences:  l'échantillon
        sampler : la base laquelle prendre comme des échantillons (NUCLEOTIDES ou AMINO_ACIDS)

    Returns:
        Dictionnaire qui contients les stats
    '''
    stats = {}
    stats["moy"] = call_stat_prop(moyenne, sequences, sampler)
    stats["med"] = call_stat_prop(mediane, sequences, sampler)
    stats["ecartt"] = call_stat_prop(ecart_type, sequences, sampler)
    stats["var"] = call_stat_prop(variance, sequences, sampler)
    stats["quart1"] = call_stat_prop(quartile, sequences, sampler, 1)
    stats["quart3"] = call_stat_prop(quartile, sequences, sampler, 3)
    stats["int_quart"] = call_stat_prop(intervalle_interquartile, sequences, sampler)
    return stats


def perform_all_stats(sequences, sampler):
    '''Fonction general qui fait tout l'analyse statistique

    Args:
        stat_func:  fonction statistique à appeler
        sampler:    les valeurs à prendre comme des echantillons
    
    Returns: 
        Dictionnaire qui contients les stats
    '''
    # Optimise this function by calling nombre_element_echantillion outside
    nbr_elm_ech = nombre_element_echantillon(sequences, sampler)
    stats = {}
    stats["moy"]        = call_stat_on_echantillon(moyenne, nbr_elm_ech)
    stats["med"]        = call_stat_on_echantillon(mediane, nbr_elm_ech)
    stats["ecartt"]     = call_stat_on_echantillon(ecart_type, nbr_elm_ech)
    stats["var"]        = call_stat_on_echantillon(variance, nbr_elm_ech)
    stats["quart1"]     = call_stat_on_echantillon(quartile, nbr_elm_ech, 1)
    stats["quart3"]     = call_stat_on_echantillon(quartile, nbr_elm_ech, 3)
    stats["int_quart"]  = call_stat_on_echantillon(intervalle_interquartile, nbr_elm_ech)
    return stats
