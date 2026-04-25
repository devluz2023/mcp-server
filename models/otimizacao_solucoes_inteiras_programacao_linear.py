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

mapa = folium.Map(location = [48.856614, 2.352222], zoom_start = 12)

for atracao in atracoes:
    popup = folium.Popup(f'''<b>{atracao}</b><br>
    Tempo recomendado: {tempo_recomendado_atracoes[atracao]} hora(s)<br>
    Valor da entrada: € {custo_entrada_atracoes[atracao]}
    ''',
    max_width = 200,
    sticky = True)
    folium.Marker(localizacao_atracoes[atracao], popup = popup).add_to(mapa)

mapa

"""## Modelagem em Programação Linear para Solução

**Conjuntos:**

- $pontos\_turisticos$: Conjunto de pontos turísticos que vão indexar as variáveis de decisão, restrições e função objetivo.

**Parâmetros:**

- $tempo\_maximo$: O tempo máximo disponível para a visita (em horas).
- $num\_min\_atracoes$: O número mínimo de atrações que você deseja visitar (um valor ajustável).

- $tempo\_recomendado[ponto]$: O tempo recomendado da visita de cada ponto turístico (em horas).
- $custo\_entrada[ponto]$: O custo de entrada da visita de cada ponto turístico.

**Variáveis de Decisão:**

- $visitas[ponto]$: Variável binária que indica se você visitará a atração $ponto$ (0 para não visitar, 1 para visitar).

**Função Objetivo:**

A função objetivo tem como objetivo minimizar o custo total da viagem e é definida da seguinte forma:

$
\mbox{min} \displaystyle \sum_{ponto \in atracoes} custo\_entrada\_atracoes[ponto] \cdot visitas[ponto]
$

Essa função considera o custo de entrada em cada atração multiplicado pela variável binária que indica se a atração é visitada ou não.

**Restrições:**

1. **Número Mínimo de Visitas:**

$
\displaystyle \sum_{ponto \in atracoes} visitas[ponto] \geq num\_min\_atracoes
$

Essa restrição garante que você deve visitar um número mínimo de atrações especificado.

2. **Restrição de Tempo:**

$
\displaystyle \sum_{ponto \in atracoes} tempo\_recomendado\_atracoes[ponto] \cdot visitas[ponto] \leq tempo\_maximo
$

Essa restrição limita o tempo total gasto nas visitas, incluindo o tempo recomendado para cada atração multiplicado pela variável binária que indica se a atração é visitada ou não.

## Implementação e Resolução com Programação Linear

Resolvido a definição do problema, podemos partir para a resolução. Para isso, utilizaremos um modelo de programação linear. Esse tipo de modelo é adequado para problemas em que temos que tomar decisões, considerando restrições.

No nosso caso, temos que decidir quais atrações visitar, considerando o orçamento e o tempo disponíveis.O modelo de programação linear nos permitirá encontrar a solução ótima para esse problema.

Para implementar o modelo, utilizaremos a biblioteca Pyomo com o solver GLPK. Essa biblioteca é uma ferramenta poderosa para a resolução de problemas de programação linear. Com ela, podemos escrever o modelo de forma clara e concisa, e resolver o problema de forma eficiente.

Inicialmente, precisamos instalar a bibloteca Pyomo e o solver GLPK.
"""


"""Com isso instalado, podemos implementar nosso modelo."""

import pyomo.environ as pyo

tempo_maximo = 6
num_min_atracoes = 4

modelo = pyo.ConcreteModel()

modelo.pontos_turisticos = pyo.Set(initialize = atracoes)

modelo.tempo_maximo = pyo.Param(initialize = tempo_maximo)
modelo.num_min_atracoes = pyo.Param(initialize = num_min_atracoes)
modelo.custo_entrada = pyo.Param(modelo.pontos_turisticos, initialize = custo_entrada_atracoes)
modelo.tempo_recomendado = pyo.Param(modelo.pontos_turisticos, initialize = tempo_recomendado_atracoes)

modelo.visitas = pyo.Var(atracoes, domain = pyo.NonNegativeReals, bounds = (0, 1))

modelo.obj = pyo.Objective(
    expr = sum(modelo.custo_entrada[ponto]*modelo.visitas[ponto] for ponto in atracoes),
    sense = pyo.minimize
)

modelo.restr_num_min_visitas = pyo.Constraint(
    expr = sum(modelo.visitas[ponto] for ponto in atracoes) >= modelo.num_min_atracoes
)

modelo.restr_tempo = pyo.Constraint(
    expr = sum(modelo.tempo_recomendado[ponto]*modelo.visitas[ponto] for ponto in atracoes) <= modelo.tempo_maximo
)

solver = pyo.SolverFactory('glpk')
resultado = solver.solve(modelo, tee = True)

"""Com o modelo resolvido, podemos imprimir na tela a resolução."""

print(f'Função objetivo: {pyo.value(modelo.obj)}')

for atracao in atracoes:
    valor = round(pyo.value(modelo.visitas[atracao]), 2)
    if valor>0:
        print(f'{atracao}: Visitado = {valor}')

"""## Preparação para busca por soluções inteiras

Antes de buscar estratégias para o modelo sempre retornar 0 ou 1, é necessário criar funções para facilitar os testes. Essas funções permitirão que executemos o modelo rapidamente e analisemos os resultados de forma mais eficiente.

 A função `criar_modelo()` cria um novo modelo de programação linear com as variáveis de decisão, a função objetivo e as restrições definidas anteriormente. A função `resolver_modelo()` resolve o modelo e imprime na tela a solução
"""

