"""Módulo principal da API FastAPI para previsão de preços de imóveis com autenticação JWT."""

from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, Generator

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import joblib
from jose import JWTError, jwt
import pandas as pd
from pydantic import BaseModel, Field
import uvicorn

# Configurações e Constantes
SECRET_KEY: str = "minha_chave_secreta"
ALGORITHM: str = "HS256"
TEMPO_EXPIRACAO_MINUTOS: int = 30

DIRETORIO_ATUAL: Path = Path(__file__).resolve().parent
CAMINHO_MODELO: Path = DIRETORIO_ATUAL / "modelos" / "modelo_preco_imoveis.pkl"

# Dicionário em memória para armazenar o modelo e o status global
estado_aplicacao: Dict[str, Any] = {
    "modelo": None,
    "carregado": False,
}

security = HTTPBearer()


# Gerenciador de Ciclo de Vida da API (Lifespan)
@asynccontextmanager
async def lifespan(app: FastAPI) -> Generator[None, None, None]:
    """Gerencia a inicialização e o encerramento do aplicativo FastAPI.

    Carrega o modelo de Machine Learning ao iniciar a aplicação.
    """
    if CAMINHO_MODELO.exists():
        estado_aplicacao["modelo"] = joblib.load(CAMINHO_MODELO)
        estado_aplicacao["carregado"] = True
    else:
        estado_aplicacao["modelo"] = None
        estado_aplicacao["carregado"] = False

    yield

# Modelos Pydantic
class UsuarioRequisicao(BaseModel):
    """Esquema para autenticação e login de usuário."""

    usuario: str = Field(..., description="Nome de usuário para autenticação")
    senha: str = Field(..., description="Senha do usuário")


class RespostaToken(BaseModel):
    """Esquema de resposta do token de acesso JWT."""

    access_token: str
    token_type: str = "bearer"


class ImovelRequisicao(BaseModel):
    """Esquema com as características do imóvel para predição."""

    area_m2: float = Field(
        ...,
        gt=0,
        description="Área do imóvel em metros quadrados (deve ser maior que zero).",
        examples=[75.5],
    )


class RespostaPredicao(BaseModel):
    """Esquema de resposta da predição de preço."""

    area_m2: float
    preco_previsto: float


class StatusModeloResposta(BaseModel):
    """Esquema com o status atual do modelo carregado."""

    modelo_carregado: bool
    caminho_modelo: str
    mensagem: str


# Inicialização do App FastAPI
app = FastAPI(
    title="API de Previsão de Preço de Imóveis",
    description="API desenvolvida com FastAPI para servir modelo de regressão para preços de imóveis.",
    version="1.0.0",
    lifespan=lifespan,
)


# Funções Utilitárias e de Segurança
def criar_token(usuario: str) -> str:
    """Gera um token JWT com tempo de expiração definido.

    Parameters
    ----------
    usuario : str
        Identificador do usuário (subject do token).

    Returns
    -------
    str
        Token JWT codificado.
    """
    expiracao = datetime.now(timezone.utc) + timedelta(minutes=TEMPO_EXPIRACAO_MINUTOS)
    payload = {"sub": usuario, "exp": expiracao}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def verificar_token(
    credenciais: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    """Valida o token JWT fornecido no cabeçalho Authorization.

    Parameters
    ----------
    credenciais : HTTPAuthorizationCredentials
        Credenciais do tipo Bearer injetadas via dependência FastAPI.

    Returns
    -------
    str
        Nome do usuário autenticado contido no payload.

    Raises
    ------
    HTTPException
        Retorna status 401 caso o token seja inválido ou expirado.
    """
    token = credenciais.credentials
    excecao_autenticacao = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido ou expirado.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario: str | None = payload.get("sub")

        if usuario is None:
            raise excecao_autenticacao

        return usuario
    except JWTError:
        raise excecao_autenticacao


# Rotas da API
@app.get("/", summary="Rota Raiz")
async def root() -> Dict[str, str]:
    """Retorna uma mensagem de boas-vindas da API."""
    return {"mensagem": "API de previsão de preço de imóveis ativa."}


@app.post("/login", response_model=RespostaToken, summary="Autenticação do Usuário")
def login(dados_usuario: UsuarioRequisicao) -> RespostaToken:
    """Realiza a autenticação e retorna um token de acesso JWT de curta duração."""
    if dados_usuario.usuario != "admin" or dados_usuario.senha != "1234":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha inválidos.",
        )

    token = criar_token(dados_usuario.usuario)
    return RespostaToken(access_token=token, token_type="bearer")


@app.get(
    "/modelo/status",
    response_model=StatusModeloResposta,
    summary="Status do Modelo",
)
async def status_modelo() -> StatusModeloResposta:
    """Verifica se o arquivo do modelo foi carregado e está pronto para inferência."""
    carregado = estado_aplicacao["carregado"]
    mensagem = (
        "Modelo carregado e pronto para uso."
        if carregado
        else "Modelo não encontrado. Execute 'treinar_modelo.py' antes de iniciar a API."
    )

    return StatusModeloResposta(
        modelo_carregado=carregado,
        caminho_modelo=str(CAMINHO_MODELO),
        mensagem=mensagem,
    )


@app.post(
    "/predict",
    response_model=RespostaPredicao,
    summary="Prever Preço de Imóvel",
)
async def predict(
    imovel: ImovelRequisicao, usuario: str = Depends(verificar_token)
) -> RespostaPredicao:
    """Calcula o preço estimado do imóvel com base na sua área em m². Exige autenticação JWT."""
    if not estado_aplicacao["carregado"]:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Modelo de ML não está carregado no servidor.",
        )

    modelo = estado_aplicacao["modelo"]
    entrada = pd.DataFrame([[imovel.area_m2]], columns=["area_m2"])
    preco_previsto = float(modelo.predict(entrada)[0])

    return RespostaPredicao(
        area_m2=imovel.area_m2, preco_previsto=round(preco_previsto, 2)
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True)