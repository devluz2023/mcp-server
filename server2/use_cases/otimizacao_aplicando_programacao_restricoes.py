# -*- coding: utf-8 -*-


import pandas as pd

dados = pd.read_csv('../data/visibilidade.csv')
dados


slots_tempo_disponiveis = dados.index.tolist()
slots_tempo_disponiveis

dados_visibilidade = dados.to_dict()
dados_visibilidade

from ortools.linear_solver import pywraplp

modelo = pywraplp.Solver.CreateSolver('SCIP')

x = {}
for anunciante in dados_visibilidade:
    for slot in slots_tempo_disponiveis:
        x[anunciante, slot] = modelo.BoolVar(f'x[{anunciante, slot}]')

modelo.Maximize(sum(dados_visibilidade[anunciante][slot]*x[anunciante, slot] for anunciante in dados_visibilidade for slot in slots_tempo_disponiveis))

for slot in slots_tempo_disponiveis:
    modelo.Add(sum(x[anunciante, slot] for anunciante in dados_visibilidade) == 1)

status = modelo.Solve()

if status == pywraplp.Solver.OPTIMAL:
    grade = []
    print('Visibilidade total máxima:', modelo.Objective().Value())
    print('Alocações:')
    for slot in slots_tempo_disponiveis:
        for anunciante in dados_visibilidade:
            if x[anunciante, slot].solution_value():
                grade.append(anunciante)
                print('Anunciante ', anunciante, 'alocado para o slot de tempo ', slot)
else:
    print('O problema não possui solução ótima')

grade

"""## Modelo de programação por restrições"""

from ortools.sat.python import cp_model

modelo = cp_model.CpModel()

x = {}
for anunciante in dados_visibilidade:
    for slot in slots_tempo_disponiveis:
        x[anunciante, slot] = modelo.NewBoolVar(f'x[{anunciante, slot}]')

modelo.Maximize(sum(dados_visibilidade[anunciante][slot]*x[anunciante, slot] for anunciante in dados_visibilidade for slot in slots_tempo_disponiveis))

for slot in slots_tempo_disponiveis:
    modelo.Add(sum(x[anunciante, slot] for anunciante in dados_visibilidade) == 1)

solver = cp_model.CpSolver()
status = solver.Solve(modelo)

if status == cp_model.OPTIMAL:
    grade = []
    print('Visibilidade total máxima:', solver.ObjectiveValue())
    print('Alocações:')
    for slot in slots_tempo_disponiveis:
        for anunciante in dados_visibilidade:
            if solver.Value(x[anunciante, slot]):
                grade.append(anunciante)
                print('Anunciante ', anunciante, 'alocado para o slot de tempo ', slot)
else:
    print('O problema não possui solução ótima')

grade

"""## Restrição exatamente um ("ExactlyOne")"""

def alocar_anunciante_cp(dados_visibilidade, slots_tempo_disponiveis):

    modelo = cp_model.CpModel()

    x = {}
    for anunciante in dados_visibilidade:
        for slot in slots_tempo_disponiveis:
            x[anunciante, slot] = modelo.NewBoolVar(f'x[{anunciante, slot}]')

    modelo.Maximize(sum(dados_visibilidade[anunciante][slot]*x[anunciante, slot] for anunciante in dados_visibilidade for slot in slots_tempo_disponiveis))

    for slot in slots_tempo_disponiveis:
        variaveis_slot = [x[anunciante, slot] for anunciante in dados_visibilidade]
        modelo.AddExactlyOne(variaveis_slot)

    solver = cp_model.CpSolver()
    status = solver.Solve(modelo)

    if status == cp_model.OPTIMAL:
        grade = []
        valor_obj = solver.ObjectiveValue()
        for slot in slots_tempo_disponiveis:
            for anunciante in dados_visibilidade:
                if solver.Value(x[anunciante, slot]):
                    grade.append(anunciante)
        return valor_obj, grade
    else:
        return None, None

alocar_anunciante_cp(dados_visibilidade, slots_tempo_disponiveis)



