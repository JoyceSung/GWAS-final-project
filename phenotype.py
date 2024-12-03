import pandas as pd
import os

# Specify input and output paths
fid_path = f"{path}/binary_ICD_011924.txt"

out_path = f"{output_dir}/GWAS_input_data/pheno/"

# Read the data, selecting relevant columns

df = pd.read_csv(fid_path, sep=' ', header=0, usecols=['Patient EID', 'C50'])

# Create FID and IID columns from the patient ID column
df['IID'] = df['Patient EID']
df['FID'] = df['Patient EID']

# Convert E11 values to binary: 1 for breast cancer, 0 otherwise

df['Breast_cancer'] = df['C50'].apply(lambda x: 1 if x == 1 else 0)

# Remove rows with any missing values
df.dropna(inplace=True)

# Keep only rows with valid binary values (0 or 1)
df = df[df['Breast_cancer'].isin([0, 1])]

# Select columns for the final output
df = df[['FID', 'IID', 'Breast_cancer']]

# Save to output file
output_file = os.path.join(out_path, "BC_pheno.txt")
df.to_csv(output_file, sep=' ', index=False)


print(f"Phenotype file created: {output_file}")

