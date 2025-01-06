import __init__ 
from views.view import SubscriptionSevice
from models.model import Subscription
from models.database import engine
from datetime import datetime
from decimal import Decimal

class UI:
    def __init__(self):
        self.subscription_service = SubscriptionSevice(engine)

    def start(self):
        while True:
            print(''' 
            [1] -> Adicionar assinatura
            [2] -> Remover assinatura
            [3] -> Valor total
            [4] -> Gastos últimos 12 meses
            [5] -> Efetuar pagamento   
            [6] -> Sair
            ''')
            choice = int(input('Escolha uma opção: '))
            if choice == 1:
                self.add_subscription()
            elif choice == 2:
                self.delete_subscription()
            elif choice == 3:
                self.total_value()
            elif choice == 4:
                self.subscription_service.gen_chart()
            elif choice == 5:
                self.pay_subscription()
            else:
                break

    def add_subscription(self):
        empresa = input('Empresa: ')
        site = input('Site: ')
        data_assinatura = datetime.strptime(input('Data da assinatura: '), '%d/%m/%Y')
        valor = Decimal(input('Valor: '))
        subscription = Subscription(empresa=empresa, site=site, data_assinatura=data_assinatura, valor=valor)
        self.subscription_service.create(subscription)

    def delete_subscription(self):
        subscriptions = self.subscription_service.list_all()
        print('Escolha qual assinatura deseja excluir')

        for i in subscriptions:
            print(f'[{i.id}] -> {i.empresa}')

        choice = int(input('Escolha a assinatura: '))

        if not any(subscription.id == choice for subscription in subscriptions):
            print("Assinatura não encontrada!")
            return
    
        self.subscription_service.delete(choice)
        print('Assinatura excluida com sucesso')

    def total_value(self):
        print(f'Seu valor total mensal em assinaturas é {self.subscription_service.total_value()}')

    def pay_subscription(self):
        subscriptions = self.subscription_service.list_all()
        print('Escolha qual assinatura deseja pagar')

        for i in subscriptions:
            print(f'[{i.id}] -> {i.empresa}')

        choice = int(input('Escolha o ID da assinatura para pagamento: '))

        if not any(subscription.id == choice for subscription in subscriptions):
            print("Assinatura não encontrada!")
            return

        subscription = next(subscription for subscription in subscriptions if subscription.id == choice)
        self.subscription_service.pay(subscription)
        print(f'Pagamento realizado para a assinatura de {subscription.empresa} com sucesso!')


UI().start()