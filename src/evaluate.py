from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score
)
import numpy as np
import time
import pandas as pd


def evaluate_model(model, X, y, name="Unnamed", is_keras=False):
    """
    Evaluate a given model on input data and return the basic performeance metrics (accuracy, f1, recision, recall)
    all using macro averaging. This function also includes inference latency which is pretty cool.

    """
    start_time = time.time() # timer to actually count inference latency

    if is_keras:
        y_pred = model.predict(X)
        if y_pred.ndim == 2:  # Softmax output
            y_pred = np.argmax(y_pred, axis=1)
    else:
        y_pred = model.predict(X)

    end_time = time.time()
    latency = round(end_time - start_time, 2)

    return {
        "model": name,
        "accuracy": accuracy_score(y, y_pred),
        "f1_score": f1_score(y, y_pred, average="macro"),
        "precision": precision_score(y, y_pred, average="macro"),
        "recall": recall_score(y, y_pred, average="macro"),
        "latency": latency
    }

def summarize(results: list, sort_by: str = "f1_score", return_best: bool = True):
    """
    Summarizes evaluation results from multiple models, takes in return_best which is essentially
    whether or not we want it to decide which one is the best (yes we do)
    """
    df = pd.DataFrame([{
        "Model": r["model"],
        "Accuracy": r["accuracy"],
        "F1 Score": r["f1_score"],
        "Precision": r["precision"],
        "Recall": r["recall"],
        "Latency (s)": r["latency"]
    } for r in results])

    df = df.sort_values(by=sort_by, ascending=False).reset_index(drop=True)

    if return_best:
        best_model = df.iloc[0]["Model"]
        return df, best_model

    return df
