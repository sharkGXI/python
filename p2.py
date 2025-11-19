from datetime import datetime
import random
import os

# cria o arquivo na pasta documentos do computador

documentos = os.path.join(os.path.expanduser("~"), "Documents")
caminho_arquivo = os.path.join(documentos, "cadastro.txt")

print("============Sistema de Cadastro de Compras=============")

nome = input("Digite o nome do cliente: ")

# Entrada do valor com tratamento de erro
try:
    valor = float(input("Digite o valor da compra: "))
except ValueError:
    print("Erro: digite apenas números no valor da compra!")
    exit()  # Sai do programa

# Escolha da forma de pagamento
pagamento = input(
    "=====FORMA DE PAGAMENTO======\n1 = cartão\n2 = pix\n3 = dinheiro\nDigite: ")

if pagamento == "1":
    pagamento = "cartão"
elif pagamento == "2":
    pagamento = "pix"
elif pagamento == "3":
    pagamento = "dinheiro"
else:
    print("ERRO: digite apenas 1, 2 ou 3 !!!")
    exit()

# Data da compra
data_compra = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

# Número do pedido aleatório
numero_pedido = random.randint(1000, 9999)

# Função para aplicar desconto


def desconto(valor):
    valor_final = valor * 0.90
    print("Desconto de 10% aplicado.")
    return valor_final


# Verifica se tem desconto
if valor > 100:
    valor_final = desconto(valor)
else:
    valor_final = valor
    print("Sem desconto. Valor final:", valor_final)

# Dicionário dos dados do cliente
cliente = {
    "Nome": nome,
    "Valor da compra": valor,
    "Valor final": valor_final,
    "Forma de pagamento": pagamento,
    "Data da compra": data_compra,
    "Numero do pedido": numero_pedido
}

# Salvando no arquivo
with open(caminho_arquivo, "a", encoding="utf-8") as arquivo:
    arquivo.write("===== COMPRA REGISTRADA =====\n")
    arquivo.write(f"Cliente: {cliente['Nome']}\n")
    arquivo.write(f"Valor da compra: R$ {cliente['Valor da compra']}\n")
    arquivo.write(f"Valor final: R$ {cliente['Valor final']}\n")
    arquivo.write(f"Forma de pagamento: {cliente['Forma de pagamento']}\n")
    arquivo.write(f"Data: {cliente['Data da compra']}\n")
    arquivo.write(f"Número do pedido: {cliente['Numero do pedido']}\n")
    arquivo.write(
        "-------------------------------------------------------------------------------\n\n")

print("\nCadastro salvo com sucesso na pasta arquivos como 'cadastro.txt'!")
