from sqlalchemy import Column, String, Integer, Float, ForeignKey
from typing import Union

from models.base import Base



class ItemPedido(Base):
    __tablename__ = 'itens_pedido'
    
    id = Column(Integer, primary_key=True)
    produto_id = Column(Integer)
    produto_nome = Column(String(140))
    quantidade = Column(Integer)
    preco_unitario = Column(Float)
    
    # Chave estrangeira para o pedido
    pedido = Column(Integer, ForeignKey("pedidos.pk_pedido"), nullable=False)
    
    def __init__(self, produto_id, produto_nome, quantidade, preco_unitario):
        """
        Cria um Item de Pedido
        """
        self.produto_id = produto_id
        self.produto_nome = produto_nome
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario
    
    def to_dict(self):
        """
        Retorna a representação em dicionário do Item de Pedido
        """
        return {
            "id": self.id,
            "produto_id": self.produto_id,
            "produto_nome": self.produto_nome,
            "quantidade": self.quantidade,
            "preco_unitario": self.preco_unitario,
            "subtotal": self.quantidade * self.preco_unitario
        }