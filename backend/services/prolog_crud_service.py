import os
import re

BASE_PATH      = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'prolog', 'doctor_byte_base.pl'))
DYNAMIC_PATH   = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'prolog', 'doctor_byte_dynamic.pl'))
GENERATED_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'prolog', 'doctor_byte.pl'))


def _leer(path):
    if not os.path.exists(path):
        return ''
    with open(path, 'r', encoding='cp1252') as f:
        return f.read()

def _escribir(path, contenido):
    with open(path, 'w', encoding='cp1252') as f:
        f.write(contenido)

def _regenerar():
    base    = _leer(BASE_PATH)
    dynamic = _leer(DYNAMIC_PATH)
    combined = (
        "% ============================================================\n"
        "%  Doctor Byte - Archivo generado automaticamente\n"
        "% ============================================================\n\n"
        ":- discontiguous sintoma/1.\n"
        ":- discontiguous nombre_sintoma/2.\n"
        ":- discontiguous falla_sintoma/2.\n"
        ":- discontiguous nombre_falla/2.\n"
        ":- discontiguous recomendacion/2.\n\n"
        + base + "\n\n% --- DINAMICO ---\n\n" + dynamic
    )
    _escribir(GENERATED_PATH, combined)

def _existe_sintoma(sid):
    for path in [BASE_PATH, DYNAMIC_PATH]:
        if re.search(rf'sintoma\({re.escape(sid)}\)', _leer(path)):
            return True
    return False

def _existe_falla(fid):
    for path in [BASE_PATH, DYNAMIC_PATH]:
        if re.search(rf'falla_sintoma\({re.escape(fid)},', _leer(path)):
            return True
    return False


# ── Sintomas ──────────────────────────────────────────────────

def crear_sintoma(sid, nombre):
    if _existe_sintoma(sid):
        return False, 'El sintoma ya existe'
    lineas = f"sintoma({sid}).\nnombre_sintoma({sid}, '{nombre}').\n"
    _escribir(DYNAMIC_PATH, _leer(DYNAMIC_PATH) + lineas)
    _regenerar()
    return True, 'Sintoma creado'

def eliminar_sintoma(sid):
    contenido = _leer(DYNAMIC_PATH)
    patron    = rf'(sintoma\({re.escape(sid)}\)\.|nombre_sintoma\({re.escape(sid)},.*?\)\.)\n?'
    nuevo     = re.sub(patron, '', contenido)
    if nuevo == contenido:
        return False, 'Sintoma no encontrado en archivo dinamico'
    _escribir(DYNAMIC_PATH, nuevo)
    _regenerar()
    return True, 'Sintoma eliminado'

def listar_sintomas_dynamic():
    contenido = _leer(DYNAMIC_PATH)
    patron    = r"nombre_sintoma\((\w+),\s*'(.+?)'\)"
    return [{'id': m.group(1), 'nombre': m.group(2)}
            for m in re.finditer(patron, contenido)]


# ── Fallas ────────────────────────────────────────────────────

def crear_falla(fid, nombre, sintomas, recomendacion):
    if _existe_falla(fid):
        return False, 'La falla ya existe'
    lista  = '[' + ', '.join(sintomas) + ']'
    lineas = (
        f"falla_sintoma({fid}, {lista}).\n"
        f"nombre_falla({fid}, '{nombre}').\n"
        f"recomendacion({fid}, '{recomendacion}').\n"
    )
    _escribir(DYNAMIC_PATH, _leer(DYNAMIC_PATH) + lineas)
    _regenerar()
    return True, 'Falla creada'

def eliminar_falla(fid):
    contenido = _leer(DYNAMIC_PATH)
    patron    = rf'(falla_sintoma\({re.escape(fid)},.*?\)\.|nombre_falla\({re.escape(fid)},.*?\)\.|recomendacion\({re.escape(fid)},.*?\)\.)\n?'
    nuevo     = re.sub(patron, '', contenido)
    if nuevo == contenido:
        return False, 'Falla no encontrada en archivo dinamico'
    _escribir(DYNAMIC_PATH, nuevo)
    _regenerar()
    return True, 'Falla eliminada'

