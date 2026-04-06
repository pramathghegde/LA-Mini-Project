import numpy as np

def fill_missing_with_mean(matrix):
    filled = matrix.copy().astype(float)
    for col in range(matrix.shape[1]):
        non_zero = matrix[:, col][matrix[:, col] != 0]
        mean = np.mean(non_zero) if len(non_zero) > 0 else 0
        for row in range(matrix.shape[0]):
            if filled[row, col] == 0:
                filled[row, col] = mean
    return filled

def compute_all(matrix):
    A_filled = fill_missing_with_mean(matrix)
    user_means = np.mean(A_filled, axis=1, keepdims=True)
    A_norm = A_filled - user_means

    similarity = A_norm @ A_norm.T

    pred = np.zeros(matrix.shape)

    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if matrix[i, j] == 0:
                weights = similarity[i].copy()
                ratings = matrix[:, j]
                weights[i] = 0
                if np.sum(np.abs(weights)) != 0:
                    pred[i, j] = np.dot(weights, ratings) / np.sum(np.abs(weights))
            else:
                pred[i, j] = matrix[i, j]

    cov_matrix = A_norm.T @ A_norm
    eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)

    return A_filled, A_norm, similarity, pred, eigenvalues, eigenvectors