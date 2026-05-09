# -*- coding: utf-8 -*-

atracoes = [
    "Torre Eiffel",
    "Museu do Louvre",
    "Catedral de Notre-Dame",
    "Sacré-Cœur",
    "Arco do Triunfo",
    "Jardim de Luxemburgo",
    "Sainte-Chapelle",
    "Place de la Concorde",
    "Panthéon",
    "Museu d'Orsay",
    "Stade de France",
    "Parc des Princes",
]

"""```
localizacao_atracoes = {
    "Torre Eiffel": (48.85837, 2.29448),
    "Museu do Louvre": (48.86115, 2.33929),
    "Catedral de Notre-Dame": (48.85329, 2.34449),
    "Sacré-Cœur": (48.88722, 2.3225),
    "Arco do Triunfo": (48.86889, 2.29448),
    "Jardim de Luxemburgo": (48.85661, 2.35222),
    "Sainte-Chapelle": (48.85329, 2.34449),
    "Place de la Concorde": (48.86667, 2.33333),
    "Panthéon": (48.85333, 2.34667),
    "Museu d'Orsay": (48.86667, 2.33333),
    "Stade de France": (48.83418, 2.33595),
    "Parc des Princes": (48.82761, 2.29809),
}
```


"""

localizacao_atracoes = {
    "Torre Eiffel": (48.85837, 2.29448),
    "Museu do Louvre": (48.86115, 2.33929),
    "Catedral de Notre-Dame": (48.85329, 2.34449),
    "Sacré-Cœur": (48.88722, 2.3225),
    "Arco do Triunfo": (48.86889, 2.29448),
    "Jardim de Luxemburgo": (48.85661, 2.35222),
    "Sainte-Chapelle": (48.85329, 2.34449),
    "Place de la Concorde": (48.86667, 2.33333),
    "Panthéon": (48.85333, 2.34667),
    "Museu d'Orsay": (48.86667, 2.33333),
    "Stade de France": (48.83418, 2.33595),
    "Parc des Princes": (48.82761, 2.29809),
}

"""```
custo_entrada_atracoes = {
    "Torre Eiffel": 25,
    "Museu do Louvre": 17,
    "Catedral de Notre-Dame": 0,
    "Sacré-Cœur": 0,
    "Arco do Triunfo": 0,
    "Jardim de Luxemburgo": 0,
    "Sainte-Chapelle": 12,
    "Place de la Concorde": 0,
    "Panthéon": 8,
    "Museu d'Orsay": 17,
    "Stade de France": 15,
    "Parc des Princes": 12,
}
```
"""

custo_entrada_atracoes = {
    "Torre Eiffel": 25,
    "Museu do Louvre": 17,
    "Catedral de Notre-Dame": 0,
    "Sacré-Cœur": 0,
    "Arco do Triunfo": 0,
    "Jardim de Luxemburgo": 0,
    "Sainte-Chapelle": 12,
    "Place de la Concorde": 0,
    "Panthéon": 8,
    "Museu d'Orsay": 17,
    "Stade de France": 15,
    "Parc des Princes": 12,
}

"""```
tempo_recomendado_atracoes = {
    "Torre Eiffel": 3,
    "Museu do Louvre": 5,
    "Catedral de Notre-Dame": 2,
    "Sacré-Cœur": 1,
    "Arco do Triunfo": 1,
    "Jardim de Luxemburgo": 3,
    "Sainte-Chapelle": 2,
    "Place de la Concorde": 3,
    "Panthéon": 1,
    "Museu d'Orsay": 2,
    "Stade de France": 2,
    "Parc des Princes": 2,
}
```
"""

tempo_recomendado_atracoes = {
    "Torre Eiffel": 3,
    "Museu do Louvre": 5,
    "Catedral de Notre-Dame": 2,
    "Sacré-Cœur": 1,
    "Arco do Triunfo": 1,
    "Jardim de Luxemburgo": 3,
    "Sainte-Chapelle": 2,
    "Place de la Concorde": 3,
    "Panthéon": 1,
    "Museu d'Orsay": 2,
    "Stade de France": 2,
    "Parc des Princes": 2,
}

import folium

mapa = folium.Map(location=[48.856614, 2.352222], zoom_start=12)

for atracao in atracoes:
    popup = folium.Popup(
        f"""<b>{atracao}</b><br>
    Tempo recomendado: {tempo_recomendado_atracoes[atracao]} hora(s)<br>
    Valor da entrada: € {custo_entrada_atracoes[atracao]}
    """,
        max_width=200,
        sticky=True,
    )
    folium.Marker(localizacao_atracoes[atracao], popup=popup).add_to(mapa)

