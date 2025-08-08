def get_canon(kmer):
    # Return the canonical kmer  
    
    if kmer <= kmer.reverse_complement():
        return kmer
    else:
        return kmer.reverse_complement()


def kmer_locs(sequence, k = 5):
    # Get kmers from seq object
    # Output kmers and their location as (kmer,location) tuples.

    for i in range(len(sequence) - k + 1):
        kmer = sequence[i : i + k]
        if 'N' in kmer:
            continue
        else:
            yield (kmer, i)


def build_hash_table(kmer_list):
    # Builds and returns kmer index as hash table.
    # Collisions resolved using linear probing. 
    kmer_dict = dict()
    for kmer, loc in kmer_list:
        # Check if the kmer already exists
        if kmer in kmer_dict:
            # Append the location to the list
            kmer_dict[kmer].append(loc)
        # Firt time see the kmer
        else:
            kmer_dict[kmer] = [loc]
    return kmer_dict


def mapKmers(read, hash_table = {}, k = 3):
    read_kmers = kmer_locs(read, k = k) 
    # raise NotImplementedError
    
    for key, value in read_kmers:
        if key in hash_table:
            genome_locs = hash_table[key]
            for genome_loc in genome_locs:
                yield(value, genome_loc)