def criar_modelo(atracoes, custo_entrada_atracoes, tempo_recomendado_atracoes, tempo_maximo, num_min_atracoes):

    modelo = pyo.ConcreteModel()

    modelo.pontos_turisticos = pyo.Set(initialize = atracoes)

    modelo.tempo_maximo = pyo.Param(initialize = tempo_maximo)
    modelo.num_min_atracoes = pyo.Param(initialize = num_min_atracoes)
    modelo.custo_entrada = pyo.Param(modelo.pontos_turisticos, initialize = custo_entrada_atracoes)
    modelo.tempo_recomendado = pyo.Param(modelo.pontos_turisticos, initialize = tempo_recomendado_atracoes)

    modelo.visitas = pyo.Var(atracoes, domain = pyo.NonNegativeReals, bounds = (0, 1))

    modelo.obj = pyo.Objective(
        expr = sum(modelo.custo_entrada[ponto]*modelo.visitas[ponto] for ponto in atracoes),
        sense = pyo.minimize
    )

    modelo.restr_num_min_visitas = pyo.Constraint(
        expr = sum(modelo.visitas[ponto] for ponto in atracoes) >= modelo.num_min_atracoes
    )

    modelo.restr_tempo = pyo.Constraint(
        expr = sum(modelo.tempo_recomendado[ponto]*modelo.visitas[ponto] for ponto in atracoes) <= modelo.tempo_maximo
    )

    return modelo

from pyomo.opt import SolverStatus, TerminationCondition

def resolver_modelo(modelo, log = False):
    solver = pyo.SolverFactory('glpk')
    resultado = solver.solve(modelo, tee = log)
    print(resultado.solver.status)
    if resultado.solver.status == SolverStatus.ok and resultado.solver.termination_condition == TerminationCondition.optimal:
        print('Solução ótima encontrada!')
        print(f'Função objetivo: {pyo.value(modelo.obj)}')

        for atracao in atracoes:
            valor = round(pyo.value(modelo.visitas[atracao]), 2)
            if valor>0:
                print(f'{atracao}: Visitado = {valor}')
    elif resultado.solver.status == SolverStatus.warning:
        print('Atenção: Problema pode não ter solução ótima')
    elif resultado.solver.termination_condition == TerminationCondition.infeasible:
        print('O modelo é inviável. Não há solução possível.')
    else:
        print(f'Solver status: {resultado.solver.status}')

tempo_maximo = 6
num_min_atracoes = 4
modelo = criar_modelo(atracoes, custo_entrada_atracoes, tempo_recomendado_atracoes, tempo_maximo, num_min_atracoes)
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
        valor = dic['valor']
        sinal = dic['sinal']
        if sinal == '<=':
            modelo.add_component(f'restr_{ponto}', pyo.Constraint(expr = modelo.visitas[ponto]<= valor))
        elif sinal == '>=':
            modelo.add_component(f'restr_{ponto}', pyo.Constraint(expr = modelo.visitas[ponto]>= valor))
        else:
            raise ValueError('Sinal inválido. Use "<=" ou ">="')

tempo_maximo = 6
num_min_atracoes = 4
condicoes = {"Jardim de Luxemburgo": {'valor': 0, 'sinal':'<='}}
modelo = criar_modelo(atracoes, custo_entrada_atracoes, tempo_recomendado_atracoes, tempo_maximo, num_min_atracoes)
adicionar_restricoes(modelo, condicoes)
resolver_modelo(modelo)

"""## Iniciando a Busca por Soluções Inteiras"""

modelo = criar_modelo(atracoes, custo_entrada_atracoes, tempo_recomendado_atracoes, tempo_maximo, num_min_atracoes)
condicoes = {"Jardim de Luxemburgo": {'valor': 0, 'sinal':'<='},
             "Place de la Concorde": {'valor': 0, 'sinal':'<='}}
adicionar_restricoes(modelo, condicoes)
resolver_modelo(modelo)

modelo = criar_modelo(atracoes, custo_entrada_atracoes, tempo_recomendado_atracoes, tempo_maximo, num_min_atracoes)
condicoes = {"Jardim de Luxemburgo": {'valor': 0, 'sinal':'<='},
             "Place de la Concorde": {'valor': 1, 'sinal':'>='}}
adicionar_restricoes(modelo, condicoes)
resolver_modelo(modelo)

modelo = criar_modelo(atracoes, custo_entrada_atracoes, tempo_recomendado_atracoes, tempo_maximo, num_min_atracoes)
condicoes = {"Jardim de Luxemburgo": {'valor': 1, 'sinal':'>='}}
adicionar_restricoes(modelo, condicoes)
resolver_modelo(modelo)

"""No nosso processo de otimização, estamos seguindo uma abordagem iterativa na qual adicionamos restrições ao nosso modelo de programação linear com o objetivo de determinar em que ponto todas as variáveis do modelo assumem valores inteiros. É importante destacar que, nesse processo, começamos por ramificar em uma variável específica que inicialmente possuía um valor de 0,5 (ou seja, uma fração). No entanto, poderíamos ter escolhido outra variável para iniciar o processo de ramificação.

A ideia central é identificar quais restrições podem ser adicionadas ao modelo para forçar a solução a se tornar inteira.

Essa abordagem de busca que utilizamos é conhecida como 'branch and bound' (ramificação e limite). Basicamente, ela envolve a construção de uma árvore de possibilidades, na qual adicionamos restrições a cada nível da árvore até que obtenhamos uma solução inteira. Em seguida, comparamos essa solução com as soluções previamente buscadas.

A pergunta que surge é: será que precisamos realizar esse processo manualmente?

## Variáveis Binárias
"""