mapa



import pyomo.environ as pyo

tempo_maximo = 6
num_min_atracoes = 4

modelo = pyo.ConcreteModel()

modelo.pontos_turisticos = pyo.Set(initialize=atracoes)

modelo.tempo_maximo = pyo.Param(initialize=tempo_maximo)
modelo.num_min_atracoes = pyo.Param(initialize=num_min_atracoes)
modelo.custo_entrada = pyo.Param(
    modelo.pontos_turisticos, initialize=custo_entrada_atracoes
)
modelo.tempo_recomendado = pyo.Param(
    modelo.pontos_turisticos, initialize=tempo_recomendado_atracoes
)

modelo.visitas = pyo.Var(atracoes, domain=pyo.NonNegativeReals, bounds=(0, 1))

modelo.obj = pyo.Objective(
    expr=sum(modelo.custo_entrada[ponto] * modelo.visitas[ponto] for ponto in atracoes),
    sense=pyo.minimize,
)

modelo.restr_num_min_visitas = pyo.Constraint(
    expr=sum(modelo.visitas[ponto] for ponto in atracoes) >= modelo.num_min_atracoes
)

modelo.restr_tempo = pyo.Constraint(
    expr=sum(
        modelo.tempo_recomendado[ponto] * modelo.visitas[ponto] for ponto in atracoes
    )
    <= modelo.tempo_maximo
)

solver = pyo.SolverFactory("glpk")
resultado = solver.solve(modelo, tee=True)

"""Com o modelo resolvido, podemos imprimir na tela a resolução."""

print(f"Função objetivo: {pyo.value(modelo.obj)}")

for atracao in atracoes:
    valor = round(pyo.value(modelo.visitas[atracao]), 2)
    if valor > 0:
        print(f"{atracao}: Visitado = {valor}")

"""## Preparação para busca por soluções inteiras

Antes de buscar estratégias para o modelo sempre retornar 0 ou 1, é necessário criar funções para facilitar os testes. Essas funções permitirão que executemos o modelo rapidamente e analisemos os resultados de forma mais eficiente.

 A função `criar_modelo()` cria um novo modelo de programação linear com as variáveis de decisão, a função objetivo e as restrições definidas anteriormente. A função `resolver_modelo()` resolve o modelo e imprime na tela a solução
"""


def criar_modelo(
    atracoes,
    custo_entrada_atracoes,
    tempo_recomendado_atracoes,
    tempo_maximo,
    num_min_atracoes,
):
    modelo = pyo.ConcreteModel()

    modelo.pontos_turisticos = pyo.Set(initialize=atracoes)

    modelo.tempo_maximo = pyo.Param(initialize=tempo_maximo)
    modelo.num_min_atracoes = pyo.Param(initialize=num_min_atracoes)
    modelo.custo_entrada = pyo.Param(
        modelo.pontos_turisticos, initialize=custo_entrada_atracoes
    )
    modelo.tempo_recomendado = pyo.Param(
        modelo.pontos_turisticos, initialize=tempo_recomendado_atracoes
    )

    modelo.visitas = pyo.Var(atracoes, domain=pyo.NonNegativeReals, bounds=(0, 1))

    modelo.obj = pyo.Objective(
        expr=sum(
            modelo.custo_entrada[ponto] * modelo.visitas[ponto] for ponto in atracoes
        ),
        sense=pyo.minimize,
    )

    modelo.restr_num_min_visitas = pyo.Constraint(
        expr=sum(modelo.visitas[ponto] for ponto in atracoes) >= modelo.num_min_atracoes
    )

    modelo.restr_tempo = pyo.Constraint(
        expr=sum(
            modelo.tempo_recomendado[ponto] * modelo.visitas[ponto]
            for ponto in atracoes
        )
        <= modelo.tempo_maximo
    )

    return modelo


from pyomo.opt import SolverStatus, TerminationCondition


def resolver_modelo(modelo, log=False):
    solver = pyo.SolverFactory("glpk")
    resultado = solver.solve(modelo, tee=log)
    print(resultado.solver.status)
    if (
        resultado.solver.status == SolverStatus.ok
        and resultado.solver.termination_condition == TerminationCondition.optimal
    ):
        print("Solução ótima encontrada!")
        print(f"Função objetivo: {pyo.value(modelo.obj)}")

        for atracao in atracoes:
            valor = round(pyo.value(modelo.visitas[atracao]), 2)
            if valor > 0:
                print(f"{atracao}: Visitado = {valor}")
    elif resultado.solver.status == SolverStatus.warning:
        print("Atenção: Problema pode não ter solução ótima")
    elif resultado.solver.termination_condition == TerminationCondition.infeasible:
        print("O modelo é inviável. Não há solução possível.")
    else:
        print(f"Solver status: {resultado.solver.status}")


