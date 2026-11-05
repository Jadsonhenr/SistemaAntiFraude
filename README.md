# Antifraude DT — Sistema de análise de similaridade

Aplicação web para apoiar professores na identificação de possíveis similaridades entre trabalhos de Desenho Técnico. O sistema não declara fraude: apresenta dados técnicos para avaliação docente.

## Estado desta entrega

Implementado nesta versão inicial:
- Cadastro e login de professores com hash de senha.
- Sessões com Flask-Login e proteção CSRF.
- Isolamento de turmas e análises por professor.
- Cadastro de turmas e atividades.
- Upload de pastas pelo navegador (`webkitdirectory`).
- Validação de extensão, nome interno aleatório e armazenamento separado por usuário/análise.
- Hash SHA-256 e identificação de arquivos binariamente idênticos.
- Extração inicial de metadados DXF (ezdxf) e texto/páginas PDF (PyMuPDF).
- DWG explicitamente não processado se o adaptador ODA não estiver configurado.
- Dashboard e relatório web inicial.
- Docker Compose com PostgreSQL e Redis, mais serviço worker Celery preparado.

Ainda não implementado nesta versão:
- Tarefas Celery conectadas ao fluxo real de upload (o processamento atual é síncrono).
- Conversão real DWG→DXF via ODA.
- Comparação geométrica CAD, visual CAD/PDF e comparação cruzada.
- Exportação PDF/CSV, visualizador comparativo e filtros avançados.
- Auditoria completa, retenção LGPD, backup automatizado e HTTPS real.
- Migrações iniciais geradas; devem ser criadas pelo comando abaixo.

## Execução local

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Para desenvolvimento sem PostgreSQL, edite `DATABASE_URL` no `.env`:
`DATABASE_URL=sqlite:///antifraude-dev.db`

Depois:
```bash
flask --app run.py db init
flask --app run.py db migrate -m "initial schema"
flask --app run.py db upgrade
python run.py
```
Acesse http://127.0.0.1:5000.

## Execução com Docker

```bash
cp .env.example .env
# Ajuste SECRET_KEY antes de expor o serviço.
docker compose up --build
```
Acesse http://localhost:5000.

## Testes

```bash
pytest -q
```

## Segurança e implantação

Não use as credenciais de exemplo em produção. Altere `SECRET_KEY` e a senha do PostgreSQL, configure domínio e HTTPS, restrinja acesso aos arquivos e implemente política de retenção e exclusão compatível com a LGPD. O Caddyfile é apenas um modelo e não significa que o sistema já esteja publicado.

## Limitações técnicas

- O upload preserva o caminho relativo enviado pelo navegador como metadado, mas nunca o utiliza como caminho físico de gravação.
- Arquivos aceitos por extensão ainda precisam de validação de conteúdo mais rigorosa e varredura antimalware antes de uso em produção.
- A comparação SHA-256 encontra igualdade binária, não cópia visual ou geométrica.
- A leitura DXF atual coleta contagem por tipo e layers; não calcula invariantes geométricos.
- O conversor ODA é uma dependência externa e não está incluído no contêiner.
