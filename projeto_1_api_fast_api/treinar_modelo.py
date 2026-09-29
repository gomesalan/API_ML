"""Módulo responsável pelo treinamento, avaliação e exportação do modelo de regressão."""

from pathlib import Path
from typing import Tuple

import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import root_mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

from dados import gera_base


def treina_e_avalia_modelo(
    df: pd.DataFrame, test_size: float = 0.2, seed: int = 42
) -> Tuple[LinearRegression, float, float]:
    """Divide os dados, treina um modelo de regressão linear e calcula suas métricas.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame contendo as colunas 'area_m2' (feature) e 'preco' (target).
    test_size : float, optional
        Proporção da base destinada aos testes, por padrão 0.2.
    seed : int, optional
        Semente para reprodutibilidade do split de dados, por padrão 42.

    Returns
    -------
    Tuple[LinearRegression, float, float]
        Retorna uma tupla contendo:
        - O modelo treinado (LinearRegression).
        - O valor da métrica RMSE (float).
        - O valor da métrica R² (float).
    """
    x = df[["area_m2"]]
    y = df["preco"]

    x_treino, x_teste, y_treino, y_teste = train_test_split(
        x, y, test_size=test_size, random_state=seed
    )

    print(f"Tamanho do conjunto de treino: {len(x_treino)}")
    print(f"Tamanho do conjunto de teste: {len(x_teste)}")

    modelo = LinearRegression()
    modelo.fit(x_treino, y_treino)
    print("\nModelo treinado com sucesso.")

    y_pred = modelo.predict(x_teste)
    rmse = root_mean_squared_error(y_teste, y_pred)
    r2 = r2_score(y_teste, y_pred)

    print("\nMétricas de Avaliação:")
    print(f"RMSE: R$ {rmse:,.2f}")
    print(f"R²: {r2:.4f}")

    return modelo, rmse, r2


def salva_modelo(modelo: LinearRegression, nome_arquivo: str = "modelo_preco_imoveis.pkl") -> Path:
    """Salva o modelo treinado em disco no diretório 'modelos'.

    Parameters
    ----------
    modelo : LinearRegression
        Modelo de Machine Learning a ser persistido.
    nome_arquivo : str, optional
        Nome do arquivo `.pkl` de saída, por padrão "modelo_preco_imoveis.pkl".

    Returns
    -------
    Path
        Caminho absoluto do arquivo salvo.
    """
    diretorio_atual = Path(__file__).resolve().parent
    pasta_modelos = diretorio_atual / "modelos"
    pasta_modelos.mkdir(parents=True, exist_ok=True)

    caminho_modelo = pasta_modelos / nome_arquivo
    joblib.dump(modelo, caminho_modelo)

    print(f"\nModelo salvo em: {caminho_modelo}")
    return caminho_modelo

dados = gera_base()
modelo, rmse, r2 = treina_e_avalia_modelo(dados)
salva_modelo(modelo)