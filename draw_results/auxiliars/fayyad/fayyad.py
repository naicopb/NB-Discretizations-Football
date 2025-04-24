import numpy as np
from mdlp.discretization import MDLP

def main():
    array = [{'position': 1, 'porcentaje': 0.8009009009009009}, {'position': 2, 'porcentaje': 0.7563063063063062}, {'position': 3, 'porcentaje': 0.6743243243243244}, {'position': 4, 'porcentaje': 0.5666666666666667}, {'position': 5, 'porcentaje': 0.5216216216216216}, {'position': 6, 'porcentaje': 0.5099099099099098}, {'position': 7, 'porcentaje': 0.4806306306306306}, {'position': 8, 'porcentaje': 0.45855855855855865}, {'position': 9, 'porcentaje': 0.4398398398398399}, {'position': 10, 'porcentaje': 0.4247247247247247}, {'position': 11, 'porcentaje': 0.4204704704704705}, {'position': 12, 'porcentaje': 0.40875875875875883}, {'position': 13, 'porcentaje': 0.3972472472472473}, {'position': 14, 'porcentaje': 0.3834334334334334}, {'position': 15, 'porcentaje': 0.3711711711711711}, {'position': 16, 'porcentaje': 0.3626126126126126}, {'position': 17, 'porcentaje': 0.3517517517517518}, {'position': 18, 'porcentaje': 0.34609609609609604}, {'position': 19, 'porcentaje': 0.3422922922922923}, {'position': 20, 'porcentaje': 0.32497497497497496}]
    X = []
    y = [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4]
    for element in array:
        X.append([element['porcentaje']])
    X = np.array(X)
    y = np.array(y)

    discretizer = MDLP()
    X_discretized = discretizer.fit_transform(X, y)

    print("Original:", X.ravel())
    print("Discretizado:", X_discretized.ravel())


"""
# Simulamos una variable continua (X) y sus clases (y)
X = np.array([[5.1], [4.9], [6.2], [5.5], [7.3], [4.7], [6.8], [5.0]])
y = np.array([0, 0, 1, 1, 2, 0, 2, 1])

# Instanciar y aplicar el discretizador
discretizer = MDLP()
X_discretized = discretizer.fit_transform(X, y)

print("Original:", X.ravel())
print("Discretizado:", X_discretized.ravel())
"""

main()
