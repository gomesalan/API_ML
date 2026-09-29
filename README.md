### Projeto1 - Previsão de Preço de Imóveis (`/app`)

API REST desenvolvida em Python com **FastAPI** para estimar o preço de imóveis com base na área em metros quadrados (`area_m2`).

* **Algoritmo:** Regressão Linear (armazenado em `.pkl`)
* **Principais Recursos:**
* Script automatizado para geração de dados, treinamento e avaliação do modelo ($R^2$ e RMSE).
* Endpoints HTTP para verificação de status do modelo (`GET /modelo/status`) e predição (`POST /predict`).
* Documentação interativa automática com Swagger UI (`/docs`) e ReDoc (`/redoc`).
* **Tecnologias:** Python, FastAPI, Uvicorn, Scikit-Learn.

---
