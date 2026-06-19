import os
from pathlib import Path

import joblib
from huggingface_hub import hf_hub_download


def load_model(
    repo_id: str = None,
    filename: str = "model.pkl",
    force_download: bool = False,
):
    """
    Carrega o modelo. Se repo_id for fornecido, tenta baixar do Hugging Face.
    Caso contrario, tenta carregar localmente.
    """
    repo_id = repo_id or os.environ.get("HF_MODEL_REPO_ID")

    if repo_id:
        try:
            local_path = hf_hub_download(
                repo_id=repo_id,
                filename=filename,
                force_download=force_download,
                token=os.environ.get("HF_TOKEN") or None,
            )
            return joblib.load(local_path)
        except Exception as e:
            print(f"Erro ao baixar do Hub: {e}. Tentando local...")

    local_path = Path(__file__).with_name(filename)
    if local_path.exists():
        return joblib.load(local_path)

    raise FileNotFoundError("Modelo nao encontrado localmente nem no Hub.")
