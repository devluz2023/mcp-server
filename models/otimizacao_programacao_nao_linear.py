# -*- coding: utf-8 -*-


lucro_por_tipo = {"Tomate": 2.00, "Alface": 1.50}

# Lucro por quilo de cada tipo de alimento
lucro_por_tipo = {"Tomate": 2.00, "Alface": 1.50}

# Demanda de recursos por quilo de cada tipo de alimento
# Agora, removemos o 'tempo_cuidado' e ajustamos as quantidades de água e espaço
demanda_por_tipo = {
    "Tomate": {"agua": 3, "espaco": 2},
    "Alface": {"agua": 2, "espaco": 3},
}

# Disponibilidade total de recursos na fazenda
disponibilidade_recursos = {
    "agua": 5900,  # litros disponíveis
    "espaco": 5400,  # metros quadrados de terra arável
}



# Cálculo do máximo que pode ser produzido para cada tipo de vegetal
max_tomate = min(
    disponibilidade_recursos["agua"] / demanda_por_tipo["Tomate"]["agua"],
    disponibilidade_recursos["espaco"] / demanda_por_tipo["Tomate"]["espaco"],
)

max_alface = min(
    disponibilidade_recursos["agua"] / demanda_por_tipo["Alface"]["agua"],
    disponibilidade_recursos["espaco"] / demanda_por_tipo["Alface"]["espaco"],
)

max_tomate

max_alface



def calcular_lucro_e_viabilidade(qtd_tomate, qtd_alface):
    # Calcula o uso total de água e espaço para as quantidades escolhidas de tomate e alface
    uso_agua = (
        qtd_tomate * demanda_por_tipo["Tomate"]["agua"]
        + qtd_alface * demanda_por_tipo["Alface"]["agua"]
    )
    uso_espaco = (
        qtd_tomate * demanda_por_tipo["Tomate"]["espaco"]
        + qtd_alface * demanda_por_tipo["Alface"]["espaco"]
    )

    restricoes = {
        "agua": uso_agua,
        "espaco": uso_espaco,
        "diversificacao": (qtd_alface, qtd_tomate),
    }

    # Verifica se a combinação de produção viola as restrições de recursos e diversificação
    viola_restricoes = (
        uso_agua > disponibilidade_recursos["agua"]
        or uso_espaco > disponibilidade_recursos["espaco"]
        or qtd_tomate < 10 / 100 * qtd_alface
    )

    # Calcula o lucro total
    lucro = (
        qtd_tomate * lucro_por_tipo["Tomate"] + qtd_alface * lucro_por_tipo["Alface"]
    )

    return lucro, viola_restricoes, restricoes


calcular_lucro_e_viabilidade(16, 0)

calcular_lucro_e_viabilidade(16, 0)

calcular_lucro_e_viabilidade(10, 5)



lista_solucoes = []

# Testando diferentes combinações de produção de tomates e alfaces
for qtd_tomate in range(0, int(max_tomate) + 1, 100):
    for qtd_alface in range(0, int(max_alface) + 1, 100):
        lucro, viola, restricoes = calcular_lucro_e_viabilidade(qtd_tomate, qtd_alface)
        lista_solucoes.append([qtd_tomate, qtd_alface, lucro, viola, restricoes])

        # Se a combinação não viola as restrições, imprime a solução
        if not viola:
            print(
                f"Tomate: {qtd_tomate} kg, Alface: {qtd_alface} kg, Lucro: R$ {lucro:.2f}"
            )



import pandas as pd

# Criando um DataFrame com os resultados
df = pd.DataFrame(
    lista_solucoes,
    columns=["qtd_tomate", "qtd_alface", "lucro", "viola_restricoes", "restricoes"],
)
df.head()  # Visualizando as primeiras linhas do DataFrame/


df.query("viola_restricoes == False")



row_index = df.query("viola_restricoes == False")["lucro"].idxmax()
df.loc[row_index]



import matplotlib.pyplot as plt
import numpy as np

# Limites para o gráfico
x_max = 4000  # Máximo para Tomates (em quilos)
y_max = 4000  # Máximo para Alfaces (em quilos)

