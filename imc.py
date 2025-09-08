peso = float(input("digite o peso: "))
altura = float(input("digite a altura: "))

if (peso < 0 or altura < 0):
    print("digite um peso valido ")

else:
    print("seu peso é: ", peso, "e sua altura é: ", altura)


imc = peso / (altura ** 2)


if imc < 18.5:
    classificacao = "Abaixo do peso"
    dica = "Tente manter uma alimentação equilibrada e saudável."
elif 18.5 <= imc <= 24.9:
    classificacao = "Peso normal"
    dica = "Parabéns! Continue mantendo hábitos saudáveis."
elif 25.0 <= imc <= 29.9:
    classificacao = "Sobrepeso"
    dica = "Praticar atividades físicas pode ajudar a melhorar seu bem-estar."
else:
    classificacao = "Obesidade"
    dica = "Procure acompanhamento médico e adote hábitos mais saudáveis."

# Exibição dos resultados
print("\n===== RESULTADO =====")
print(f"Seu IMC é: {imc:.2f}")
print(f"Classificação: {classificacao}")
print(f"Dica: {dica}")
print("\n Cuide sempre da sua saúde, você é capaz de evoluir! ")
