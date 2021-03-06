def needleman(seq1, seq2, cost_table = None, cost_mat = None, key = None, verbose = False):
    '''Function that calculates the global alignement of two sequences
    
    Args:
        seq1: first sequence
        seq2: second sequence
        cost_table: contains the match, mismatch and the gap cost in this order (mutual exlusive with cost_mat)
        cost_mat: contains the cost matrix and the gap at the end (mutual exlusive with cost_table and used with key)
        key: the order of the letters in the cost matrix (mutual exlusive with cost_table)
            E.g: [  1, 2, 3, 1, 2, 3, 1, 2, 3, 4  ] key = "ABC"
                    |  |  |  |  |  |  |  |  |  |
                    A  A  A  B  B  B  C  C  C gap
                    A  B  C  A  B  C  A  B  C  
    
    Returns:
        An array contains one possible alignements with its score 
        E.g: [seq1 alignement, seq2 alignement, score]
    '''
    # Some sanity checks:
    if cost_table and cost_mat and key:
        print("Error: cost_mat and key are mutually exlusive with cost_table, please use the one or the other")
        return
    
    if cost_table and len(cost_table) != 3:
        print("Error: cost_table must be of length 3 and contain the match, mismatch and the gap respectively ")
        return
    
    if not cost_table and ((not cost_mat and key) or (cost_mat and not key)):
        print("Error: cost_mat and key must be defined togther")
        return

    if cost_mat and key and len(cost_mat) != len(key) ** 2 + 1:
        print("Error: cost_mat must have the same length of the suqare of the length of key^2 + 1 (the last number is the gap)")
        return
    
    letter_dict = {}
    gap = 0

    if key and cost_mat:
        letter_dict = { key[i]: i for i in range(len(key)) }
        gap = cost_mat[len(key) ** 2]
    else:
        gap = cost_table[2]

    def get_cost(letter1, letter2):
        if key and cost_mat:
            return cost_mat[letter_dict[letter1] * len(key) + letter_dict[letter2]]
        else:
            if letter1 == letter2:
                return cost_table[0]
            else:
                return cost_table[1]

    len_seq1, len_seq2 = len(seq1), len(seq2)
    alignement_mat = [ [ 0 for _ in range(len_seq1 + 1) ] for _ in range(len_seq2 + 1) ]

    # Init step:
    for i in range(1, len_seq1+1):
        alignement_mat[0][i] = alignement_mat[0][i - 1] + gap

    for j in range(1, len_seq2+1):
        alignement_mat[j][0] = alignement_mat[j - 1][0] + gap

    # Filling:
    for j in range(1, len_seq2+1):
        for i in range(1, len_seq1+1):
            left_val = alignement_mat[j][i - 1] + gap
            up_val = alignement_mat[j - 1][i] + gap
            diag_val = alignement_mat[j - 1][i - 1] + get_cost(seq1[i - 1], seq2[j - 1])
            alignement_mat[j][i] = max(max(left_val, up_val), diag_val)

    # Trace back:
    coord = (len_seq2, len_seq1)
    output_seq1 = ""
    output_seq2 = ""
    coord_path = []
    coord_path.append(coord)

    while coord != (0, 0):
        cost = get_cost(seq1[coord[1] - 1], seq2[coord[0] - 1])
        if coord[0] == 0:
            coord = (coord[0], coord[1] - 1)
            output_seq1 = seq1[coord[1]] + output_seq1
            output_seq2 = '-' + output_seq2
        elif coord[1] == 0:
            coord = (coord[0] - 1, coord[1])
            output_seq1 = '-' + output_seq1
            output_seq2 = seq2[coord[0]] + output_seq2
        elif alignement_mat[coord[0] - 1][coord[1] - 1] + cost == alignement_mat[coord[0]][coord[1]]: 
            coord = (coord[0] - 1, coord[1] - 1)
            output_seq1 = seq1[coord[1]] + output_seq1
            output_seq2 = seq2[coord[0]] + output_seq2
        else:
            neighbours = [ (coord[0], coord[1] - 1), (coord[0] - 1, coord[1]) ]
            fit_neighbour = [c for c in neighbours if alignement_mat[c[0]][c[1]] + gap == alignement_mat[coord[0]][coord[1]]][0]
            
            if fit_neighbour == neighbours[0]:
                output_seq1 = seq1[fit_neighbour[1]] + output_seq1
                output_seq2 = '-' + output_seq2
            else:
                output_seq1 = '-' + output_seq1
                output_seq2 = seq2[fit_neighbour[0]] + output_seq2
            coord = fit_neighbour
        coord_path.append(coord)

    if not verbose:
        return [ output_seq1, output_seq2, alignement_mat[len_seq2][len_seq1] ]
    else:
        return [ output_seq1, output_seq2, alignement_mat[len_seq2][len_seq1] ], alignement_mat, coord_path