def criar_modelo_inteiro(atracoes, custo_entrada_atracoes, tempo_recomendado_atracoes, tempo_maximo, num_min_atracoes):

    modelo = pyo.ConcreteModel()

    modelo.pontos_turisticos = pyo.Set(initialize = atracoes)

    modelo.tempo_maximo = pyo.Param(initialize = tempo_maximo)
    modelo.num_min_atracoes = pyo.Param(initialize = num_min_atracoes)
    modelo.custo_entrada = pyo.Param(modelo.pontos_turisticos, initialize = custo_entrada_atracoes)
    modelo.tempo_recomendado = pyo.Param(modelo.pontos_turisticos, initialize = tempo_recomendado_atracoes)

    modelo.visitas = pyo.Var(atracoes, domain = pyo.Binary)

    modelo.obj = pyo.Objective(
        expr = sum(modelo.custo_entrada[ponto]*modelo.visitas[ponto] for ponto in atracoes),
        sense = pyo.minimize
    )

    modelo.restr_num_min_visitas = pyo.Constraint(
        expr = sum(modelo.visitas[ponto] for ponto in atracoes) >= modelo.num_min_atracoes
    )

    modelo.restr_tempo = pyo.Constraint(
        expr = sum(modelo.tempo_recomendado[ponto]*modelo.visitas[ponto] for ponto in atracoes) <= modelo.tempo_maximo
    )

    return modelo

tempo_maximo = 6
num_min_atracoes = 4
modelo = criar_modelo_inteiro(atracoes, custo_entrada_atracoes, tempo_recomendado_atracoes, tempo_maximo, num_min_atracoes)
resolver_modelo(modelo, log = True)

"""# Refinando as Restrições em Modelos de Programação Linear

Com isso em mente, podemos explorar tipos de restrições extremamente úteis para problemas de tomada de decisão. Em particular, as variáveis inteiras do tipo binária desempenham um papel fundamental na criação de restrições lógicas como "E" (AND), "OU" (OR) e "SE Então" (IF-THEN). Essas restrições são essenciais para modelar e resolver problemas complexos com múltiplas condições e escolhas a serem feitas de forma lógica e eficaz.

## Incorporando Restrições do Tipo E

A restrição lógica "E" (AND) em programação inteira é utilizada para modelar situações em que duas ou mais variáveis binárias devem assumir o valor 1 simultaneamente para que a condição seja satisfeita. Em outras palavras, todas as condições devem ser verdadeiras para que a restrição seja válida.

No exemplo:

```python
modelo.visitas["Torre Eiffel"] + modelo.visitas["Jardim de Luxemburgo"] == 2
```

Nós temos duas variáveis binárias, uma representando a visita à "Torre Eiffel" e outra representando a visita ao "Jardim de Luxemburgo". Essas variáveis podem assumir apenas dois valores: 0 (não visitado) ou 1 (visitado).

A restrição `modelo.visitas["Torre Eiffel"] + modelo.visitas["Jardim de Luxemburgo"] == 2` estabelece que ambas as atrações, "Torre Eiffel" e "Jardim de Luxemburgo", devem ser visitadas ao mesmo tempo. A soma das variáveis binárias que representam essas atrações deve ser igual a 2 para que a restrição seja satisfeita.

A lógica por trás disso é a seguinte:

- Se `modelo.visitas["Torre Eiffel"]` e `modelo.visitas["Jardim de Luxemburgo"]` forem ambas iguais a 1, significa que ambas as atrações foram visitadas (1 + 1 = 2), atendendo à condição "E" (ambas).

- Se qualquer uma das variáveis for igual a 0, isso significa que pelo menos uma das atrações não foi visitada, o que torna a soma igual a 1 ou menos, não atendendo à condição "E".

Portanto, a restrição garante que as duas atrações sejam visitadas simultaneamente, representando uma lógica de "E" (AND) na programação inteira.
"""

def criar_modelo_inteiro(atracoes, custo_entrada_atracoes, tempo_recomendado_atracoes, tempo_maximo, num_min_atracoes):

    modelo = pyo.ConcreteModel()

    modelo.pontos_turisticos = pyo.Set(initialize = atracoes)

    modelo.tempo_maximo = pyo.Param(initialize = tempo_maximo)
    modelo.num_min_atracoes = pyo.Param(initialize = num_min_atracoes)
    modelo.custo_entrada = pyo.Param(modelo.pontos_turisticos, initialize = custo_entrada_atracoes)
    modelo.tempo_recomendado = pyo.Param(modelo.pontos_turisticos, initialize = tempo_recomendado_atracoes)

    modelo.visitas = pyo.Var(atracoes, domain = pyo.Binary)

    modelo.obj = pyo.Objective(
        expr = sum(modelo.custo_entrada[ponto]*modelo.visitas[ponto] for ponto in atracoes),
        sense = pyo.minimize
    )

    modelo.restr_num_min_visitas = pyo.Constraint(
        expr = sum(modelo.visitas[ponto] for ponto in atracoes) >= modelo.num_min_atracoes
    )

    modelo.restr_tempo = pyo.Constraint(
        expr = sum(modelo.tempo_recomendado[ponto]*modelo.visitas[ponto] for ponto in atracoes) <= modelo.tempo_maximo
    )

    modelo.restr_E = pyo.Constraint(
        expr = modelo.visitas['Torre Eiffel'] + modelo.visitas['Jardim de Luxemburgo'] == 2
    )

    return modelo