def alocar_anunciante_cp(dados_visibilidade, slots_tempo_disponiveis):

    modelo = cp_model.CpModel()

    x = {}
    for anunciante in dados_visibilidade:
        for slot in slots_tempo_disponiveis:
            x[anunciante, slot] = modelo.NewBoolVar(f'x[{anunciante, slot}]')

    total_visibilidade = {}
    total_anuncios = {}
    media_visibilidade = {}

    for anunciante in dados_visibilidade:
        soma_visibilidade_anunciante = sum(dados_visibilidade[anunciante].values())
        total_visibilidade[anunciante] = modelo.NewIntVar(lb = 0, ub = soma_visibilidade_anunciante, name = f'total_visibilidade[{anunciante}]')
        total_anuncios[anunciante] = modelo.NewIntVar(lb = 0, ub = len(slots_tempo_disponiveis), name = f'total_anuncios[{anunciante}]')
        media_visibilidade[anunciante] = modelo.NewIntVar(lb = 0, ub = soma_visibilidade_anunciante, name = f'media_visibilidade[{anunciante}]')

    modelo.Maximize(sum(media_visibilidade[anunciante] for anunciante in dados_visibilidade))

    for slot in slots_tempo_disponiveis:
        variaveis_slot = [x[anunciante, slot] for anunciante in dados_visibilidade]
        modelo.AddExactlyOne(variaveis_slot)

    for anunciante in dados_visibilidade:
        modelo.Add(total_visibilidade[anunciante]==sum(dados_visibilidade[anunciante][slot]*x[anunciante, slot] for slot in slots_tempo_disponiveis))
        modelo.Add(total_anuncios[anunciante] == sum(x[anunciante, slot] for slot in slots_tempo_disponiveis))
        modelo.AddDivisionEquality(
            target = media_visibilidade[anunciante],
            num = total_visibilidade[anunciante],
            denom = total_anuncios[anunciante]
        )

    solver = cp_model.CpSolver()
    status = solver.Solve(modelo)

    if status == cp_model.OPTIMAL:
        grade = []
        valor_obj = solver.ObjectiveValue()
        for slot in slots_tempo_disponiveis:
            for anunciante in dados_visibilidade:
                if solver.Value(x[anunciante, slot]):
                    grade.append(anunciante)

        for anunciante in dados_visibilidade:
            print(anunciante, solver.Value(media_visibilidade[anunciante]))
        return valor_obj, grade
    else:
        return None, None

alocar_anunciante_cp(dados_visibilidade, slots_tempo_disponiveis)

"""## Identificando inviabilidade e resolvendo modelo

[Documentação de descrições de status OR-Tools](https://developers.google.com/optimization/cp/cp_solver?hl=pt-br#cp-sat_return_values)

- **OPTIMAL**: Foi encontrada uma solução ideal viável.
- **FEASIBLE**:	Foi encontrada uma solução viável, mas não sabemos se é a ideal.
- **INFEASIBLE**: O problema se mostrou inviável.
- **MODEL_INVALID**:	O CpModelProto fornecido não passou na etapa de validação. Para receber um erro detalhado, chame ValidateCpModel(model_proto).
- **UNKNOWN**:	O status do modelo é desconhecido porque nenhuma solução foi encontrada (ou o problema não foi considerado inviável) antes de algo fazer com que o solucionador parasse, como um limite de tempo, um limite de memória ou um limite personalizado definido pelo usuário.
"""

def descricao_status(status):
    if status == cp_model.OPTIMAL:
        return 'Foi encontrada uma solução ideal viável.'
    elif status == cp_model.FEASIBLE:
        return 'Foi encontrada uma solução viável, mas não sabemos se é a ideal.'
    elif status == cp_model.INFEASIBLE:
        return 'O problema se mostrou inviável.'
    elif status == cp_model.MODEL_INVALID:
        return 'O CpModelProto fornecido não passou na etapa de validação. Para receber um erro detalhado, chame ValidateCpModel(model_proto).'
    elif status == cp_model.UNKNOWN:
        return 'O status do modelo é desconhecido porque nenhuma solução foi encontrada (ou o problema não foi considerado inviável) antes de algo fazer com que o solucionador parasse, como um limite de tempo, um limite de memória ou um limite personalizado definido pelo usuário.'
    else:
        return 'Status desconhecido'

