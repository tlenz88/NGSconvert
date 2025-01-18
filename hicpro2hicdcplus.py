import pandas as pd
import sys

def load_chrom_sizes(chrom_sizes_file, bin_size):
    """Load chromosome sizes and create a bin-to-genomic-coordinate dictionary."""
    chrom_bins = {}
    for line in open(chrom_sizes_file):
        chrom, size = line.strip().split()
        size = int(size)
        
        # Calculate number of bins for the chromosome
        num_bins = size // bin_size
        if size % bin_size != 0:
            num_bins += 1  # If there's a remainder, we need one more bin
        
        chrom_bins[chrom] = (size, num_bins)  # Store size and number of bins for each chromosome
    
    return chrom_bins

def convert_hicpro_to_hicdc(hicpro_file, chrom_sizes_file, bin_size, output_file):
    # Load chromosome bin information
    chrom_bins = load_chrom_sizes(chrom_sizes_file, bin_size)
    
    # Load the HiC-Pro matrix file
    hicpro_df = pd.read_csv(hicpro_file, sep='\t', names=['bin1', 'bin2', 'count'])

    # Prepare columns for HiCDC+ output
    output_data = []

    for _, row in hicpro_df.iterrows():
        bin1, bin2, count = row['bin1'], row['bin2'], row['count']
        
        # Find the chromosome and coordinates for bin1
        bin1_chr, bin1_start, bin1_end = None, None, None
        for chrom, (chrom_size, num_bins) in chrom_bins.items():
            if bin1 < num_bins:
                bin1_chr = chrom
                bin1_start = bin1 * bin_size
                bin1_end = (bin1 + 1) * bin_size
                break
        
        # Find the chromosome and coordinates for bin2
        bin2_chr, bin2_start, bin2_end = None, None, None
        for chrom, (chrom_size, num_bins) in chrom_bins.items():
            if bin2 < num_bins:
                bin2_chr = chrom
                bin2_start = bin2 * bin_size
                bin2_end = (bin2 + 1) * bin_size
                break

        # If both bin1 and bin2 have valid chromosomes, add to output data
        if bin1_chr and bin2_chr:
            output_data.append([
                bin1_chr, bin1_start, bin1_end,
                bin2_chr, bin2_start, bin2_end,
                count
            ])
        else:
            print(f"Warning: bin1 or bin2 out of bounds for bin indices {bin1} or {bin2} with count {count}")

    # Convert to DataFrame and save as a tab-separated file
    output_df = pd.DataFrame(output_data, columns=['chr1', 'start1', 'end1', 'chr2', 'start2', 'end2', 'count'])
    output_df.to_csv(output_file, sep='\t', index=False)

    print(f"Conversion complete. Output saved to {output_file}")

# Usage example
if __name__ == "__main__":
    hicpro_file = sys.argv[1]
    chrom_sizes_file = sys.argv[2]
    bin_size = int(sys.argv[3])
    output_file = sys.argv[4]
    convert_hicpro_to_hicdc(hicpro_file, chrom_sizes_file, bin_size, output_file)
