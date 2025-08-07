
import os
import re
import sys 
import shutil
import subprocess
import pandas as pd

pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 10)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 100)
pd.options.display.float_format = '{:.2f}'.format

# test configuration at bottom of this file

########################
### HELPER FUNCTIONS ###
########################

def compare_outputs(user_filepath: str, expected_filepath: str) -> dict:
    info = {
        'exists_ok': False,  
        'format_ok': False,  
        'oligos_ok': False,  
        'wnt_hit_similarity': 0,   # jaccard
        'wnt_miss_similarity': 0,   # jaccard
        'otg_similarity': 0,   # mean jaccard
    }

    # check file exists 
    # user writing to unexpected path (not --outfile)
    if os.path.exists(user_filepath):
        info['exists_ok'] = True 
    else:
        return info

    # check file can be read by pandas
    try:
        u_df = pd.read_csv(user_filepath, sep='\t', header=0)
    except Exception:
        return info
    
    # check format
    if _correct_format(u_df):
        info['format_ok'] = True 
    else:
        return info

    # read expected output for comparison
    e_df = pd.read_csv(expected_filepath, sep='\t', header=0)
    u_df = u_df.sort_values(['oligo', 'WNT4', 'off_target'])
    e_df = e_df.sort_values(['oligo', 'WNT4', 'off_target'])
    info['oligos_ok'] = _all_oligos_present(u_df, e_df)
    info['wnt_hit_similarity'] = _calc_wnt_hit_similarity(u_df, e_df)
    info['wnt_miss_similarity'] = _calc_wnt_miss_similarity(u_df, e_df)
    info['otg_similarity'] = _calc_otg_similarity(u_df, e_df)
    return info 
    
def _correct_format(df: pd.DataFrame) -> bool:
    # columns are correct
    if df.shape[1] != 3 or df.columns.to_list() != ['oligo', 'WNT4', 'off_target']:
        return False
    
    # check no missing values in first two columns
    if df.shape[0] != df.dropna(subset=['oligo', 'WNT4']).shape[0]:
        return False 

    # check types can be cast to str/bool for first two columns
    try:
        df['oligo'] = df['oligo'].astype(str)
        df['WNT4'] = df['WNT4'].astype(bool)
    except Exception:
        return False 
    return True 
    
def _all_oligos_present(u_df: pd.DataFrame, e_df: pd.DataFrame) -> bool:
    n_oligos_expected = set(e_df['oligo'].unique())
    n_oligos_actual = set(u_df['oligo'].unique())
    return n_oligos_actual == n_oligos_expected

def _jaccard(a: set, b: set) -> float:
    if len(a) == 0 & len(b) == 0:
        return 1
    intersection = len(a.intersection(b))
    union = len(a.union(b))
    j = intersection / union
    return j

def _calc_wnt_hit_similarity(u_df: pd.DataFrame, e_df: pd.DataFrame) -> str:
    oligos_user = set(u_df[u_df['WNT4']==True]['oligo'].unique())
    oligos_expected = set(e_df[e_df['WNT4']==True]['oligo'].unique())
    return f"{_jaccard(oligos_user, oligos_expected)*100:.1f}%"

def _calc_wnt_miss_similarity(u_df: pd.DataFrame, e_df: pd.DataFrame) -> str:
    oligos_user = set(u_df[u_df['WNT4']==False]['oligo'].unique())
    oligos_expected = set(e_df[e_df['WNT4']==False]['oligo'].unique())
    return f"{_jaccard(oligos_user, oligos_expected)*100:.1f}%"

def _calc_otg_similarity(u_df: pd.DataFrame, e_df: pd.DataFrame) -> str:
    e_df = e_df.set_index('oligo')
    u_df = u_df.set_index('oligo')
    table = pd.DataFrame(index=sorted(list(set(e_df.index.to_list()) | set(e_df.index.to_list()))))
    table['user'] = u_df['off_target']
    table['expected'] = e_df['off_target']
    table = table.fillna('')
    table['user'] = table['user'].apply(lambda x: set(x.split(',')))
    table['expected'] = table['expected'].apply(lambda x: set(x.split(',')))
    table['jaccard'] = table.apply(lambda rec: _jaccard(rec.user, rec.expected), axis=1)
    return f"{table['jaccard'].mean()*100:.1f}%"