# Criando uma matriz de valores para x (Tomates) e y (Alfaces)
x = np.linspace(0, x_max, 400)
y = np.linspace(0, y_max, 400)

# Restrições
y1 = (5900 - 3 * x) / 2  # Restrição de Água
y2 = (5400 - 2 * x) / 3  # Restrição de Espaço
y3 = 10 * x  # Restrição de Diversificação (Tomates pelo menos 10% de Alfaces)

plt.figure(figsize=(10, 8))

# Área de solução viável
plt.fill_between(
    x,
    0,
    np.minimum(np.minimum(y1, y2), y3),
    where=(y1 >= 0) & (y2 >= 0) & (y3 >= 0),
    color="gray",
    alpha=0.3,
)

# Linhas de restrição
plt.plot(x, y1, color="b", label="Restrição de Água")
plt.plot(x, y2, color="g", label="Restrição de Espaço")
plt.plot(x, y3, color="r", label="Restrição de Diversificação")

# Eixos e limites
plt.xlim(0, x_max)
plt.ylim(0, y_max)
plt.xlabel("Quantidade de Tomates (em quilos)")
plt.ylabel("Quantidade de Alfaces (em quilos)")

# Adicionando título e legenda
plt.title("Solução Gráfica para o Problema de Otimização da Produção na Fazenda")
plt.legend()



plt.figure(figsize=(10, 8))

# Área de solução viável
plt.fill_between(
    x,
    0,
    np.minimum(np.minimum(y1, y2), y3),
    where=(y1 >= 0) & (y2 >= 0) & (y3 >= 0),
    color="gray",
    alpha=0.3,
)

# Linhas de restrição
plt.plot(x, y1, color="b", label="Restrição de Água")
plt.plot(x, y2, color="g", label="Restrição de Espaço")
plt.plot(x, y3, color="r", label="Restrição de Diversificação")

# Curvas de nível para a função objetivo
X, Y = np.meshgrid(x, y)

# Função objetivo: Z = 2x_Tomate + 1.5x_Alfaces
Z = 2 * X + 1.5 * Y

plt.contour(X, Y, Z, 50, alpha=0.5, cmap="jet")


# Eixos e limites
plt.xlim(0, x_max)
plt.ylim(0, y_max)
plt.xlabel("Quantidade de Tomates (em quilos)")
plt.ylabel("Quantidade de Alfaces (em quilos)")

# Adicionando título e legenda
plt.title("Solução Gráfica para o Problema de Otimização da Produção na Fazenda")
plt.legend()


plt.figure(figsize=(10, 8))

# Área de solução viável
plt.fill_between(
    x,
    0,
    np.minimum(np.minimum(y1, y2), y3),
    where=(y1 >= 0) & (y2 >= 0) & (y3 >= 0),
    color="gray",
    alpha=0.3,
)

# Linhas de restrição
plt.plot(x, y1, color="b", label="Restrição de Água")
plt.plot(x, y2, color="g", label="Restrição de Espaço")
plt.plot(x, y3, color="r", label="Restrição de Diversificação")

# Curvas de nível para a função objetivo
X, Y = np.meshgrid(x, y)

# Função objetivo: Z = 2x_Tomate + 1.5x_Alfaces
Z = 3 * X + 2 * Y

plt.contour(X, Y, Z, 50, alpha=0.5, cmap="jet")


# Eixos e limites
plt.xlim(0, x_max)
plt.ylim(0, y_max)
plt.xlabel("Quantidade de Tomates (em quilos)")
plt.ylabel("Quantidade de Alfaces (em quilos)")

# Adicionando título e legenda
plt.title("Solução Gráfica para o Problema de Otimização da Produção na Fazenda")
plt.legend()



# Área de solução viável
plt.fill_between(x, 0, (y3 >= 0), color="gray", alpha=0.3)

# Linhas de restrição
plt.plot(x, y3, color="r", label="Restrição de Diversificação")

# Curvas de nível para a função objetivo
X, Y = np.meshgrid(x, y)

# Função objetivo: Z = 2x_Tomate + 1.5x_Alfaces
Z = 2 * X + 1.5 * Y

plt.contour(X, Y, Z, 50, alpha=0.5, cmap="jet")

