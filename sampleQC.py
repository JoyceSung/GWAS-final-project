def subset_eids(inpath="../", ethnicity="white_british", outpath="../GWAS_INPUT/", sex="all", remove="None"):
    try:
        # ALL UK Biobank PATIENTS

        all_ukb = pd.read_csv(f"{inpath}/fid31.csv")[['eid']]

        # ETHNICITY QC
        if ethnicity == "white_british":
            eth_genetic = pd.read_csv(f"{inpath}/fid22006.csv")
            eth_genetic = eth_genetic.dropna(subset=['22006-0.0']).rename(columns={'22006-0.0': 'caucasian'})

            eth_survey = pd.read_csv(f"{inpath}/fid21000.csv")
            cauc_whit_brit = pd.merge(eth_genetic, eth_survey, on='eid', how='inner').dropna()

        # GENETIC QC
        sex_report_df = pd.read_csv(f"{inpath}/fid31.csv").rename(columns={'31-0.0': 'sex_report'})
        sex_df = (sex_gen_df.merge(sex_report_df, on='eid'))
        if sex == "male":
            sex_df = sex_df.query('sex_genetic == 1')
        elif sex == "female":
            sex_df = sex_df.query('sex_genetic == 0')

        # Combine everything
        all_filter_df = (all_ukb[~all_ukb.eid.isin(withdraw_eids.remove_eid)]
                             .merge(cauc_whit_brit, on='eid')
                             .merge(sex_df, on='eid'))

        df = pd.DataFrame({'eid': all_filter_df.eid, 'eid_copy': all_filter_df.eid})
        output_file = f"{outpath}/geno_qced_eids_{ethnicity}_{sex}_{date.today()}.txt"
        df.to_csv(output_file, sep=' ', index=False, header=False)

        print(f"qced_eids file successfully created: {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")
