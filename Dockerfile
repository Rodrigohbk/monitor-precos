# syntax=docker/dockerfile:1
FROM python:3.12-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Instala dependências do sistema necessárias para algumas bibliotecas Python
# (ex.: psycopg2, bcrypt, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Instala o Poetry
RUN pip install poetry
RUN pip install pydantic[email]

# Copia os arquivos de definição de dependências
COPY backend/pyproject.toml backend/poetry.lock* /app/

# Configura o Poetry para não criar um ambiente virtual separado
# (já estamos em um container, não precisamos de isolamento extra)
RUN poetry config virtualenvs.create false

# Instala as dependências do projeto
RUN poetry install --no-interaction --no-ansi --no-root

# Copia o código da aplicação
COPY backend /app

# Expõe a porta que a aplicação usará
EXPOSE 8000

# Comando padrão (pode ser sobrescrito pelo docker-compose)
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]