tempo_maximo = 6
num_min_atracoes = 4
modelo = criar_modelo(
    atracoes,
    custo_entrada_atracoes,
    tempo_recomendado_atracoes,
    tempo_maximo,
    num_min_atracoes,
)
resolver_modelo(modelo)

"""Com essas funções, podemos criar estratégias para obter soluções que sejam sempre 0 ou 1. No entanto, às vezes, obtemos resultados que não estão exatamente em 0 ou 1, mas estão próximos, como o valor ótimo de 0.5. Nesses casos, é importante aplicar restrições adicionais para forçar as variáveis a se aproximarem de 0 ou 1, dependendo do objetivo do problema.

Por exemplo, a atração "Jardim de Luxemburgo" teve seu valor ótimo de 0.5, podemos melhorar o modelo ao aplicar as seguintes restrições:

1. Restrição para Forçar a Variável a ser Menor ou Igual a 0:
   - Podemos adicionar uma restrição que diz que a variável "Jardim de Luxemburgo" deve ser menor ou igual a 0. Isso significa que a atração "Jardim de Luxemburgo" não pode ser escolhida, ou seja, deve ser 0 ou próxima de 0.

2. Restrição para Forçar a Variável a ser Maior ou Igual a 1:
   - Por outro lado, podemos reotimizar o modelo com uma nova restrição que diz que a variável "Jardim de Luxemburgo" deve ser maior ou igual a 1. Isso significa que a atração "Jardim de Luxemburgo" deve ser escolhida com certeza, ou seja, deve ser 1 ou próxima de 1.

Essas abordagens permitem que ajustemos o modelo de otimização para se adequar melhor às nossas necessidades, forçando as variáveis a se aproximarem de 0 ou 1, dependendo do contexto do problema.

```
{"Jardim de Luxemburgo": {'valor': 0, 'sinal':'<='}}
```
"""


def adicionar_restricoes(modelo, condicoes):
    for ponto, dic in condicoes.items():
        valor = dic["valor"]
        sinal = dic["sinal"]
        if sinal == "<=":
            modelo.add_component(
                f"restr_{ponto}", pyo.Constraint(expr=modelo.visitas[ponto] <= valor)
            )
        elif sinal == ">=":
            modelo.add_component(
                f"restr_{ponto}", pyo.Constraint(expr=modelo.visitas[ponto] >= valor)
            )
        else:
            raise ValueError('Sinal inválido. Use "<=" ou ">="')


tempo_maximo = 6
num_min_atracoes = 4
condicoes = {"Jardim de Luxemburgo": {"valor": 0, "sinal": "<="}}
modelo = criar_modelo(
    atracoes,
    custo_entrada_atracoes,
    tempo_recomendado_atracoes,
    tempo_maximo,
    num_min_atracoes,
)
adicionar_restricoes(modelo, condicoes)
resolver_modelo(modelo)

"""## Iniciando a Busca por Soluções Inteiras"""

modelo = criar_modelo(
    atracoes,
    custo_entrada_atracoes,
    tempo_recomendado_atracoes,
    tempo_maximo,
    num_min_atracoes,
)
condicoes = {
    "Jardim de Luxemburgo": {"valor": 0, "sinal": "<="},
    "Place de la Concorde": {"valor": 0, "sinal": "<="},
}
adicionar_restricoes(modelo, condicoes)
resolver_modelo(modelo)

modelo = criar_modelo(
    atracoes,
    custo_entrada_atracoes,
    tempo_recomendado_atracoes,
    tempo_maximo,
    num_min_atracoes,
)
condicoes = {
    "Jardim de Luxemburgo": {"valor": 0, "sinal": "<="},
    "Place de la Concorde": {"valor": 1, "sinal": ">="},
}
adicionar_restricoes(modelo, condicoes)
resolver_modelo(modelo)

modelo = criar_modelo(
    atracoes,
    custo_entrada_atracoes,
    tempo_recomendado_atracoes,
    tempo_maximo,
    num_min_atracoes,
)
condicoes = {"Jardim de Luxemburgo": {"valor": 1, "sinal": ">="}}
adicionar_restricoes(modelo, condicoes)
resolver_modelo(modelo)

