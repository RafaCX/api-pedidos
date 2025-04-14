from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from models.item_pedido import ItemPedido
from models.base import Base

class Pedido(Base):
    __tablename__ = 'pedidos'
    
    id = Column("pk_pedido", Integer, primary_key=True)
    cliente_nome = Column(String(140))
    cliente_email = Column(String(140))
    valor_total = Column(Float)
    status = Column(String(20), default="Criado")
    data_criacao = Column(DateTime, default=datetime.now())
    
    # Relacionamento com os itens do pedido
    itens = relationship('ItemPedido')
    
    def __init__(self, cliente_nome, cliente_email, valor_total=0,
                 status="Criado", data_criacao=None):
        """
        Cria um Pedido
        """
        self.cliente_nome = cliente_nome
        self.cliente_email = cliente_email
        self.valor_total = valor_total
        self.status = status
        
        if data_criacao:
            self.data_criacao = data_criacao
    
    def to_dict(self):
        """
        Retorna a representação em dicionário do Pedido
        """
        return {
            "id": self.id,
            "cliente_nome": self.cliente_nome,
            "cliente_email": self.cliente_email,
            "valor_total": self.valor_total,
            "status": self.status,
            "data_criacao": self.data_criacao,
            "itens": [item.to_dict() for item in self.itens]
        }