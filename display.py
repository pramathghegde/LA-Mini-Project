def format_matrix(users, products, matrix, title="===== USER-PRODUCT MATRIX ====="):
    output = title + "\n\n"
    header = "User".ljust(10)
    for p in products:
        header += p.ljust(12)
    output += header + "\n"

    for i in range(len(users)):
        row = users[i].ljust(10)
        for j in range(len(products)):
            row += str(round(matrix[i][j], 2)).ljust(12)
        output += row + "\n"

    return output


def format_recommendations(users, products, matrix, pred, selected_user):
    output = "\n===== SELECTED USER RECOMMENDATION =====\n\n"

    idx = users.index(selected_user)
    unrated = [i for i, v in enumerate(matrix[idx]) if v == 0]

    if unrated:
        best = max(unrated, key=lambda x: pred[idx][x])
        output += f"{selected_user} → {products[best]} ({pred[idx][best]:.2f})\n"
    else:
        output += "All products rated\n"

    output += "\n===== FINAL RECOMMENDATIONS =====\n\n"

    for i in range(len(users)):
        unrated = [j for j, v in enumerate(matrix[i]) if v == 0]
        if unrated:
            best = max(unrated, key=lambda x: pred[i][x])
            output += f"{users[i]} → {products[best]} ({pred[i][best]:.2f})\n"
        else:
            output += f"{users[i]} → All products rated\n"

    return output


def format_eigen(eigenvalues, eigenvectors):
    output = "\n===== EIGENVALUES =====\n\n"
    output += str(eigenvalues) + "\n"
    output += "\n===== EIGENVECTORS =====\n\n"
    output += str(eigenvectors) + "\n"
    return output