def alocar_anunciante_cp(dados_visibilidade, slots_tempo_disponiveis):

    modelo = cp_model.CpModel()

    x = {}
    for anunciante in dados_visibilidade:
        for slot in slots_tempo_disponiveis:
            x[anunciante, slot] = modelo.NewBoolVar(f'x[{anunciante, slot}]')

    total_visibilidade = {}
    total_anuncios = {}
    media_visibilidade = {}

    for anunciante in dados_visibilidade:
        soma_visibilidade_anunciante = sum(dados_visibilidade[anunciante].values())
        total_visibilidade[anunciante] = modelo.NewIntVar(lb = 0, ub = soma_visibilidade_anunciante, name = f'total_visibilidade[{anunciante}]')
        total_anuncios[anunciante] = modelo.NewIntVar(lb = 1, ub = len(slots_tempo_disponiveis), name = f'total_anuncios[{anunciante}]')
        media_visibilidade[anunciante] = modelo.NewIntVar(lb = 0, ub = soma_visibilidade_anunciante, name = f'media_visibilidade[{anunciante}]')

    modelo.Maximize(sum(media_visibilidade[anunciante] for anunciante in dados_visibilidade))

    for slot in slots_tempo_disponiveis:
        variaveis_slot = [x[anunciante, slot] for anunciante in dados_visibilidade]
        modelo.AddExactlyOne(variaveis_slot)

    for anunciante in dados_visibilidade:
        modelo.Add(total_visibilidade[anunciante]==sum(dados_visibilidade[anunciante][slot]*x[anunciante, slot] for slot in slots_tempo_disponiveis))
        modelo.Add(total_anuncios[anunciante] == sum(x[anunciante, slot] for slot in slots_tempo_disponiveis))
        modelo.AddDivisionEquality(
            target = media_visibilidade[anunciante],
            num = total_visibilidade[anunciante],
            denom = total_anuncios[anunciante]
        )

    print(modelo.Validate())

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 60
    status = solver.Solve(modelo)

    print(status, descricao_status(status))

    if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
        grade = []
        valor_obj = solver.ObjectiveValue()
        for slot in slots_tempo_disponiveis:
            for anunciante in dados_visibilidade:
                if solver.Value(x[anunciante, slot]):
                    grade.append(anunciante)

        for anunciante in dados_visibilidade:
            print(anunciante, solver.Value(media_visibilidade[anunciante]))
        return valor_obj, grade
    else:
        return None, None

alocar_anunciante_cp(dados_visibilidade, slots_tempo_disponiveis)

"""# Equilíbrio da visibilidade ao longo dos dias

## Garantindo o equilíbrio de visibilidade
"""

def dividir_em_dias(slots_tempo_disponiveis):
    dias = {}
    num_dias = len(slots_tempo_disponiveis) // 10
    for i in range(num_dias):
        inicio = i*10
        fim = inicio+10
        dias[i] = slots_tempo_disponiveis[inicio:fim]
    return dias

dias = dividir_em_dias(slots_tempo_disponiveis)
dias

