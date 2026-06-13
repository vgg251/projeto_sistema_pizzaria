from gerencador_de_arquivos import GerenciadorArquivo


class PedidoPizza:
    def __init__(self, sabor, tamanho, quantidade, preco):
        self.sabor = sabor
        self.tamanho = tamanho
        self.quantidade = quantidade
        self.preco = preco
    def lista(self):
        return [self.sabor, self.tamanho, self.quantidade, self.preco]


class PizzaCardapio:
    def __init__(self, sabor, ingredientes):
        self.sabor = sabor
        self.ingredientes = ingredientes
    def lista(self):
        return [self.sabor, self.ingredientes]


def menu_de_entrada():
    print('\n' + '=' * 35)
    print('     PIZZARIA PIZZAZ COM Z MESMO    ')
    print('=' * 35)
    print('1. Entrar como cliente')
    print('2. Entrar como administrador')
    print('=' * 35)


def menu_cliente():
    print('\n' + '=' * 35)
    print('     PIZZARIA PIZZAZ COM Z MESMO    ')
    print('=' * 35)
    print('1. Fazer Novo Pedido')
    print('2. Listar Todos os Pedidos')
    print('3. Cardápio da Pizzaria Pizzaz Com Z mesmo')
    print('4. Limpar Pedidos')
    print('5. Sair')
    print('=' * 35)


def menu_administrador():
    print('\n' + '=' * 35)
    print('  PIZZARIA PIZZAZ COM Z MESMO (ADM)   ')
    print('=' * 35)
    print('1. Fazer Novo Pedido')
    print('2. Listar Todos os Pedidos')
    print('3. Cardápio da Pizzaria Pizzaz Com Z mesmo')
    print('4. Adicionar pizza ao cardápio')
    print('5. Remover pizza do cardápio')
    print('6. Editar pizzas adicionadas')
    print('7. Limpar Pedidos')
    print('8. Sair')
    print('76. Explodir tudo num raio de 500km')
    print('=' * 35)

##################################################################################################################################################################################################################
def carregar_pedidos(db):
    lista_pedidos = []
    dados_brutos = db.recuperaDados()
    for linha in dados_brutos:
        pedido = PedidoPizza(linha[0], linha[1], linha[2], linha[3])
        lista_pedidos.append(pedido)
    return lista_pedidos
##################################################################################################################################################################################################################

def carregar_cardapio(db):
    lista_cardapio = []
    dados_brutos = db.recuperaDados()
    for linha in dados_brutos:
        if not linha:
            continue

        sabor = linha[0]
        ingredientes = ", ".join(str(item) for item in linha[1:]) if len(linha) > 1 else ''
        lista_cardapio.append(PizzaCardapio(sabor, ingredientes))
    return lista_cardapio
##################################################################################################################################################################################################################

def salvar_pedidos(db, lista_pedidos):
    salvar_dados = []
    for ped in lista_pedidos:
        salvar_dados.append(ped.lista())
    db.salvarDados(salvar_dados)
##################################################################################################################################################################################################################

def salvar_cardapio(db, lista_cardapio):
    salvar_dados = []
    for pizza in lista_cardapio:
        salvar_dados.append(pizza.lista())
    db.salvarDados(salvar_dados)
##################################################################################################################################################################################################################

def limpar_pedidos(db):
    db.salvarDados([])
##################################################################################################################################################################################################################

def main():
    db_pedidos_cliente = GerenciadorArquivo('pedidos_cliente.csv')
    db_cardapio = GerenciadorArquivo('cardapio.csv')
    db_pedidos_adm = GerenciadorArquivo('pedidos_adm.csv')

    while True:
        menu_de_entrada()
        entrar_no_sistema = input('Escolha uma opção (1 para Cliente, 2 para ADM): ').strip()
##################################################################################################################################################################################################################
        if entrar_no_sistema == '1':
            print('\n--- Entrando no menu para clientes da Pizzaria Pizzaz Com Z Mesmo ---')

            while True:
                menu_cliente()
                pedidos = carregar_pedidos(db_pedidos_cliente)
                cardapio = carregar_cardapio(db_cardapio)
                opcao = input('Escolha uma opção (1-5): ').strip()
