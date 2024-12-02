import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse
import os
 
 
def parse_args():
    parser = argparse.ArgumentParser(description="Create a Manhattan plot from GWAS summary statistics.")
    parser.add_argument("--input", type=str, required=True, help="Path to the input GWAS summary statistics file.")
    parser.add_argument("--sep", type=str, default=" ", required=False, help="Separator of the input file.")
    parser.add_argument("--outpath", type=str, required=True, help="Path to save the output Manhattan plot.")
    parser.add_argument("--title", type=str, default="Example", help="Title of the plot.")
    parser.add_argument("--chr", type=str, default="CHROM", help="Name of the chromosome column.")
    parser.add_argument("--pos", type=str, default="GENPOS", help="Name of the base pair position column.")
    parser.add_argument("--p", type=str, default="NONE", help="Name of the p-value column.")
    parser.add_argument("--neglog10p", type=str, default="NONE", help="Name of the -log10(p-value) column.")
    parser.add_argument("--size", type=float, default=3.0, help="Size of the inner point.")
    parser.add_argument("--stroke_size", type=float, default=0.7, help="Size of the point stroke.")
    parser.add_argument("--figsize", type=float, nargs=2, default=(15, 6), help="Figure size (width, height).")
    parser.add_argument("--sig_threshold", type=float, default=5e-8, help="Genome-wide significance threshold.")
    parser.add_argument("--qq", type=bool, default=False, help="Show QQ plot.")
    return parser.parse_args()
 
 
def manhattan_plot(df,
                   title="Manhattan Plot",
                   chr="CHROM",
                   pos="GENPOS",
                   p="NONE",
                   neglog10p="NONE",
                   size=3.0,
                   stroke_size=0.7,
                   figsize=(15, 6),
                   sig_threshold=5e-8,
                   outpath=None,
                   qq=True):
    """
    Create a Manhattan plot from GWAS summary statistics.
    
    Parameters:
    df (pd.DataFrame): DataFrame containing GWAS summary statistics.
    title (str): Title of the plot. Default is "Manhattan Plot".
    chr (str): Name of the chromosome column. Default is "CHROM".
    pos (str): Name of the base pair position column. Default is "GENPOS".
    p (str): Name of the p-value column. Default is "NONE".
    neglog10p (str): Name of the -log10(p-value) column. Default is "NONE".
    size (float): Size of the inner point. Default is 3.0.
    stroke_size (float): Size of the point stroke. Default is 0.7.
    figsize (tuple): Figure size. Default is (15, 6).
    sig_threshold (float): Genome-wide significance threshold. Default is 5e-8.
    outpath (str): Path to save the output Manhattan plot.
    qq (bool): Show QQ plot. Default is True.
    Returns:
    matplotlib.figure.Figure: The created figure object.
    """
    
    plt.figure(figsize=figsize)
 
    colors = ['#db6e64', '#d16d3b', '#f4dc65', '#31a868', '#b07aa1']
    x_pos = 0
    x_ticks = []
    x_labels = []
 
    df[chr] = pd.to_numeric(df[chr].replace('X', '23'))
 
    def geom_caviar(x, y, c, size=size, stroke_size=stroke_size):
        bgsize = size + stroke_size * 2
        plt.scatter(x, y, s=bgsize**2, c='black')
        plt.scatter(x, y, s=size**2, c=c, alpha=1)
 
    for chrom in sorted(df[chr].unique()):
        chrom_data = df[df[chr] == chrom].sort_values(pos)
        
        if neglog10p != "NONE":
            y_values = chrom_data[neglog10p]
        elif p != "NONE":
            y_values = -np.log10(chrom_data[p])
        elif neglog10p != "NONE" and p != "NONE":
            raise ValueError("Only one of 'neglog10p' or 'p' must be specified.")
        else:
            raise ValueError("Either 'neglog10p' or 'p' must be specified.")
 
        geom_caviar(chrom_data[pos] + x_pos, y_values, colors[int(chrom) % len(colors)])
        
        # Calculate the midpoint of each chromosome's data
        chrom_midpoint = x_pos + (chrom_data[pos].max() + chrom_data[pos].min()) / 2
        x_ticks.append(chrom_midpoint)
        x_labels.append('X' if chrom == 23 else str(chrom))
 
        x_pos += chrom_data[pos].max()
 
    plt.xticks(x_ticks, x_labels)
    plt.xlabel('Chromosome', fontsize=14)
    plt.ylabel(r'$-\log_{10}(p\text{-value})$', fontsize=14)
    plt.ylim(0, None)
    plt.xlim(-0.007 * x_pos, 1.007 * x_pos)
    plt.title(title, fontsize=14)
 
    plt.axhline(y=-np.log10(sig_threshold), color='gray', linestyle='--', label='Genome-wide significance', linewidth=0.5)
 
    plt.tight_layout()
    plt.tick_params(axis='both', which='both', direction='in')
 
    plt.savefig(os.path.join(outpath, f"{title}_manhattan_plot.png"), dpi=600)
 
    print("")
    print(f"Manhattan plot saved to {os.path.join(outpath, f'{title}_manhattan_plot.png')}")
    print("")
 
if __name__ == "__main__":
    args = parse_args()
 
    # show all the args and align them
    print("")
    print("*" * 80)
    print(f"Input file:                 {args.input}")
    print(f"Output path:                {args.outpath}")
    print(f"Title:                      {args.title}")
    print(f"Chromosome column:          {args.chr}")
    print(f"Position column:            {args.pos}")
    print(f"P-value column:             {args.p}")
    print(f"Neglog10(p-value) column:   {args.neglog10p}")
    print(f"Size:                       {args.size}")
    print(f"Stroke size:                {args.stroke_size}")
    print(f"Figure size:                {args.figsize}")
    print(f"Output path:                {args.outpath}")
    print(f"Show QQ plot:               {args.qq}")
    print("*" * 80)
    print("")
 
    df = pd.read_csv(args.input, sep=args.sep)
    fig = manhattan_plot(df,
                         title=args.title,
                         chr=args.chr,
                         pos=args.pos,
                         p=args.p,
                         neglog10p=args.neglog10p,
                         size=args.size,
                         stroke_size=args.stroke_size,
                         figsize=args.figsize,
                         sig_threshold=args.sig_threshold,
                         outpath=args.outpath,
                         qq=args.qq)
