from notificacao.notificacao import Notificacao

class NotificacaoSms(Notificacao):
    def enviar_notificacao(self, cliente, mensagem):
        print(f"Enviando sms para {cliente.nome}: {mensagem}")