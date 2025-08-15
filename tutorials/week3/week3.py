
import numpy as np

##################
### EXERCISE 1 ###
##################
def hamming(a, b):
    """
    Calculate the Hamming distance between strings a and b.
    The strings must be the same length.
    """

    if len(a) != len(b):
        print('Input strings must be equal length')
        return
    
    hamming_distance = 0
    for i in range(len(a)):
        if a[i] != b[i]:
            hamming_distance += 1
    
    return hamming_distance
    
    # # Another solution (compact)
    # assert len(a) == len(b), "Input sequences must be same length"
    # return sum(char_a != char_b for char_a, char_b in zip(a, b))


##################
### EXERCISE 2 ###
##################

# LIVE CODING #
def lev(a,b):
    """
    Recursively calculate Levenshtein distance between strings a and b.
    """
    if len(a) == 0:
        return len(b)
    if len(b) == 0:
        return len(a)
    
    if a[0] == b[0]:
        mismatch_cost = 0
    else:
        mismatch_cost = 1

    # Case 1: No gap
    no_gap = lev(a[1 : ], b[1 : ]) + mismatch_cost
    # Case 2: Introduce gap in a
    gap_a = lev(a, b[1 : ]) + 1
    # Case 3: Introduce gap in b
    gap_b = lev(a[1 : ], b) + 1
    
    return min(no_gap, gap_a, gap_b)


##################
### EXERCISE 3 ###
##################
def levenshtein_distance(str1, str2):
    """
    Calculate the Levenshtein distance between two strings using dynamic programming.

    Parameters:
    str1 (str): The first input string.
    str2 (str): The second input string.

    Returns:
    int: The Levenshtein distance between the two input strings.
    """

    len_str1 = len(str1)
    len_str2 = len(str2)
    
    # Initialize a matrix to store distances
    dist_matrix = np.zeros((len_str1 + 1, len_str2 + 1), dtype=int)
    
    # Initialize the first row and column of the matrix
    # Note: This bit only works because our penalty score is +1
    #       Think about how you would do this for idel penalties > 1
    for i in range(len_str1 + 1):
        dist_matrix[i, 0] = i
    for j in range(len_str2 + 1):
        dist_matrix[0, j] = j
    
    # Fill in the rest of the matrix
    for i in range(1, len_str1 + 1):
        for j in range(1, len_str2 + 1):
            if str1[i - 1] == str2[j - 1]:
                cost = 0
            else:
                cost = 1
            dist_matrix[i, j] = min(dist_matrix[i - 1, j] + 1,       # Deletion
                                    dist_matrix[i, j - 1] + 1,       # Insertion
                                    dist_matrix[i - 1, j - 1] + cost) # Substitution
    
    # The value at the bottom right corner of the matrix is the Levenshtein distance
    levenshtein_distance = dist_matrix[len_str1, len_str2]
    return levenshtein_distance


############################
### Extension Exercise 1 ###
############################
def levenshtein_tracking_matrix(str1, str2):
    """
    Calculate the Levenshtein distance between two strings using dynamic programming.

    Parameters:
    str1 (str): The first input string.
    str2 (str): The second input string.

    Returns:
    tuple of numpy.ndarray: The distance matrix of Levenshtein distance and the tracking matrix
    """
    len_str1 = len(str1)
    len_str2 = len(str2)
    
    # Initialize a matrix to store distances and the tracking matrix
    dist_matrix = np.zeros((len_str1 + 1, len_str2 + 1), dtype=int)
    # Integer, 0 for diagonal, 1 for above, and 2 for left
    tracking_matrix = np.zeros((len_str1 + 1, len_str2 + 1), dtype=int)
    
    # Initialize the first row and column of the matrix
    # Note: This bit only works because our penalty score is +1
    #       Think about how you would do this for idel penalties > 1
    for i in range(len_str1 + 1):
        dist_matrix[i, 0] = i
        tracking_matrix[i, 0] = 1
    for j in range(len_str2 + 1):
        dist_matrix[0, j] = j
        tracking_matrix[0, j] = 2

    # Set the start of the tracking matrix to -1
    tracking_matrix[0, 0] = -1 
    
    # Fill in the rest of the matrix
    for i in range(1, len_str1 + 1):
        for j in range(1, len_str2 + 1):
            if str1[i - 1] == str2[j - 1]:
                cost = 0
            else:
                cost = 1

            diag = dist_matrix[i - 1, j - 1] + cost     # substitution / match
            above = dist_matrix[i - 1, j] + 1              # deletion
            left = dist_matrix[i, j - 1] + 1            # insertion

            # Choose the best; break ties preferring diagonal, then up, then left
            choices = [diag, above, left]
            move = int(np.argmin(choices))
            dist_matrix[i, j] = choices[move]
            tracking_matrix[i, j] = move
    
    # Instead of returning the distance, return the matrix
    return dist_matrix, tracking_matrix


############################
### Extension Exercise 2 ###
############################

def traceback_global_alignment(str1, str2):
    """
    Reconstruct the global (Needleman-Wunsch) alignment from the distance and tracking matrices.

    Parameters:
    str1 (str): The first input string.
    str2 (str): The second input string.

    Returns:
    tuple of str: The aligned versions of str1 and str2 with '-' for gaps.
    """

    dist_matrix, tracking_matrix = levenshtein_tracking_matrix(str1, str2)
    i = len(str1)
    j = len(str2)

    # Collect alignment characters in reverse while walking from bottom-right to top-left
    aligned_1 = []
    aligned_2 = []

    # Start from the bottom-right corner
    while not (i == 0 and j == 0):
        move = tracking_matrix[i, j]

        if move == 0:
            # diagonal: match/substitution
            aligned_1.append(str1[i - 1])
            aligned_2.append(str2[j - 1])
            i -= 1
            j -= 1
        elif move == 1:
            # above: deletion (gap in str2)
            aligned_1.append(str1[i - 1])
            aligned_2.append('-')
            i -= 1
        elif move == 2:
            # left: insertion (gap in str1)
            aligned_1.append('-')
            aligned_2.append(str2[j - 1])
            j -= 1

    # Reverse because we built the alignment from end to start
    aligned_1.reverse()
    aligned_2.reverse()

    return ''.join(aligned_1), ''.join(aligned_2)