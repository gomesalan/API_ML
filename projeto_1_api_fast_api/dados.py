"""Módulo responsável pela geração de dados sintéticos para o modelo de ML."""

import numpy as np
import pandas as pd


def gera_base(
    n_amostras: int = 500, seed: int = 42
) -> pd.DataFrame:
    """Gera um DataFrame com dados sintéticos de imóveis (área e preço).

    A função simula um conjunto de dados onde o preço do imóvel possui uma
    relação linear com a sua área em metros quadrados, acrescido de um ruído
    com distribuição normal para simular variações do mundo real.

    Parameters
    ----------
    n_amostras : int, optional
        Quantidade de registros/imóveis a serem gerados, por padrão 500.
    seed : int, optional
        Semente para o gerador de números aleatórios, garantindo
        reprodutibilidade, por padrão 42.

    Returns
    -------
    pd.DataFrame
        DataFrame contendo as colunas:
        - 'area_m2': Área do imóvel em metros quadrados (float).
        - 'preco': Preço estimado do imóvel em reais (float).
    """
    rng = np.random.default_rng(seed)

    area_m2 = rng.integers(low=30, high=250, endpoint=True, size=n_amostras).astype(float)
    ruido = rng.normal(loc=0.0, scale=20000.0, size=n_amostras)
    preco = (area_m2 * 5000.0) + ruido

    return pd.DataFrame({"area_m2": area_m2, "preco": preco})
 