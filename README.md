# CineSlap

O **CineSlap** é uma plataforma social voltada para amantes de filmes e séries, permitindo que os usuários descubram conteúdos, publiquem críticas, compartilhem opiniões e interajam com outros membros da comunidade.

A aplicação integra informações em tempo real do catálogo do TMDB, possibilitando a busca e visualização de filmes e séries, além de permitir a criação de avaliações personalizadas acompanhadas de GIFs e imagens.

Este projeto foi desenvolvido utilizando conceitos de **Programação Orientada a Objetos (POO)** e seguindo a arquitetura **MVC (Model-View-Controller)**.

---

# Arquitetura do Projeto

A aplicação está organizada em camadas para garantir maior organização, manutenção e escalabilidade.

## View (`app.py`)

Responsável pela interface gráfica da aplicação.

Desenvolvida com **Streamlit**, oferece uma experiência moderna e intuitiva para:

- Login e cadastro de usuários;
- Navegação pelo catálogo;
- Visualização de perfis;
- Publicação de avaliações;
- Interação com conteúdos da comunidade.

---

## Controller (`controllers/controllers.py`)

Camada intermediária responsável por:

- Controle de fluxo da aplicação;
- Validação de dados;
- Gerenciamento das sessões do usuário;
- Coordenação entre interface, banco de dados e serviços externos.

---

## Model (`models/`)

Contém as classes que representam as entidades do sistema, como:

- Usuário;
- Filme;
- Série;
- Avaliação (Slap Review).

---

## Data (`data/`)

Camada responsável pela persistência dos dados.

Inclui:

- Conexão com banco MySQL;
- Repositórios de usuários;
- Repositórios de avaliações.

---

## Services (`services/services.py`)

Responsável pela integração com APIs externas.

Atualmente o sistema utiliza:

- TMDB API (The Movie Database);
- Giphy API.

---

# Tecnologias Utilizadas

- Python 3
- Streamlit
- MySQL
- Requests
- Python Dotenv
- Dataclasses
- Arquitetura MVC

---

# Integrações Externas

## TMDB API

Utilizada para:

- Buscar filmes;
- Buscar séries;
- Obter detalhes completos dos conteúdos;
- Exibir filmes em cartaz;
- Exibir séries populares.

---

## Giphy API

Utilizada para:

- Buscar GIFs relacionados às avaliações;
- Tornar as críticas mais dinâmicas e interativas.

---

# Banco de Dados

O sistema utiliza o **MySQL** como banco de dados principal para armazenar:

- Usuários;
- Perfis;
- Avaliações;
- Relacionamentos entre conteúdos e usuários.

O script de criação da estrutura encontra-se em:

```text
banco de dados.sql
```

---

# Estrutura do Projeto

```text
CineSlap
│
├── app.py
│
├── controllers/
│   └── controllers.py
│
├── models/
│   ├── filme.py
│   ├── serie.py
│   ├── slap_review.py
│   ├── usuario.py
│   └── models.py
│
├── data/
│   ├── database.py
│   ├── review_repository.py
│   └── usuario_repository.py
│
├── services/
│   └── services.py
│
├── banco de dados.sql
├── .env
└── README.md
```

---

# Configuração do Ambiente

## 1. Clonar o Repositório

```bash
git clone https://github.com/eduardutorres/cineslap.git
cd cineslap
```

---

## 2. Instalar Dependências

```bash
pip install -r requirements.txt
```

Ou:

```bash
pip install streamlit requests mysql-connector-python python-dotenv
```

---

## 3. Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
TMDB_BEARER_TOKEN=SEU_TOKEN_TMDB
GIPHY_API_KEY=SUA_CHAVE_GIPHY
```

---

## 4. Configurar o Banco de Dados

1. Inicie o MySQL.
2. Execute o script:

```sql
banco de dados.sql
```

3. Verifique as configurações de conexão em:

```python
data/database.py
```

---

## 5. Executar o Projeto

```bash
streamlit run app.py
```

---

# Funcionalidades

- Cadastro de usuários
- Login e autenticação
- Edição de perfil
- Upload de foto de perfil
- Busca de filmes
- Busca de séries
- Visualização de detalhes dos conteúdos
- Publicação de críticas e avaliações
- Integração com GIFs do Giphy
- Catálogo atualizado via TMDB
- Persistência em banco MySQL
- Interface moderna desenvolvida com Streamlit

---
---

Desenvolvido para fins acadêmicos e de aprendizagem.