def alocar_anunciante_cp(dados_visibilidade, slots_tempo_disponiveis, dias):

    modelo = cp_model.CpModel()

    x = {}
    for anunciante in dados_visibilidade:
        for slot in slots_tempo_disponiveis:
            x[anunciante, slot] = modelo.NewBoolVar(f'x[{anunciante, slot}]')

    menor_visibilidade_dia = {}

    for anunciante in dados_visibilidade:
        maior_visibilidade_anunciante = max(dados_visibilidade[anunciante].values())
        menor_visibilidade_dia[anunciante] = modelo.NewIntVar(lb = 0, ub = maior_visibilidade_anunciante, name = f'menor_visibilidade_dia[{anunciante}]')

    modelo.Maximize(sum(menor_visibilidade_dia[anunciante] for anunciante in dados_visibilidade))

    for slot in slots_tempo_disponiveis:
        variaveis_slot = [x[anunciante, slot] for anunciante in dados_visibilidade]
        modelo.AddExactlyOne(variaveis_slot)

    for anunciante in dados_visibilidade:
        variaveis_visibilidade = [sum(dados_visibilidade[anunciante][slot]*x[anunciante, slot] for slot in slots) for dia, slots in dias.items()]
        modelo.AddMinEquality(menor_visibilidade_dia[anunciante], variaveis_visibilidade)

    print(modelo.Validate())

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 60
    status = solver.Solve(modelo)

    print(status, descricao_status(status))

    if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
        grade = []
        valor_obj = solver.ObjectiveValue()
        for slot in slots_tempo_disponiveis:
            for anunciante in dados_visibilidade:
                if solver.Value(x[anunciante, slot]):
                    grade.append(anunciante)

        for anunciante in dados_visibilidade:
            print(anunciante, solver.Value(menor_visibilidade_dia[anunciante]))
        return valor_obj, grade
    else:
        return None, None

alocar_anunciante_cp(dados_visibilidade, slots_tempo_disponiveis, dias)

"""## Considerando os anunciantes presentes em pelo menos um dia"""

def alocar_anunciante_cp(dados_visibilidade, slots_tempo_disponiveis, dias):

    modelo = cp_model.CpModel()

    x = {}
    for anunciante in dados_visibilidade:
        for slot in slots_tempo_disponiveis:
            x[anunciante, slot] = modelo.NewBoolVar(f'x[{anunciante, slot}]')

    menor_visibilidade_dia = {}

    for anunciante in dados_visibilidade:
        maior_visibilidade_anunciante = max(dados_visibilidade[anunciante].values())
        menor_visibilidade_dia[anunciante] = modelo.NewIntVar(lb = 0, ub = maior_visibilidade_anunciante, name = f'menor_visibilidade_dia[{anunciante}]')

    modelo.Maximize(sum(menor_visibilidade_dia[anunciante] for anunciante in dados_visibilidade))

    for slot in slots_tempo_disponiveis:
        variaveis_slot = [x[anunciante, slot] for anunciante in dados_visibilidade]
        modelo.AddExactlyOne(variaveis_slot)

    for anunciante in dados_visibilidade:
        variaveis_visibilidade = [sum(dados_visibilidade[anunciante][slot]*x[anunciante, slot] for slot in slots) for dia, slots in dias.items()]
        modelo.AddMinEquality(menor_visibilidade_dia[anunciante], variaveis_visibilidade)

        for dia, slots in dias.items():
            numero_anuncios = [x[anunciante, slot] for slot in slots]
            modelo.AddAtLeastOne(numero_anuncios)

    print(modelo.Validate())

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 60
    status = solver.Solve(modelo)

    print(status, descricao_status(status))

    if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
        grade = []
        valor_obj = solver.ObjectiveValue()
        for slot in slots_tempo_disponiveis:
            for anunciante in dados_visibilidade:
                if solver.Value(x[anunciante, slot]):
                    grade.append(anunciante)

        for anunciante in dados_visibilidade:
            print(anunciante, solver.Value(menor_visibilidade_dia[anunciante]))
        return valor_obj, grade
    else:
        return None, None

alocar_anunciante_cp(dados_visibilidade, slots_tempo_disponiveis, dias)

"""## Utilizando o equilíbrio absoluto de visibilidade"""

