from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote
from sqlalchemy.exc import IntegrityError

from models._init_ import Session
from models.item_pedido import ItemPedido
from models.pedido import Pedido
from logger import logger
from schemas import *
from flask_cors import CORS
from schemas.error import ErrorSchema
from schemas.pedido import ListagemPedidosSchema, PedidoBuscaPorIDSchema, PedidoDelSchema, PedidoSchema, PedidoUpdateStatusSchema, PedidoViewSchema, apresenta_pedido, apresenta_pedidos

info = Info(title="API de Pedidos", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# Definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
pedido_tag = Tag(name="Pedido", description="Adição, visualização e remoção de pedidos")
item_tag = Tag(name="Item", description="Adição de itens a um pedido")

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

@app.post('/pedido', tags=[pedido_tag],
          responses={"200": PedidoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_pedido(body: PedidoSchema):  # Mudou de 'form' para 'body'
    """Adiciona um novo Pedido à base de dados
    """
    pedido = Pedido(
        cliente_nome=body.cliente_nome,  # Agora usa body em vez de form
        cliente_email=body.cliente_email,
        valor_total=0  # Será calculado ao adicionar itens
    )
    
    logger.info(f"Adicionando pedido para cliente: '{pedido.cliente_nome}'")
    
    try:
        # Criando conexão com a base
        session = Session()
        # Adicionando pedido
        session.add(pedido)
        session.commit()
        
        # Adicionando itens ao pedido
        valor_total = 0
        for item in body.itens:  # Usando body.itens em vez de form.itens
            item_pedido = ItemPedido(
                produto_id=item.produto_id,
                produto_nome=item.produto_nome,
                quantidade=item.quantidade,
                preco_unitario=item.preco_unitario
            )
            pedido.itens.append(item_pedido)
            valor_total += item.quantidade * item.preco_unitario
        
        # Atualizando o valor total do pedido
        pedido.valor_total = valor_total
        session.commit()
        
        logger.info(f"Adicionado pedido: {pedido.id}")
        return apresenta_pedido(pedido), 200

    except Exception as e:
        # Caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo pedido"
        logger.warning(f"Erro ao adicionar pedido para '{pedido.cliente_nome}', {error_msg}")
        return {"mesage": error_msg}, 400
    
@app.get('/pedidos', tags=[pedido_tag],
         responses={"200": ListagemPedidosSchema, "404": ErrorSchema})
def get_pedidos():
    """Faz a busca por todos os Pedidos cadastrados
    """
    logger.info(f"Coletando pedidos")
    # Criando conexão com a base
    session = Session()
    # Fazendo a busca
    pedidos = session.query(Pedido).all()

    if not pedidos:
        # Se não há pedidos cadastrados
        return {"pedidos": []}, 200
    else:
        logger.info(f"{len(pedidos)} pedidos encontrados")
        # Retorna a representação dos pedidos
        return apresenta_pedidos(pedidos), 200

@app.delete('/pedido', tags=[pedido_tag],
            responses={"200": PedidoDelSchema, "404": ErrorSchema})
def del_pedido(query: PedidoBuscaPorIDSchema):
    """Deleta um Pedido a partir do id informado

    Retorna uma mensagem de confirmação da remoção.
    """
    pedido_id = query.id
    logger.info(f"Deletando pedido #{pedido_id}")
    
    # Criando conexão com a base
    session = Session()
    
    # Verificando se o pedido existe
    pedido = session.query(Pedido).filter(Pedido.id == pedido_id).first()
    
    if not pedido:
        # Se o pedido não foi encontrado
        error_msg = "Pedido não encontrado na base"
        logger.warning(f"Erro ao deletar pedido #{pedido_id}, {error_msg}")
        return {"mesage": error_msg}, 404
    
    # Removendo os itens associados ao pedido
    session.query(ItemPedido).filter(ItemPedido.pedido == pedido_id).delete()
    
    # Deletando o pedido
    session.delete(pedido)
    session.commit()
    
    # Retorna a mensagem de confirmação
    logger.info(f"Deletado pedido #{pedido_id}")
    return {"mesage": "Pedido removido", "id": pedido_id}, 200
@app.put('/pedido', tags=[pedido_tag],
         responses={"200": PedidoViewSchema, "404": ErrorSchema, "400": ErrorSchema})
def update_pedido(body: PedidoUpdateStatusSchema):
    """Atualiza o status de um Pedido a partir do id informado
    
    Retorna uma representação atualizada do pedido.
    """
    pedido_id = body.id
    novo_status = body.status
    
    logger.info(f"Atualizando status do pedido #{pedido_id} para '{novo_status}'")
    
    # Criando conexão com a base
    session = Session()
    
    # Buscando pedido
    pedido = session.query(Pedido).filter(Pedido.id == pedido_id).first()
    
    if not pedido:
        # Se o pedido não foi encontrado
        error_msg = "Pedido não encontrado na base"
        logger.warning(f"Erro ao atualizar pedido #{pedido_id}, {error_msg}")
        return {"mesage": error_msg}, 404
    
    # Verificando se o status é válido
    status_validos = ["Criado", "Em processamento", "Pago", "Enviado", "Entregue", "Cancelado"]
    if novo_status not in status_validos:
        error_msg = f"Status inválido. Status permitidos: {', '.join(status_validos)}"
        logger.warning(f"Erro ao atualizar pedido #{pedido_id}, {error_msg}")
        return {"mesage": error_msg}, 400
    
    # Atualizando o status
    pedido.status = novo_status
    session.commit()
    
    logger.info(f"Pedido #{pedido_id} atualizado com sucesso para status '{novo_status}'")
    return apresenta_pedido(pedido), 200