tempo_maximo = 8
num_min_atracoes = 3
modelo = criar_modelo_inteiro(atracoes, custo_entrada_atracoes, tempo_recomendado_atracoes, tempo_maximo, num_min_atracoes)
resolver_modelo(modelo, log = False)

"""## Incorporando Restrições do Tipo OU exclusivo

A restrição condicional "OU exclusivo" em programação inteira é utilizada para modelar situações em no máximo uma das várias variáveis binárias pode assumir o valor 1 para que a condição seja satisfeita.

No exemplo:

```python
modelo.visitas["Parc des Princes"] + modelo.visitas["Stade de France"] <= 1
```

Temos duas variáveis binárias, uma representando a visita ao "Parc des Princes" e outra representando a visita ao "Stade de France". Ambas as variáveis podem assumir apenas dois valores: 0 (não visitado) ou 1 (visitado).

A restrição `modelo.visitas["Parc des Princes"] + modelo.visitas["Stade de France"] <= 1` estabelece que no máximo uma das atrações, "Parc des Princes" ou "Stade de France", pode ser visitada. A soma das variáveis binárias que representam essas atrações deve ser menor ou igual a 1 para que a restrição seja satisfeita.

A lógica por trás disso é a seguinte:

- Se `modelo.visitas["Parc des Princes"]` e `modelo.visitas["Stade de France"]` simultaneamente forem iguais a 1, significa que a soma das variáveis de decisão será igual a 2, indicando que as duas não podem ser visitadas na mesma viagem.
ls
- Se ambas as variáveis forem iguais a 0, isso significaria que nenhuma das atrações foi visitada, tornando a soma igual a 0, o que ainda atende à condição "OU exclusiva" (no máximo uma).

Portanto, a restrição garante que no máximo uma das duas atrações seja visitada, representando uma lógica de "OU exclusivo" na programação inteira.
"""

def criar_modelo_inteiro(atracoes, custo_entrada_atracoes, tempo_recomendado_atracoes, tempo_maximo, num_min_atracoes):

    modelo = pyo.ConcreteModel()

    modelo.pontos_turisticos = pyo.Set(initialize = atracoes)

    modelo.tempo_maximo = pyo.Param(initialize = tempo_maximo)
    modelo.num_min_atracoes = pyo.Param(initialize = num_min_atracoes)
    modelo.custo_entrada = pyo.Param(modelo.pontos_turisticos, initialize = custo_entrada_atracoes)
    modelo.tempo_recomendado = pyo.Param(modelo.pontos_turisticos, initialize = tempo_recomendado_atracoes)

    modelo.visitas = pyo.Var(atracoes, domain = pyo.Binary)

    modelo.obj = pyo.Objective(
        expr = sum(modelo.custo_entrada[ponto]*modelo.visitas[ponto] for ponto in atracoes),
        sense = pyo.minimize
    )

    modelo.restr_num_min_visitas = pyo.Constraint(
        expr = sum(modelo.visitas[ponto] for ponto in atracoes) >= modelo.num_min_atracoes
    )

    modelo.restr_tempo = pyo.Constraint(
        expr = sum(modelo.tempo_recomendado[ponto]*modelo.visitas[ponto] for ponto in atracoes) <= modelo.tempo_maximo
    )

    modelo.restr_OU = pyo.Constraint(
        expr = modelo.visitas['Parc des Princes'] + modelo.visitas['Stade de France'] <= 1
    )

    return modelo

tempo_maximo = 8
num_min_atracoes = 3
modelo = criar_modelo_inteiro(atracoes, custo_entrada_atracoes, tempo_recomendado_atracoes, tempo_maximo, num_min_atracoes)
resolver_modelo(modelo, log = False)

tempo_maximo = 8
num_min_atracoes = 3
modelo = criar_modelo_inteiro(atracoes, custo_entrada_atracoes, tempo_recomendado_atracoes, tempo_maximo, num_min_atracoes)
condicoes = {'Parc des Princes': {'valor': 1, 'sinal': '>='}}
adicionar_restricoes(modelo, condicoes)
resolver_modelo(modelo, log = False)

tempo_maximo = 8
num_min_atracoes = 3
modelo = criar_modelo_inteiro(atracoes, custo_entrada_atracoes, tempo_recomendado_atracoes, tempo_maximo, num_min_atracoes)
condicoes = {'Parc des Princes': {'valor': 1, 'sinal': '>='},
             'Stade de France': {'valor': 1, 'sinal': '>='}}
adicionar_restricoes(modelo, condicoes)
resolver_modelo(modelo, log = False)

