import sys
sys.path.insert(0,'/home/xuenan/py310/lib/python3.6/site-packages')
import esm
import torch
import numpy as np
from transformers import AutoTokenizer, AutoModelForMaskedLM
import random
import csv

# Load pre-trained ESM model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("facebook/esm2_t36_3B_UR50D")
model = AutoModelForMaskedLM.from_pretrained("facebook/esm2_t36_3B_UR50D")

# Original sequence (replace this with your actual sequence)
sequence = "FTSYNMHWVKQTPGRGLEWIGAIYPGNGDTSYNQKFKGKATLTADKSSSTAYMQLSSLTSEDSAVYYCARSTYYGGDWYF"
fix = [0,4,6,21,22,23,28,29,30,70,72,75,77]
total_positions = len(sequence)

# Output CSV file
output_file = "rituximab_ESM_2_MLM.csv"

with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write header
    writer.writerow(["Mask Percentage", "Original Sequence", "Masked Positions", "New Sequence", "Similarity"])
    seq_index = 0
    # Specify which residues to mask
    for mask_percentage in np.arange(0.1, 1, 0.1):
        for rep in range(40,60):
            random.seed(rep)
            num_to_mask = int((total_positions - len(fix)) * mask_percentage)
            positions = list(range(total_positions))
            for fixed_position in fix:
                positions.remove(fixed_position)
            mask_positions = random.sample(positions, num_to_mask)
            masked_sequence = list(sequence)
            for i in mask_positions:
                # masked_sequence[i] = "<mask>"
                masked_sequence[i] = tokenizer.mask_token
            masked_sequence_str = "".join(masked_sequence)
            print('masked_sequence:',masked_sequence_str)
            # Tokenize the masked sequence
            input_ids = tokenizer(masked_sequence_str, return_tensors="pt")["input_ids"]
            # Predict masked residues
            with torch.no_grad():
                outputs = model(input_ids)
                predictions = outputs.logits
            # Decode predictions (get top predicted amino acids)
            predicted_sequence = list(sequence)
            for i in mask_positions:
                predicted_token_id = predictions[0, i].argmax(dim=-1).item()
                predicted_amino_acid = tokenizer.convert_ids_to_tokens(predicted_token_id)
                predicted_sequence[i] = predicted_amino_acid
                # predicted_tokens = predictions[0].argmax(dim=-1)
                # predicted_sequence = tokenizer.decode(predicted_tokens, skip_special_tokens=True)
                # print(predicted_sequence)
            # Replace masked positions with predicted residues
            # new_sequence[i] = predicted_sequence[i]
            new_sequence = "".join(predicted_sequence)
            # Skip sequences that contain the residue 'X'
            if 'X' in new_sequence:
                continue
            # print("Original sequence:", sequence)
            print("New sequence:", new_sequence)
            # Calculate sequence similarity (identity)
            with open('/home/xuenan/song/mutants/mutant_seq/rituximab_var_seq_'+str(seq_index)+'.fasta', 'w') as f:
                f.write(""">rituximab_var_seq_"""+str(seq_index)+"""
MRESKTLGAVQIMNGLFHIALGGLLMIPAGIYAPICVTVWYPLWGGIMYIISGSLLAATEKNSRKCLVKGKMIMNSLSLFAAISGMILSIMDILNIKISHFLKMESLNFIRAHTPYINIYNCEPANPSEKNSPSTQYCYSIQSLFLGILSVMLIFAFFQELVIAG:MRESKTLGAVQIMNGLFHIALGGLLMIPAGIYAPICVTVWYPLWGGIMYIISGSLLAATEKNSRKCLVKGKMIMNSLSLFAAISGMILSIMDILNIKISHFLKMESLNFIRAHTPYINIYNCEPANPSEKNSPSTQYCYSIQSLFLGILSVMLIFAFFQELVIAG:"""+new_sequence)
            seq_index += 1
            identical_residues = sum(1 for a, b in zip(sequence, new_sequence) if a == b)
            similarity = identical_residues / total_positions
            print(f"Sequence similarity (identity): {similarity:.2%}")
            writer.writerow([f"{mask_percentage * 100:.1f}%", sequence, mask_positions, new_sequence, f"{similarity:.2%}"])
print(f"Results saved to {output_file}")