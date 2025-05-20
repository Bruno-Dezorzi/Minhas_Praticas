from cliente import Cliente
from item import Item
from pedido.pedido_delivery import PedidoDelivery
from pagamento.pagamento_factory import PagamentoFactory
from notificacao.notificacao_facade import NotificacaoFacade
from observador.observador_status import ObservadorStatus


cliente = Cliente("Bruno", "Rua Sucuri")
itens = [Item("Pizza",30.00),Item("Refrigerante",5.00)]
taxa_entrega = 10.00



pedido = PedidoDelivery(cliente= cliente, itens= itens, taxa_entrega= taxa_entrega)
total_pedido = pedido.calcular_total()


valor_pedido = pedido.calcular_total()

# pagamento_cartao = PagamentoCartao().processar(valor_pedido)
# pagamento_pix = PagamentoPix().processar(valor_pedido)

tipo_pagamento = "pix"
pagamento = PagamentoFactory.criar_pagamento(tipo= tipo_pagamento).processar(valor= valor_pedido)

MENSAGEM_PAGO = "O pagamento foi confirmado"
MENSAGEM_PREPARANDO = "O pedido esta sendo preparado"
MENSAGEM_ENVIADO = "O pedido saiu para a entrega!"


observador = ObservadorStatus(notificacoes= NotificacaoFacade())

pedido.adicionar_observadores(observador= observador)

pedido.status = MENSAGEM_PAGO
pedido.status = MENSAGEM_PREPARANDO
pedido.status = MENSAGEM_ENVIADO
# notificao_email = NotificacaoEmail().enviar_notificacao(cliente= cliente, mensagem= MENSAGEM)
# notificacao_sms = NotificacaoSms().enviar_notificacao(cliente= cliente, mensagem= MENSAGEM)



