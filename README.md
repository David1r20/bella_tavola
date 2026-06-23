# Bella Tavola - Projeto P1/P2

API FastAPI do restaurante Bella Tavola, com rotas de pratos, bebidas, pedidos, reservas, predicao de fraude com Machine Learning, CI/CD no GitHub Actions e conteinerizacao com Docker.

## Estrutura

- `main.py`: cria a aplicacao FastAPI e registra os routers.
- `models/`: esquemas Pydantic usados na validacao.
- `routers/`: rotas da API.
- `ml/`: geracao de dados, treinamento e carregamento do modelo.
- `storage.py`: persistencia SQLite simples para pratos em `data/bella_tavola.db`.
- `tests/`: testes automatizados com Pytest.
- `.github/workflows/ci.yml`: pipeline de qualidade, integracao, Docker e relatorio.
- `Dockerfile`, `.dockerignore`, `docker-compose.yml`, `nginx.conf`: arquivos da etapa Docker.

## Rodando localmente

```bash
pip install -r requirements.txt
python main.py
```

Acesse:

```text
http://localhost:8000/docs
```

## Testes e qualidade

```bash
black --check .
autoflake --check --remove-all-unused-imports -r .
pytest tests/ -v
```

## Docker

Build da imagem:

```bash
docker build -t bella-tavola:v3 .
```

Rodar a API diretamente:

```bash
docker run -p 8000:8000 --rm --env-file .env -v bella-dados:/app/data bella-tavola:v3
```

Rodar API, PostgreSQL e Nginx com Compose:

```bash
docker compose up -d
curl http://localhost/
docker compose down
```

O volume `bella-dados` persiste o SQLite da API em `/app/data`. O comando `docker compose down -v` remove os volumes e apaga os dados.

## Variaveis importantes

- `HF_TOKEN`: token do Hugging Face, usado quando o modelo precisa ser baixado do Hub.
- `HF_MODEL_REPO_ID`: repositorio do modelo no Hugging Face, por exemplo `david1r20/bella-tavola-model`.
- `DOCKER_USERNAME`: usuario do Docker Hub, configurado como secret no GitHub Actions.
- `DOCKER_PASSWORD`: token do Docker Hub, configurado como secret no GitHub Actions.

Nunca commite `.env` ou tokens no repositorio.
