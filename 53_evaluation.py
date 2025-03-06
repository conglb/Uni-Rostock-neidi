from sklearn.metrics import accuracy_score, f1_score, classification_report

def evaluate_model(true_hidden_sequence, predicted_hidden_sequence):
    # Calculate accuracy
    accuracy = accuracy_score(true_hidden_sequence, predicted_hidden_sequence)
    print(f"Accuracy: {accuracy:.2f}")

    # Calculate F1 score (weighted)
    f1 = f1_score(true_hidden_sequence, predicted_hidden_sequence, average='weighted')
    print(f"F1 Score (weighted): {f1:.2f}")

    # Print the classification report
    print("\nClassification Report:")
    print(classification_report(true_hidden_sequence, predicted_hidden_sequence))
