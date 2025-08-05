
import time
import resource
import argparse
import sys


def main(database_path: str, oligos_path: str, outfile: str) -> None:
    """
    Identifies which oligos will bind to gene coding sequences (CDS).

    Inputs 
        database_path: path to .tsv file containing gene CDS.
        oligos_path: path to .txt file containing oligos to assess.
        outfile: path to .tsv file which summarises results. 

    Output
        Single .tsv (tab seperated) file.
        - Column 1: The oligo being assessed.
        - Column 2: True if the oligo matches the WNT4 gene (up to 1 mismatch) else False.
        - Column 3: Comma-separated string of other genes the oligo matches (up to 1 mismatch). 
        Example files are available in the ./test_data/expected directory. 
    """

    # Your code here.
    # Please do not put all logic within this function!
    # Define other functions which are then called from main(). 
    raise NotImplementedError



### DO NOT ALTER ###
def load_cmdline_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Identifies the best oligo for a gene which minimises off-target mRNA transcript binding.")
    parser.add_argument("--database", type=str, required=True, help="Coding sequence database path (.tsv)")
    parser.add_argument("--oligos", type=str, required=True, help="Oligos path (.txt)")
    parser.add_argument("--outfile", type=str, required=True, help="Results path (.tsv)")
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = load_cmdline_args()
    start_time = time.time()
    main(args.database, args.oligos, args.outfile)
    stop_time = time.time()
    peak_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if sys.platform == "darwin":        # macOS -> bytes
        peak_memory_mb = peak_memory / (1024 * 1024)
    else:
        peak_memory_mb = peak_memory / 1024
    print(f"Time={stop_time - start_time:.2f} seconds")
    print(f"Memory={peak_memory_mb:.2f} MB")
### DO NOT ALTER ###

