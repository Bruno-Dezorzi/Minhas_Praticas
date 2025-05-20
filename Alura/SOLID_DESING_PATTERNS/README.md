# **Sistema de Gerenciamento de Pedidos**

## **Descrição**

Este projeto implementa um sistema de gerenciamento de pedidos que simula um fluxo de pedidos de clientes, incluindo cálculo de totais, notificações, pagamento e atualização de status.

---

## **Funcionalidades**

- **Cadastro de Clientes e Itens**: Gerencia informações de clientes e produtos.
- **Gestão de Pedidos**: Suporte a pedidos para delivery e retirada.
- **Sistema de Pagamento**: Simulação de processamento de pagamentos.
- **Notificações**: Envio de notificações por e-mail e SMS.
- **Atualização de Status**: Rastreamento e notificação do status do pedido.
---

## **Tecnologias Utilizadas**

- **Python 3.10+**
- Design Patterns: _Factory Method, Template, Strategy, Facade, Observer_.
- Princípios **SOLID**.

---

## **Estrutura do Projeto**

```
.
├── cliente.py
├── item.py
├── main.py
├── notificacao/
│   ├── notificacao.py
│   ├── notificacao_email.py
│   ├── notificacao_sms.py
│   └── notificacao_facade.py
├── observador/
│   └── observador_status.py
├── pagamento/
│   ├── pagamento.py
│   ├── pagamento_cartao.py
│   ├── pagamento_pix.py
|   └── pagamento_factory
├── pedido/
│   ├── pedido.py
│   ├── pedido_delivery.py
│   └── pedido_retirada.py
└── README.md
```

---

## **Como Executar**

1. Acesse o arquivo `main.py`.
2. Execute o programa:
   ```bash
   python main.py
   ```

---

## **Exemplo de Uso**

- **Cadastrar Cliente e Itens**:
  Crie um cliente e adicione itens ao pedido.
- **Criar Pedido**:
  Escolha entre _delivery_ ou _retirada_.
- **Efetuar Pagamento**:
  Simule pagamentos via Pix ou Cartão.
- **Receber Notificações**:
  Clientes recebem notificações do status do pedido.

---

## **Autoria**

Projeto desenvolvido como estudo dos princípios **SOLID** e padrões de design para organização de software escalável e modular.

Feito pela Escola de Programação da Alura!

Fique à vontade para contribuir! 🎉


## **Explicação do SOLID segundo as aulas**

### S - Princípio da Responsabilidade Única

Cada classe deve possuir uma única responsabilidade/função.

Com isso, seria inicialmente criado o método itens() dentro da classe Cliente, mas isso não está de acordo com o princípio. Portanto, para respeita-lo, criamos uma classe Item, com isso, a existência do Item não fica limitado somente a instânciar a o classe Cliente junto.

### O - Princípio aberto/fechado

Quando se necessita de uma nova funcionalidade ou atributos, uma classe não deve ser modíficada, mas se deve instânciar a funcionalidade de outra classe/ interface.

***Aberto para extensão e fechado para modificação***

Isso foi demostrado nas classes de Pedido, onde foi criado uma classe base outras classes derivadas dessas que realizam herança na base.

A classe Pedido não possui o atributo taxa_entrega igual o pedido_delivery mas, o pedido_delivery, possuia todos os atributos base que vem do pedido, não foi nescessário modificar os atributos de pedido para adicionar uma funcionalidade de taxa de entrega, somente foi nescessário construir uma classe derivada.

### L - Princípio da Substituição de Liskov

Esse princípio descreve que uma classe filha, deve poder substituir sua classe mãe sem quebrar o código, portanto, todas as filhas devem possuir os atributos e métodos das classes mães.

Podemos pegar o exemplo das classes de pagamento, onde a pagamento_cartao e a pagamento_pix possuem a mesma funcionalidade base da pagamento e, portanto, consegume substituíla.




### I - Princípio da Segregação de Interfaces

Classes não possuir os métodos que não precisam

Para esse princípio se constroi interfaces para ser opcional uma classe herdar certos métodos de outra

Um exemplo disso é com as classes notificações onde, no python, é utilizado como classe abstrata já que não é igual outras lingiagens para possuir interfaces, com isso, as classes filhas decicem quais e como seus métodos devem funcionar.

### D - Princípio da Inversão de Dependências

É abstrair métodos bases para serem utilizados por classses filhas

## Explicação dos Padrões de Projeto utilizados

### [Factory Method](https://refactoring.guru/pt-br/design-patterns/factory-method)


O Factory method é um padrão de projeto criacional, que resolve o problema de criar objetos de produtos sem especificar suas classes concretas.

O Factory foi utilizado ao criar a classe pagamento_factory, onde ela possuir um método que cria o objeto(pagamento), de acordo com o tipo passado para a função. Portanto, não precisamos instânciar os pagamentoss de forma direta, instânciamos a fábrica para ela produzir os pagamentos para nós.

Nota: O método criar_pagamento é estático para que na verdade, não sermos dependentes em criar um objeto ao instânciar a fábrica, mas criar os pagamentos de forma direta.

### [Template Method](https://refactoring.guru/pt-br/design-patterns/template-method)

O Template Method é um padrão de projeto comportamental que define o esqueleto de um algoritmo na superclasse mas deixa as subclasses sobrescreverem etapas específicas do algoritmo sem modificar sua estrutura.

O Template Method é um padrão comportamental que permite definir um esqueleto na superclasse. No caso do nosso projeto, criamos um template para o gerenciamento de pedidos. As classes derivadas podem implementar suas próprias estruturas, adicionar novos atributos e métodos, mas sempre seguindo o formato estabelecido pela classe base.

No caso, a classe pedido foi um template para as outras subordinadas a ela

### [Strategy](https://refactoring.guru/pt-br/design-patterns/strategy)

O Strategy é um padrão de projeto comportamental que permite que você defina uma família de algoritmos, coloque-os em classes separadas, e faça os objetos deles intercambiáveis.

No código desenvolvido, é usado juntamente o Strategy e os Princípios S,O e L; Foi utilizado ao criar as três classes de pagamento e as três possuírem métodos com certo nível de semelhança, é uma fámília de métodos em classes separas e são intercambiáveis

### [Facade](https://refactoring.guru/pt-br/design-patterns/facade) 

O Facade é um padrão de projeto estrutural que fornece uma interface simplificada para uma biblioteca, um framework, ou qualquer conjunto complexo de classes.

No caso de exemplo foi as notificações, onde o facade reuniu os tipos de notificações que devem ser chamadas juntas, as estruturando em apenas uma classe que seria invocada

### [Observer](https://refactoring.guru/pt-br/design-patterns/observer)

O Observer é um padrão de projeto comportamental que permite que você defina um mecanismo de assinatura para notificar múltiplos objetos sobre quaisquer eventos que aconteçam com o objeto que eles estão observando.

Ele vai observar o status de um objeto e notificando

É utilizado para notificar o status do pedido