##################################################################################################################################################################################################################
                if opcao == '1':
                    print('\n--- FAZER NOVO PEDIDO ---')
                    informar_sabor = input('Escolha o sabor da Pizza: ')
                    informar_tamanho = input('Escolha o tamanho (P, M, G, GG): ').strip().upper()
                    if informar_tamanho not in ('P', 'M', 'G', 'GG'):
                        print('Tamanho inválido!\nEscolha entre os tamanhos: P, M, G, GG ')
                    else:
                        informar_quantidade = input('Informe a quantidade: ').strip()
                        try:
                            informar_quantidade_int = int(informar_quantidade)
                            if informar_quantidade_int <= 0:
                                raise ValueError
                        except ValueError:
                            print('Quantidade inválida! Informe um número inteiro maior que zero.')
                            continue

                        if informar_tamanho == 'P':
                            informar_preco = 30.00
                        elif informar_tamanho == 'M':
                            informar_preco = 40.00
                        elif informar_tamanho == 'G':
                            informar_preco = 50.00
                        else:
                            informar_preco = 60.00

                        valor_total = informar_preco * informar_quantidade_int
                        print(f'Valor total do pedido: R${valor_total:.2f}')
                        confirmar_pedido = input('Deseja confirmar o pedido? (s/n): ').strip().capitalize()
                        if confirmar_pedido == 'S':     
                            novo_pedido = PedidoPizza(informar_sabor, informar_tamanho, informar_quantidade_int, informar_preco)
                            pedidos.append(novo_pedido)
                            salvar_pedidos(db_pedidos_cliente, pedidos)
                            print('Pedido confirmado')
                        else:                            
                            print('Pedido cancelado.')            
##################################################################################################################################################################################################################

                elif opcao == '2':
                    print('\n--- SEUS PEDIDOS REALIZADOS ---')
                    if len(pedidos) == 0:
                        print('Você ainda não fez nenhum pedido')
                    else:
                        for posicao, p in enumerate(pedidos, 1):
                            total_do_item = p.quantidade * p.preco
                            print(f'{posicao}. Pizza de {p.sabor} ({p.tamanho}) | Qtd: {p.quantidade} | Total: R$ {total_do_item:.2f}')
##################################################################################################################################################################################################################

                elif opcao == '3':
                    print('\n--- CARDÁPIO ---')
                    print('Sabores disponíveis hoje:')
                    for posicao, pizza in enumerate(cardapio, 1):
                        print(f'{posicao}. Pizza de {pizza.sabor}')
##################################################################################################################################################################################################################

                elif opcao == '4':
                    confirmar = input('Tem certeza que deseja limpar todos os pedidos? (s/n): ').strip().lower()
                    if confirmar == 's':
                        limpar_pedidos(db_pedidos_cliente)
                        pedidos = []
                        print('Todos os pedidos foram limpos.')
                    else:
                        print('Operação cancelada.')

                elif opcao == '5':
                    print('Encerrando...')
                    break
                else:
                    print('Opção inválida!')
##################################################################################################################################################################################################################

        elif entrar_no_sistema == '2':
            senha = input('Digite a senha do administrador: ')
            if senha == 'Lembro mais não':
                print('\n--- Entrando com acesso de Administrador ---')
                while True:
                    menu_administrador()
                    pedidos = carregar_pedidos(db_pedidos_adm)
                    cardapio = carregar_cardapio(db_cardapio)
                    opcao_adm = input('Escolha uma opção (1-8 ou 76): ').strip()

                    if opcao_adm == '1':
                        print('\n--- FAZER NOVO PEDIDO ---')
                        informar_sabor = input('Escolha o sabor da Pizza: ')
                        informar_tamanho = input('Escolha o tamanho (P, M, G, GG): ').strip().upper()
                        if informar_tamanho not in ('P', 'M', 'G', 'GG'):
                            print('Tamanho inválido!\nEscolha entre os tamanhos: P, M, G, GG ')
                        else:
                            informar_quantidade = input('Informe a quantidade: ').strip()
                            try:
                                informar_quantidade_int = int(informar_quantidade)
                                if informar_quantidade_int <= 0:
                                    raise ValueError
                            except ValueError:
                                print('Quantidade inválida! Informe um número inteiro maior que zero.')
                                continue

                            if informar_tamanho == 'P':
                                informar_preco = 30.00
                            elif informar_tamanho == 'M':
                                informar_preco = 40.00
                            elif informar_tamanho == 'G':
                                informar_preco = 50.00
                            else:
                                informar_preco = 60.00

                            valor_total = informar_preco * informar_quantidade_int
                            print(f'Valor total do pedido: R${valor_total:.2f}')
                            confirmar_pedido = input('Deseja confirmar o pedido? (s/n): ').strip().capitalize()
                            if confirmar_pedido == 'S':
                                novo_pedido = PedidoPizza(informar_sabor, informar_tamanho, informar_quantidade_int, informar_preco)
                                pedidos.append(novo_pedido)
                                salvar_pedidos(db_pedidos_adm, pedidos)
                                print('Pedido confirmado')
                            else:
                                print('Pedido cancelado.')
