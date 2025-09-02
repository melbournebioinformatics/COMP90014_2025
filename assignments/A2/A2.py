
import sys
import argparse 
import resource 
import time 


def main(indir: str, k_size: int, min_plasmid_len: int, outfile: str) -> None:
    """
    Identifies AMR plasmid sequence given DNA sequencing reads for 5 bacterial organisms ABCDE.
    Organisms A,B,C contain the AMR plasmid, while organisms D,E do not. 

    Inputs 
        indir:              Path to directory containing sequencing read .fasta files.
        k_size:             Size of K to use (if using kmers).
        min_plasmid_len:    Minimum length of plasmid to consider AMR.
        outfile:            Path to output file where AMR plasmid sequence is written.

    Output
        Single .txt file containing suspected AMR plasmid sequence. 
    """
    # Your code here.
    # Please do not put all logic within this function!
    # Define other functions which are then called from main(). 
    raise NotImplementedError


### DO NOT ALTER ###
def rotate_sequence(seq: str):
    """
    Finds the lexicographically smallest rotation of an input DNA sequence.
    """
    n = len(seq)
    seq_concat = seq + seq
    best_rotation = seq
    for i in range(n):
        rotation = seq_concat[i : i + n]
        if rotation < best_rotation:
            best_rotation = rotation
    return best_rotation

def load_cmdline_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Identifies AMR plasmid sequence given DNA sequencing reads for 5 bacterial organisms ABCDE.")
    parser.add_argument("--indir", type=str, required=True, help="Path to directory containing sequencing read .fasta files")
    parser.add_argument("--kmer-size", type=int, required=True, help="Size of K to use (if using kmers)")
    parser.add_argument("--min-plasmid-size", type=int, required=True, help="Minimum length of plasmid to consider AMR")
    parser.add_argument("--outfile", type=str, required=True, help="Path to output file where AMR plasmid sequence is written")
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = load_cmdline_args()
    start_time = time.time()
    main(args.indir, args.kmer_size, args.min_plasmid_size, args.outfile)
    stop_time = time.time()
    peak_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if sys.platform == "darwin":        # macOS -> bytes
        peak_memory_mb = peak_memory / (1024 * 1024)
    else:
        peak_memory_mb = peak_memory / 1024
    print(f"Time={stop_time - start_time:.2f} seconds")
    print(f"Memory={peak_memory_mb:.2f} MB")
### DO NOT ALTER ###

