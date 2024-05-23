import numpy as np
from scipy.sparse import csr_matrix, hstack, vstack
import os
import sys

def GreConD(I, max_factors=100):
    M = (I == 1)
    m, n = M.shape
    U = M.copy()
    k = 0

    A = csr_matrix((m, 0), dtype=bool)
    B = csr_matrix((0, n), dtype=bool)
    coverage_list = []

    while np.sum(U) > 0:
        v = 0
        d = np.zeros(n, dtype=bool)
        d_old = d.copy()
        d_mid = d.copy()
        e = np.ones((m, 1), dtype=bool)

        atr = np.where(np.sum(U, axis=0) > 0)[0]

        while True:
            for j in atr:
                if not d[j]:
                    a = np.logical_and(e.flatten(), M[:, j])
                    b = np.all(M[a, :], axis=0) if np.sum(a) > 0 else np.ones(n, dtype=bool)
                    cost = np.sum(U[a, :][:, b])

                    if cost > v:
                        v = cost
                        d_mid = b
                        cc = a

            d = d_mid
            e = cc[:, np.newaxis]

            if np.array_equal(d, d_old):
                break
            else:
                d_old = d

        k += 1

        A = hstack([A, csr_matrix(cc[:, np.newaxis], dtype=bool)])
        B = vstack([B, csr_matrix(d[np.newaxis, :], dtype=bool)])

        U[cc, :] = np.logical_and(U[cc, :], np.logical_not(d))
        
        # Calculate coverage
        coverage = 1 - np.sum(U) / np.sum(M)
        coverage_list.append(coverage)

        if k >= max_factors:
            break

    return A, B, k, coverage_list

if __name__ == "__main__":
    input_file = sys.argv[1]
    max_factors = int(sys.argv[2])
    sample = os.path.basename(input_file).split('.')[0]
    data = np.load(input_file)
    I = data['matrix']

    A, B, k, coverage_list = GreConD(I, max_factors=max_factors)

    output_dir = f'results/{sample}'
    os.makedirs(output_dir, exist_ok=True)

    # Save A and B matrices as .txt files
    np.savetxt(f'{output_dir}/A_matrix.txt', A.todense(), fmt='%d')
    np.savetxt(f'{output_dir}/B_matrix.txt', B.todense(), fmt='%d')
    np.savetxt(f'{output_dir}/coverage_results.txt', coverage_list)