"""No nosso processo de otimização, estamos seguindo uma abordagem iterativa na qual adicionamos restrições ao nosso modelo de programação linear com o objetivo de determinar em que ponto todas as variáveis do modelo assumem valores inteiros. É importante destacar que, nesse processo, começamos por ramificar em uma variável específica que inicialmente possuía um valor de 0,5 (ou seja, uma fração). No entanto, poderíamos ter escolhido outra variável para iniciar o processo de ramificação.

A ideia central é identificar quais restrições podem ser adicionadas ao modelo para forçar a solução a se tornar inteira.

Essa abordagem de busca que utilizamos é conhecida como 'branch and bound' (ramificação e limite). Basicamente, ela envolve a construção de uma árvore de possibilidades, na qual adicionamos restrições a cada nível da árvore até que obtenhamos uma solução inteira. Em seguida, comparamos essa solução com as soluções previamente buscadas.

A pergunta que surge é: será que precisamos realizar esse processo manualmente?

## Variáveis Binárias
"""


def criar_modelo_inteiro(
    atracoes,
    custo_entrada_atracoes,
    tempo_recomendado_atracoes,
    tempo_maximo,
    num_min_atracoes,
):
    modelo = pyo.ConcreteModel()

    modelo.pontos_turisticos = pyo.Set(initialize=atracoes)

    modelo.tempo_maximo = pyo.Param(initialize=tempo_maximo)
    modelo.num_min_atracoes = pyo.Param(initialize=num_min_atracoes)
    modelo.custo_entrada = pyo.Param(
        modelo.pontos_turisticos, initialize=custo_entrada_atracoes
    )
    modelo.tempo_recomendado = pyo.Param(
        modelo.pontos_turisticos, initialize=tempo_recomendado_atracoes
    )

    modelo.visitas = pyo.Var(atracoes, domain=pyo.Binary)

    modelo.obj = pyo.Objective(
        expr=sum(
            modelo.custo_entrada[ponto] * modelo.visitas[ponto] for ponto in atracoes
        ),
        sense=pyo.minimize,
    )

    modelo.restr_num_min_visitas = pyo.Constraint(
        expr=sum(modelo.visitas[ponto] for ponto in atracoes) >= modelo.num_min_atracoes
    )

    modelo.restr_tempo = pyo.Constraint(
        expr=sum(
            modelo.tempo_recomendado[ponto] * modelo.visitas[ponto]
            for ponto in atracoes
        )
        <= modelo.tempo_maximo
    )

    return modelo


tempo_maximo = 6
num_min_atracoes = 4
modelo = criar_modelo_inteiro(
    atracoes,
    custo_entrada_atracoes,
    tempo_recomendado_atracoes,
    tempo_maximo,
    num_min_atracoes,
)
resolver_modelo(modelo, log=True)




def criar_modelo_inteiro(
    atracoes,
    custo_entrada_atracoes,
    tempo_recomendado_atracoes,
    tempo_maximo,
    num_min_atracoes,
):
    modelo = pyo.ConcreteModel()

    modelo.pontos_turisticos = pyo.Set(initialize=atracoes)

    modelo.tempo_maximo = pyo.Param(initialize=tempo_maximo)
    modelo.num_min_atracoes = pyo.Param(initialize=num_min_atracoes)
    modelo.custo_entrada = pyo.Param(
        modelo.pontos_turisticos, initialize=custo_entrada_atracoes
    )
    modelo.tempo_recomendado = pyo.Param(
        modelo.pontos_turisticos, initialize=tempo_recomendado_atracoes
    )

    modelo.visitas = pyo.Var(atracoes, domain=pyo.Binary)

    modelo.obj = pyo.Objective(
        expr=sum(
            modelo.custo_entrada[ponto] * modelo.visitas[ponto] for ponto in atracoes
        ),
        sense=pyo.minimize,
    )

    modelo.restr_num_min_visitas = pyo.Constraint(
        expr=sum(modelo.visitas[ponto] for ponto in atracoes) >= modelo.num_min_atracoes
    )

    modelo.restr_tempo = pyo.Constraint(
        expr=sum(
            modelo.tempo_recomendado[ponto] * modelo.visitas[ponto]
            for ponto in atracoes
        )
        <= modelo.tempo_maximo
    )

    modelo.restr_E = pyo.Constraint(
        expr=modelo.visitas["Torre Eiffel"] + modelo.visitas["Jardim de Luxemburgo"]
        == 2
    )

    return modelo


