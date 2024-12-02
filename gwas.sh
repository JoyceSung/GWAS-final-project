#!/bin/bash

#SBATCH -J breast_imp_bt
#SBATCH -o /scratch1/10173/chiayusung0526/GWAS/GWAS_result/log/breast_imp_bt.%j.o
#SBATCH -e /scratch1/10173/chiayusung0526/GWAS/GWAS_result/log/breast_imp_bt.%j.e
#SBATCH -p small
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -t 48:00:00
#SBATCH -A MCB20049
#SBATCH --mail-user=chiayusung@utexas.edu
#SBATCH --mail-type=all

source /home1/10173/chiayusung0526/miniconda3/etc/profile.d/conda.sh
conda activate regenie_env

# Set directories
OUT_DIR="/scratch1/10173/chiayusung0526/GWAS/GWAS_result/BreasrCancer/REGENIE_output_data/breast_imp_bt"
GWAS_DATA="/scratch1/10173/chiayusung0526/GWAS/GWAS_data/ukb_maf0.001_pfile/merged_pfile_maf0.001"
SNPS_STEP1="/scratch1/10173/chiayusung0526/GWAS/GWAS_result/BreasrCancer/GWAS_input_data/qced_snps/wb_qced_snps_regenie_step1/qced_wb_both_step1.snplist"
SNPS_STEP2="/scratch1/10173/chiayusung0526/GWAS/GWAS_result/BreasrCancer/GWAS_input_data/qced_snps/wb_qced_snps_regenie_step2/qced_wb_both_step2.snplist"
EIDS="/scratch1/10173/chiayusung0526/GWAS/GWAS_result/BreasrCancer/GWAS_input_data/eids_snps/geno_qced_eids_white_british_all_2024-09-25_removed_image_data.txt"
PHENO="/scratch1/10173/chiayusung0526/GWAS/GWAS_result/BreasrCancer/GWAS_input_data/pheno/bc_pheno_combined.txt"
COVAR="/scratch1/10173/chiayusung0526/GWAS/GWAS_result/BreasrCancer/GWAS_input_data/covariant/covar_all_2024-10-02.txt"

# Step 1
mkdir -p $OUT_DIR
regenie \
   --step 1 \
   --pgen $GWAS_DATA \
   --extract $SNPS_STEP1 \
   --keep $EIDS \
   --phenoFile $PHENO \
   --phenoCol Breast_cancer \
   --covarFile $COVAR \
   --covarColList PC1-PC20,AGE,SEX,AGE2,SEXAGE,SEXAGE2 \
   --bsize 1000 \
   --bt \
   --out $OUT_DIR/breast_imp_bt_step1_out

# Step 2
regenie \
   --step 2 \
   --pgen $GWAS_DATA \
   --ref-first \
   --extract $SNPS_STEP2 \
   --keep $EIDS \
   --phenoFile $PHENO \
   --phenoCol Breast_cancer \
   --covarFile $COVAR \
   --covarColList PC1-PC20,AGE,SEX,AGE2,SEXAGE,SEXAGE2 \
   --bt \
   --pred $OUT_DIR/breast_imp_bt_step1_out_pred.list \
   --bsize 400 \
   --out $OUT_DIR/breast_imp_bt_step2
