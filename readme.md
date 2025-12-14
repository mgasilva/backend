# ⚙️ Tabela Periódica Interativa — Back-end (API)

Back-end desenvolvido em **Python + Flask**, responsável por fornecer os dados da **Tabela Periódica dos Elementos** por meio de uma **API RESTful**, consumida por um front-end em HTML/CSS/JavaScript.

A API utiliza **SQLite** como banco de dados e organiza suas rotas em um **Blueprint** (`elementos_bp`), com prefixo `/elementos`.

---

## 🎯 Objetivo do Back-end

- Disponibilizar dados estruturados dos elementos químicos
- Permitir consulta de detalhes de cada elemento
- Permitir leitura e escrita de **informações adicionais**
- Servir como base para um **MVP full-stack educacional**

---

## 🧱 Arquitetura

- **Framework:** Flask
- **Banco de dados:** SQLite
- **Acesso ao banco:** função `get_db_connection()`
- **Formato de resposta:** JSON
- **Blueprint:** `/elementos`

---

## 🌐 Endpoints da API

A API possui **4 rotas principais**, descritas detalhadamente a seguir.

---

## 1️⃣ GET `/elementos`

### 📌 Descrição
Retorna a lista completa de elementos químicos cadastrados no banco de dados, ordenados pelo número atômico.

### 🔸 Método
```

GET

````

### 🔸 Parâmetros
Nenhum.

### 🔸 O que a rota faz
- Consulta a tabela `elementos`
- Seleciona número atômico, símbolo, nome, massa atômica e categoria
- Ordena os resultados pelo número atômico
- Retorna uma lista JSON

### 🔸 Estrutura de Retorno (200 OK)

```json
[
  {
    "numero_atomico": 1,
    "simbolo": "H",
    "nome": "Hidrogênio",
    "massa_atomica": 1.008,
    "categoria": "não metal"
  },
  {
    "numero_atomico": 2,
    "simbolo": "He",
    "nome": "Hélio",
    "massa_atomica": 4.0026,
    "categoria": "gás nobre"
  }
]
````

---

## 2️⃣ GET `/elementos/<numero_atomico>`

### 📌 Descrição

Retorna os **detalhes básicos de um elemento específico**, identificado pelo seu número atômico.

### 🔸 Método

```
GET
```

### 🔸 Parâmetros de URL

| Nome             | Tipo | Descrição                  |
| ---------------- | ---- | -------------------------- |
| `numero_atomico` | int  | Número atômico do elemento |

### 🔸 O que a rota faz

* Busca o elemento na tabela `elementos`
* Retorna os dados básicos do elemento
* Retorna erro caso o elemento não exista

### 🔸 Estrutura de Retorno (200 OK)

```json
{
  "numero_atomico": 26,
  "simbolo": "Fe",
  "nome": "Ferro",
  "massa_atomica": 55.845,
  "categoria": "metal de transição"
}
```

### 🔸 Possíveis Erros

| Código | Motivo                  |
| ------ | ----------------------- |
| 404    | Elemento não encontrado |

---

## 3️⃣ GET `/elementos/<numero_atomico>/info_adicional`

### 📌 Descrição

Retorna todas as **informações adicionais** associadas a um determinado elemento químico.

### 🔸 Método

```
GET
```

### 🔸 Parâmetros de URL

| Nome             | Tipo | Descrição                  |
| ---------------- | ---- | -------------------------- |
| `numero_atomico` | int  | Número atômico do elemento |

### 🔸 O que a rota faz

* Consulta a tabela `informacoes`
* Retorna todas as informações adicionais do elemento
* Ordena pelo ID de inserção

### 🔸 Estrutura de Retorno (200 OK)

```json
{
  "numero_atomico": 26,
  "info_adicional": [
    {
      "informacoes": "Presente na hemoglobina."
    },
    {
      "informacoes": "Elemento essencial para o transporte de oxigênio."
    }
  ]
}
```

### 🔸 Observação

Caso não existam informações adicionais, o array `info_adicional` será retornado vazio.

---

## 4️⃣ POST `/elementos/<numero_atomico>/info_adicional`

### 📌 Descrição

Permite **adicionar uma nova informação adicional** a um elemento químico.

### 🔸 Método

```
POST
```

### 🔸 Parâmetros de URL

| Nome             | Tipo | Descrição                  |
| ---------------- | ---- | -------------------------- |
| `numero_atomico` | int  | Número atômico do elemento |

### 🔸 Corpo da Requisição (JSON)

```json
{
  "info": "Texto da informação adicional"
}
```

### 🔸 O que a rota faz

* Valida a presença do campo `info`
* Remove espaços em branco
* Verifica se o elemento existe
* Insere a informação na tabela `informacoes`
* Retorna status de sucesso ou erro

### 🔸 Estrutura de Retorno — Sucesso (201 Created)

```json
{
  "status": "ok",
  "mensagem": "Informação adicional inserida com sucesso"
}
```

### 🔸 Possíveis Erros

| Código | Motivo                        |
| ------ | ----------------------------- |
| 400    | Campo `info` ausente ou vazio |
| 404    | Elemento não encontrado       |

---

## 🗄️ Estrutura Esperada do Banco de Dados

### Tabela `elementos`

* `numero_atomico` (INTEGER, PK)
* `simbolo` (TEXT)
* `nome` (TEXT)
* `massa_atomica` (REAL)
* `categoria` (TEXT)

### Tabela `informacoes`

* `id` (INTEGER, PK)
* `numero_atomico` (INTEGER, FK)
* `info` (TEXT)

---

## ▶️ Como Executar o Back-end

```bash
pip install flask
python app.py
```

A API ficará disponível em:

```
http://127.0.0.1:5000
```

---

## 🔗 Integração com o Front-end

Este back-end foi projetado para ser consumido por um front-end estático que utiliza:

* `fetch`
* `async/await`
* JSON como formato de dados

Caso a API não esteja disponível, o front-end funciona parcialmente utilizando dados *fallback*.

---

## 📜 Licença

Projeto de caráter **educacional e acadêmico**.
Uso livre para fins de estudo, aprendizado e extensão.