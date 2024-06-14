GENOTYPE_FILES = ["PL", "GU"]
k_values = [5, 10, 20, 30, 40, 50]

configfile: "config.yaml"

rule all:
    input:
        expand("results/{sample}/FastUndercover/Ak{k}FastU.csv", sample=GENOTYPE_FILES, k=k_values),
        expand("results/{sample}/FastUndercover/Bk{k}FastU.csv", sample=GENOTYPE_FILES, k=k_values),
        expand("results/{sample}/Optiblock/Ak{k}OptiB.csv", sample=GENOTYPE_FILES, k=k_values),
        expand("results/{sample}/Optiblock/Bk{k}OptiB.csv", sample=GENOTYPE_FILES, k=k_values)

rule convert_to_csv:
    input:
        "data/{sample}.txt"
    output:
        "data/{sample}.csv"
    conda:
        "envs/gmf.yaml"
    shell:
        "python tocsv.py {input} {output}"

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
        "results/{sample}/coverage_results.txt",
        "results/{sample}/error_results.txt",
        "results/{sample}/results_summary.csv"

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

rule calculate_error:
    input:
        original="data/{sample}.npz",
        A_matrix="results/{sample}/A_matrix.txt",
        B_matrix="results/{sample}/B_matrix.txt"
    output:
        "results/{sample}/error.txt"
    conda:
        "envs/gmf.yaml"
    shell:
        "python error.py {input.original} {input.A_matrix} {input.B_matrix} {output}"

rule FastUndercover:
    input:
        csv_file="data/{sample}.csv"
    output:
        A=expand("results/{{sample}}/FastUndercover/Ak{k}FastU.csv", k=k_values),
        B=expand("results/{{sample}}/FastUndercover/Bk{k}FastU.csv", k=k_values)
    params:
        k_values=k_values
    conda:
        "envs/gmf.yaml"
    shell:
        """
        for k in {params.k_values}; do
            ./UndercoverBMF/inferbmf -k $k fromFile -o results/{wildcards.sample}/FastUndercover/Ak${{k}}FastU.csv -O results/{wildcards.sample}/FastUndercover/Bk${{k}}FastU.csv {input.csv_file}
        done
        """
rule Optiblock:
    input:
        csv_file="data/{sample}.csv"
    output:
        A=expand("results/{{sample}}/Optiblock/Ak{k}OptiB.csv", k=k_values),
        B=expand("results/{{sample}}/Optiblock/Bk{k}OptiB.csv", k=k_values)
    params:
        k_values=k_values
    conda:
        "envs/gmf.yaml"
    shell:
        """
        for k in {params.k_values}; do
            ./UndercoverBMF/inferbmf -k $k --OptiBlock fromFile -o results/{wildcards.sample}/OptiBlock/Ak${{k}}OptiB.csv -O results/{wildcards.sample}/Optiblock/Bk${{k}}OptiB.csv {input.csv_file}
        done
        """