def needleman_all(seq1, seq2, cost_table = None, cost_mat = None, key = None):
    '''Function that calculates the global alignement of two sequences
    
    Args:
        seq1: first sequence
        seq2: second sequence
        cost_table: contains the match, mismatch and the gap cost in this order (mutual exlusive with cost_mat)
        cost_mat: contains the cost matrix and the gap at the end (mutual exlusive with cost_table and used with key)
        key: the order of the letters in the cost matrix (mutual exlusive with cost_table)
            E.g: [  1, 2, 3, 1, 2, 3, 1, 2, 3, 4  ] key = "ABC"
                    |  |  |  |  |  |  |  |  |  |
                    A  A  A  B  B  B  C  C  C gap
                    A  B  C  A  B  C  A  B  C  
    
    Returns:
        An array contains all possible alignements with their respective scores
        E.g: [ [seq1 alignement 1, seq2 alignement 1, score 1], [seq1 alignement 2, seq2 alignement 2, score 2] ]
    '''
    # Some sanity checks:
    if cost_table and cost_mat and key:
        print("Error: cost_mat and key are mutually exlusive with cost_table, please use the one or the other")
        return
    
    if cost_table and len(cost_table) != 3:
        print("Error: cost_table must be of length 3 and contain the match, mismatch and the gap respectively ")
        return
    
    if not cost_table and ((not cost_mat and key) or (cost_mat and not key)):
        print("Error: cost_mat and key must be defined togther")
        return

    if cost_mat and key and len(cost_mat) != len(key) ** 2 + 1:
        print("Error: cost_mat must have the same length of the suqare of the length of key^2 + 1 (the last number is the gap)")
        return

    letter_dict = {}
    gap = 0

    if key and cost_mat:
        letter_dict = { key[i]: i for i in range(len(key)) }
        gap = cost_mat[len(key) ** 2]
    else:
        gap = cost_table[2]

    def get_cost(letter1, letter2):
        if key and cost_mat:
            return cost_mat[letter_dict[letter1] * len(key) + letter_dict[letter2]]
        else:
            if letter1 == letter2:
                return cost_table[0]
            else:
                return cost_table[1]

    len_seq1, len_seq2 = len(seq1), len(seq2)
    alignement_mat = [ [ 0 for _ in range(len_seq1 + 1) ] for _ in range(len_seq2 + 1) ]
    # Matrix that contain directions coded with 3 binary digits for all the possibles combinations of diections
    # xyz: z is the digonal bit, y is the left bit, x is the upward bit
    # x y z
    # | | |
    # U L D (U:Up / L: Left / D:Diag )
    mat_dir = [ [0 for _ in range(len_seq1 + 1) ] for _ in range(len_seq2 + 1) ]

    # Init step:
    for i in range(1, len_seq1+1):
        alignement_mat[0][i] = alignement_mat[0][i - 1] + gap
        mat_dir[0][i] = 1 << 1 # we go left all the way left!

    for j in range(1, len_seq2+1):
        alignement_mat[j][0] = alignement_mat[j - 1][0] + gap
        mat_dir[j][0] = 1 << 2 # we go all the way up!

    # Filling:
    for j in range(1, len_seq2+1):
        for i in range(1, len_seq1+1):
            left_val = alignement_mat[j][i - 1] + gap
            up_val = alignement_mat[j - 1][i] + gap
            diag_val = alignement_mat[j - 1][i - 1] + get_cost(seq1[i - 1], seq2[j - 1])
            alignement_mat[j][i] = max(max(left_val, up_val), diag_val)
            if diag_val == alignement_mat[j][i]:
                mat_dir[j][i] |= 1
            if left_val == alignement_mat[j][i]:
                mat_dir[j][i] |= (1 << 1)
            if up_val == alignement_mat[j][i]:
                mat_dir[j][i] |= (1 << 2)

    # Trace back:
    coord = (len_seq2, len_seq1)
    output = []
    coord_fifo = [ (len_seq2, len_seq1) ]
    path_fifo = [ [ "", "", alignement_mat[len_seq2][len_seq1] ] ]
    seq1 = "-"+seq1
    seq2 = "-"+seq2

    while len(coord_fifo):
        coord = coord_fifo[0]
        path = path_fifo[0]

        while (1):
            if coord == (0, 0):
                output.append(path)
                path_fifo.pop(0)
                coord_fifo.pop(0)
                break

            taken = False
            coord_tmp = coord
            nc = coord # new coord that will be our path in this loop
            org_path = path[:]

            if mat_dir[coord[0]][coord[1]] & 1: # Diag
                coord_tmp = (coord[0] - 1, coord[1] - 1)
                nc = coord_tmp
                path[0] = seq1[coord[1]] + path[0]
                path[1] = seq2[coord[0]] + path[1]
                taken = True
            if mat_dir[coord[0]][coord[1]] & (1 << 1):  # Left
                coord_tmp = (coord[0], coord[1] - 1)
                if not taken:
                    nc = coord_tmp
                    taken = True
                    path[0] = seq1[coord[1]] + path[0]
                    path[1] = '-' + path[1]
                else:
                    path_fifo.append(org_path[:])
                    coord_fifo.append(coord_tmp)
                    path_fifo[-1][0] = seq1[coord[1]] + path_fifo[-1][0]
                    path_fifo[-1][1] = '-' + path_fifo[-1][1]
            if mat_dir[coord[0]][coord[1]] & (1 << 2):  # Up
                coord_tmp = (coord[0] - 1, coord[1])
                if not taken:
                    nc = coord_tmp
                    taken = True
                    path[0] = '-' + path[0]
                    path[1] = seq2[coord[0]] + path[1]
                else:
                    path_fifo.append(org_path[:])
                    coord_fifo.append(coord_tmp)
                    path_fifo[-1][0] = '-' + path_fifo[-1][0]
                    path_fifo[-1][1] = seq2[coord[0]] + path_fifo[-1][1]
            coord = nc
    
    return output

