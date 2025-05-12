from cliente import Cliente
from item import Item
from pedido.pedido_retirada import PedidoRetirada
from pedido.pedido_delivery import PedidoDelivery

cliente = Cliente("Bruno", "Rua Sucuri")
itens = [Item("Pizza",30.00),Item("Refrigerante",5.00)]
taxa_entrega = 10.00


pedido_retirada = PedidoRetirada(cliente= cliente, itens= itens)
total_pedido_retirada = pedido_retirada.calcular_total()

pedido_delivery = PedidoDelivery(cliente= cliente, itens= itens, taxa_entrega= taxa_entrega)
total_pedido_delivery = pedido_delivery.calcular_total()

print(f"Ola {cliente.nome}, tudo bem?")

print(f"Seu total foi de: R${total_pedido_retirada:.2f} para a retirada")

print(f"Seu total foi de: R${total_pedido_delivery:.2f} para a delivery")

