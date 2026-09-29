# 🏢 API de Previsão de Preço de Imóveis

Projeto de Machine Learning e API REST desenvolvidos em Python. O objetivo deste sistema é treinar um modelo de Regressão Linear com base na área em metros quadrados (`area_m2`) de imóveis e disponibilizar um serviço para realizar previsões de preços via requisições HTTP.

---

## 📁 Estrutura do Projeto
```markdown
app/
│
├── dados.py                 # Módulo responsável por gerar/carregar a base de dados
├── treinar_modelo.py        # Script para treinar, avaliar e salvar o modelo ML (.pkl)
├── main.py                  # API FastAPI com os endpoints de verificação e previsão
├── requirements.txt         # Lista de dependências do projeto
│
└── modelos/                 # Pasta onde o modelo treinado é armazenado
    └── modelo_preco_imoveis.pkl

```

---

## 🚀 Instalação e Configuração

### 1. Clonar o repositório

```bash
git clone [https://github.com/SEU-USUARIO/NOME-DO-REPOSITORIO.git](https://github.com/SEU-USUARIO/NOME-DO-REPOSITORIO.git)
cd NOME-DO-REPOSITORIO

```

### 2. Criar e ativar um ambiente virtual (Recomendado)

* **Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate

```


* **Windows:**
```cmd
python -m venv venv
venv\Scripts\activate

```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt

```

---

## 🛠️ Passo a Passo de Execução

### Step 1: Treinar o Modelo de Machine Learning

Antes de iniciar a API, é necessário gerar o modelo `.pkl` executando o script de treinamento:

```bash
python treinar_modelo.py

```

> O script treinará o modelo de regressão, exibirá as métricas de avaliação (RMSE e R²) e salvará o arquivo na pasta `modelos/modelo_preco_imoveis.pkl`.

### Step 2: Iniciar a API FastAPI

Com o modelo gerado, execute a aplicação com o Uvicorn:

```bash
python main.py

```

> A API estará rodando localmente no endereço: `http://127.0.0.1:5000`

---

## 📌 Endpoints da API

| Método | Endpoint | Descrição |
| --- | --- | --- |
| `GET` | `/` | Retorna uma mensagem de boas-vindas informando o status da API. |
| `GET` | `/modelo/status` | Verifica se o modelo de ML foi carregado corretamente. |
| `POST` | `/predict` | Recebe os dados da área (`area_m2`) e retorna o preço estimado. |

---

## 🧪 Exemplos de Requisição

### 1. Checar status do modelo

```bash
curl -X GET "[http://127.0.0.1:5000/modelo/status](http://127.0.0.1:5000/modelo/status)"

```

### 2. Realizar uma previsão de preço (`POST /predict`)

**Body da Requisição (JSON):**

```json
{
  "area_m2": 75.5
}

```

**Resposta da API (JSON):**

```json
{
  "Preco_previsto": 350000.00
}

```

---

## 📄 Documentação Interativa

O FastAPI gera documentações interativas automáticas. Com a API rodando, acesse no navegador:

* **Swagger UI:** [http://127.0.0.1:5000/docs](https://www.google.com/search?q=http://127.0.0.1:5000/docs&utm_source=gemini)
* **ReDoc:** [http://127.0.0.1:5000/redoc](https://www.google.com/search?q=http://127.0.0.1:5000/redoc&utm_source=gemini)


** Obs: gerado por IA(Gemini) e revisado pelo autor