"""## Incorporando Restrições do Tipo SE ENTAO

A restrição condicional "SE ENTÃO" em programação inteira é utilizada para modelar situações em que uma variável binária deve assumir o valor 1 se outra variável binária assumir o valor 1. Ou seja, se a primeira condição for verdadeira (a variável à esquerda for 1), então a segunda condição também deve ser verdadeira (a variável à direita deve ser 1).

No exemplo:

```python
modelo.visitas["Parc des Princes"] <= modelo.visitas["Jardim de Luxemburgo"]
```

Temos duas variáveis binárias, uma representando a visita ao "Parc des Princes" e outra representando a visita ao "Jardim de Luxemburgo". Ambas as variáveis podem assumir apenas dois valores: 0 (não visitado) ou 1 (visitado).

A restrição `modelo.visitas["Parc des Princes"] <= modelo.visitas["Jardim de Luxemburgo"]` estabelece que, se a variável `modelo.visitas["Parc des Princes"]` for igual a 1 (ou seja, se "Parc des Princes" for visitado), então a variável `modelo.visitas["Jardim de Luxemburgo"]` também deve ser igual a 1 (ou seja, "Jardim de Luxemburgo" deve ser visitado).

A lógica por trás disso é a seguinte:

- Se `modelo.visitas["Parc des Princes"]` for igual a 0 (não visitado), a restrição não impõe nenhuma restrição à variável `modelo.visitas["Jardim de Luxemburgo"]`. Pode ser 0 ou 1.

- No entanto, se `modelo.visitas["Parc des Princes"]` for igual a 1 (visitado), a restrição exige que `modelo.visitas["Jardim de Luxemburgo"]` também seja igual a 1, garantindo assim que, se "Parc des Princes" for visitado, "Jardim de Luxemburgo" também deve ser visitado.

Portanto, a restrição condicional "SE ENTÃO" na programação inteira modela uma lógica em que uma ação (visitar "Parc des Princes") implica necessariamente em outra ação (visitar "Jardim de Luxemburgo").
"""

def criar_modelo_inteiro(atracoes, custo_entrada_atracoes, tempo_recomendado_atracoes, tempo_maximo, num_min_atracoes):

    modelo = pyo.ConcreteModel()

    modelo.pontos_turisticos = pyo.Set(initialize = atracoes)

    modelo.tempo_maximo = pyo.Param(initialize = tempo_maximo)
    modelo.num_min_atracoes = pyo.Param(initialize = num_min_atracoes)
    modelo.custo_entrada = pyo.Param(modelo.pontos_turisticos, initialize = custo_entrada_atracoes)
    modelo.tempo_recomendado = pyo.Param(modelo.pontos_turisticos, initialize = tempo_recomendado_atracoes)

    modelo.visitas = pyo.Var(atracoes, domain = pyo.Binary)

    modelo.obj = pyo.Objective(
        expr = sum(modelo.custo_entrada[ponto]*modelo.visitas[ponto] for ponto in atracoes),
        sense = pyo.minimize
    )

    modelo.restr_num_min_visitas = pyo.Constraint(
        expr = sum(modelo.visitas[ponto] for ponto in atracoes) >= modelo.num_min_atracoes
    )

    modelo.restr_tempo = pyo.Constraint(
        expr = sum(modelo.tempo_recomendado[ponto]*modelo.visitas[ponto] for ponto in atracoes) <= modelo.tempo_maximo
    )

    modelo.restr_SE_ENTAO = pyo.Constraint(
        expr = modelo.visitas["Parc des Princes"] <= modelo.visitas["Jardim de Luxemburgo"]
    )

    return modelo

tempo_maximo = 8
num_min_atracoes = 3
modelo = criar_modelo_inteiro(atracoes, custo_entrada_atracoes, tempo_recomendado_atracoes, tempo_maximo, num_min_atracoes)
resolver_modelo(modelo, log = False)

tempo_maximo = 8
num_min_atracoes = 3
modelo = criar_modelo_inteiro(atracoes, custo_entrada_atracoes, tempo_recomendado_atracoes, tempo_maximo, num_min_atracoes)
condicoes = {'Parc des Princes': {'valor': 1, 'sinal': '>='}}
adicionar_restricoes(modelo, condicoes)
resolver_modelo(modelo, log = False)

"""# Explorando Variações no Modelo de Planejamento de Visitas Turísticas

## Estratégias com Soft Constraints para Acomodar Mais Atrações por Dia

Vamos abordar a situação atual do nosso modelo, onde temos uma restrição rígida que nos obriga a visitar no mínimo 4 atrações turísticas. Agora, imagine o que aconteceria se decidíssemos aumentar esse número para 8 atrações
"""

def criar_modelo_inteiro(atracoes, custo_entrada_atracoes, tempo_recomendado_atracoes, tempo_maximo, num_min_atracoes):

    modelo = pyo.ConcreteModel()

    modelo.pontos_turisticos = pyo.Set(initialize = atracoes)

    modelo.tempo_maximo = pyo.Param(initialize = tempo_maximo)
    modelo.num_min_atracoes = pyo.Param(initialize = num_min_atracoes)
    modelo.custo_entrada = pyo.Param(modelo.pontos_turisticos, initialize = custo_entrada_atracoes)
    modelo.tempo_recomendado = pyo.Param(modelo.pontos_turisticos, initialize = tempo_recomendado_atracoes)

    modelo.visitas = pyo.Var(atracoes, domain = pyo.Binary)

    modelo.obj = pyo.Objective(
        expr = sum(modelo.custo_entrada[ponto]*modelo.visitas[ponto] for ponto in atracoes),
        sense = pyo.minimize
    )

    modelo.restr_num_min_visitas = pyo.Constraint(
        expr = sum(modelo.visitas[ponto] for ponto in atracoes) >= modelo.num_min_atracoes
    )

    modelo.restr_tempo = pyo.Constraint(
        expr = sum(modelo.tempo_recomendado[ponto]*modelo.visitas[ponto] for ponto in atracoes) <= modelo.tempo_maximo
    )

    return modelo

tempo_maximo = 8
num_min_atracoes = 8
modelo = criar_modelo_inteiro(atracoes, custo_entrada_atracoes, tempo_recomendado_atracoes, tempo_maximo, num_min_atracoes)
resolver_modelo(modelo, log = False)

