from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
from ml.data_gen import gerar_dataset


def treinar():
    df, X, y = gerar_dataset(n_samples=2000, seed=42)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print("Relatório de Classificação:")
    print(classification_report(y_test, y_pred, target_names=["legítimo", "fraude"]))

    model_path = "c:/Users/DRN/Desktop/projeto aula/bella_tavola/ml/model.pkl"
    joblib.dump(model, model_path)
    print(f"Modelo salvo em {model_path}")


if __name__ == "__main__":
    treinar()