tempo_maximo = 8
num_min_atracoes = 3
modelo = criar_modelo_inteiro(
    atracoes,
    custo_entrada_atracoes,
    tempo_recomendado_atracoes,
    tempo_maximo,
    num_min_atracoes,
)
resolver_modelo(modelo, log=False)



def criar_modelo_inteiro(
    atracoes,
    custo_entrada_atracoes,
    tempo_recomendado_atracoes,
    tempo_maximo,
    num_min_atracoes,
):
    modelo = pyo.ConcreteModel()

    modelo.pontos_turisticos = pyo.Set(initialize=atracoes)

    modelo.tempo_maximo = pyo.Param(initialize=tempo_maximo)
    modelo.num_min_atracoes = pyo.Param(initialize=num_min_atracoes)
    modelo.custo_entrada = pyo.Param(
        modelo.pontos_turisticos, initialize=custo_entrada_atracoes
    )
    modelo.tempo_recomendado = pyo.Param(
        modelo.pontos_turisticos, initialize=tempo_recomendado_atracoes
    )

    modelo.visitas = pyo.Var(atracoes, domain=pyo.Binary)

    modelo.obj = pyo.Objective(
        expr=sum(
            modelo.custo_entrada[ponto] * modelo.visitas[ponto] for ponto in atracoes
        ),
        sense=pyo.minimize,
    )

    modelo.restr_num_min_visitas = pyo.Constraint(
        expr=sum(modelo.visitas[ponto] for ponto in atracoes) >= modelo.num_min_atracoes
    )

    modelo.restr_tempo = pyo.Constraint(
        expr=sum(
            modelo.tempo_recomendado[ponto] * modelo.visitas[ponto]
            for ponto in atracoes
        )
        <= modelo.tempo_maximo
    )

    modelo.restr_OU = pyo.Constraint(
        expr=modelo.visitas["Parc des Princes"] + modelo.visitas["Stade de France"] <= 1
    )

    return modelo


tempo_maximo = 8
num_min_atracoes = 3
modelo = criar_modelo_inteiro(
    atracoes,
    custo_entrada_atracoes,
    tempo_recomendado_atracoes,
    tempo_maximo,
    num_min_atracoes,
)
resolver_modelo(modelo, log=False)

tempo_maximo = 8
num_min_atracoes = 3
modelo = criar_modelo_inteiro(
    atracoes,
    custo_entrada_atracoes,
    tempo_recomendado_atracoes,
    tempo_maximo,
    num_min_atracoes,
)
condicoes = {"Parc des Princes": {"valor": 1, "sinal": ">="}}
adicionar_restricoes(modelo, condicoes)
resolver_modelo(modelo, log=False)

tempo_maximo = 8
num_min_atracoes = 3
modelo = criar_modelo_inteiro(
    atracoes,
    custo_entrada_atracoes,
    tempo_recomendado_atracoes,
    tempo_maximo,
    num_min_atracoes,
)
condicoes = {
    "Parc des Princes": {"valor": 1, "sinal": ">="},
    "Stade de France": {"valor": 1, "sinal": ">="},
}
adicionar_restricoes(modelo, condicoes)
resolver_modelo(modelo, log=False)



def criar_modelo_inteiro(
    atracoes,
    custo_entrada_atracoes,
    tempo_recomendado_atracoes,
    tempo_maximo,
    num_min_atracoes,
):
    modelo = pyo.ConcreteModel()

    modelo.pontos_turisticos = pyo.Set(initialize=atracoes)

    modelo.tempo_maximo = pyo.Param(initialize=tempo_maximo)
    modelo.num_min_atracoes = pyo.Param(initialize=num_min_atracoes)
    modelo.custo_entrada = pyo.Param(
        modelo.pontos_turisticos, initialize=custo_entrada_atracoes
    )
    modelo.tempo_recomendado = pyo.Param(
        modelo.pontos_turisticos, initialize=tempo_recomendado_atracoes
    )

    modelo.visitas = pyo.Var(atracoes, domain=pyo.Binary)

    modelo.obj = pyo.Objective(
        expr=sum(
            modelo.custo_entrada[ponto] * modelo.visitas[ponto] for ponto in atracoes
        ),
        sense=pyo.minimize,
    )

    modelo.restr_num_min_visitas = pyo.Constraint(
        expr=sum(modelo.visitas[ponto] for ponto in atracoes) >= modelo.num_min_atracoes
    )

    modelo.restr_tempo = pyo.Constraint(
        expr=sum(
            modelo.tempo_recomendado[ponto] * modelo.visitas[ponto]
            for ponto in atracoes
        )
        <= modelo.tempo_maximo
    )

    modelo.restr_SE_ENTAO = pyo.Constraint(
        expr=modelo.visitas["Parc des Princes"]
        <= modelo.visitas["Jardim de Luxemburgo"]
    )

    return modelo