"""Quando fizemos essa mudança, nosso problema se tornou inviável. Em outras palavras, o modelo não conseguiu encontrar uma solução que atendesse à nova restrição de visitar no mínimo 8 atrações. Isso ocorreu porque a restrição anterior era considerada "hard", o que significa que o modelo era absolutamente obrigado a respeitá-la, e não havia margem para flexibilidade.

Agora, surge a pergunta: existe uma maneira mais flexível de modelar essa restrição? A resposta é sim, podemos usar o conceito de "restrições soft" (ou restritivas flexíveis). Aqui está como funciona:

As "restrições soft" permitem uma abordagem mais adaptável. Em vez de impor uma condição rígida que deve ser estritamente obedecida, atribuímos um peso a essa restrição e incorporamos esse peso na função objetivo do problema de otimização.

Nesse caso, em vez de simplesmente minimizar o número de atrações visitadas, podemos maximizar o número de atrações visitadas enquanto minimizamos o custo total das visitas (orçamento). Isso nos permite encontrar um equilíbrio entre visitar o máximo possível de atrações e controlar o custo da viagem.

"""

def criar_modelo_inteiro(atracoes, custo_entrada_atracoes, tempo_recomendado_atracoes, tempo_maximo, num_min_atracoes, peso_restricao = 1000):

    modelo = pyo.ConcreteModel()

    modelo.pontos_turisticos = pyo.Set(initialize = atracoes)

    modelo.tempo_maximo = pyo.Param(initialize = tempo_maximo)
    modelo.custo_entrada = pyo.Param(modelo.pontos_turisticos, initialize = custo_entrada_atracoes)
    modelo.tempo_recomendado = pyo.Param(modelo.pontos_turisticos, initialize = tempo_recomendado_atracoes)

    modelo.visitas = pyo.Var(atracoes, domain = pyo.Binary)

    modelo.obj = pyo.Objective(
        expr = sum(modelo.custo_entrada[ponto]*modelo.visitas[ponto] for ponto in atracoes)+
        peso_restricao*(num_min_atracoes-sum(modelo.visitas[ponto] for ponto in atracoes)),
        sense = pyo.minimize
    )

    modelo.restr_tempo = pyo.Constraint(
        expr = sum(modelo.tempo_recomendado[ponto]*modelo.visitas[ponto] for ponto in atracoes) <= modelo.tempo_maximo
    )

    return modelo

tempo_maximo = 8
num_min_atracoes = 8
peso_restricao = 10
modelo = criar_modelo_inteiro(atracoes, custo_entrada_atracoes, tempo_recomendado_atracoes, tempo_maximo, num_min_atracoes, peso_restricao)
resolver_modelo(modelo, log = False)

"""É importante destacar que, ao utilizar "restrições soft" e atribuir pesos na função objetivo, é crucial ponderar cuidadosamente a importância relativa dessas restrições. A escolha dos pesos influenciará diretamente a solução ótima do problema de otimização.

Ao atribuir pesos, você está essencialmente fazendo um compromisso entre diferentes objetivos. Por exemplo, se você atribuir um peso maior à maximização do número de atrações visitadas, o modelo priorizará visitar o maior número possível de locais, possivelmente ignorando o orçamento.

Por outro lado, se você atribuir um peso maior à minimização do orçamento, o modelo priorizará a economia de custos, o que pode resultar em visitar menos atrações, mas dentro do orçamento disponível.

Portanto, a escolha dos pesos na função objetivo deve ser baseada em considerações específicas do problema e nas prioridades do tomador de decisão. É uma parte crítica do processo de modelagem e otimização, e é importante encontrar um equilíbrio que atenda às suas metas e restrições de forma satisfatória. Experimentar diferentes combinações de pesos e realizar análises de sensibilidade pode ser útil para tomar decisões informadas.


Em resumo, as "restrições soft" proporcionam maior flexibilidade ao modelo, permitindo que ele ajuste automaticamente o número de atrações a serem visitadas com base em outras considerações, como o orçamento. Isso torna o modelo mais realista e adaptável às necessidades da viagem.

## Maximizando a Menor Quantidade e Outras Funções Objetivas

Agora, vamos abordar um novo problema que envolve mais complexidade. Imagine que temos a oportunidade de passar 4 dias em Paris, e durante cada dia, desejamos visitar o maior número possível de atrações, sem repetir nenhuma delas. Isso significa que queremos explorar Paris de forma abrangente, visitando o máximo de pontos turísticos diferentes em cada dia, sem revisitar nenhum deles.

Para ajustar o modelo anterior para esse novo cenário, precisaremos fazer algumas modificações. Primeiro, precisamos dividir as atrações em 4 conjuntos, um para cada dia da nossa estadia. Em seguida, garantiremos que, para cada conjunto de atrações de um dia, escolhamos no máximo uma atração para visitar, garantindo que não haja repetições. Também ajustaremos a função objetivo para considerar o custo total durante os 4 dias e, ao mesmo tempo, maximizar o número de atrações visitadas em cada dia.

Essa é uma extensão interessante do problema anterior, onde consideramos não apenas o custo e o tempo, mas também a distribuição das visitas ao longo dos dias da nossa estadia. A otimização desse novo cenário nos permitirá aproveitar ao máximo nossa viagem a Paris, explorando uma ampla variedade de atrações durante toda a estadia.
"""

