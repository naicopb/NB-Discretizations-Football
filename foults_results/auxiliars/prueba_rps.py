import numpy as np

def main(true_labels, predicted_probs):
    """
    Calcula el Rank Probability Score (RPS) para un problema de clasificación con múltiples clases.

    Parameters:
    - true_labels: Array de etiquetas verdaderas (0, 1, 2, 3, ...).
    - predicted_probs: Matriz de probabilidades predichas por el modelo.

    Returns:
    - rps: Valor del RPS.
    """
    n_samples, n_classes = predicted_probs.shape
    rps = 0

    for i in range(n_samples):
        true_label = true_labels[i]
        sorted_probs = np.sort(predicted_probs[i, :])
        true_class_prob = sorted_probs[true_label]
        ecdf = np.cumsum(sorted_probs)
        rps += np.sum((ecdf[:true_label] - true_class_prob) ** 2)

    rps /= (n_samples * (n_classes - 1))  # Ajuste para el número de clases

    return rps