##############################################
# These functions use BioPython and are used 
# to cross-check our results and test them
##############################################

from Bio.Align import PairwiseAligner
from Bio.Align import substitution_matrices

def nw_bio(seq1, seq2, cost_table):
    aligner = PairwiseAligner(alphabet=list(set(seq1+seq2)))
    aligner.match_score = cost_table[0]
    aligner.mismatch_score = cost_table[1]
    aligner.gap_score = cost_table[2]
    alignments = aligner.align(seq1, seq2)
    formated_alignments = []

    for i in range(len(alignments)):
        als = str(alignments[i]).split("\n")
        formated_alignments.append([als[0], als[2], int(alignments[i].score)])

    return formated_alignments


def nw_bio_mat(seq1, seq2, cost_mat, key):
    aligner = PairwiseAligner(alphabet=key)
    matrix = {}
    for i in range(len(key)):
        for j in range(0, len(key)):
            matrix[(key[i], key[j])] = cost_mat[i * len(key) + j]
    aligner.substitution_matrix  = substitution_matrices.Array(data=matrix)
    aligner.gap_score = cost_mat[len(key) ** 2]
    alignments = aligner.align(seq1, seq2)
    formated_alignments = []

    for i in range(len(alignments)):
        als = str(alignments[i]).split("\n")
        formated_alignments.append([als[0], als[2], int(alignments[i].score)])

    return formated_alignments

def nw_bio_generic(seq1, seq2, cost_table = None, cost_mat = None, key = None):
    if cost_table == None:
        return nw_bio_mat(seq1, seq2, cost_mat, key)
    else:
        return nw_bio(seq1, seq2, cost_table)