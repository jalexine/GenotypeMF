# Discovering Structure in Genotype Matrices using Boolean Matrix Factorization

## Overview
This repository contains the code and data for my internship project on Boolean Matrix Factorization (BMF) applied to genotype matrices. The project was conducted at CBI under the supervision of Prof. Dr. Sven Rahmann from May 1 to July 12, 2024.

## Abstract
The Boolean Matrix Factorization (BMF) problem aims to approximate an m × n Boolean matrix X as the Boolean product of m× k and k × n matrices A and B. This project evaluates various BMF algorithms, including GreConD, ASSO, FastUndercover, and TopFiberM, to determine their effectiveness and efficiency in reconstructing genotype matrices.

## Algorithms Evaluated
ASSO : Uses a greedy approach with association confidences to construct binary basis vectors. Selects vectors to maximize 1s coverage while minimizing 0s.
GreConD : Creates formal concepts on demand, adding those that best cover uncovered entries until factor matrices match the input. 
TopFiberM : Selects and extends fibers (rows/columns) to optimally represent the matrix, using sum vectors to find fibers with maximum 1s.
FastUndercover Turns the problem into a MaxSAT instance with hard constraints to avoid false positives and soft constraints to maximize true positives.

## Project Structure
- **data/**: Contains genotype matrices used for the project.
- **scripts/**: Python and R scripts for reading matrices, running factorization algorithms, and plotting results.
- **results/**: Output files from the factorization algorithms, including coverage, false positives, false negatives, and true positives.
- **plots/**: Visualization of the normalized errors, running times, and Matthews Correlation Coefficient (MCC) for each algorithm.


## Getting Started

### Prerequisites
- Conda
(soon)