def run_tests(o_size_l: list[int], n_oligos_l: list[int], n_genes_l: list[int]) -> None:
    data_perf = []
    data_sim = []
    test_num = 0
    print('Running tests:')
    for o_size in o_size_l:
        for n_oligos in n_oligos_l:
            for n_genes in n_genes_l:
                test_num += 1
                label = f"test {test_num}"
                # define input and output files 
                db_path = f"{BASE_DIR}/test_data/databases/{n_genes}_genes.tsv"
                ol_path = f"{BASE_DIR}/test_data/oligos/{n_oligos}_oligos.{o_size}_mer.txt"
                expected_outfile = f"{BASE_DIR}/test_data/expected/{o_size}_mer.{n_oligos}_oligos.{n_genes}_genes.tsv"
                user_outfile = f"{BASE_DIR}/results/{o_size}_mer.{n_oligos}_oligos.{n_genes}_genes.tsv"
                
                # report to user which test is being conducted
                print(f"k={o_size}, n={n_oligos}, m={n_genes}")
                    
                # run the A1.py python script with these inputs
                command = [
                    CMD, SCRIPT_PATH, 
                    '--database', db_path, 
                    '--oligos', ol_path, 
                    '--outfile', user_outfile
                ]
                res = subprocess.run(command, capture_output=True, text=True)

                # capture the time and memory usage report
                PATTERN_TIME = r'Time=([\d\.]+) seconds'
                PATTERN_MEM = r'Memory=([\d\.]+) MB'
                time = None
                mem = None
                for line in res.stdout.split('\n'):
                    m_time = re.match(PATTERN_TIME, line)
                    m_mem = re.match(PATTERN_MEM, line)
                    if m_time is not None:
                        time = float(m_time.group(1))
                    if m_mem is not None:
                        mem = float(m_mem.group(1))
                data_perf.append((label, o_size, n_oligos, n_genes, time, mem))

                # assess output similarity 
                info = compare_outputs(user_outfile, expected_outfile)
                info['label'] = label
                data_sim.append(info)

    fields_performance = [
        'label', 'oligo_length (k)', 'n_oligos (n)', 
        'n_genes (m)', 'runtime_seconds', 'peak_mem_mb'
    ]
    df_perf = pd.DataFrame.from_records(data=data_perf, columns=fields_performance)
    df_sim = pd.DataFrame.from_records(data=data_sim)
    df_sim = df_sim[['label'] + [x for x in df_sim.columns if x!='label']]
    print('\nPerformance:')
    print(df_perf.set_index('label'))
    print('\nOutput Similarity:')
    print(df_sim.set_index('label'))


##############
### CONFIG ###
##############

this_path = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(this_path)
SCRIPT_PATH = f"{BASE_DIR}/A1.py"

# configure correct python (or inform user that they need to take action)
python_path = shutil.which("python")
python3_path = shutil.which("python3")
if python_path:
    CMD = 'python'
elif python3_path:
    CMD = 'python3'
else:
    print(
        "Neither 'python' nor 'python3' are valid commands in your current shell.\n" \
        "Please check your python installation or environment.\n" \
        "You can manually set CMD=[python command] above this code block in A1test.py to override.\n"
    )
    sys.exit(1)


##################
### TEST SUITE ###
##################

RUN_BASIC = True 
RUN_OLIGO_LENGTHS = True 
RUN_OLIGO_COUNTS = True 
RUN_GENE_COUNTS = True 

# set this to True if you want to profile 
# oligo size & count scaling with the largest gene database (1000).
USE_LARGE_DB = False

print('\n-----------')
print('Test Config')
print('-----------\n')
print(f"CMD: {CMD}")
print(f"BASE_DIR: {BASE_DIR}")
print(f"SCRIPT_PATH: {SCRIPT_PATH}")
print()
print(f"RUN_BASIC: {RUN_BASIC}")
print(f"RUN_OLIGO_LENGTHS: {RUN_OLIGO_LENGTHS}")
print(f"RUN_OLIGO_COUNTS: {RUN_OLIGO_COUNTS}")
print(f"RUN_GENE_COUNTS: {RUN_GENE_COUNTS}")
print(f"USE_LARGE_DB: {USE_LARGE_DB}")

if RUN_BASIC:
    print('\n-----------')
    print('Basic tests')
    print('-----------\n')
    df = run_tests(o_size_l=[15], n_oligos_l=[100, 500], n_genes_l=[10, 100])

if RUN_OLIGO_LENGTHS:
    print('\n--------------------------')
    print('Oligo length scaling tests')
    print('--------------------------\n')
    n_genes_l = [1000] if USE_LARGE_DB else [100]
    df = run_tests(o_size_l=[11, 15, 19], n_oligos_l=[500], n_genes_l=n_genes_l)

if RUN_OLIGO_COUNTS:
    print('\n-------------------------')
    print('Oligo count scaling tests')
    print('-------------------------\n')
    n_genes_l = [1000] if USE_LARGE_DB else [100]
    df = run_tests(o_size_l=[15], n_oligos_l=[100, 500, 2500], n_genes_l=n_genes_l)

if RUN_GENE_COUNTS:
    print('\n-----------------------')
    print('Gene count scaling tests')
    print('------------------------\n')
    df = run_tests(o_size_l=[15], n_oligos_l=[500], n_genes_l=[10, 100, 1000])


