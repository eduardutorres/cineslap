# CineSlap - Plataforma de Crítica Interativa

O **CineSlap** é uma plataforma voltada para o gerenciamento, catalogação e avaliação colaborativa de produções cinematográficas e televisivas. O sistema permite que os usuários cadastrem, pesquisem e acompanhem avaliações de filmes e séries de forma organizada e intuitiva.

Este projeto foi desenvolvido como requisito acadêmico para a disciplina de **Programação Orientada a Objetos (POO)**.

---

# Arquitetura e Tecnologias

A aplicação foi desenvolvida seguindo o padrão arquitetural **MVC (Model-View-Controller)**, sendo organizada nas seguintes camadas:

## View (`app.py`)

Interface gráfica desenvolvida com o framework **Streamlit**, responsável pela renderização das páginas e pela interação com o usuário.

## Controller (`controllers.py`)

Camada responsável pela validação de dados, gerenciamento do estado da aplicação e coordenação das operações entre a interface e as regras de negócio.

## Model (`models.py`)

Camada de modelagem de dados, implementada por meio de classes baseadas em **dataclasses**, que representam as entidades do sistema.

## Service (`services.py`)

Camada de serviços responsável pela integração com APIs externas e pelo isolamento das regras de comunicação com sistemas terceiros.

---

# Integrações e Persistência

## The Movie Database (TMDB) API

Utilizada para alimentar o catálogo de filmes e séries por meio de consultas aos endpoints de busca da plataforma.

## Giphy API

Utilizada para associar GIFs às avaliações e críticas realizadas pelos usuários.

## MySQL

Banco de dados relacional utilizado para garantir a persistência, integridade e consistência dos dados armazenados.

---

# Estrutura do Projeto

```text
├── controllers/       # Controladores e regras de negócio
├── data/              # Scripts SQL e arquivos relacionados ao banco de dados
├── models/            # Definição das entidades e modelos de dados
├── services/          # Integração com APIs externas
├── app.py             # Arquivo principal da aplicação (View)
└── README.md          # Documentação do projeto
```

---

# Como Executar o Projeto

## 1. Clonar o Repositório

```bash
git clone <URL_DO_REPOSITORIO>
cd CineSlap
```

---

## 2. Instalar as Dependências

Instale as bibliotecas necessárias utilizando o comando abaixo:

```bash
pip install streamlit requests mysql-connector-python
```

Ou, caso exista um arquivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## 3. Configurar o Banco de Dados e as APIs

1. Certifique-se de que o serviço do **MySQL** esteja em execução.
2. Execute os scripts SQL presentes na pasta `data/` para criar a estrutura do banco de dados.
3. Configure as chaves de acesso (API Keys) da **TMDB API** e da **Giphy API** conforme definido no projeto.
4. Verifique se as credenciais de conexão com o banco de dados estão configuradas corretamente.

---

## 4. Executar a Aplicação

Após concluir as etapas de configuração, inicie a aplicação com o seguinte comando:

```bash
streamlit run app.py
```

---

# Acessando a Aplicação

Após a execução, o Streamlit iniciará um servidor local e exibirá um endereço semelhante ao abaixo:

```text
http://localhost:8501
```

Abra esse endereço em seu navegador para acessar o sistema.

---

# Funcionalidades

* Cadastro e gerenciamento de avaliações de filmes e séries;
* Pesquisa de conteúdos por meio da API do TMDB;
* Associação de GIFs às avaliações utilizando a API do Giphy;
* Armazenamento persistente de dados em banco MySQL;
* Interface web interativa desenvolvida com Streamlit;
* Organização do código seguindo o padrão MVC.



