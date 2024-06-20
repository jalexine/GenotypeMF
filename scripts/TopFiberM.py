import sys
import os
import rpy2.robjects as ro
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr
import numpy as np

pandas2ri.activate()

def main(input_file, output_A, output_B, output_X, k, tP, verbose, search_limit):
    data = np.load(input_file)
    dblp_np = data['matrix']
    rbmf = importr('rBMF')
    params = ro.ListVector({
        'r': k,
        'tP': tP,
        'verbose': verbose,
        'SR': search_limit
    })

    result = rbmf.topFiberM(dblp_np, k, tP, verbose, search_limit)

    r_A = result.rx2('A')
    r_B = result.rx2('B')

    A = np.array(ro.conversion.rpy2py(ro.r['as'](r_A, 'matrix')))
    B = np.array(ro.conversion.rpy2py(ro.r['as'](r_B, 'matrix')))

    X = np.dot(A, B)

    np.savez(output_A, matrix=A)
    np.savez(output_B, matrix=B)
    np.savez(output_X, matrix=X)

if __name__ == "__main__":
    input_file = sys.argv[1]
    output_A = sys.argv[2]
    output_B = sys.argv[3]
    output_X = sys.argv[4]
    k = int(sys.argv[5])
    tP = float(sys.argv[6])
    verbose = int(sys.argv[7])
    search_limit = int(sys.argv[8])

    main(input_file, output_A, output_B, output_X, k, tP, verbose, search_limit)