def listar_fallas_dynamic():
    contenido = _leer(DYNAMIC_PATH)
    patron    = r"nombre_falla\((\w+),\s*'(.+?)'\)"
    return [{'id': m.group(1), 'nombre': m.group(2)}
            for m in re.finditer(patron, contenido)]

def actualizar_falla(fid, nombre, sintomas, recomendacion):
    ok, msg = eliminar_falla(fid)
    if not ok:
        return False, msg
    return crear_falla(fid, nombre, sintomas, recomendacion)


# ── Recomendaciones ───────────────────────────────────────────

def crear_recomendacion(fid, texto):
    contenido = _leer(DYNAMIC_PATH)
    if re.search(rf"recomendacion\({re.escape(fid)},", contenido):
        return actualizar_recomendacion(fid, texto)
    linea = f"recomendacion({fid}, '{texto}').\n"
    _escribir(DYNAMIC_PATH, contenido + linea)
    _regenerar()
    return True, 'Recomendacion creada'

def actualizar_recomendacion(fid, texto):
    contenido = _leer(DYNAMIC_PATH)
    patron    = rf"recomendacion\({re.escape(fid)},.*?\)\.\n?"
    if not re.search(patron, contenido):
        return False, 'Recomendacion no encontrada en archivo dinamico'
    nuevo = re.sub(patron, f"recomendacion({fid}, '{texto}').\n", contenido)
    _escribir(DYNAMIC_PATH, nuevo)
    _regenerar()
    return True, 'Recomendacion actualizada'

def eliminar_recomendacion(fid):
    contenido = _leer(DYNAMIC_PATH)
    patron    = rf"recomendacion\({re.escape(fid)},.*?\)\.\n?"
    nuevo     = re.sub(patron, '', contenido)
    if nuevo == contenido:
        return False, 'Recomendacion no encontrada en archivo dinamico'
    _escribir(DYNAMIC_PATH, nuevo)
    _regenerar()
    return True, 'Recomendacion eliminada'

def listar_recomendaciones_dynamic():
    contenido = _leer(DYNAMIC_PATH)
    patron    = r"recomendacion\((\w+),\s*'(.+?)'\)"
    return [{'falla_id': m.group(1), 'texto': m.group(2)}
            for m in re.finditer(patron, contenido)]


# ── Reglas ────────────────────────────────────────────────────

def listar_reglas():
    base    = _leer(BASE_PATH)
    dynamic = _leer(DYNAMIC_PATH)
    patron  = r"falla_sintoma\((\w+),\s*\[([^\]]+)\]\)"
    reglas  = []
    for contenido, origen in [(base, 'base'), (dynamic, 'dynamic')]:
        for m in re.finditer(patron, contenido):
            sintomas = [s.strip() for s in m.group(2).split(',')]
            reglas.append({
                'falla_id': m.group(1),
                'sintomas': sintomas,
                'origen':   origen
            })
    return reglas

def crear_regla(fid, sintomas):
    if _existe_falla(fid):
        return False, 'La falla ya existe, use actualizar'
    lista  = '[' + ', '.join(sintomas) + ']'
    linea  = f"falla_sintoma({fid}, {lista}).\n"
    _escribir(DYNAMIC_PATH, _leer(DYNAMIC_PATH) + linea)
    _regenerar()
    return True, 'Regla creada'

def eliminar_regla(fid):
    contenido = _leer(DYNAMIC_PATH)
    patron    = rf"falla_sintoma\({re.escape(fid)},.*?\)\.\n?"
    nuevo     = re.sub(patron, '', contenido)
    if nuevo == contenido:
        return False, 'Regla no encontrada en archivo dinamico'
    _escribir(DYNAMIC_PATH, nuevo)
    _regenerar()
    return True, 'Regla eliminada'