def alocar_anunciante_cp(dados_visibilidade, slots_tempo_disponiveis, dias):

    modelo = cp_model.CpModel()

    x = {}
    for anunciante in dados_visibilidade:
        for slot in slots_tempo_disponiveis:
            x[anunciante, slot] = modelo.NewBoolVar(f'x[{anunciante, slot}]')

    menor_visibilidade_dia = {}

    for anunciante in dados_visibilidade:
        maior_visibilidade_anunciante = max(dados_visibilidade[anunciante].values())
        menor_visibilidade_dia[anunciante] = modelo.NewIntVar(lb = 0, ub = maior_visibilidade_anunciante, name = f'menor_visibilidade_dia[{anunciante}]')

    dif_visibilidade = {}
    for anunciante1 in dados_visibilidade:
        for anunciante2 in dados_visibilidade:
            if anunciante1 < anunciante2:
                maior_visibilidade_anunciante1 = sum(dados_visibilidade[anunciante1].values())
                maior_visibilidade_anunciante2 = sum(dados_visibilidade[anunciante2].values())
                maior_visibilidade_anunciante = max(maior_visibilidade_anunciante1, maior_visibilidade_anunciante2)
                dif_visibilidade[anunciante1, anunciante2] = modelo.NewIntVar(lb = 0, ub = maior_visibilidade_anunciante, name = f'dif_visibilidade[{anunciante1, anunciante2}]')

    modelo.Maximize(
        100*sum(menor_visibilidade_dia[anunciante] for anunciante in dados_visibilidade) -
        sum(dif_visibilidade[anunciante1, anunciante2] for anunciante1 in dados_visibilidade for anunciante2 in dados_visibilidade if anunciante1 < anunciante2)
        )

    for slot in slots_tempo_disponiveis:
        variaveis_slot = [x[anunciante, slot] for anunciante in dados_visibilidade]
        modelo.AddExactlyOne(variaveis_slot)

    for anunciante in dados_visibilidade:
        variaveis_visibilidade = [sum(dados_visibilidade[anunciante][slot]*x[anunciante, slot] for slot in slots) for dia, slots in dias.items()]
        modelo.AddMinEquality(menor_visibilidade_dia[anunciante], variaveis_visibilidade)

        for dia, slots in dias.items():
            numero_anuncios = [x[anunciante, slot] for slot in slots]
            modelo.AddAtLeastOne(numero_anuncios)

    for anunciante1 in dados_visibilidade:
        for anunciante2 in dados_visibilidade:
            if anunciante1 < anunciante2:
                modelo.AddAbsEquality(dif_visibilidade[anunciante1, anunciante2],
                                      (sum(dados_visibilidade[anunciante1][slot]*x[anunciante1, slot] for slot in slots_tempo_disponiveis)-sum(dados_visibilidade[anunciante2][slot]*x[anunciante2, slot] for slot in slots_tempo_disponiveis)))

    print(modelo.Validate())

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 60
    status = solver.Solve(modelo)

    print(status, descricao_status(status))

    if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
        grade = []
        valor_obj = solver.ObjectiveValue()
        for slot in slots_tempo_disponiveis:
            for anunciante in dados_visibilidade:
                if solver.Value(x[anunciante, slot]):
                    grade.append(anunciante)

        for anunciante in dados_visibilidade:
            print(anunciante, solver.Value(menor_visibilidade_dia[anunciante]))
        return valor_obj, grade
    else:
        return None, None

alocar_anunciante_cp(dados_visibilidade, slots_tempo_disponiveis, dias)

"""# Restrições avançadas e restrições globais

## Restrições de implicação e negação
"""

def alocar_anunciante_cp(dados_visibilidade, slots_tempo_disponiveis):

    modelo = cp_model.CpModel()

    x = {}
    for anunciante in dados_visibilidade:
        for slot in slots_tempo_disponiveis:
            x[anunciante, slot] = modelo.NewBoolVar(f'x[{anunciante, slot}]')

    modelo.Maximize(sum(dados_visibilidade[anunciante][slot]*x[anunciante, slot] for anunciante in dados_visibilidade for slot in slots_tempo_disponiveis))

    for slot in slots_tempo_disponiveis:
        variaveis_slot = [x[anunciante, slot] for anunciante in dados_visibilidade]
        modelo.AddExactlyOne(variaveis_slot)

        if slot < len(slots_tempo_disponiveis)-1:
            modelo.AddImplication(x['EnergiaViva', slot], x['EsportivaMax', slot+1].Not())

    solver = cp_model.CpSolver()
    status = solver.Solve(modelo)

    if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
        grade = []
        valor_obj = solver.ObjectiveValue()
        for slot in slots_tempo_disponiveis:
            for anunciante in dados_visibilidade:
                if solver.Value(x[anunciante, slot]):
                    grade.append(anunciante)
        return valor_obj, grade
    else:
        return None, None

