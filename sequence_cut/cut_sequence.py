import random
import pickle

def find_all_subsequences(seq, length, required_positions):
    """
    Find all subsequences of the given length from the input sequence that must include required positions.

    :param seq: The original sequence (string).
    :param length: Length of the subsequence (int).
    :param required_positions: List of required positions to be included in the subsequence (0-based).
    :return: A list of all subsequences of the given length that include the required positions.
    """
    seq_length = len(seq)

    # Validate input
    if length > seq_length:
        raise ValueError("Requested length is longer than the sequence.")
    
    if max(required_positions) >= seq_length:
        raise ValueError("Required positions are outside the sequence length.")
    
    # Find valid start positions
    min_start = min(required_positions) - (length - 1)  # Ensure the first required position fits
    max_start = max(required_positions)  # Ensure the last required position fits

    # Adjust start range to be within valid bounds
    valid_start_positions = range(max(0, min_start), min(seq_length - length + 1, max_start + 1))

    # Collect all valid subsequences
    subsequences = []
    for start_position in valid_start_positions:
        subsequence = seq[start_position:start_position + length]

        # Check if all required positions are within the subsequence
        if all(start_position <= pos < start_position + length for pos in required_positions):
            subsequences.append(subsequence)

    return subsequences

# Example usage:
sequence = "QVQLQQPGAELVKPGASVKMSCKASGYTFTSYNMHWVKQTPGRGLEWIGAIYPGNGDTSYNQKFKGKATLTADKSSSTAYMQLSSLTSEDSAVYYCARSTYYGGDWYFNVWGAGTTVTVS"
required_positions = [32, 34, 46, 49, 50, 51, 56, 57, 58]  # Positions that must be included (0-based)
print([sequence[i] for i in required_positions])

all_subseqs = find_all_subsequences(sequence, 80, required_positions)

# Print all possible subsequences
for i, subseq in enumerate(all_subseqs):
    print(f"Subsequence {i+1}: {subseq}")
    with open('rituximab_ori_seq_'+str(i)+'.fasta', 'w') as f:
                f.write(""">rituximab_ori_"""+str(i)+"""
MRESKTLGAVQIMNGLFHIALGGLLMIPAGIYAPICVTVWYPLWGGIMYIISGSLLAATEKNSRKCLVKGKMIMNSLSLFAAISGMILSIMDILNIKISHFLKMESLNFIRAHTPYINIYNCEPANPSEKNSPSTQYCYSIQSLFLGILSVMLIFAFFQELVIAG:MRESKTLGAVQIMNGLFHIALGGLLMIPAGIYAPICVTVWYPLWGGIMYIISGSLLAATEKNSRKCLVKGKMIMNSLSLFAAISGMILSIMDILNIKISHFLKMESLNFIRAHTPYINIYNCEPANPSEKNSPSTQYCYSIQSLFLGILSVMLIFAFFQELVIAG:"""+subseq+"""
""" )

with open("all_cut_seq.pkl", 'wb') as f:
     pickle.dump(all_subseqs,f)

