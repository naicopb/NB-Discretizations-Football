import numpy as np
from mdlp.discretization import MDLP

def main():
    arr1 = [655.0, 625.5, 609.5, 596.5, 593.0, 586.0, 582.5, 563.0, 560.0, 557.5, 554.0, 545.0, 539.5, 533.5, 528.5, 525.5, 506.5, 501.0, 494.5, 454.5]
    arr2 = [682.0, 665.5, 647.5, 622.5, 621.5, 606.0, 583.5, 573.0, 569.0, 562.5, 545.0, 543.5, 537.0, 531.5, 514.5, 500.0, 488.0, 468.0, 447.5, 403.0]

    X = []
    y = [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4]
    for element in arr1:
        X.append([element])
    X = np.array(X)
    y = np.array(y)

    discretizer = MDLP()
    X_discretized = discretizer.fit_transform(X, y)

    print("Original_1:", X.ravel())
    print("Discretizado_1:", X_discretized.ravel())

    X = []
    y = [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4]
    for element in arr2:
        X.append([element])
    X = np.array(X)
    y = np.array(y)

    discretizer = MDLP()
    X_discretized = discretizer.fit_transform(X, y)

    print("Original_2:", X.ravel())
    print("Discretizado_2:", X_discretized.ravel())



main()
