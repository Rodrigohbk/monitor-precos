
# 🏗️ Decisões Arquiteturais

## Visão Geral

O sistema segue uma arquitetura baseada em microsserviços? Não, é uma aplicação monolítica modular, organizada em camadas para facilitar manutenção e evolução.

## Diagrama de Contexto
```markdown
[Agendador] → [Orquestrador] → [Coletor Específico] → [Fonte Externa]
                                  ↓
                           [Preço / Produto]
                                  ↓
                           [Banco de Dados]
```
## Camadas

- **Camada de Apresentação**: Endpoints RESTful (FastAPI). Comunicação via HTTP/JSON.
- **Camada de Serviço**: Lógica de negócio (em `services/`). Isolada das rotas.
- **Camada de Acesso a Dados**: Repositórios com SQLAlchemy, separando a lógica de banco.
- **Camada de Infraestrutura**: Configurações, segurança, dependências externas.

## Decisões Técnicas e Justificativas

### FastAPI vs. Django/Flask
Escolhi FastAPI por:
- **Performance assíncrona**: Suporte nativo a `async/await`, essencial para operações de I/O (banco, scraping).
- **Validação automática**: Pydantic reduz código boilerplate e documenta a API.
- **OpenAPI integrado**: Geração automática da documentação, facilitando testes e adoção.

### PostgreSQL vs. MongoDB
Optei por PostgreSQL porque:
- Os dados são altamente relacionais (produtos, preços, usuários).
- Suporte a JSONB permite flexibilidade para dados semi-estruturados (ex.: detalhes de produtos).
- Extensões como TimescaleDB podem ser adicionadas futuramente para séries temporais.

### SQLAlchemy (assíncrono) vs. queries cruas
- SQLAlchemy fornece abstração e segurança contra SQL injection.
- Com `asyncpg`, obtemos performance próxima de queries cruas.
- Migrações com Alembic garantem evolução controlada do schema.

### Autenticação JWT
- Stateless, ideal para escalabilidade horizontal.
- Tokens de curta duração (30 min) com refresh token (futuro) equilibram segurança e usabilidade.

### Docker
- Isolamento do ambiente de desenvolvimento e produção.
- Facilita a replicação do projeto por recrutadores e contribuidores.

## Trade-offs e Considerações

- **Async vs. Sync**: A complexidade adicional do código assíncrono vale pela ganho em concorrência.
- **ORM vs. SQL puro**: Para consultas complexas, podemos usar SQLAlchemy Core ou queries customizadas.
- **Scraping vs. API oficial**: Como muitos sites não oferecem API, usaremos scraping com boas práticas (robots.txt, delays). Em versões futuras, podemos implementar um sistema de plugins para diferentes fontes.

## Segurança

- Hash de senhas com `bcrypt`.
- Tokens JWT assinados com chave secreta forte (variável de ambiente).
- CORS configurado para origens confiáveis.
- Validação de entradas com Pydantic evita injeção de código.
- Conexões com banco via URL segura.

## Escalabilidade e Performance

- Uso de `asyncpg` driver para PostgreSQL.
- Índices apropriados nas colunas mais consultadas (produto, data).
- Futuramente, implementação de cache com Redis para consultas frequentes.
- Tarefas pesadas (scraping, processamento) delegadas a workers Celery.

## Lições Aprendidas

Durante a Sprint 0, enfrentamos desafios com a configuração do Alembic em ambiente assíncrono e a correta estruturação dos pacotes Python. A solução envolveu garantir a presença de arquivos `__init__.py` e ajustar o `env.py` para usar a URL do banco via variável de ambiente. Isso reforçou a importância de uma boa documentação interna.
Durante a construção da imagem docker, também houve dificuldade com as dependencia do Alembic e a importação dos módulos, foi necessário análisar as importações que não estavam sendo encontradas.
O que reforça a importancia de realizar as impletações na ordem correta.
