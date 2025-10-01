
import argparse


def main(abundance_path: str, meta_path: str, outfile_path: str) -> None:
    """
    Uses the clinical metadata and log2 abundance values (derived from LC-MS data) 
    to make predictions about which unobserved rooms are 'compromised' by an evil cat. 

    Inputs 
        abundance_path:   Path to log2 metabolite abundance values (.tsv)
        meta_path:        Path to clinical metadata and room information (.tsv)
        outfile_path:     Path to output file (.tsv)

    Output
        Single .tsv file where room predictions and probabilities are written ('outfile_path')
    """
    # Your code here.
    # Please do not put all logic within this function!
    # Define other functions which are then called from main(). 
    raise NotImplementedError


def load_cmdline_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Predicts whether unobserved rooms are 'compromised' by the presence of an evil cat.")
    parser.add_argument("--abundance", type=str, required=True, help="Path to log2 metabolite abundance values (.tsv)")
    parser.add_argument("--meta", type=str, required=True, help="Path to clinical metadata and room information for the cancer study (.tsv)")
    parser.add_argument("--outfile", type=str, required=True, help="Path to output file where room predictions and probabilities are written (.tsv)")
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = load_cmdline_args()
    main(args.abundance, args.meta, args.outfile)
