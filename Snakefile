GENOTYPE_FILES = ["PL.txt", "GU.txt"]
MAX_FACTORS = 100

rule all:
    input:
        "results/PL/A_matrix.txt",
        "results/PL/B_matrix.txt",
        "results/PL/coverage_plot.png",
        "results/GU/A_matrix.txt",
        "results/GU/B_matrix.txt",
        "results/GU/coverage_plot.png"

rule read_matrix:
    input:
        "data/{sample}.txt"
    output:
        "data/{sample}.npz"
    shell:
        "python readmatrix.py {input} {output}"

rule grecond:
    input:
        "data/{sample}.npz"
    output:
        "results/{sample}/A_matrix.txt",
        "results/{sample}/B_matrix.txt",
        "results/{sample}/coverage_results.txt"
    shell:
        "python GreConD.py {input} " + str(MAX_FACTORS)

rule plot_coverage:
    input:
        "results/{sample}/coverage_results.txt"
    output:
        "results/{sample}/coverage_plot.png"
    shell:
        "python coverage.py {input} {output}"
