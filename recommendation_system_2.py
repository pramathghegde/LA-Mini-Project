import numpy as np

# -------------------------------
# STEP 1: Realistic Dataset
# -------------------------------

users = ["Aman", "Riya", "Karan", "Neha", "Arjun"]
products = ["Laptop", "Phone", "Shoes", "Watch"]

# 0 means not rated
A = np.array([
    [5, 3, 0, 1],
    [4, 0, 0, 1],
    [1, 1, 0, 5],
    [0, 0, 5, 4],
    [0, 1, 5, 4],
])

# -------------------------------
# DISPLAY MATRIX WITH HEADERS
# -------------------------------

print("\n===== USER-PRODUCT MATRIX =====\n")

# Print header
print("User".ljust(10), end="")
for p in products:
    print(p.ljust(10), end="")
print()

# Print rows
for i in range(len(users)):
    print(users[i].ljust(10), end="")
    for j in range(len(products)):
        print(str(A[i][j]).ljust(10), end="")
    print()


# -------------------------------
# STEP 2: Fill Missing Values
# -------------------------------

def fill_missing_with_mean(matrix):
    filled = matrix.copy().astype(float)
    
    for col in range(matrix.shape[1]):
        non_zero = matrix[:, col][matrix[:, col] != 0]
        mean = np.mean(non_zero) if len(non_zero) > 0 else 0
        
        for row in range(matrix.shape[0]):
            if filled[row, col] == 0:
                filled[row, col] = mean
                
    return filled


A_filled = fill_missing_with_mean(A)

print("\n===== FILLED MATRIX =====\n")
print(A_filled)


# -------------------------------
# STEP 3: Normalize
# -------------------------------

user_means = np.mean(A_filled, axis=1, keepdims=True)
A_normalized = A_filled - user_means

print("\n===== NORMALIZED MATRIX =====\n")
print(A_normalized)


# -------------------------------
# STEP 4: Similarity Matrix
# -------------------------------

similarity = A_normalized @ A_normalized.T

print("\n===== USER SIMILARITY MATRIX =====\n")
print(similarity)


# -------------------------------
# STEP 5: Predict Ratings
# -------------------------------

def predict_ratings(original, similarity):
    pred = np.zeros(original.shape)
    
    for i in range(original.shape[0]):
        for j in range(original.shape[1]):
            
            if original[i, j] == 0:
                weights = similarity[i].copy()
                ratings = original[:, j]
                
                weights[i] = 0
                
                if np.sum(np.abs(weights)) != 0:
                    pred[i, j] = np.dot(weights, ratings) / np.sum(np.abs(weights))
                else:
                    pred[i, j] = 0
            else:
                pred[i, j] = original[i, j]
    
    return pred


predicted = predict_ratings(A, similarity)

# -------------------------------
# DISPLAY PREDICTED MATRIX WITH NAMES
# -------------------------------

print("\n===== PREDICTED RATINGS MATRIX =====\n")

print("User".ljust(10), end="")
for p in products:
    print(p.ljust(12), end="")
print()

for i in range(len(users)):
    print(users[i].ljust(10), end="")
    for j in range(len(products)):
        print(f"{predicted[i][j]:.2f}".ljust(12), end="")
    print()


# -------------------------------
# STEP 6: Recommendations
# -------------------------------

print("\n===== FINAL RECOMMENDATIONS =====\n")

for i in range(len(users)):
    unrated = np.where(A[i] == 0)[0]
    
    if len(unrated) > 0:
        best_index = unrated[np.argmax(predicted[i, unrated])]
        
        print(f"{users[i]} → Recommended: {products[best_index]} "
              f"(Predicted Rating: {predicted[i][best_index]:.2f})")
    else:
        print(f"{users[i]} → All products already rated")


# -------------------------------
# STEP 7: Eigen Analysis
# -------------------------------

cov_matrix = A_normalized.T @ A_normalized

eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)

print("\n===== EIGENVALUES =====\n")
print(eigenvalues)

print("\n===== EIGENVECTORS =====\n")
print(eigenvectors)