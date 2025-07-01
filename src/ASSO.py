import sys
import os
import rpy2.robjects as ro
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr
import numpy as np

pandas2ri.activate()

def main(input_file, output_A, output_B, output_X, k, verbose, threshold, penalty, bonus):
    data = np.load(input_file)
    dblp_np = data['matrix']
    rbmf = importr('rBMF')

    opti = ro.ListVector({
        'verbose': verbose,
        'threshold': threshold,
        'penalty_overcovered': penalty,
        'bonus_covered': bonus
    })

    result = rbmf.Asso_approximate(dblp_np, k, opti)

    r_A = result.rx2('B')
    r_B = result.rx2('O')
    r_X = result.rx2('D')

    A = np.array(ro.conversion.rpy2py(ro.r['as'](r_A, 'matrix')))
    B = np.array(ro.conversion.rpy2py(ro.r['as'](r_B, 'matrix')))
    X = np.array(ro.conversion.rpy2py(ro.r['as'](r_X, 'matrix')))

    np.savez(output_A, matrix=A)
    np.savez(output_B, matrix=B)
    np.savez(output_X, matrix=X)


if __name__ == "__main__":
    input_file = sys.argv[1]
    output_A = sys.argv[2]
    output_B = sys.argv[3]
    output_X = sys.argv[4]
    k = int(sys.argv[5])
    verbose = int(sys.argv[6])
    threshold = float(sys.argv[7])
    penalty = float(sys.argv[8])
    bonus = float(sys.argv[9])

    main(input_file, output_A, output_B, output_X, k, verbose, threshold, penalty, bonus)
