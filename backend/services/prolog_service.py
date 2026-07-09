import subprocess
import os

SWIPL_PATH = r"C:\Program Files\swipl\bin\swipl.exe"
PL_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..', 'prolog', 'doctor_byte.pl')
).replace('\\', '/')


def _run_query(query):
    goal = f"consult('{PL_PATH}'), {query}, halt."
    result = subprocess.run(
        [SWIPL_PATH, '-g', goal],
        capture_output=True,
        timeout=10,
        encoding='cp1252'
    )
    return result.stdout, result.stderr


def get_sintomas():
    query = (
        "lista_sintomas(S), "
        "forall(member(Id-Nombre, S), "
        "format('SINTOMA|~w|~w~n', [Id, Nombre]))"
    )
    stdout, _ = _run_query(query)
    sintomas = []
    for line in stdout.strip().splitlines():
        if line.startswith('SINTOMA|'):
            partes = line.split('|')
            if len(partes) == 3:
                sintomas.append({'id': partes[1], 'nombre': partes[2]})
    return sintomas


def diagnosticar(sintomas_lista):
    lista_prolog = '[' + ','.join(sintomas_lista) + ']'
    query = (
        f"todos_diagnosticos({lista_prolog}, D), "
        "forall(member(diag(P,F,N,R), D), "
        "format('DIAG|~w|~w|~w|~w~n', [P,F,N,R]))"
    )
    stdout, _ = _run_query(query)
    diagnosticos = []
    for line in stdout.strip().splitlines():
        if line.startswith('DIAG|'):
            partes = line.split('|')
            if len(partes) == 5:
                diagnosticos.append({
                    'porcentaje':    int(partes[1]),
                    'falla':         partes[2],
                    'nombre_falla':  partes[3],
                    'recomendacion': partes[4]
                })
    return diagnosticos