# Eixos e limites
plt.xlim(0, x_max)
plt.ylim(0, y_max)
plt.xlabel("Quantidade de Tomates (em quilos)")
plt.ylabel("Quantidade de Alfaces (em quilos)")

# Adicionando título e legenda
plt.title(
    "Solução Gráfica para o Problema de Otimização da Produção na Fazenda (Sem Restrição de Espaço)"
)
plt.legend()

# Mostrar gráfico
plt.show()



import matplotlib.pyplot as plt
import numpy as np

# Limites para o gráfico
x_max = 4000  # Máximo para Tomates (em quilos)
y_max = 4000  # Máximo para Alfaces (em quilos)

# Criando uma matriz de valores para x (Tomates) e y (Alfaces)
x = np.linspace(0, x_max, 400)

# Restrições
y1 = (5900 - 3 * x) / 2  # Restrição de Água para Alfaces
y2 = (5400 - 2 * x) / 3  # Restrição de Espaço
y3 = 10 * x  # Restrição de Diversificação (Tomates pelo menos 10% de Alfaces)
y4 = 3000 - x  # Correção da restrição ambiental

plt.figure(figsize=(10, 8))

# Linhas de restrição
plt.plot(x, y1, label="Restrição de Água", color="blue")
plt.plot(x, y2, label="Restrição de Espaço", color="green")
plt.plot(x, y3, label="Restrição de Diversificação", color="red")
plt.plot(x, y4, label="Nova Restrição Ambiental", color="purple")


# Eixos e limites
plt.xlim(0, x_max)
plt.ylim(0, y_max)
plt.xlabel("Quantidade de Tomates (em quilos)")
plt.ylabel("Quantidade de Alfaces (em quilos)")

# Adicionando título e legenda
plt.title("Solução Gráfica para o Problema de Otimização da Produção na Fazenda")
plt.legend()

# Mostrar gráfico
plt.show()


import pyomo.environ as pyo

# Criando um modelo concreto
modelo = pyo.ConcreteModel()

# Definindo as variáveis de decisão
modelo.x_tomate = pyo.Var(domain=pyo.NonNegativeReals)
modelo.x_alface = pyo.Var(domain=pyo.NonNegativeReals)

# Definindo a função objetivo
modelo.lucro = pyo.Objective(
    expr=2 * modelo.x_tomate + 1.5 * modelo.x_alface, sense=pyo.maximize
)

# Adicionando as restrições
modelo.restricao_agua = pyo.Constraint(
    expr=3 * modelo.x_tomate + 2 * modelo.x_alface <= 5900
)
modelo.restricao_espaco = pyo.Constraint(
    expr=2 * modelo.x_tomate + 3 * modelo.x_alface <= 5400
)
modelo.restricao_diversificacao = pyo.Constraint(
    expr=modelo.x_tomate >= 0.1 * modelo.x_alface
)




# Resolvendo o modelo
solver = pyo.SolverFactory("glpk")
resultado = solver.solve(modelo, tee=True)



# Exibindo resultados
modelo.x_tomate.display()
modelo.x_alface.display()


# Imprimindo a solução
print(f"Quantidade de Tomate: {pyo.value(modelo.x_tomate)} kg")
print(f"Quantidade de Alface: {pyo.value(modelo.x_alface)} kg")
print(f"Lucro total: R$ {pyo.value(modelo.lucro)}")


import pyomo.environ as pyo

# Dados do problema
alimentos = ["Tomate", "Alface", "Cenoura", "Batata"]
recursos = ["agua", "espaco"]

lucro_por_alimento = {"Tomate": 2.00, "Alface": 1.50, "Cenoura": 1.80, "Batata": 1.20}
demanda_por_alimento = {
    "Tomate": {"agua": 3, "espaco": 2},
    "Alface": {"agua": 2, "espaco": 1},
    "Cenoura": {"agua": 4, "espaco": 3},
    "Batata": {"agua": 5, "espaco": 2.5},
}
disponibilidade_recursos = {"agua": 20000, "espaco": 10000}

# Modelo
modelo = pyo.ConcreteModel()

# Variáveis de decisão
modelo.x = pyo.Var(alimentos, domain=pyo.NonNegativeReals)

