from pathlib import Path

import joblib
import numpy as np
from ml.data_gen import gerar_dataset
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

MODEL_PATH = Path(__file__).with_name("model.pkl")


def treinar():
    df, X, y = gerar_dataset(n_samples=2000, seed=42)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print("Relatorio de Classificacao:")
    print(classification_report(y_test, y_pred, target_names=["legitimo", "fraude"]))

    joblib.dump(model, MODEL_PATH)
    tamanho_kb = MODEL_PATH.stat().st_size / 1024
    print(f"Modelo salvo em {MODEL_PATH} ({tamanho_kb:.1f} KB)")

    model_carregado = joblib.load(MODEL_PATH)
    amostra = X_test[:5]
    pred_original = model.predict(amostra)
    pred_carregado = model_carregado.predict(amostra)

    assert np.array_equal(pred_original, pred_carregado), "Predicoes divergem!"
    print("Artefato validado: predicoes identicas")
    print(f"Predicoes: {pred_carregado}")
    print(f"Probabilidades: {model_carregado.predict_proba(amostra).round(3)}")

    return df, model


if __name__ == "__main__":
    treinar()
