from pydantic import BaseModel


class ItemPedidoSchema(BaseModel):
    """ Define como um novo item de pedido deve ser representado
    """
    produto_id: int = 1
    produto_nome: str = "Camiseta Casual"
    quantidade: int = 1
    preco_unitario: float = 29.99