##################################################################################################################################################################################################################

                    elif opcao_adm == '2':
                        print('\nSimulação de pedidos. (ADM)')
                        if len(pedidos) == 0:
                            print('Você ainda não fez nenhum pedido.')
                        else:
                            for posicao, p in enumerate(pedidos, 1):
                                total_do_item = p.quantidade * p.preco
                                print(f'{posicao}. Pizza de {p.sabor} ({p.tamanho}) | Qtd: {p.quantidade} | Total: R$ {total_do_item:.2f}')
##################################################################################################################################################################################################################

                    elif opcao_adm == '3':
                        print('Visualizar cardápio (ADM)')
                        for posicao, pizza in enumerate(cardapio, 1):
                            print(f'{posicao}. Sabor: {pizza.sabor} | Ingredientes: {pizza.ingredientes}')
##################################################################################################################################################################################################################

                    elif opcao_adm == '4':
                        print('Adicionar novo sabor ao cardápio (ADM)')
                        novo_sabor = input('Digite o nome do novo sabor: ').strip()
                        novos_ingredientes = input('Digite os ingredientes da pizza: ').strip()
                        if novo_sabor and novos_ingredientes:
                            cardapio.append(PizzaCardapio(novo_sabor, novos_ingredientes))
                            salvar_cardapio(db_cardapio, cardapio)
                            print(f'Sabor "{novo_sabor}" adicionado com sucesso!')
                        else:
                            print('Erro: Nome do sabor ou ingredientes não podem ser vazios.')
##################################################################################################################################################################################################################

                    elif opcao_adm == '5':
                        print('Remover sabor do cardápio (ADM)')
                        if len(cardapio) == 0:
                            print('O cardápio já está vazio.')
                        else:
                            for posicao, pizza in enumerate(cardapio, 1):
                                print(f'{posicao}. {pizza.sabor}')
                            try:
                                indice = int(input('\nDigite o número da pizza que deseja remover: ')) - 1
                                if 0 <= indice < len(cardapio):
                                    removida = cardapio.pop(indice)
                                    salvar_cardapio(db_cardapio, cardapio)
                                    print(f'Sabor "{removida.sabor}" foi removido do cardápio!')
                                else:
                                    print('Número inválido!')
                            except ValueError:
                                print('Erro: Digite um número inteiro válido.')
##################################################################################################################################################################################################################

                    elif opcao_adm == '6':
                        print('Editar sabor do cardápio (ADM)')
                        if len(cardapio) == 0:
                            print('Não há pizzas para editar.')
                        else:
                            for posicao, pizza in enumerate(cardapio, 1):
                                print(f'{posicao}. {pizza.sabor}')
                            try:
                                indice = int(input('\nDigite o número da pizza que deseja editar: ')) - 1
                                if 0 <= indice < len(cardapio):
                                    pizza_alvo = cardapio[indice]
                                    print(f'\nEditando: {pizza_alvo.sabor}')
                                    mudar_sabor = input(f'Novo nome (Deixe em branco para manter "{pizza_alvo.sabor}"): ').strip()
                                    mudar_ingredientes = input('Novos ingredientes (Deixe em branco para manter): ').strip()
                                    if mudar_sabor:
                                        pizza_alvo.sabor = mudar_sabor
                                    if mudar_ingredientes:
                                        pizza_alvo.ingredientes = mudar_ingredientes
                                    salvar_cardapio(db_cardapio, cardapio)
                                    print('Sabor atualizado com sucesso no cardápio!')
                                else:
                                    print('Número inválido!')
                            except ValueError:
                                print('Erro: Digite um número inteiro válido.')
##################################################################################################################################################################################################################

                    elif opcao_adm == '7':
                        confirmar = input('Tem certeza que deseja limpar todos os pedidos do administrador? (s/n): ').strip().lower()
                        if confirmar == 's':
                            limpar_pedidos(db_pedidos_adm)
                            pedidos = []
                            print('Todos os pedidos do administrador foram limpos.')
                        else:
                            print('Operação cancelada.')
##################################################################################################################################################################################################################

                    elif opcao_adm == '8':
                        print('Saindo do menu de Administrador...')
                        break
##################################################################################################################################################################################################################

                    elif opcao_adm == '76':
                        print('\nPROTOCOLO RICO ATIVADO')
                        print('3... 2... 1...')
                        break
                    else:
                        print('Opção inválida!')
            else:
                print('Senha incorreta!')
        else:
            print('Opção inválida! \n Escolha 1 ou 2.')

if __name__ == '__main__':
    main()








