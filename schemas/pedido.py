from pydantic import BaseModel
from typing import Optional, List
from models.pedido import Pedido
from schemas.item_pedido import ItemPedidoSchema


class PedidoSchema(BaseModel):
    """ Define como um novo pedido deve ser representado
    """
    cliente_nome: str = "João Silva"
    cliente_email: str = "joao@example.com"
    itens: List[ItemPedidoSchema]


class PedidoBuscaPorIDSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca por ID
    """
    id: int = 1


class PedidoViewSchema(BaseModel):
    """ Define como um pedido será retornado
    """
    id: int = 1
    cliente_nome: str = "João Silva"
    cliente_email: str = "joao@example.com"
    valor_total: float = 59.98
    status: str = "Criado"
    data_criacao: str
    itens: List[dict]


class ListagemPedidosSchema(BaseModel):
    """ Define como uma listagem de pedidos será retornada
    """
    pedidos: List[PedidoViewSchema]


class PedidoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção
    """
    mesage: str
    id: int


class PedidoUpdateStatusSchema(BaseModel):
    """ Define como uma atualização de status de pedido deve ser representada
    """
    id: int = 1
    status: str = "Em processamento"


def apresenta_pedido(pedido: Pedido):
    """ Retorna uma representação do pedido seguindo o schema definido em
        PedidoViewSchema
    """
    itens_lista = []
    for item in pedido.itens:
        itens_lista.append({
            "id": item.id,
            "produto_id": item.produto_id,
            "produto_nome": item.produto_nome,
            "quantidade": item.quantidade,
            "preco_unitario": item.preco_unitario,
            "subtotal": item.quantidade * item.preco_unitario
        })
        
    return {
        "id": pedido.id,
        "cliente_nome": pedido.cliente_nome,
        "cliente_email": pedido.cliente_email,
        "valor_total": pedido.valor_total,
        "status": pedido.status,
        "data_criacao": pedido.data_criacao.strftime("%Y-%m-%d %H:%M:%S"),
        "itens": itens_lista
    }


def apresenta_pedidos(pedidos):
    """ Retorna uma representação da listagem de pedidos
    """
    result = []
    for pedido in pedidos:
        result.append(apresenta_pedido(pedido))
    
    return {"pedidos": result}