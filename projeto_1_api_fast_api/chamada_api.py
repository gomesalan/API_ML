"""Módulo de cliente para consumo e teste automatizado dos endpoints da API."""

from typing import Any, Dict, Optional

import requests

BASE_URL = "http://127.0.0.1:5000"


def obter_token_acesso(
    base_url: str = BASE_URL, usuario: str = "admin", senha: str = "1234"
) -> Optional[str]:
    """Autentica na API e retorna o token de acesso JWT.

    Parameters
    ----------
    base_url : str, optional
        URL base do servidor da API, por padrão "http://127.0.0.1:5000".
    usuario : str, optional
        Nome de usuário para login, por padrão "admin".
    senha : str, optional
        Senha do usuário, por padrão "1234".

    Returns
    -------
    Optional[str]
        String contendo o token JWT caso a autenticação seja bem-sucedida,
        ou None em caso de falha.
    """
    endpoint = f"{base_url}/login"
    payload = {"usuario": usuario, "senha": senha}

    try:
        resposta = requests.post(endpoint, json=payload, timeout=10)
        resposta.raise_for_status()

        dados = resposta.json()
        token = dados.get("access_token")
        print("Login realizado com sucesso!")
        return token

    except requests.HTTPError:
        print(f"Falha no login (Status {resposta.status_code}): {resposta.text}")
    except requests.RequestException as erro:
        print(f"Erro de conexão ao tentar autenticar: {erro}")

    return None


def realizar_predicao(
    area_m2: float, token: str, base_url: str = BASE_URL
) -> Optional[Dict[str, Any]]:
    """Envia uma solicitação de inferência para o endpoint /predict.

    Parameters
    ----------
    area_m2 : float
        Área do imóvel em metros quadrados para cálculo da estimativa.
    token : str
        Token Bearer JWT para autenticação na requisição.
    base_url : str, optional
        URL base do servidor da API, por padrão "http://127.0.0.1:5000".

    Returns
    -------
    Optional[Dict[str, Any]]
        Dicionário com a resposta da API contendo o preço previsto,
        ou None em caso de falha.
    """
    endpoint = f"{base_url}/predict"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"area_m2": area_m2}

    try:
        resposta = requests.post(
            endpoint, json=payload, headers=headers, timeout=10
        )
        resposta.raise_for_status()

        resultado = resposta.json()
        print("Previsão realizada com sucesso!")
        return resultado

    except requests.HTTPError:
        print(
            f"Erro na predição (Status {resposta.status_code}): {resposta.text}"
        )
    except requests.RequestException as erro:
        print(f"Erro de conexão ao solicitar predição: {erro}")

    return None


if __name__ == "__main__":
    token_acesso = obter_token_acesso()
    if token_acesso:
        resultado_predicao = realizar_predicao(area_m2=70.0, token=token_acesso)
        if resultado_predicao:
            print(f"Resposta da API: {resultado_predicao}")