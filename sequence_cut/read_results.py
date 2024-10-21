import pandas as pd
import re
import pickle

# Read the sequences
all_subseqs = pickle.load(open("all_cut_seq.pkl", 'rb'))

# Initialize an empty list to store the extracted data
data = []

for i in range(33):
      # Open the log file and iterate through its lines
      with open('rituximab_ori_seq_' + str(i) + '/log.txt', 'r') as file:
            for line in file:
                  # Check if the line starts with the specified string
                  if "rank_001_alphafold2_multimer_v3_model_" in line:
                        # Use regular expressions to extract the pLDDT, pTM, and ipTM values
                        plddt_match = re.search(r'pLDDT=(\d+\.?\d*)', line)
                        ptm_match = re.search(r'pTM=(\d+\.?\d*)', line)
                        iptm_match = re.search(r'ipTM=(\d+\.?\d*)', line)

                        if plddt_match and ptm_match and iptm_match:
                              pLDDT = float(plddt_match.group(1))
                              pTM = float(ptm_match.group(1))
                              ipTM = float(iptm_match.group(1))
                        
                              # Append the extracted values to the list
                              data.append([i, all_subseqs[i], pLDDT, pTM, ipTM])

# Create a DataFrame from the extracted data
df = pd.DataFrame(data, columns=['index', 'sequence', 'pLDDT', 'pTM', 'ipTM'])

# Display the DataFrame
# print(df)

df.to_csv("rituximab_cut_sequences_predict.csv")
