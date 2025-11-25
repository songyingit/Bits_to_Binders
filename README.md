# BioML Challenge 2024: Bits to Binders, Human CD20 Targeting Antibody Sequence Design

This repository presents our work for the BioML Challenge 2024, where the task is to design an 80 amino acid antibody sequence that binds to human CD20, a critical target in immunotherapy.

Here, we combined protein language model, Alphafold2, and generative model ProteinMPNN to generate candidate sequences with optimized binding potential. 

## Rituximab Sequence Processing and ESM-2 Masked Language Modeling

We first aimed at extracting subsequences from Rituximab, a previous resolved monoclonal antibody targeting human CD20, and applying Masked Language Modeling (MLM) on pre-trained protein language model, ESM-2, to predict mutations. 

1. **Subsequence Generation (`cut_sequence.py`)**:
   - This script extracts all subsequences of a given length from a specified sequence (in this case, Rituximab), ensuring that specific required positions are included in each subsequence.
   - We employed AlphaFold2 Multimer (localcolabfold version) to predict the binding interactions of subsequences with human CD20. The subsequence displaying the highest ipTM score in `rituximab_cut_sequences_predict.csv` was identified for subsequent mutation generation.

2. **Generate mutants by Masked Language Modeling with ESM-2 (`ESM_MLM_gen.py`)**:
   - This script uses Meta's pre-trained protein language model, ESM-2, to predict mutants in the best Rituximab subsequence using Masked Language Modeling (MLM).
   - Masked positions are chosen based on a specified percentage of non-fixed positions in the sequence. The results are summarized in a CSV file that includes the sequence similarity between the original and the predicted sequences.
   - AlphaFold2 Multimer (localcolabfold version) was further used to evaluate the binding of mutant sequences with human CD20. The top-performing mutants, based on the ipTM score from `rituximab_mutant_sequences_predict.csv`, was selected for futher Binder design loop optimizations.

## Human CD20 Binder Optimization Loop 
Then we developed the following binder design loop to optimize previously designed sequences. 

**[Binder Optimization (Credit to Diego E Kleiman)](https://github.com/diegoeduardok/binder_design_loop)**:
   - This script automates an iterative design process involving protein structure prediction and sequence generation, using AlphaFold2 Multimer (localcolabfold version)  and ProteinMPNN in a loop. 
   - First, AlphaFold2 Multimer (localcolabfold version) was leveraged to predict the complex structure of previous selected sequence.
   - Then, ProteinMPNN was used to generate mutant protein sequences. It takes a protein structure, designs sequences for specific chains and positions, and outputs multiple new sequences. Then These sequences 
   - We further design a loss function by evaluating structure files based on metrics such as pLDDT, ipTM, iPAE, and radius of gyration, to select the best binding structure. 
   - Run the previous steps in multiple rounds. In each round, it compares the predicted structures to select the best model based on the loss function, and then uses that structure to design new sequences for the next round. This loop continues for a specified number of rounds, keep updating the best-performing structure and sequence at each iteration.

## Installation

You should follow the instructions from [localcolabfold](https://github.com/YoshitakaMo/localcolabfold) to install that package. You will need to include the colabfold path in your PATH variable in `~/.bashrc` or edit the `colabfold_template.sh` file to include the full path to `colabfold_batch`.

Then, follow the instructions in [ProteinMPNN](https://github.com/dauparas/ProteinMPNN) to create a conda environment that can run those codes and clone the GitHub repo in your machine. You will need to provide the path to the Python executable from that environment and the paths to the ProteinMPNN codes in `proteinMPNN_template.sh`.

You will also need to have a access to a Python environment with `numpy`, `mdtraj`, and `natsort` installed to run the script `run_design_loop.py`. This environment can be the same as the one that runs ProteinMPNN. 

## Running the code

To run the code, first open `run_design_loop.py`. Edit line 153 according to your desired output path and total number of runs. 

```python
def main():
    run_loop(outpath="./loop_oct_2/", initial_round=0, total_rounds=10)
``` 

Notice that you can restart from a round larger than 0 if you already ran some of them, but the loop will have no memory of the best models produced in past rounds.

You can control the chains and residue positions (indexed from 1, not 0!) that will be designed by editing lines 137-138:

```python
run_proteinMPNN(
            template_script="proteinMPNN_template.sh", 
            pdb_path=protein_mpnn_output, 
            chains_to_design="C", # Modify as needed
            positions_to_design="2 3 4 6 8 9 10 11 12 13 14 15 16 17 18 19 20 21 25 26 27 28 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 72 74 75 77 79 80", # Modify as needed
            output_path=protein_mpnn_output, 
            seqs_per_target=30
        )
```

To start a loop, create the folder where the output will be saved. Then, in that directory, create a folder `round_0`. This folder must contain a fasta file named `designed_sequences_round_0.fa` to start the loop. If you have a PDB file with the initial guess for the binder and want to start from there, follow these steps to generate the fasta file:

1. Create a copy of `proteinMPNN_template.sh` (e.g., `proteinMPNN_init.sh`)
1. Edit `proteinMPNN_init.sh`: change `"{INPUT_PDB_PATH}"` with the path to the PDB file and change `"{OUTPUT_PATH}"` with the path to `round_0`.
1. Run `proteinMPNN_init.sh`. Check that ProteinMPNN created the output (.fa file) in the directory `round_0/seqs`.
1. Run the following code in an interactive Python session:

```python
>>>from run_design_loop import prepare_sequence_to_structure # May need to change import depending on where you stored the code
>>>prepare_sequence_to_structure("{output_path}/round_0", "{output_path}/round_0", 0) # Change output path here
```

After the last step, the file `round_0/designed_sequences_round_0.fa` should be available.

Now, you can run the desing loop:

```bash
$ python run_desing_loop.py
```


## Output

The output is organized as follows:

```
output_directory
	|
	round_{r}
		|_colabfold_results # Prdicted structures, scores, log file, etc.
		|_seqs # Sequences designed by ProteinMPNN
		|_designed_sequences_round_{r}.fa # Sequences from ProteinMPNN formatted for colabfold
		|_Other files from ProteinMPNN...

```