tempo_maximo = 8
num_min_atracoes = 3
modelo = criar_modelo_inteiro(
    atracoes,
    custo_entrada_atracoes,
    tempo_recomendado_atracoes,
    tempo_maximo,
    num_min_atracoes,
)
resolver_modelo(modelo, log=False)

tempo_maximo = 8
num_min_atracoes = 3
modelo = criar_modelo_inteiro(
    atracoes,
    custo_entrada_atracoes,
    tempo_recomendado_atracoes,
    tempo_maximo,
    num_min_atracoes,
)
condicoes = {"Parc des Princes": {"valor": 1, "sinal": ">="}}
adicionar_restricoes(modelo, condicoes)
resolver_modelo(modelo, log=False)



def criar_modelo_inteiro(
    atracoes,
    custo_entrada_atracoes,
    tempo_recomendado_atracoes,
    tempo_maximo,
    num_min_atracoes,
):
    modelo = pyo.ConcreteModel()

    modelo.pontos_turisticos = pyo.Set(initialize=atracoes)

    modelo.tempo_maximo = pyo.Param(initialize=tempo_maximo)
    modelo.num_min_atracoes = pyo.Param(initialize=num_min_atracoes)
    modelo.custo_entrada = pyo.Param(
        modelo.pontos_turisticos, initialize=custo_entrada_atracoes
    )
    modelo.tempo_recomendado = pyo.Param(
        modelo.pontos_turisticos, initialize=tempo_recomendado_atracoes
    )

    modelo.visitas = pyo.Var(atracoes, domain=pyo.Binary)

    modelo.obj = pyo.Objective(
        expr=sum(
            modelo.custo_entrada[ponto] * modelo.visitas[ponto] for ponto in atracoes
        ),
        sense=pyo.minimize,
    )

    modelo.restr_num_min_visitas = pyo.Constraint(
        expr=sum(modelo.visitas[ponto] for ponto in atracoes) >= modelo.num_min_atracoes
    )

    modelo.restr_tempo = pyo.Constraint(
        expr=sum(
            modelo.tempo_recomendado[ponto] * modelo.visitas[ponto]
            for ponto in atracoes
        )
        <= modelo.tempo_maximo
    )

    return modelo


tempo_maximo = 8
num_min_atracoes = 8
modelo = criar_modelo_inteiro(
    atracoes,
    custo_entrada_atracoes,
    tempo_recomendado_atracoes,
    tempo_maximo,
    num_min_atracoes,
)
resolver_modelo(modelo, log=False)




def criar_modelo_inteiro(
    atracoes,
    custo_entrada_atracoes,
    tempo_recomendado_atracoes,
    tempo_maximo,
    num_min_atracoes,
    peso_restricao=1000,
):
    modelo = pyo.ConcreteModel()

    modelo.pontos_turisticos = pyo.Set(initialize=atracoes)

    modelo.tempo_maximo = pyo.Param(initialize=tempo_maximo)
    modelo.custo_entrada = pyo.Param(
        modelo.pontos_turisticos, initialize=custo_entrada_atracoes
    )
    modelo.tempo_recomendado = pyo.Param(
        modelo.pontos_turisticos, initialize=tempo_recomendado_atracoes
    )

    modelo.visitas = pyo.Var(atracoes, domain=pyo.Binary)

    modelo.obj = pyo.Objective(
        expr=sum(
            modelo.custo_entrada[ponto] * modelo.visitas[ponto] for ponto in atracoes
        )
        + peso_restricao
        * (num_min_atracoes - sum(modelo.visitas[ponto] for ponto in atracoes)),
        sense=pyo.minimize,
    )

    modelo.restr_tempo = pyo.Constraint(
        expr=sum(
            modelo.tempo_recomendado[ponto] * modelo.visitas[ponto]
            for ponto in atracoes
        )
        <= modelo.tempo_maximo
    )

    return modelo


tempo_maximo = 8
num_min_atracoes = 8
peso_restricao = 10
modelo = criar_modelo_inteiro(
    atracoes,
    custo_entrada_atracoes,
    tempo_recomendado_atracoes,
    tempo_maximo,
    num_min_atracoes,
    peso_restricao,
)
resolver_modelo(modelo, log=False)