def criar_modelo_inteiro_dias(atracoes, custo_entrada_atracoes, tempo_recomendado_atracoes, tempo_maximo_diario, orcamento_diario, dias):

    modelo = pyo.ConcreteModel()

    modelo.pontos_turisticos = pyo.Set(initialize=atracoes)
    modelo.dias = pyo.Set(initialize = dias)

    modelo.custo_entrada = pyo.Param(modelo.pontos_turisticos, initialize=custo_entrada_atracoes)
    modelo.tempo_recomendado = pyo.Param(modelo.pontos_turisticos, initialize=tempo_recomendado_atracoes)
    modelo.tempo_maximo_diario = pyo.Param(modelo.dias, initialize = tempo_maximo_diario)
    modelo.orcamento_diario = pyo.Param(modelo.dias, initialize = orcamento_diario)

    modelo.visitas = pyo.Var(modelo.pontos_turisticos, modelo.dias, domain = pyo.Binary)

    modelo.obj = pyo.Objective(
        expr= sum(modelo.visitas[ponto, dia] for ponto in atracoes for dia in dias),
        sense = pyo.maximize
    )

    modelo.restr_tempo_diario = pyo.Constraint(
        modelo.dias,
        rule= lambda modelo, dia: sum(modelo.tempo_recomendado[ponto]*modelo.visitas[ponto, dia] for ponto in atracoes) <= modelo.tempo_maximo_diario[dia]
    )

    modelo.restr_orcamento_diario = pyo.Constraint(
        modelo.dias,
        rule= lambda modelo, dia: sum(modelo.custo_entrada[ponto]*modelo.visitas[ponto, dia] for ponto in atracoes) <= modelo.orcamento_diario[dia]
    )

    modelo.restr_visita_unica = pyo.Constraint(
        modelo.pontos_turisticos,
        rule= lambda modelo, ponto: sum(modelo.visitas[ponto, dia] for dia in modelo.dias) <= 1
    )

    return modelo

def resolver_modelo_dias(modelo, log = False):
    solver = pyo.SolverFactory('glpk')
    resultado = solver.solve(modelo, tee = log)
    print(resultado.solver.status)
    if resultado.solver.status == SolverStatus.ok and resultado.solver.termination_condition == TerminationCondition.optimal:
        print('Solução ótima encontrada!')
        print(f'Função objetivo: {round(pyo.value(modelo.obj), 2)}')
        for dia in modelo.dias:
            for atracao in modelo.pontos_turisticos:
                valor_variavel_decisao = round(pyo.value(modelo.visitas[atracao, dia]), 2)
                if valor_variavel_decisao > 0:
                    print(f'No dia {dia} visitar {atracao}')
    elif resultado.solver.status == SolverStatus.warning:
        print('Atenção: Problema pode não ter solução ótima')
    elif resultado.solver.termination_condition == TerminationCondition.infeasible:
        print('O modelo é inviável. Não há solução possível.')
    else:
        print(f'Solver status: {resultado.solver.status}')

tempo_maximo_diario = {1:6, 2:6, 3:6, 4:6}
orcamento_diario = {1:100, 2:100, 3:100, 4:100}
dias = [1,2,3,4]
modelo = criar_modelo_inteiro_dias(atracoes, custo_entrada_atracoes, tempo_recomendado_atracoes, tempo_maximo_diario, orcamento_diario, dias)
resolver_modelo_dias(modelo, log = False)

def criar_modelo_inteiro_dias(atracoes, custo_entrada_atracoes, tempo_recomendado_atracoes, tempo_maximo_diario, orcamento_diario, dias):

    modelo = pyo.ConcreteModel()

    modelo.pontos_turisticos = pyo.Set(initialize=atracoes)
    modelo.dias = pyo.Set(initialize = dias)

    modelo.custo_entrada = pyo.Param(modelo.pontos_turisticos, initialize=custo_entrada_atracoes)
    modelo.tempo_recomendado = pyo.Param(modelo.pontos_turisticos, initialize=tempo_recomendado_atracoes)
    modelo.tempo_maximo_diario = pyo.Param(modelo.dias, initialize = tempo_maximo_diario)
    modelo.orcamento_diario = pyo.Param(modelo.dias, initialize = orcamento_diario)

    modelo.visitas = pyo.Var(modelo.pontos_turisticos, modelo.dias, domain = pyo.Binary)
    modelo.menor_qtd_atracoes = pyo.Var(within= pyo.NonNegativeIntegers)

    modelo.obj = pyo.Objective(
        expr= modelo.menor_qtd_atracoes,
        sense = pyo.maximize
    )

    modelo.restr_tempo_diario = pyo.Constraint(
        modelo.dias,
        rule= lambda modelo, dia: sum(modelo.tempo_recomendado[ponto]*modelo.visitas[ponto, dia] for ponto in atracoes) <= modelo.tempo_maximo_diario[dia]
    )

    modelo.restr_orcamento_diario = pyo.Constraint(
        modelo.dias,
        rule= lambda modelo, dia: sum(modelo.custo_entrada[ponto]*modelo.visitas[ponto, dia] for ponto in atracoes) <= modelo.orcamento_diario[dia]
    )

    modelo.restr_visita_unica = pyo.Constraint(
        modelo.pontos_turisticos,
        rule= lambda modelo, ponto: sum(modelo.visitas[ponto, dia] for dia in modelo.dias) <= 1
    )

    modelo.restr_menor_qtd_atracoes = pyo.Constraint(
        modelo.dias,
        rule = lambda modelo, dia: sum(modelo.visitas[ponto,dia] for ponto in atracoes) >= modelo.menor_qtd_atracoes
    )

    return modelo