alocar_anunciante_cp(dados_visibilidade, slots_tempo_disponiveis)

"""## Método "OnlyEnforceIf"
"""

marcas = list(dados_visibilidade.keys())
marcas

def alocar_anunciante_cp(dados_visibilidade, slots_tempo_disponiveis):

    modelo = cp_model.CpModel()

    x = {}
    for anunciante in dados_visibilidade:
        for slot in slots_tempo_disponiveis:
            x[anunciante, slot] = modelo.NewBoolVar(f'x[{anunciante, slot}]')

    num_anunciantes = len(dados_visibilidade)
    y = {}
    for slot in slots_tempo_disponiveis:
        y[slot] = modelo.NewIntVar(lb = 0, ub = num_anunciantes, name = f'y[{anunciante}]')

    modelo.Maximize(sum(dados_visibilidade[anunciante][slot]*x[anunciante, slot] for anunciante in dados_visibilidade for slot in slots_tempo_disponiveis))

    for slot in slots_tempo_disponiveis:
        variaveis_slot = [x[anunciante, slot] for anunciante in dados_visibilidade]
        modelo.AddExactlyOne(variaveis_slot)

        for anunciante in dados_visibilidade:
            modelo.Add(y[slot] == marcas.index(anunciante)).OnlyEnforceIf(x[anunciante, slot])

    solver = cp_model.CpSolver()
    status = solver.Solve(modelo)
    print(status, descricao_status(status))
    if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
        grade = []
        valor_obj = solver.ObjectiveValue()
        for slot in slots_tempo_disponiveis:
            idx = solver.Value(y[slot])
            print(slot, idx, marcas[idx])
            for anunciante in dados_visibilidade:
                if solver.Value(x[anunciante, slot]):
                    grade.append(anunciante)
        return valor_obj, grade
    else:
        return None, None

alocar_anunciante_cp(dados_visibilidade, slots_tempo_disponiveis)

"""## Restrição "AllDifferent"
"""

def alocar_anunciante_cp(dados_visibilidade, slots_tempo_disponiveis):

    modelo = cp_model.CpModel()

    x = {}
    for anunciante in dados_visibilidade:
        for slot in slots_tempo_disponiveis:
            x[anunciante, slot] = modelo.NewBoolVar(f'x[{anunciante, slot}]')

    num_anunciantes = len(dados_visibilidade)
    y = {}
    for slot in slots_tempo_disponiveis:
        y[slot] = modelo.NewIntVar(lb = 0, ub = num_anunciantes, name = f'y[{anunciante}]')

    modelo.Maximize(sum(dados_visibilidade[anunciante][slot]*x[anunciante, slot] for anunciante in dados_visibilidade for slot in slots_tempo_disponiveis))

    for slot in slots_tempo_disponiveis:
        variaveis_slot = [x[anunciante, slot] for anunciante in dados_visibilidade]
        modelo.AddExactlyOne(variaveis_slot)

        for anunciante in dados_visibilidade:
            modelo.Add(y[slot] == marcas.index(anunciante)).OnlyEnforceIf(x[anunciante, slot])

    for slot in range(0, len(slots_tempo_disponiveis)-2):
        anunciantes = [y[slot], y[slot+1], y[slot+2]]
        modelo.AddAllDifferent(anunciantes)

    solver = cp_model.CpSolver()
    status = solver.Solve(modelo)
    print(status, descricao_status(status))
    if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
        grade = []
        valor_obj = solver.ObjectiveValue()
        for slot in slots_tempo_disponiveis:
            idx = solver.Value(y[slot])
            print(slot, idx, marcas[idx])
            for anunciante in dados_visibilidade:
                if solver.Value(x[anunciante, slot]):
                    grade.append(anunciante)
        return valor_obj, grade
    else:
        return None, None

alocar_anunciante_cp(dados_visibilidade, slots_tempo_disponiveis)