def criar_modelo_inteiro_dias(
    atracoes,
    custo_entrada_atracoes,
    tempo_recomendado_atracoes,
    tempo_maximo_diario,
    orcamento_diario,
    dias,
):
    modelo = pyo.ConcreteModel()

    modelo.pontos_turisticos = pyo.Set(initialize=atracoes)
    modelo.dias = pyo.Set(initialize=dias)

    modelo.custo_entrada = pyo.Param(
        modelo.pontos_turisticos, initialize=custo_entrada_atracoes
    )
    modelo.tempo_recomendado = pyo.Param(
        modelo.pontos_turisticos, initialize=tempo_recomendado_atracoes
    )
    modelo.tempo_maximo_diario = pyo.Param(modelo.dias, initialize=tempo_maximo_diario)
    modelo.orcamento_diario = pyo.Param(modelo.dias, initialize=orcamento_diario)

    modelo.visitas = pyo.Var(modelo.pontos_turisticos, modelo.dias, domain=pyo.Binary)

    modelo.obj = pyo.Objective(
        expr=sum(modelo.visitas[ponto, dia] for ponto in atracoes for dia in dias),
        sense=pyo.maximize,
    )

    modelo.restr_tempo_diario = pyo.Constraint(
        modelo.dias,
        rule=lambda modelo, dia: (
            sum(
                modelo.tempo_recomendado[ponto] * modelo.visitas[ponto, dia]
                for ponto in atracoes
            )
            <= modelo.tempo_maximo_diario[dia]
        ),
    )

    modelo.restr_orcamento_diario = pyo.Constraint(
        modelo.dias,
        rule=lambda modelo, dia: (
            sum(
                modelo.custo_entrada[ponto] * modelo.visitas[ponto, dia]
                for ponto in atracoes
            )
            <= modelo.orcamento_diario[dia]
        ),
    )

    modelo.restr_visita_unica = pyo.Constraint(
        modelo.pontos_turisticos,
        rule=lambda modelo, ponto: (
            sum(modelo.visitas[ponto, dia] for dia in modelo.dias) <= 1
        ),
    )

    return modelo


def resolver_modelo_dias(modelo, log=False):
    solver = pyo.SolverFactory("glpk")
    resultado = solver.solve(modelo, tee=log)
    print(resultado.solver.status)
    if (
        resultado.solver.status == SolverStatus.ok
        and resultado.solver.termination_condition == TerminationCondition.optimal
    ):
        print("Solução ótima encontrada!")
        print(f"Função objetivo: {round(pyo.value(modelo.obj), 2)}")
        for dia in modelo.dias:
            for atracao in modelo.pontos_turisticos:
                valor_variavel_decisao = round(
                    pyo.value(modelo.visitas[atracao, dia]), 2
                )
                if valor_variavel_decisao > 0:
                    print(f"No dia {dia} visitar {atracao}")
    elif resultado.solver.status == SolverStatus.warning:
        print("Atenção: Problema pode não ter solução ótima")
    elif resultado.solver.termination_condition == TerminationCondition.infeasible:
        print("O modelo é inviável. Não há solução possível.")
    else:
        print(f"Solver status: {resultado.solver.status}")


tempo_maximo_diario = {1: 6, 2: 6, 3: 6, 4: 6}
orcamento_diario = {1: 100, 2: 100, 3: 100, 4: 100}
dias = [1, 2, 3, 4]
modelo = criar_modelo_inteiro_dias(
    atracoes,
    custo_entrada_atracoes,
    tempo_recomendado_atracoes,
    tempo_maximo_diario,
    orcamento_diario,
    dias,
)
resolver_modelo_dias(modelo, log=False)


