from pagamento.pagamento import Pagamento

class PagamentoPix(Pagamento):
    def processar(self, valor):
        print(f"Processando pagamento de R$: {valor:.2f} via Pix") 