# Função objetivo
modelo.lucro = pyo.Objective(
    expr=sum(lucro_por_alimento[i] * modelo.x[i] for i in alimentos), sense=pyo.maximize
)

# Restrições
for r in recursos:
    modelo.add_component(
        f"restricao_{r}",
        pyo.Constraint(
            expr=sum(demanda_por_alimento[i][r] * modelo.x[i] for i in alimentos)
            <= disponibilidade_recursos[r]
        ),
    )

# Resolver o modelo
solver = pyo.SolverFactory("glpk")
resultado = solver.solve(modelo, tee=True)

# Imprimir resultados
for alimento in alimentos:
    print(f"Produção de {alimento}: {pyo.value(modelo.x[alimento])} kg")
print(f"Lucro total: R$ {pyo.value(modelo.lucro)}")


# Criando um modelo concreto
modelo = pyo.ConcreteModel()

# Definindo as variáveis de decisão
modelo.x_tomate = pyo.Var(domain=pyo.NonNegativeReals)
modelo.x_alface = pyo.Var(domain=pyo.NonNegativeReals)

# Definindo a função objetivo
modelo.lucro = pyo.Objective(
    expr=2 * modelo.x_tomate + 1.5 * modelo.x_alface, sense=pyo.maximize
)

# Adicionando as restrições
modelo.restricao_agua = pyo.Constraint(
    expr=3 * modelo.x_tomate + 2 * modelo.x_alface <= 5900
)
modelo.restricao_espaco = pyo.Constraint(
    expr=2 * modelo.x_tomate + 3 * modelo.x_alface <= 5400
)
modelo.restricao_diversificacao = pyo.Constraint(
    expr=modelo.x_tomate >= 0.1 * modelo.x_alface
)

solver = pyo.SolverFactory("glpk")
resultado = solver.solve(modelo, tee=True)

"""Após resolver o modelo, podemos verificar as folgas nas restrições:"""

# Exibindo as folgas das restrições
agua_folga = modelo.restricao_agua.slack()
espaco_folga = modelo.restricao_espaco.slack()
diversificacao_folga = modelo.restricao_diversificacao.slack()

print(f"Folga na Restrição de Água: {agua_folga}")
print(f"Folga na Restrição de Espaço: {espaco_folga}")
print(f"Folga na Restrição de Diversificação: {diversificacao_folga}")




def criar_modelo(coef_tomate):
    modelo = pyo.ConcreteModel()

    modelo.x_tomate = pyo.Var(domain=pyo.NonNegativeReals)
    modelo.x_alface = pyo.Var(domain=pyo.NonNegativeReals)

    modelo.lucro = pyo.Objective(
        expr=coef_tomate * modelo.x_tomate + 1.5 * modelo.x_alface, sense=pyo.maximize
    )

    modelo.restricao_agua = pyo.Constraint(
        expr=3 * modelo.x_tomate + 2 * modelo.x_alface <= 6000
    )
    modelo.restricao_espaco = pyo.Constraint(
        expr=2 * modelo.x_tomate + 3 * modelo.x_alface <= 5500
    )
    modelo.restricao_diversificacao = pyo.Constraint(
        expr=modelo.x_tomate >= 0.1 * modelo.x_alface
    )

    solver = pyo.SolverFactory("glpk")
    resultado = solver.solve(modelo, tee=True)

    return modelo


solver = pyo.SolverFactory("glpk")

coeficientes_tomate = np.linspace(1.5, 2.5, 12)

lucros_otimos = []
quantidades_tomate = []
quantidades_alface = []

for coef_tomate in coeficientes_tomate:
    modelo = criar_modelo(coef_tomate)
    resultado = solver.solve(modelo, tee=True)

    lucros_otimos.append(pyo.value(modelo.lucro))
    quantidades_tomate.append(pyo.value(modelo.x_tomate))
    quantidades_alface.append(pyo.value(modelo.x_alface))


plt.plot(coeficientes_tomate, lucros_otimos, ".")

plt.plot(coeficientes_tomate, quantidades_tomate, ".")

plt.plot(coeficientes_tomate, quantidades_alface, ".")
