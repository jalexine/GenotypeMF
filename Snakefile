GENOTYPE_FILES = ["PL", "GU"]
k_values = [5,10, 20, 30, 40, 50]


rule all:
    input:
        expand("results/{sample}/ABMatrix/{sample}_GreConDA_k{k}.npz", sample=GENOTYPE_FILES, k=k_values),
        expand("results/{sample}/ABMatrix/{sample}_GreConDB_k{k}.npz", sample=GENOTYPE_FILES, k=k_values),
        expand("results/{sample}/reconstructed_matrix/{sample}_GreConD_reconstructed_k{k}.npz", sample=GENOTYPE_FILES, k=k_values),
        expand("results/{sample}/ABMatrix/{sample}_TopFiberA_k{k}.npz", sample=GENOTYPE_FILES, k=k_values),
        expand("results/{sample}/ABMatrix/{sample}_TopFiberB_k{k}.npz", sample=GENOTYPE_FILES, k=k_values),
        expand("results/{sample}/reconstructed_matrix/{sample}_TopFiber_reconstructed_k{k}.npz", sample=GENOTYPE_FILES, k=k_values),
        expand("results/{sample}/ABMatrix/{sample}_ASSOA_k{k}.npz", sample=GENOTYPE_FILES, k=k_values),
        expand("results/{sample}/ABMatrix/{sample}_ASSOB_k{k}.npz", sample=GENOTYPE_FILES, k=k_values),
        expand("results/{sample}/reconstructed_matrix/{sample}_ASSO_reconstructed_k{k}.npz", sample=GENOTYPE_FILES, k=k_values)

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
        "results/{sample}/ABMatrix/{sample}_GreConDA_k{k}.npz",
        "results/{sample}/ABMatrix/{sample}_GreConDB_k{k}.npz",
        "results/{sample}/reconstructed_matrix/{sample}_GreConD_reconstructed_k{k}.npz"
    log:
        "results/{sample}/{sample}TopFiber_k{k}.log"
    params:
        k="{k}"
    shell:
        "python scripts/GreConD.py {input} {output[0]} {output[1]} {output[2]} {params.k}"

rule asso:
    input:
        "data/{sample}.npz"
    output:
        "results/{sample}/ABMatrix/{sample}_ASSOA_k{k}.npz",
        "results/{sample}/ABMatrix/{sample}_ASSOB_k{k}.npz",
        "results/{sample}/reconstructed_matrix/{sample}_ASSO_reconstructed_k{k}.npz"
    log:
        "results/{sample}/{sample}ASSO_k{k}.log"
    params:
        k="{k}",
        sample="{sample}",
        verbose=0,
        threshold=0.6,
        penalty=4,
        bonus=2
    shell:
        "python scripts/ASSO.py {input} {output[0]} {output[1]} {output[2]} {params.k} {params.verbose} {params.threshold} {params.penalty} {params.bonus}"

rule topfiber:
    input:
        "data/{sample}.npz"
    output:
        "results/{sample}/ABMatrix/{sample}_TopFiberA_k{k}.npz",
        "results/{sample}/ABMatrix/{sample}_TopFiberB_k{k}.npz",
        "results/{sample}/reconstructed_matrix/{sample}_TopFiber_reconstructed_k{k}.npz"
    log:
        "results/{sample}/{sample}TopFiber_k{k}.log"
    params:
        k="{k}",  
        sample="{sample}",
        tPval=0.8,
        verbose=2,
        search_limits=200
    shell:
        "python scripts/TopFiberM.py {input} {output[0]} {output[1]} {output[2]} {params.k} {params.tPval} {params.verbose} {params.search_limits}"
