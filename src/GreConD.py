import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix, hstack, vstack
import os
import sys

def GreConD(I, k):
    M = (I == 1).astype(int)
    m, n = M.shape
    U = M.copy()
    
    A = csr_matrix((m, 0), dtype=bool)
    B = csr_matrix((0, n), dtype=bool)

    for _ in range(k):
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

        A = hstack([A, csr_matrix(cc[:, np.newaxis], dtype=bool)])
        B = vstack([B, csr_matrix(d[np.newaxis, :], dtype=bool)])

        U[cc, :] = np.logical_and(U[cc, :], np.logical_not(d))

    return A, B

if __name__ == "__main__":
    input_file = sys.argv[1]
    output_A = sys.argv[2]
    output_B = sys.argv[3]
    output_X = sys.argv[4]
    k = int(sys.argv[5])

    sample = os.path.basename(input_file).split('.')[0]
    data = np.load(input_file)
    I = data['matrix']

    A, B = GreConD(I, k)
    X_reconstructed = A.dot(B).toarray()

    for output in [output_A, output_B, output_X]:
        os.makedirs(os.path.dirname(output), exist_ok=True)

    for output, matrix in zip([output_A, output_B, output_X], [A, B, X_reconstructed]):
        np.savez_compressed(output, **{os.path.basename(output).split('.')[0]: matrix})
