from abc import ABC,abstractmethod
from cliente import Cliente

class Pedido(ABC):
    def __init__(self, cliente: Cliente,itens: list):
        self.cliente = cliente
        self.itens = itens
     
    @abstractmethod    
    def calcular_total(self):
        pass