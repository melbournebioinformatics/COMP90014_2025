
#################
### Exercise 1 ##
#################

def jaccard(a: set, b: set) -> float:
    intersection = len(a & b)
    union = len(a | b)
    j = intersection / union
    return j

def extract_kmers(seq: str, k: int) -> set:
    """
    Extract all kmers. Return Set of kmers.
    """
    kmers = set()
    for i in range(len(seq) - k + 1):
        kmer = seq[i : i + k]
        kmers.add(kmer)
    return kmers

def true_jaccard_similarity(seqA: str, seqB: str, k: int) -> float:
    kmersA = extract_kmers(seqA, k)
    kmersB = extract_kmers(seqB, k)
    j = jaccard(kmersA, kmersB)
    return j


#################
### Exercise 2 ##
#################

def minhash_sketch(seq: str, k: int, s: int) -> set:
    """
    Calulate minhash sketch from DNA sequence.
    """
    hashes = set()
    
    for i in range(len(seq) - k + 1):
        kmer = seq[i : i + k]
        hash_value = hash(kmer)  
        hashes.add(hash_value)
    
    min_hashes = sorted(list(hashes))[ : s]
    return set(min_hashes)


#################
### Exercise 3 ##
#################

def minhash_jaccard_similarity(seqA: str, seqB: str, k: int, s: int) -> float:
    """
    Calculate the Jaccard similarity using MinHash
    """
    sketchA = minhash_sketch(seqA, k, s)
    sketchB = minhash_sketch(seqB, k, s)
    j = jaccard(set(sketchA), set(sketchB))
    return j



#################
### Exercise 4 ##
#################

def minimizer_sketch(seq: str, k: int, s: int) -> set:
    """
    Calulate minimizer sketch from DNA sequence.
    """
    seq_len = len(seq)
    stride = seq_len // s
    # Ensure windows overlap by k - 1
    window_size = stride + k - 1
    minimizer_set = set()

    for i in range(0, s):
        window_start = i * stride
        window_end = window_start + window_size
        # Check boundaries
        if window_end > seq_len:
            window_end = seq_len
        sub_seq = seq[window_start : window_end]
        kmer_set = extract_kmers(sub_seq, k)
        minimizer_set.add(min(kmer_set))
    
    return minimizer_set