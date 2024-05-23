GENOTYPE_FILES = ["PL.txt", "GU.txt"]

# Default configuration
configfile: "config.yaml"

rule all:
    input:
        "results/PL/coverage_plot.png",
        "results/GU/coverage_plot.png"

rule read_matrix:
    input:
        "data/{sample}.txt"
    output:
        "data/{sample}.npz"
    conda:
        "envs/gmf.yaml"
    shell:
        "python readmatrix.py {input} {output}"

rule grecond:
    input:
        "data/{sample}.npz"
    output:
        "results/{sample}/A_matrix.txt",
        "results/{sample}/B_matrix.txt",
        "results/{sample}/coverage_results.txt"
    params:
        max_factors=config["maxf"]
    conda:
        "envs/gmf.yaml"
    shell:
        "python GreConD.py {input} {params.max_factors}"

rule plot_coverage:
    input:
        "results/{sample}/coverage_results.txt"
    output:
        "results/{sample}/coverage_plot.png"
    conda:
        "envs/gmf.yaml"
    shell:
        "python coverage.py {input} {output}"
