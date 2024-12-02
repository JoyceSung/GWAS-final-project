import pandas as pd
import os
from datetime import date

# Set paths
path = f"{path}/pheno_split_into_files_011924"
output = f"{output_dir}covariant"

# Load data
pcs = pd.read_csv(os.path.join(path, "fid22009.csv"), sep=',')
pcs.columns = ["eid"] + [f"PC{i}" for i in range(1, 41)]
age = pd.read_csv(os.path.join(path, "fid21003.csv"))[['eid', '21003-0.0']].rename(columns={'21003-0.0': 'AGE'})
sex = pd.read_csv(os.path.join(path, "fid31.csv")).rename(columns={'31-0.0': 'SEX'})

indiv = pd.read_csv("/scratch1/10173/chiayusung0526/GWAS/GWAS_result/Diabetes/GWAS_input_data/eids_snps/geno_qced_eids_white_british_all_2024-09-25.txt", sep=' ', header=None)
indiv.columns = ['eid', 'eid_copy']

# Merge data
covar = indiv.merge(pcs, on='eid', how='inner').merge(age, on='eid', how='inner').merge(sex, on='eid', how='inner')

# Remove NAs and create derived columns

covar = covar.dropna()
covar['AGE2'] = covar['AGE']**2
covar['SEXAGE'] = covar['SEX'] * covar['AGE']
covar['SEXAGE2'] = covar['SEX'] * covar['AGE']**2

# Rename columns and save
covar.rename(columns={'eid': 'FID', 'eid_copy': 'IID'}, inplace=True)
covar.to_csv(f"{output}/covar_all_{date.today()}.txt", sep=' ', index=False)

print(f"Covariates file saved to {output}/covar_all_{date.today()}.txt")
