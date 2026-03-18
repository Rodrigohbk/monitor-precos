# 📊 Monitor de Tendências de Preços em Tempo Real

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green?style=for-the-badge&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue?style=for-the-badge&logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-24-blue?style=for-the-badge&logo=docker)
![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)
![Visitors](https://api.visitorbadge.io/api/visitors?path=seu-usuario.monitor-precos&countColor=%23263759)

> Acompanhe a evolução de preços de produtos em e-commerces com gráficos interativos e atualizações em tempo real. Ideal para analistas de mercado, pequenos vendedores e entusiastas de dados.

![Demonstração](https://via.placeholder.com/800x400.png?text=Adicione+um+GIF+aqui)  
*Exemplo da interface Swagger e do dashboard (em desenvolvimento).*

---

## 🔍 Funcionalidades

- ✅ Cadastro e autenticação de usuários com JWT.
- ✅ Coleta automatizada de preços de fontes externas (via scraping ou APIs).
- ✅ Armazenamento histórico em PostgreSQL.
- ✅ API RESTful documentada com Swagger.
- ✅ Processamento de dados com Pandas/NumPy.
- ✅ Visualização de tendências (dashboard futuro).

---

## 📦 Tecnologias

- **Backend**: Python 3.12, FastAPI, SQLAlchemy 2.0 (async), Alembic
- **Banco de Dados**: PostgreSQL 16, Redis (para tarefas assíncronas)
- **Autenticação**: JWT com python-jose e bcrypt
- **Infraestrutura**: Docker, Docker Compose
- **Gerenciamento de dependências**: Poetry
- **Testes**: Pytest, pytest-asyncio, httpx

---

## 🚀 Como Executar

### Pré-requisitos
- [Docker](https://docs.docker.com/get-docker/) e [Docker Compose](https://docs.docker.com/compose/install/)
- Git

### Passos

1. **Clone o repositório**
   ```bash
   git clone https://github.com/seu-usuario/monitor-precos.git
   cd monitor-precos

2. **Configure as variáveis de ambiente**
   ```bash
   cp backend/.env.example backend/.env
   ```
   Gere uma chave secreta para o JWT:
   ```bash
   openssl rand -hex 32
   ```
   Edite o arquivo backend/.env e cole o valor em SECRET_KEY

3. **Suba os containers**
   ```bash
   docker-compose up --build

4. **Acesse a documentação interativa**
   Abra http://localhost:8000/docs e explore os endpoints.

5. **Teste o endpoint de heath**
   ```bash
   curl http://localhost:8000/api/v1/health
   ```
   Resposta esperada:
   ```bash
   {"status:"ok","database":"ok"}
   ```

## 🧪 Testes
Execute o suíte de testes dentro do container:
```bash
docker exec -it monitor_app poetry run pytest -v
```

## 📁 Estrutura do Projeto
```text
monitor-precos/
├── backend/
│   ├── app/
│   │   ├── api/            # Rotas da API (versão 1)
│   │   ├── core/           # Configurações, segurança, banco de dados
│   │   ├── models/         # Modelos SQLAlchemy
│   │   ├── schemas/        # Schemas Pydantic
│   │   └── services/       # Lógica de negócio (futuro)
│   ├── migrations/         # Migrações Alembic
│   ├── tests/              # Testes automatizados
│   ├── .env.example        # Exemplo de variáveis de ambiente
│   ├── alembic.ini         # Configuração do Alembic
│   └── pyproject.toml      # Dependências (Poetry)
├── docker-compose.yml      # Orquestração de containers
├── Dockerfile              # Imagem da aplicação
├── ARCHITECTURE.md         # Decisões arquiteturais
└── README.md
```

## 🤝 Como Contribuir
Contribuições são bem-vindas! Por favor, leia o [guia de contribuição](https://contributing.md/) antes de abrir um pull request.

## ✨ Autor
Rodrigo Honda – [@Rodrigohbk-github](https://github.com/Rodrigohbk) – rodrigohonda@live.com

[⬆ Voltar ao topo](#readme)


   
