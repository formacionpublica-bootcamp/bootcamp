#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Descarga y curatoría reproducible de los datasets del rearmado (Fase 1b).

Fuentes públicas (verificadas 26-ago-2026):
  matricula  Resumen de matrícula por establecimiento 2025 — datosabiertos.mineduc.cl (.rar)
  aire       PM2.5 diario + meteorología horaria por estación — SINCA (sinca.mma.gob.cl)
  fichas     Fichas de trámites de ChileAtiende (crawl de /temas → /fichas/<id>)
  reclamos   Base de reclamos SERNAC 2011 — datos.gob.cl (solo categorías, sin texto libre)
  sismos     Catálogo USGS FDSN, Chile 2020-2025 M>=4.5
  aire_nuevos  SINCA ene–sep 2026, mismas estaciones (datos no vistos para R2-09)
  matricula_sucia  errores inyectados con seed sobre matricula.csv (R1-04)
  manifiesto  data/rearmado/MANIFEST.json (filas, columnas, sha256, procedencia)
  publicar   copia CSV + MANIFEST.json a data/ (lo que consumen los notebooks)

`todo` corre todas las fuentes en orden y termina con `publicar`.

Uso:
  /opt/anaconda3/bin/python tools/make_datasets.py [matricula|aire|aire_nuevos|fichas|reclamos|sismos|matricula_sucia|manifiesto|publicar|todo]

