# 🍲 Django Recipes — Plataforma de Receitas Culinárias

Aplicação web full-stack construída com **Django**, onde usuários podem se cadastrar, publicar e gerenciar suas próprias receitas culinárias. O projeto reproduz o fluxo de um produto real: autenticação, upload e tratamento de imagens, busca, paginação, área administrativa do autor (dashboard) e uma API própria em JSON — tudo com cobertura de testes unitários e funcionais (Selenium).

> Projeto desenvolvido para consolidar conhecimentos em Django, boas práticas de arquitetura (apps desacopladas, views baseadas em classe, forms customizados) e testes automatizados.

---

## ✨ Funcionalidades

- **Autenticação de usuários**: cadastro, login e logout com validações customizadas de formulário.
- **CRUD de receitas**: cada autor cria, edita e exclui suas próprias receitas em um dashboard privado.
- **Publicação controlada**: receitas ficam em rascunho até serem publicadas e só então aparecem para o público.
- **Upload e processamento de imagem**: capa da receita é redimensionada automaticamente com **Pillow** ao ser salva.
- **Busca e categorias**: listagem filtrável por termo de busca (`?q=`) e por categoria.
- **Paginação** customizada nas listagens.
- **API própria em JSON**: endpoints de listagem e detalhe de receitas (`/recipes/api/v1/`), sem depender do Django REST Framework.
- **Perfil de autor**: bio pública associada a cada usuário (`Profile`).
- **Painel de debug**: `django-debug-toolbar` habilitado em desenvolvimento.

---

## 🧱 Arquitetura

O projeto segue a separação padrão de apps do Django, cada uma com uma responsabilidade clara:

```
project/          # configurações e settings do projeto (Django project)
recipes/          # app de receitas: models, views, templates, API e testes
authors/          # app de usuários: autenticação, dashboard e perfil
base_templates/   # templates globais (header, menu, footer, paginação, mensagens)
base_static/      # CSS e JS globais (interface própria, sem frameworks prontos)
utils/            # utilitários reaproveitáveis (paginação, forms, factory de dados fake)
tests/            # testes funcionais end-to-end com Selenium
```

**Principais decisões técnicas:**
- Uso de **Class-Based Views** (`ListView`, `DetailView`) combinadas com views baseadas em função onde fazia mais sentido.
- Configuração de banco de dados via variáveis de ambiente (`python-dotenv`), suportando **SQLite** para desenvolvimento e **PostgreSQL** para produção sem alterar código.
- `select_related` para otimizar consultas e evitar o problema N+1 nas listagens.
- Geração de dados fake (`Faker`, localizado em `pt_BR`) para popular o ambiente de testes/desenvolvimento.

---

## 🛠️ Tecnologias

| Categoria | Stack |
|---|---|
| Backend | Python, Django 6 |
| Banco de dados | PostgreSQL / SQLite |
| Imagens | Pillow |
| Testes | Pytest, pytest-django, Selenium, coverage |
| Configuração | python-dotenv |
| Debug | django-debug-toolbar |

---

## 🚀 Como executar o projeto

### Pré-requisitos
- Python 3.11+
- pip / virtualenv

### Passo a passo

```bash
# 1. Clone o repositório
git clone https://github.com/J-VictorJ/Django.git
cd Django

# 2. Crie e ative um ambiente virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure as variáveis de ambiente
cp .env-example .env
# edite o .env se quiser usar PostgreSQL em vez de SQLite

# 5. Aplique as migrações
python manage.py migrate

# 6. Crie um superusuário (opcional, para acessar o /admin)
python manage.py createsuperuser

# 7. Rode o servidor de desenvolvimento
python manage.py runserver
```

Acesse `http://127.0.0.1:8000/` no navegador.

---

## ✅ Testes

O projeto tem duas camadas de testes:

```bash
# Testes unitários e de integração (pytest)
pytest

# Com relatório de cobertura
coverage run -m pytest
coverage report

# Testes funcionais end-to-end (Selenium + Chromedriver)
pytest -m functional_test
```

Marcadores customizados (`slow`, `fast`, `functional_test`) permitem rodar apenas o subconjunto de testes desejado durante o desenvolvimento.

---

## 📌 Endpoints principais

| Rota | Descrição |
|---|---|
| `/` | Página inicial com listagem de receitas publicadas |
| `/recipes/search/?q=` | Busca por título ou descrição |
| `/recipes/category/<id>/` | Receitas filtradas por categoria |
| `/recipes/<id>/` | Detalhe de uma receita |
| `/recipes/api/v1/` | Listagem de receitas em JSON |
| `/recipes/api/v1/<id>/` | Detalhe de uma receita em JSON |
| `/authors/register/` | Cadastro de usuário |
| `/authors/login/` | Login |
| `/authors/dashboard/` | Painel do autor com suas receitas |
| `/authors/dashboard/recipe/new/` | Criação de nova receita |

---

## 🎓 Base experimental do meu TCC (Cibersegurança em Django)

Este projeto foi utilizado como aplicação experimental do meu Trabalho de Conclusão de Curso em Engenharia de Software, **"Cibersegurança no Desenvolvimento Backend com Django: Avaliação Experimental de Mecanismos Nativos de Proteção contra CSRF, XSS e SQL Injection"**.

O objetivo foi avaliar, de forma comparativa e controlada, o quanto as proteções nativas do Django (middleware de CSRF, autoescape de templates e o ORM) reduzem a superfície de ataque de uma aplicação real — e o que acontece quando essas proteções são deliberadamente contornadas.

**Metodologia:** o mesmo sistema foi testado em duas condições — *vulnerável* (proteção nativa desativada/contornada) e *protegida* (configuração padrão do Django) — para três classes de ataque da OWASP Top 10, em um ambiente virtualizado (VM de desenvolvimento em Ubuntu e VM de ataque em Kali Linux, com `sqlmap` para os testes de SQL Injection):

| Vulnerabilidade | Como foi desativada a proteção | Resultado protegido |
|---|---|---|
| **CSRF** | View de login decorada com `csrf_exempt` | Com o middleware padrão ativo, requisições sem token válido retornam `403 Forbidden` |
| **XSS** (refletido e armazenado) | Campo de receita marcado para renderizar como HTML sem escape | Com o autoescape padrão do Django, os payloads são neutralizados e exibidos apenas como texto |
| **SQL Injection** | Consulta de login reescrita com SQL bruto concatenado (sem parametrização) | Com o ORM padrão, o `sqlmap` não identifica nenhum parâmetro injetável |

> Os trechos de código vulnerável (ex.: a *raw query* concatenada em `authors/views/all.py`) permanecem **comentados** no repositório apenas como evidência do experimento — não estão ativos na aplicação.

**Conclusão do trabalho:** nos três casos, a exploração só foi possível mediante alteração deliberada do código, fora das práticas documentadas pelo próprio framework; ao restaurar a configuração padrão, nenhum ataque funcionou. Ou seja, o Django reduz bastante o esforço para desenvolver aplicações seguras, mas não substitui a disciplina de engenharia de quem desenvolve.

O TCC (formato artigo, 17 páginas) já foi apresentado e corrigido. 📎 [Leia o artigo completo em PDF](./tcc-cybersec.pdf).

---

## 📖 Sobre o projeto

Este repositório documenta minha evolução com Django, cobrindo desde modelagem de dados e regras de negócio até testes automatizados, boas práticas de organização de código e, mais adiante, um estudo aplicado de segurança backend — competências aplicáveis a projetos reais.

## 📄 Licença

Projeto de estudo, livre para consulta e uso educacional.