def criar_modelo_inteiro_dias(
    atracoes,
    custo_entrada_atracoes,
    tempo_recomendado_atracoes,
    tempo_maximo_diario,
    orcamento_diario,
    dias,
):
    modelo = pyo.ConcreteModel()

    modelo.pontos_turisticos = pyo.Set(initialize=atracoes)
    modelo.dias = pyo.Set(initialize=dias)

    modelo.custo_entrada = pyo.Param(
        modelo.pontos_turisticos, initialize=custo_entrada_atracoes
    )
    modelo.tempo_recomendado = pyo.Param(
        modelo.pontos_turisticos, initialize=tempo_recomendado_atracoes
    )
    modelo.tempo_maximo_diario = pyo.Param(modelo.dias, initialize=tempo_maximo_diario)
    modelo.orcamento_diario = pyo.Param(modelo.dias, initialize=orcamento_diario)

    modelo.visitas = pyo.Var(modelo.pontos_turisticos, modelo.dias, domain=pyo.Binary)
    modelo.menor_qtd_atracoes = pyo.Var(within=pyo.NonNegativeIntegers)

    modelo.obj = pyo.Objective(expr=modelo.menor_qtd_atracoes, sense=pyo.maximize)

    modelo.restr_tempo_diario = pyo.Constraint(
        modelo.dias,
        rule=lambda modelo, dia: (
            sum(
                modelo.tempo_recomendado[ponto] * modelo.visitas[ponto, dia]
                for ponto in atracoes
            )
            <= modelo.tempo_maximo_diario[dia]
        ),
    )

    modelo.restr_orcamento_diario = pyo.Constraint(
        modelo.dias,
        rule=lambda modelo, dia: (
            sum(
                modelo.custo_entrada[ponto] * modelo.visitas[ponto, dia]
                for ponto in atracoes
            )
            <= modelo.orcamento_diario[dia]
        ),
    )

    modelo.restr_visita_unica = pyo.Constraint(
        modelo.pontos_turisticos,
        rule=lambda modelo, ponto: (
            sum(modelo.visitas[ponto, dia] for dia in modelo.dias) <= 1
        ),
    )

    modelo.restr_menor_qtd_atracoes = pyo.Constraint(
        modelo.dias,
        rule=lambda modelo, dia: (
            sum(modelo.visitas[ponto, dia] for ponto in atracoes)
            >= modelo.menor_qtd_atracoes
        ),
    )

    return modelo


modelo = criar_modelo_inteiro_dias(
    atracoes,
    custo_entrada_atracoes,
    tempo_recomendado_atracoes,
    tempo_maximo_diario,
    orcamento_diario,
    dias,
)
resolver_modelo_dias(modelo, log=False)



import random


def gerar_parametros(num_atracoes, num_dias):
    atracoes = range(1, num_atracoes)
    dias = range(1, num_dias + 1)

    custo_entrada_atracoes = {
        ponto_turistico: random.randint(10, 100) for ponto_turistico in atracoes
    }
    tempo_recomendado_atracoes = {
        ponto_turistico: random.randint(1, 6) for ponto_turistico in atracoes
    }

    tempo_maximo_diario = {dia: random.randint(8, 10) for dia in dias}
    orcamento_diario = {dia: random.randint(450, 500) for dia in dias}

    return (
        atracoes,
        dias,
        custo_entrada_atracoes,
        tempo_recomendado_atracoes,
        tempo_maximo_diario,
        orcamento_diario,
    )


num_atracoes = 10000
num_dias = 60
(
    atracoes,
    dias,
    custo_entrada_atracoes,
    tempo_recomendado_atracoes,
    tempo_maximo_diario,
    orcamento_diario,
) = gerar_parametros(num_atracoes=num_atracoes, num_dias=num_dias)


modelo = criar_modelo_inteiro_dias(
    atracoes,
    custo_entrada_atracoes,
    tempo_recomendado_atracoes,
    tempo_maximo_diario,
    orcamento_diario,
    dias,
)
resolver_modelo_dias(modelo)

"""## Otimização com Dados Extensos"""


def resolver_modelo_dias(modelo, gap=None, tempo_limite=None, log=False):
    solver = pyo.SolverFactory("glpk")

    if gap is not None:
        solver.options["mipgap"] = gap
    if tempo_limite is not None:
        solver.options["tmlim"] = tempo_limite

    resultado = solver.solve(modelo, tee=log)
    print(resultado.solver.status)
    if (
        resultado.solver.status == SolverStatus.ok
        and resultado.solver.termination_condition == TerminationCondition.optimal
    ):
        print("Solução ótima encontrada!")
        print(f"Função objetivo: {round(pyo.value(modelo.obj), 2)}")
        for dia in modelo.dias:
            for atracao in modelo.pontos_turisticos:
                valor_variavel_decisao = round(
                    pyo.value(modelo.visitas[atracao, dia]), 2
                )
                if valor_variavel_decisao > 0:
                    print(f"No dia {dia} visitar {atracao}")
    elif resultado.solver.status == SolverStatus.warning:
        print("Atenção: Problema pode não ter solução ótima")
    elif resultado.solver.termination_condition == TerminationCondition.infeasible:
        print("O modelo é inviável. Não há solução possível.")
    else:
        print(f"Solver status: {resultado.solver.status}")


modelo = criar_modelo_inteiro_dias(
    atracoes,
    custo_entrada_atracoes,
    tempo_recomendado_atracoes,
    tempo_maximo_diario,
    orcamento_diario,
    dias,
)
resolver_modelo_dias(modelo, gap=0.01, tempo_limite=120)
