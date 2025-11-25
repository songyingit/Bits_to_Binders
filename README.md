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