modelo = criar_modelo_inteiro_dias(atracoes, custo_entrada_atracoes, tempo_recomendado_atracoes, tempo_maximo_diario, orcamento_diario, dias)
resolver_modelo_dias(modelo, log = False)

"""Ao lidar com o planejamento de visitas turísticas em um itinerário de vários dias, muitas vezes enfrentamos o desafio de decidir como distribuir nosso tempo e recursos de forma eficaz. Duas abordagens comuns para otimizar essa decisão são a maximização da soma total das atrações visitadas em todos os dias e a abordagem Max-Min, onde buscamos maximizar a menor quantidade de atrações visitadas em um único dia.

Na primeira abordagem, focamos na maximização da soma total de atrações visitadas durante toda a viagem. Neste cenário, estamos preocupados principalmente em aproveitar ao máximo cada dia, independentemente de quantas atrações visitemos em cada um deles. Isso significa que podemos ter dias em que visitamos um grande número de atrações e outros em que visitamos muito poucas ou nenhuma. O objetivo principal é obter o máximo de valor possível durante a viagem, sem se preocupar com a distribuição específica das visitas ao longo dos dias.

Por outro lado, a abordagem Max-Min (ou Min-Max) se concentra em maximizar a menor quantidade de atrações visitadas em um único dia. Neste caso, estamos mais preocupados com a consistência ao longo da viagem. Queremos garantir que, mesmo que tenhamos dias com muitas atrações, não deixemos nenhum dia com muito poucas ou nenhuma visita. Isso pode ser útil quando desejamos uma experiência mais equilibrada ao longo da viagem, evitando grandes variações na quantidade de atividades a cada dia.

# Desafios em Modelagem com Dados Extensos

## Dimensionando o Modelo

Imagine que estamos planejando uma viagem turística e queremos testar nosso modelo de planejamento em diferentes situações. A razão para fazer isso é verificar como o nosso modelo se comporta quando temos um grande número de atrações turísticas para visitar em vários dias.

Então, vamos criar uma função que gera parâmetros aleatórios para simular um cenário de viagem mais complexo. Nesta função, vamos gerar dados aleatórios, como custo de entrada em cada atração, tempo recomendado para visitar cada local, limites de tempo máximo disponível em cada dia da viagem e limites de orçamento diário. Esses parâmetros são cruciais para o nosso modelo tomar decisões sobre quais atrações visitar em cada dia, levando em consideração restrições de tempo e orçamento.

Gerar esses dados aleatórios nos permitirá testar o desempenho do nosso modelo em situações variadas e entender como ele se adapta a diferentes cenários de planejamento de viagens. Isso nos ajudará a avaliar a eficácia do modelo em lidar com desafios do mundo real, onde há muitas atrações e restrições de recursos.
"""

import random

def gerar_parametros(num_atracoes, num_dias):

    atracoes = range(1, num_atracoes)
    dias = range(1, num_dias+ 1)

    custo_entrada_atracoes = {ponto_turistico: random.randint(10, 100) for ponto_turistico in atracoes}
    tempo_recomendado_atracoes = {ponto_turistico: random.randint(1, 6) for ponto_turistico in atracoes}

    tempo_maximo_diario = {dia: random.randint(8, 10) for dia in dias}
    orcamento_diario = {dia: random.randint(450, 500) for dia in dias}

    return atracoes, dias, custo_entrada_atracoes, tempo_recomendado_atracoes, tempo_maximo_diario, orcamento_diario

num_atracoes = 10000
num_dias = 60
atracoes, dias, custo_entrada_atracoes, tempo_recomendado_atracoes, tempo_maximo_diario, orcamento_diario = gerar_parametros(num_atracoes = num_atracoes, num_dias = num_dias)

"""Ao tentar executar o código abaixo veremos que o modelo demora bastante para encontrar uma solução."""

modelo = criar_modelo_inteiro_dias(atracoes, custo_entrada_atracoes, tempo_recomendado_atracoes, tempo_maximo_diario, orcamento_diario, dias)
resolver_modelo_dias(modelo)

"""## Otimização com Dados Extensos"""

def resolver_modelo_dias(modelo, gap=None, tempo_limite = None, log = False):
    solver = pyo.SolverFactory('glpk')

    if gap is not None:
        solver.options['mipgap'] = gap
    if tempo_limite is not None:
        solver.options['tmlim'] = tempo_limite

    resultado = solver.solve(modelo, tee = log)
    print(resultado.solver.status)
    if resultado.solver.status == SolverStatus.ok and resultado.solver.termination_condition == TerminationCondition.optimal:
        print('Solução ótima encontrada!')
        print(f'Função objetivo: {round(pyo.value(modelo.obj), 2)}')
        for dia in modelo.dias:
            for atracao in modelo.pontos_turisticos:
                valor_variavel_decisao = round(pyo.value(modelo.visitas[atracao, dia]), 2)
                if valor_variavel_decisao > 0:
                    print(f'No dia {dia} visitar {atracao}')
    elif resultado.solver.status == SolverStatus.warning:
        print('Atenção: Problema pode não ter solução ótima')
    elif resultado.solver.termination_condition == TerminationCondition.infeasible:
        print('O modelo é inviável. Não há solução possível.')
    else:
        print(f'Solver status: {resultado.solver.status}')

modelo = criar_modelo_inteiro_dias(atracoes, custo_entrada_atracoes, tempo_recomendado_atracoes, tempo_maximo_diario, orcamento_diario, dias)
resolver_modelo_dias(modelo, gap = 0.01, tempo_limite = 120)