Salidas en data/rearmado/ (crudos en data/rearmado/raw/, se reusan si existen).
Requiere: pandas, requests; `unar` en PATH para el .rar de MINEDUC (brew install unar).
"""
import html
import io
import json
import re
import subprocess
import sys
import time
import unicodedata
from pathlib import Path

import pandas as pd
import requests

BASE = Path(__file__).resolve().parent.parent  # raíz del repo del curso
OUT = BASE / "data" / "rearmado"
RAW = OUT / "raw"
SEED = 42
UA = {"User-Agent": "formacionpublica-bootcamp/1.0 (curso abierto de ciencia de datos)"}

URL_MATRICULA = ("https://datosabiertos.mineduc.cl/wp-content/uploads/2025/11/"
                 "Resumen_Matricula_EE_2025.rar")
URL_RECLAMOS = "https://datos.gob.cl/uploads/recursos/Reclamos_2011_Data%20Set.csv"
SINCA = "https://sinca.mma.gob.cl"
SINCA_REGIONES = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX",
                  "X", "XI", "XII", "XIV", "XV", "XVI", "M"]
CHILEATIENDE = "https://www.chileatiende.gob.cl"

REGIONES = {15: "Arica y Parinacota", 1: "Tarapacá", 2: "Antofagasta", 3: "Atacama",
            4: "Coquimbo", 5: "Valparaíso", 13: "Metropolitana", 6: "O'Higgins",
            7: "Maule", 16: "Ñuble", 8: "Biobío", 9: "La Araucanía",
            14: "Los Ríos", 10: "Los Lagos", 11: "Aysén", 12: "Magallanes"}
DEPENDENCIAS = {1: "Municipal", 2: "Particular subvencionado", 3: "Particular pagado",
                4: "Administración delegada", 5: "Servicio Local de Educación"}


def descargar(url, destino, timeout=300):
    """Descarga a data/rearmado/raw/ y reusa el archivo si ya existe."""
    destino = RAW / destino
    if destino.exists() and destino.stat().st_size > 0:
        print(f"  [caché] {destino.name}")
        return destino
    print(f"  [descarga] {url}")
    r = requests.get(url, headers=UA, timeout=timeout)
    r.raise_for_status()
    destino.write_bytes(r.content)
    return destino


def limpiar_texto(s):
    return re.sub(r"\s+", " ", str(s)).strip()


def sin_tildes(s):
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()


# ---------------------------------------------------------------- matrícula
def hacer_matricula():
    print("== matricula (MINEDUC 2025) ==")
    rar = descargar(URL_MATRICULA, "matricula_2025.rar")
    extraidos = list(RAW.glob("**/*Resumen_Matricula*2025*.csv"))
    if not extraidos:
        subprocess.run(["unar", "-q", "-f", "-o", str(RAW), str(rar)], check=True)
        extraidos = list(RAW.glob("**/*Resumen_Matricula*2025*.csv"))
    df = pd.read_csv(extraidos[0], encoding="utf-8-sig")
    df.columns = [c.strip().upper() for c in df.columns]
    # filtro oficial CEM-MINEDUC para «establecimientos funcionando con matrícula»
    df = df[(df["ESTADO_ESTAB"] == 1) & (df["MAT_TOTAL"] > 0)].copy()

    out = pd.DataFrame({
        "rbd": df["RBD"],
        "nombre": df["NOM_RBD"].map(lambda s: limpiar_texto(s).title()),
        "dependencia": df["COD_DEPE2"].map(DEPENDENCIAS),
        "rural": df["RURAL_RBD"].astype(int),
        "cod_region": df["COD_REG_RBD"],
        "region": df["COD_REG_RBD"].map(REGIONES),
        "comuna": df["NOM_COM_RBD"].map(lambda s: limpiar_texto(s).title()),
        "mat_total": df["MAT_TOTAL"],
        "mat_hombres": df["MAT_HOM_TOT"],
        "mat_mujeres": df["MAT_MUJ_TOT"],
        # Enseñanzas 1..8 según diccionario MINEDUC (ER en el .rar):
        # 1 parvularia · 2/3 básica niños/adultos · 4 especial · 5/6 media HC · 7/8 media TP
        "mat_parvularia": df["MAT_ENS_1"],
        "mat_basica": df["MAT_ENS_2"] + df["MAT_ENS_3"],
        "mat_especial": df["MAT_ENS_4"],
        "mat_media_hc": df["MAT_ENS_5"] + df["MAT_ENS_6"],
        "mat_media_tp": df["MAT_ENS_7"] + df["MAT_ENS_8"],
        "mat_extranjeros": df["MAT_EXT"],
        "cursos": df["CUR_SIM_TOT"] + df["CUR_COMB_TOT"],
    })
    out.to_csv(OUT / "matricula.csv", index=False)
    print(f"  matricula.csv: {len(out)} establecimientos, {out['mat_total'].sum():,} estudiantes")

    # Par para el módulo de cruce (R1-03): conteos por RBD vs directorio oficial.
    # Los conteos usan solo MAT_TOTAL>0 (sin filtro de estado) → quedan ~4 RBD reales
    # con matrícula pero sin estado "funcionando": las filas huérfanas del left join.
    todos = pd.read_csv(extraidos[0], encoding="utf-8-sig")
    todos.columns = [c.strip().upper() for c in todos.columns]
    conteos = todos[todos["MAT_TOTAL"] > 0]
    pd.DataFrame({
        "rbd": conteos["RBD"],
        "mat_total": conteos["MAT_TOTAL"],
        "mat_hombres": conteos["MAT_HOM_TOT"],
        "mat_mujeres": conteos["MAT_MUJ_TOT"],
    }).to_csv(OUT / "matricula_rbd.csv", index=False)
    out[["rbd", "nombre", "dependencia", "rural", "region", "comuna"]] \
        .to_csv(OUT / "directorio_establecimientos.csv", index=False)
    print(f"  matricula_rbd.csv: {len(conteos)} · directorio_establecimientos.csv: {len(out)} "
          f"({len(conteos) - len(out)} huérfanas para el left join)")


# ---------------------------------------------------------------- aire (SINCA)
def _series_sinca(macro, desde, hasta):
    """Baja una serie del recuperador SINCA; devuelve DataFrame fecha/valor o None."""
    url = (f"{SINCA}/cgi-bin/APUB-MMA/apub.tsindico2.cgi?outtype=xcl"
           f"&macro={macro}&from={desde}&to={hasta}")
    r = requests.get(url, headers=UA, timeout=120)
    if "Could not load macro" in r.text[:200] or not r.ok:
        return None
    df = pd.read_csv(io.StringIO(r.text), sep=";", dtype=str)
    if df.empty or "FECHA (YYMMDD)" not in df.columns:
        return None
    df = df.rename(columns={"FECHA (YYMMDD)": "fecha", "HORA (HHMM)": "hora"})
    valores = df.columns[2:5]
    # primera columna con dato: validados > preliminares > no validados
    df["valor"] = (df[valores].apply(lambda c: c.str.replace(",", ".", regex=False))
                   .apply(pd.to_numeric, errors="coerce").bfill(axis=1).iloc[:, 0])
    df["fecha"] = pd.to_datetime(df["fecha"], format="%y%m%d", errors="coerce")
    return df.dropna(subset=["fecha"])[["fecha", "hora", "valor"]]


def _utm_a_latlon(este, norte, huso, sur=True):
    """UTM (WGS84) → (lat, lon) en grados, fórmula estándar (sin pyproj)."""
    import math
    a, f, k0 = 6378137.0, 1 / 298.257223563, 0.9996
    e2 = f * (2 - f); ep2 = e2 / (1 - e2)
    x = este - 500000.0
    y = norte - (10000000.0 if sur else 0.0)
    m = y / k0
    mu = m / (a * (1 - e2 / 4 - 3 * e2**2 / 64 - 5 * e2**3 / 256))
    e1 = (1 - math.sqrt(1 - e2)) / (1 + math.sqrt(1 - e2))
    p1 = (mu + (3 * e1 / 2 - 27 * e1**3 / 32) * math.sin(2 * mu)
          + (21 * e1**2 / 16 - 55 * e1**4 / 32) * math.sin(4 * mu)
          + (151 * e1**3 / 96) * math.sin(6 * mu))
    n1 = a / math.sqrt(1 - e2 * math.sin(p1)**2)
    t1, c1 = math.tan(p1)**2, ep2 * math.cos(p1)**2
    r1 = a * (1 - e2) / (1 - e2 * math.sin(p1)**2)**1.5
    d = x / (n1 * k0)
    lat = p1 - (n1 * math.tan(p1) / r1) * (d**2 / 2 - (5 + 3 * t1 + 10 * c1 - 4 * c1**2 - 9 * ep2) * d**4 / 24
                                          + (61 + 90 * t1 + 298 * c1 + 45 * t1**2 - 252 * ep2 - 3 * c1**2) * d**6 / 720)
    lon = (d - (1 + 2 * t1 + c1) * d**3 / 6
           + (5 - 2 * c1 + 28 * t1 - 3 * c1**2 + 8 * ep2 + 24 * t1**2) * d**5 / 120) / math.cos(p1)
    return round(math.degrees(lat), 6), round((huso - 1) * 6 - 180 + 3 + math.degrees(lon), 6)


def _ficha_estacion(id_pagina):
    """Comuna, región y coordenadas desde la página oficial de una estación SINCA."""
    if not id_pagina:
        return {}
    t = requests.get(f"{SINCA}/index.php/estacion/index/id/{id_pagina}", headers=UA, timeout=60).text
    plano = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html.unescape(t)))
    ficha = {}
    m = re.search(r"SINCA » (Región[^»]+?) » ", plano)
    if m:
        ficha["region"] = limpiar_texto(m.group(1))
    m = re.search(r"Comuna (.+?) Coordenadas UTM", plano)
    if m:
        ficha["comuna"] = limpiar_texto(m.group(1))
    m = re.search(r"Coordenadas UTM (\d+) E (\d+) N", plano)
    if m:
        este, norte = map(float, m.groups())
        # Chile continental: huso 19 al este de 72°O, huso 18 al oeste. Se prueba 19 y,
        # si la longitud resultante cae fuera de su huso (< -72), se recalcula con 18.
        lat, lon = _utm_a_latlon(este, norte, 19)
        if lon < -72:
            lat, lon = _utm_a_latlon(este, norte, 18)
        ficha["latitud"], ficha["longitud"] = lat, lon
    return ficha


def _catalogo_sinca(max_estaciones=14):
    """Catálogo de series PM2.5 diarias y la selección FIJA de estaciones."""
    # 1. catálogo de series PM2.5 diarias + id de página por estación (páginas regionales)
    series, paginas = [], {}
    for reg in SINCA_REGIONES:
        r = requests.get(f"{SINCA}/index.php/region/index/id/{reg}", headers=UA, timeout=60)
        for m in re.finditer(r'estacion/index/id/(\d+)"[^>]*>([^<]+)<', r.text):
            # clave (región, nombre): hay nombres repetidos entre regiones («Centro», «Sur», «Bomberos»)
            paginas.setdefault((f"R{reg}", limpiar_texto(html.unescape(m.group(2)))), m.group(1))
        for m in re.finditer(r'header=([^&"]+)&amp;macropath=(\./[^&"]+/Cal/PM25)&amp;'
                             r'macro=PM25\.diario\.diario&amp;from=(\d+)&amp;to=(\d+)', r.text):
            nombre, path, f0, f1 = m.groups()
            series.append({"estacion": limpiar_texto(html.unescape(nombre)),
                           "path": path, "desde": f0, "hasta": f1})
        time.sleep(0.3)
    cat = pd.DataFrame(series).drop_duplicates("path")
    # selección FIJA (mismas 14 estaciones para aire_diario y aire_nuevos)
    cat = cat[(cat["desde"] <= "200101") & (cat["hasta"] >= "250101")]
    cat["region_codigo"] = cat["path"].str.split("/").str[1]
    # diversidad territorial: hasta 2 estaciones por región, orden estable
    cat = (cat.sort_values(["region_codigo", "estacion"])
              .groupby("region_codigo").head(2).head(max_estaciones))
    print(f"  {len(cat)} estaciones seleccionadas de {len(series)} series")
    return cat, paginas


def hacer_aire(desde="200101", hasta="251231", max_estaciones=14, salida="aire_diario.csv"):
    print(f"== aire (SINCA {desde}–{hasta} → {salida}) ==")
    cat, paginas = _catalogo_sinca(max_estaciones)

    # 2. PM2.5 diario + meteorología horaria agregada a diario. Los macros de
    # meteorología varían por estación: se leen de la página de cada estación.
    filas = []
    for _, e in cat.iterrows():
        pm = _series_sinca(f"{e.path}//PM25.diario.diario.ic", desde, hasta)
        if pm is None:
            print(f"  [sin PM2.5] {e.estacion}")
            continue
        dia = pm.set_index("fecha")[["valor"]].rename(columns={"valor": "pm25"})
        macros_met = []
        if (e.region_codigo, e.estacion) in paginas:
            rp = requests.get(f"{SINCA}/index.php/estacion/index/id/{paginas[(e.region_codigo, e.estacion)]}",
                              headers=UA, timeout=60)
            macros_met = re.findall(
                r'macropath=(\./[^&"]+/Met/(TEMP|RHUM))&amp;macro=(horario_\d+)', rp.text)
        for var, col in [("TEMP", "temp"), ("RHUM", "humedad")]:
            partes = []
            for path_met, v, macro in macros_met:
                if v != var:
                    continue
                serie = _series_sinca(f"{path_met}//{macro}.ic", desde, hasta)
                time.sleep(0.3)
                if serie is not None and serie["valor"].notna().any():
                    partes.append(serie)
            if partes:
                g = pd.concat(partes).groupby("fecha")["valor"]
                dia[f"{col}_media"] = g.mean().round(1)
                if var == "TEMP":
                    dia["temp_min"] = g.min().round(1)
                    dia["temp_max"] = g.max().round(1)
        dia["estacion"] = e.estacion
        filas.append(dia.reset_index())
        print(f"  {e.estacion}: {len(dia)} días, met={'sí' if len(dia.columns) > 2 else 'no'}")
        time.sleep(0.4)
    aire = pd.concat(filas, ignore_index=True)
    aire["fecha"] = aire["fecha"].dt.date
    cols = ["fecha", "estacion", "pm25", "temp_media", "temp_min", "temp_max", "humedad_media"]
    aire = aire.reindex(columns=cols).sort_values(["estacion", "fecha"])
    aire.to_csv(OUT / salida, index=False)
    if salida != "aire_diario.csv":
        print(f"  {salida}: {len(aire)} filas")
        return

    hacer_estaciones(cat, paginas)
    print(f"  aire_diario.csv: {len(aire)} filas")


# ---------------------------------------------------------------- fichas ChileAtiende
# Campos «clásicos» de una ficha y el título de sección con que se presentan.
_CAMPOS_FICHA = [("details", "Detalle"), ("beneficiaries", "¿A quién está dirigido?"),
                 ("requirements", "Requisitos"), ("cost", "Costo"), ("validity", "Vigencia"),
                 ("plazo", "Plazo"), ("online_guide", "Trámite en línea"),
                 ("office_guide", "En oficina"), ("phone_guide", "Por teléfono"),
                 ("mail_guide", "Por correo"), ("legal", "Marco legal")]


def _html_a_texto(fragmento):
    """HTML de ChileAtiende → texto plano: un párrafo por línea, viñetas con «- »."""
    t = fragmento or ""
    t = re.sub(r"\{\{paso:([^}]*)\}\}", r"\n### \1\n", t)
    t = t.replace("{{contenido:", "").replace("}}", "")
    t = re.sub(r"<li[^>]*>", "\n- ", t)
    t = re.sub(r"</?(p|div|br|ul|ol|h[1-6]|tr|table)[^>]*>", "\n", t)
    t = html.unescape(re.sub(r"<[^>]+>", " ", t))
    lineas = [limpiar_texto(l) for l in t.splitlines()]
    return "\n".join(l for l in lineas if len(l) > 1)


def _texto_ficha(html_crudo):
    """Texto de la ficha PRINCIPAL desde el JSON que la página trae en el atributo
    `page="…"`: objetivo + campos clásicos + secciones nuevas (metadata_newpages),
    cada sección con su título como «## ». Se excluyen a propósito `related_pages` y
    `master_page`: la versión anterior leía todo HTML escapado de la página y mezclaba
    el texto de fichas relacionadas (p. ej. Bono por Hijo dentro de Bono de Invierno)."""
    m = re.search(r'\bpage="([^"]+)"', html_crudo)
    if not m:
        return ""
    d = json.loads(html.unescape(m.group(1)))
    partes = []
    if (d.get("objective") or "").strip():
        partes.append(_html_a_texto(d["objective"]))
    for campo, titulo in _CAMPOS_FICHA:
        txt = _html_a_texto(d.get(campo))
        if txt:
            partes.append(f"## {titulo}\n{txt}")
    if d.get("metadata_newpages"):
        try:
            nuevos = json.loads(d["metadata_newpages"]).get("new_elements", [])
        except (ValueError, AttributeError):
            nuevos = []
        for grupo in nuevos:
            for secciones in grupo.values():
                for sec in secciones or []:
                    txt = _html_a_texto(sec.get("description"))
                    if txt:
                        titulo = limpiar_texto(sec.get("title") or "")
                        partes.append(f"## {titulo}\n{txt}" if titulo else txt)
    vistos, salida = set(), []
    for bloque in partes:              # sin párrafos repetidos (campos clásicos y nuevos a veces se duplican)
        lineas = [l for l in bloque.splitlines() if l.startswith("## ") or l not in vistos]
        vistos.update(lineas)
        if any(not l.startswith("## ") for l in lineas):
            salida.append("\n".join(lineas))
    return "\n\n".join(salida)


def hacer_fichas():
    print("== fichas (ChileAtiende) ==")
    indice = RAW / "fichas_indice.json"   # id → tema; borrar para volver a recorrer /temas
    if indice.exists():
        enlaces = json.loads(indice.read_text(encoding="utf-8"))
        temas = sorted(set(enlaces.values()))
    else:
        r = requests.get(f"{CHILEATIENDE}/temas", headers=UA, timeout=60)
        temas = sorted(set(re.findall(r'/temas/([0-9a-z-]+)', r.text)))
        enlaces = {}
        for tema in temas:
            rt = requests.get(f"{CHILEATIENDE}/temas/{tema}", headers=UA, timeout=60)
            for ruta in set(re.findall(r'/fichas/(\d+)-[a-z0-9-]+', rt.text)):
                enlaces.setdefault(ruta, tema)
            time.sleep(0.5)
        indice.write_text(json.dumps(enlaces, ensure_ascii=False, indent=0), encoding="utf-8")
    print(f"  {len(enlaces)} fichas en {len(temas)} temas")

    cache = RAW / "fichas"
    cache.mkdir(exist_ok=True)
    filas = []
    for fid, tema in sorted(enlaces.items(), key=lambda kv: int(kv[0])):
        try:
            pagina = cache / f"{fid}.html"
            if pagina.exists():
                crudo = pagina.read_text(encoding="utf-8")
            else:
                rf = requests.get(f"{CHILEATIENDE}/fichas/{fid}", headers=UA, timeout=60)
                crudo = rf.text
                pagina.write_text(crudo, encoding="utf-8")
                time.sleep(0.4)
            titulo = re.search(r"<h1[^>]*>(.*?)</h1>", crudo, re.S)
            inst = re.search(r'instituciones/[A-Z0-9]+"?>([^<]+)<', crudo)
            texto = _texto_ficha(crudo)
            if titulo and len(texto) > 300:
                filas.append({"id": int(fid), "titulo": limpiar_texto(titulo.group(1)),
                              "tema": tema,
                              "institucion": limpiar_texto(inst.group(1)) if inst else "",
                              "url": f"{CHILEATIENDE}/fichas/{fid}",
                              "n_palabras": len(texto.split()), "texto": texto})
        except requests.RequestException as e:
            print(f"  [error] ficha {fid}: {e}")
    df = pd.DataFrame(filas).drop_duplicates("titulo")
    df.to_csv(OUT / "fichas.csv", index=False)
    print(f"  fichas.csv: {len(df)} fichas, mediana {df['n_palabras'].median():.0f} palabras")


# ---------------------------------------------------------------- reclamos SERNAC
def hacer_reclamos(n=20000):
    print("== reclamos (SERNAC 2011) ==")
    crudo = descargar(URL_RECLAMOS, "reclamos_2011.csv")
    df = pd.read_csv(crudo, sep=";", encoding="latin-1", dtype=str)
    df.columns = ["comuna", "cod_region", "region", "mercado", "categoria_mercado",
                  "producto", "motivo_legal", "categoria_motivo", "resultado"]
    df = df.dropna(subset=["mercado", "resultado"]).sample(n=n, random_state=SEED)
    for c in df.columns:
        df[c] = df[c].map(limpiar_texto)
    df.sort_index().to_csv(OUT / "reclamos.csv", index=False)
    print(f"  reclamos.csv: {len(df)} filas (muestra de la base 2011, seed={SEED})")


# ---------------------------------------------------------------- sismos (USGS)
URL_SISMOS = ("https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv"
              "&starttime=2020-01-01&endtime=2025-12-31"
              "&minlatitude=-56&maxlatitude=-17&minlongitude=-76&maxlongitude=-66"
              "&minmagnitude=4.5&orderby=time-asc")


def hacer_sismos():
    print("== sismos (catálogo USGS, Chile 2020-2025, M>=4.5) ==")
    crudo = descargar(URL_SISMOS, "sismos_usgs.csv")
    df = pd.read_csv(crudo)
    out = pd.DataFrame({
        "fecha": pd.to_datetime(df["time"]).dt.date,
        "latitud": df["latitude"].round(3),
        "longitud": df["longitude"].round(3),
        "profundidad_km": df["depth"].round(1),
        "magnitud": df["mag"],
        "lugar": df["place"].fillna(""),
    })
    out["zona"] = pd.cut(out["latitud"], bins=[-90, -45, -35, -27, 0],
                         labels=["austral", "sur", "centro", "norte"])
    out = out.sort_values("fecha").reset_index(drop=True)
    out.to_csv(OUT / "sismos.csv", index=False)
    print(f"  sismos.csv: {len(out)} eventos, magnitud {out.magnitud.min()}–{out.magnitud.max()}")


def hacer_estaciones(cat=None, paginas=None):
    """estaciones.csv: atributos oficiales de las estaciones seleccionadas."""
    if cat is None:
        print("== estaciones (SINCA) ==")
        cat, paginas = _catalogo_sinca()
    j = descargar(f"{SINCA}/index.php/json/listadomapa2k19/", "sinca_estaciones.json")
    mapa = pd.read_json(j)[["nombre", "comuna", "region", "latitud", "longitud"]]
    for c in ["nombre", "comuna", "region"]:
        mapa[c] = mapa[c].map(limpiar_texto)
    mapa["clave"] = mapa["nombre"].map(lambda s: sin_tildes(s).lower().strip())
    # La página oficial de cada estación es la fuente de verdad para comuna y región
    # (el JSON del mapa omite estaciones y repite nombres entre regiones: un cruce solo
    # por nombre ubicó «Bomberos» de Tocopilla en Quillota). Coordenadas: del mapa si
    # calza nombre + región; si no, de las UTM de la página.
    filas_est = []
    for _, e in cat.iterrows():
        ficha = _ficha_estacion(paginas.get((e.region_codigo, e.estacion)))
        clave = sin_tildes(e.estacion).lower().strip()
        en_mapa = mapa[(mapa["clave"] == clave) & (mapa["region"] == ficha.get("region"))]
        if not ficha:
            # sin página (el nombre del enlace difiere, p. ej. «Ñielol»): se usa el mapa
            # solo si el nombre es único en todo el país
            unico = mapa[mapa["clave"] == clave]
            if len(unico) == 1:
                ficha = {"comuna": unico.iloc[0]["comuna"], "region": unico.iloc[0]["region"]}
                en_mapa = unico
            else:
                print(f"  ⚠️ {e.estacion}: sin página ni nombre único en el mapa — revisar a mano")
        if len(en_mapa):
            lat, lon = en_mapa.iloc[0][["latitud", "longitud"]]
        else:
            lat, lon = ficha.get("latitud"), ficha.get("longitud")
        filas_est.append({"estacion": e.estacion, "region_codigo": e.region_codigo,
                          "comuna": ficha.get("comuna"), "region": ficha.get("region"),
                          "latitud": lat, "longitud": lon})
        time.sleep(0.3)
    est = pd.DataFrame(filas_est)
    est.to_csv(OUT / "estaciones.csv", index=False)
    print(f"  estaciones.csv: {len(est)} estaciones")


# ---------------------------------------------------------------- aire 2026 (datos «nuevos»)
def hacer_aire_nuevos():
    """Enero–septiembre 2026 de las mismas estaciones: datos que el modelo NO vio
    (R2-09 despliegue/monitoreo). La serie de entrenamiento queda en años completos."""
    hacer_aire(desde="260101", hasta="260930", salida="aire_nuevos.csv")


# ---------------------------------------------------------------- matrícula sucia (R1-04)
def hacer_matricula_sucia(n=1500):
    """Muestra de matricula.csv con errores TÍPICOS de planillas reales, inyectados con
    semilla: espacios y mayúsculas, sinónimos de categorías, números como texto con
    separador de miles, faltantes, duplicados exactos y valores imposibles."""
    import numpy as np
    rng = np.random.default_rng(SEED)
    df = pd.read_csv(OUT / "matricula.csv")
    df = df.sample(n=n, random_state=SEED)[
        ["rbd", "nombre", "dependencia", "rural", "region", "comuna",
         "mat_total", "mat_hombres", "mat_mujeres"]].reset_index(drop=True)
    df = df.astype({"rural": object, "mat_total": object, "mat_hombres": object})

    def idx(frac):
        return rng.choice(len(df), size=int(len(df) * frac), replace=False)

    for i in idx(0.10):                      # espacios y mayúsculas en comuna
        df.at[i, "comuna"] = "  " + str(df.at[i, "comuna"]).upper() + " "
    sinon = {"Metropolitana": ["RM", "Región Metropolitana", "metropolitana"],
             "Valparaíso": ["Valparaiso", "V Región"], "Biobío": ["Bio Bio", "Biobio"]}
    for i in idx(0.12):                      # sinónimos de región
        r = df.at[i, "region"]
        if r in sinon:
            df.at[i, "region"] = rng.choice(sinon[r])
    for i in idx(0.08):                      # dependencia abreviada
        df.at[i, "dependencia"] = {"Particular subvencionado": "Part. Subv.",
                                   "Particular pagado": "Part. Pagado",
                                   "Municipal": "MUNICIPAL"}.get(df.at[i, "dependencia"],
                                                                 df.at[i, "dependencia"])
    df["rural"] = df["rural"].map({0: "No", 1: "Sí"})
    for i in idx(0.06):                      # rural codificado de otra forma
        df.at[i, "rural"] = {"No": "0", "Sí": "1"}[df.at[i, "rural"]]
    for i in idx(0.07):                      # número como texto con separador de miles
        v = int(df.at[i, "mat_total"])
        if v >= 1000:
            df.at[i, "mat_total"] = f"{v:,}".replace(",", ".")
    for i in idx(0.04):                      # faltantes
        df.at[i, "mat_total"] = np.nan
    for i in idx(0.01):                      # «sin información» escrito a mano
        df.at[i, "mat_total"] = "s/i"
    for i in idx(0.005):                     # valores imposibles
        df.at[i, "mat_hombres"] = -1
    dup = df.iloc[idx(0.03)]                 # duplicados exactos
    df = pd.concat([df, dup]).sample(frac=1, random_state=SEED).reset_index(drop=True)
    df.to_csv(OUT / "matricula_sucia.csv", index=False)
    print(f"  matricula_sucia.csv: {len(df)} filas ({len(dup)} duplicados inyectados)")


# ---------------------------------------------------------------- manifiesto de procedencia
PROCEDENCIA = {
    "matricula.csv": ("MINEDUC · Resumen de matrícula por establecimiento 2025 (oficial, filtro CEM)", URL_MATRICULA, "Datos abiertos MINEDUC"),
    "matricula_rbd.csv": ("Derivado de MINEDUC 2025: conteos por RBD sin filtro de estado", URL_MATRICULA, "Datos abiertos MINEDUC"),
    "directorio_establecimientos.csv": ("Derivado de MINEDUC 2025: directorio de establecimientos funcionando", URL_MATRICULA, "Datos abiertos MINEDUC"),
    "matricula_sucia.csv": ("Derivado de matricula.csv con errores inyectados (seed 42) para R1-04", URL_MATRICULA, "Datos abiertos MINEDUC"),
    "aire_diario.csv": ("SINCA/MMA · PM2.5 diario + meteorología agregada, 14 estaciones, 2020–2025", SINCA, "Datos públicos MMA"),
    "aire_nuevos.csv": ("SINCA/MMA · mismas estaciones, ene–sep 2026 (datos no vistos)", SINCA, "Datos públicos MMA"),
    "estaciones.csv": ("SINCA/MMA · atributos de las 14 estaciones (JSON del mapa oficial)", SINCA, "Datos públicos MMA"),
    "fichas.csv": ("ChileAtiende · 245 fichas de trámites con texto completo, 18 temas", CHILEATIENDE, "Contenido público del Estado de Chile"),
    "reclamos.csv": ("SERNAC · muestra 20k de la base de reclamos 2011 (dato HISTÓRICO: SERNAC no publica una base abierta más reciente)", URL_RECLAMOS, "datos.gob.cl"),
    "sismos.csv": ("USGS · catálogo FDSN, sismos M≥4,5 en Chile 2020–2025", URL_SISMOS, "Dominio público (USGS)"),
}


def hacer_manifiesto():
    """Escribe data/rearmado/MANIFEST.json: filas, columnas, sha256 y procedencia."""
    import hashlib, json
    from datetime import date
    entradas = []
    for archivo, (desc, url, licencia) in PROCEDENCIA.items():
        f = OUT / archivo
        if not f.exists():
            continue
        df = pd.read_csv(f, low_memory=False)
        entradas.append({"archivo": archivo, "descripcion": desc, "fuente": url,
                         "licencia": licencia, "filas": len(df), "columnas": list(df.columns),
                         "sha256": hashlib.sha256(f.read_bytes()).hexdigest(),
                         "generado": date.fromtimestamp(f.stat().st_mtime).isoformat()})
    (OUT / "MANIFEST.json").write_text(json.dumps(entradas, ensure_ascii=False, indent=2) + "\n")
    print(f"  MANIFEST.json: {len(entradas)} archivos")


def hacer_publicar():
    """Copia los CSV curados + MANIFEST.json a data/ (de ahí los baja el patrón
    «en vivo o caché» de los notebooks vía raw.githubusercontent.com)."""
    import shutil
    hacer_manifiesto()
    destino = BASE / "data"
    for archivo in [*PROCEDENCIA, "MANIFEST.json"]:
        if (OUT / archivo).exists():
            shutil.copy2(OUT / archivo, destino / archivo)
    print(f"  publicados en {destino}/ ({len(PROCEDENCIA)} datasets + MANIFEST.json)")


FUENTES = {"matricula": hacer_matricula, "aire": hacer_aire,
           "aire_nuevos": hacer_aire_nuevos, "estaciones": hacer_estaciones, "fichas": hacer_fichas,
           "reclamos": hacer_reclamos, "sismos": hacer_sismos,
           "matricula_sucia": hacer_matricula_sucia, "manifiesto": hacer_manifiesto,
           "publicar": hacer_publicar}

if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)
    pedidas = sys.argv[1:] or ["todo"]
    for nombre in (FUENTES if "todo" in pedidas else pedidas):
        FUENTES[nombre]()
