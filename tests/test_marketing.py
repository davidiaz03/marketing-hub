"""Suite del ecosistema de marketing y comunicación.

Solo stdlib. Se corre desde la raíz del repo:

    python3 -m unittest discover -s tests -v

Cubre: esquema de perfiles, integridad del índice de experimentos,
plantillas completas (campaña, estrategia, calendario), biblioteca
(12 ganchos, 11 formatos) y ausencia de secretos en el contenido.
También la sincronización de la medición (scripts/sync_medicion.py):
el resumen se genera desde un JSON ficticio, las cifras coinciden con
el JSON y sin informe falla con mensaje claro, no rompe.
"""

import contextlib
import io
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

import validate as val  # noqa: E402
import sync_medicion as sm  # noqa: E402


class TestPerfiles(unittest.TestCase):
    def test_perfiles_semilla_validos(self):
        for path in sorted((REPO / "profiles").glob("*.json")):
            with self.subTest(perfil=path.name):
                self.assertEqual(val.validate_profile(path), [])

    def test_perfil_sin_campo_obligatorio_falla(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = REPO / "profiles" / "memorial.json"
            dst = Path(tmp) / "memorial.json"
            data = json.loads(src.read_text(encoding="utf-8"))
            del data["restricciones"]
            dst.write_text(json.dumps(data), encoding="utf-8")
            errors = val.validate_profile(dst)
            self.assertTrue(any("restricciones" in e for e in errors),
                            errors)

    def test_perfil_con_estado_de_canal_invalido_falla(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = REPO / "profiles" / "personal.json"
            dst = Path(tmp) / "personal.json"
            data = json.loads(src.read_text(encoding="utf-8"))
            data["canales"][0]["estado"] = "a_veces"
            dst.write_text(json.dumps(data), encoding="utf-8")
            errors = val.validate_profile(dst)
            self.assertTrue(any("estado" in e for e in errors), errors)

    def test_perfil_con_id_distinto_al_archivo_falla(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = REPO / "profiles" / "personal.json"
            dst = Path(tmp) / "otro.json"
            shutil.copy(src, dst)
            errors = val.validate_profile(dst)
            self.assertTrue(any("no coincide" in e for e in errors), errors)

    def test_perfil_personal_marca_por_definir(self):
        """El perfil personal no inventa: público y pilares quedan por definir."""
        data = json.loads(
            (REPO / "profiles" / "personal.json").read_text(encoding="utf-8"))
        self.assertEqual(data["publico"]["descripcion"], "por definir")
        self.assertEqual(data["pilares_mensaje"][0]["pilar"], "por definir")
        kpis = [o["kpi"] for o in data["objetivos"]]
        self.assertIn("por definir", kpis)


class TestExperimentos(unittest.TestCase):
    def test_indice_integro(self):
        self.assertEqual(val.validate_experiments_index(REPO), [])

    def test_indice_con_archivo_inexistente_falla(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            exp = root / "experiments"
            exp.mkdir()
            (exp / "index.json").write_text(json.dumps({
                "experiments": [{
                    "id": "x", "titulo": "x", "tipo": "observacional",
                    "estado": "cerrado", "fecha": "2026-11-21",
                    "perfil": "memorial",
                    "archivo": "experiments/no-existe.md",
                    "veredicto": "x",
                }]}), encoding="utf-8")
            errors = val.validate_experiments_index(root)
            self.assertTrue(any("no existe" in e for e in errors), errors)

    def test_archivo_sin_indice_falla(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            exp = root / "experiments"
            exp.mkdir()
            (exp / "index.json").write_text(
                json.dumps({"experiments": []}), encoding="utf-8")
            (exp / "2026-11-21-huerfano.md").write_text("# Huérfano\n",
                                                        encoding="utf-8")
            errors = val.validate_experiments_index(root)
            self.assertTrue(any("no está en el índice" in e for e in errors),
                            errors)


class TestPlantillas(unittest.TestCase):
    def test_plantilla_campana_completa(self):
        self.assertEqual(val.validate_sections(
            REPO / "campaigns" / "plantilla-campana.md",
            val.CAMPAIGN_SECTIONS), [])

    def test_ejemplo_campana_completo(self):
        packs = list((REPO / "campaigns").glob("*/pack.md"))
        self.assertTrue(packs, "debe existir al menos un pack de ejemplo")
        for pack in packs:
            with self.subTest(pack=str(pack.relative_to(REPO))):
                self.assertEqual(
                    val.validate_sections(pack, val.CAMPAIGN_SECTIONS), [])

    def test_campana_sin_seccion_falla(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "pack.md"
            path.write_text("## Objetivo\n\n## Público\n", encoding="utf-8")
            errors = val.validate_sections(path, val.CAMPAIGN_SECTIONS)
            self.assertTrue(any("Medición" in e for e in errors), errors)

    def test_plantilla_estrategia_completa(self):
        self.assertEqual(val.validate_sections(
            REPO / "strategy" / "plantilla-estrategia.md",
            val.STRATEGY_SECTIONS), [])

    def test_estrategia_personal_completa(self):
        self.assertEqual(val.validate_sections(
            REPO / "strategy" / "personal-estrategia.md",
            val.STRATEGY_SECTIONS), [])

    def test_plantilla_calendario_con_cabecera(self):
        text = (REPO / "calendar" / "plantilla-semana.md"
                ).read_text(encoding="utf-8")
        self.assertIn(val.CALENDAR_HEADER, text)


class TestBiblioteca(unittest.TestCase):
    def test_doce_ganchos_y_once_formatos(self):
        self.assertEqual(val.validate_library(REPO), [])


class TestSinSecretos(unittest.TestCase):
    def test_contenido_sin_secretos(self):
        self.assertEqual(val.scan_no_secrets(REPO), [])


class TestSyncMedicion(unittest.TestCase):
    def _informe_fixture(self, fecha="2026-11-21"):
        return {
            "fecha": fecha,
            "perfil": "Memorial de la Denuncia",
            "ventana": {"desde": "2026-11-14", "hasta": fecha},
            "plataformas": [
                {
                    "plataforma": "Facebook",
                    "via": "lectura pública por URL",
                    "senial": "reacciones",
                    "seguidores": None,
                    "n_ventana": 0,
                    "n_base": 49,
                    "mediana": 17,
                    "mediana_fiable": True,
                    "medianas_tipo": {
                        "reel": {"mediana": 60.0, "n": 12},
                        "foto": {"mediana": 14.5, "n": 32},
                    },
                    "ventana": [],
                    "top": [],
                    "bottom": [],
                    "patron_hora_dia": None,
                },
                {
                    "plataforma": "Instagram",
                    "via": "lectura pública del perfil",
                    "senial": "likes",
                    "seguidores": 4682,
                    "n_ventana": 2,
                    "n_base": 83,
                    "mediana": 22,
                    "mediana_fiable": True,
                    "medianas_tipo": {
                        "reel": {"mediana": 62, "n": 39},
                        "carrusel": {"mediana": 14, "n": 37},
                    },
                    "ventana": [],
                    "top": [{
                        "titulo": "Reel de prueba",
                        "url": "https://www.instagram.com/reel/Prueba123/",
                        "tipo": "reel",
                        "publicado": fecha,
                        "senial": 222,
                        "multiplicador": 10.09,
                        "multiplicador_tipo": 3.58,
                        "clasificacion": "destacado",
                        "comentarios": 20,
                        "compartidos": None,
                        "visualizaciones": None,
                        "alcance": None,
                        "interacciones": None,
                        "fuente": "instagram-publico",
                    }],
                    "bottom": [{
                        "titulo": "Carrusel flojo",
                        "url": "https://www.instagram.com/p/Flojo123/",
                        "tipo": "carrusel",
                        "publicado": fecha,
                        "senial": 10,
                        "multiplicador": 0.45,
                        "multiplicador_tipo": 0.71,
                        "clasificacion": "flojo",
                        "comentarios": 1,
                        "compartidos": None,
                        "visualizaciones": None,
                        "alcance": None,
                        "interacciones": None,
                        "fuente": "instagram-publico",
                    }],
                    "patron_hora_dia": None,
                },
            ],
            "hallazgos": [{
                "texto": "En Instagram, los reels rinden 4.4x la mediana "
                         "de carruseles",
                "evidencia": "mediana reel: 62 likes (n=39); mediana "
                             "carrusel: 14 likes (n=37)",
            }],
            "bloqueos": [{
                "plataforma": "Facebook",
                "via": "pages",
                "error": "pages list devolvió 0 Páginas",
                "que_falta": "que el conector descubra la Página",
            }],
            "fallos": [],
        }

    def _escribir_informe(self, research_dir, fecha="2026-11-21"):
        path = Path(research_dir) / f"medicion-{fecha}.json"
        path.write_text(
            json.dumps(self._informe_fixture(fecha), ensure_ascii=False),
            encoding="utf-8")
        return path

    def test_sync_con_json_ficticio_genera_resumen(self):
        with tempfile.TemporaryDirectory() as tmp:
            research = Path(tmp) / "research"
            research.mkdir()
            self._escribir_informe(research)
            salida = Path(tmp) / "medicion-ultima.md"
            origen, destino = sm.sincronizar(
                research_dir=research, salida=salida)
            self.assertEqual(destino, salida)
            texto = salida.read_text(encoding="utf-8")
            self.assertIn("222 likes", texto)
            self.assertIn("10,09x", texto)
            self.assertIn("DESTACADO", texto)
            self.assertIn("FLOJO", texto)
            self.assertIn("Mediana: 22 likes", texto)
            self.assertIn("Mediana: 17 reacciones", texto)
            self.assertIn("4.4x", texto)
            self.assertIn("medicion-2026-11-21.json", texto)
            self.assertIn("sync_medicion.py", texto)

    def test_cifras_del_resumen_coinciden_con_json(self):
        """Cruce programático: cada cifra del JSON aparece en el resumen."""
        with tempfile.TemporaryDirectory() as tmp:
            research = Path(tmp) / "research"
            research.mkdir()
            informe = self._escribir_informe(research)
            salida = Path(tmp) / "medicion-ultima.md"
            sm.sincronizar(research_dir=research, salida=salida)
            datos = json.loads(informe.read_text(encoding="utf-8"))
            texto = salida.read_text(encoding="utf-8")
            for plat in datos["plataformas"]:
                self.assertIn(
                    f"Mediana: {sm.fmt_num(plat['mediana'])} "
                    f"{plat['senial']}", texto)
                self.assertIn(f"Base de mediana: {plat['n_base']}", texto)
                for post in plat["top"] + plat["bottom"]:
                    self.assertIn(
                        f"{sm.fmt_num(post['senial'])} {plat['senial']}",
                        texto)
                    self.assertIn(
                        f"{sm.fmt_num(post['multiplicador'])}x", texto)
                    self.assertIn(post["url"], texto)
            for hallazgo in datos["hallazgos"]:
                self.assertIn(hallazgo["texto"], texto)
                self.assertIn(hallazgo["evidencia"], texto)

    def test_elige_el_informe_mas_reciente(self):
        with tempfile.TemporaryDirectory() as tmp:
            research = Path(tmp) / "research"
            research.mkdir()
            self._escribir_informe(research, fecha="2026-11-14")
            self._escribir_informe(research, fecha="2026-11-21")
            salida = Path(tmp) / "medicion-ultima.md"
            origen, _ = sm.sincronizar(
                research_dir=research, salida=salida)
            self.assertEqual(origen.name, "medicion-2026-11-21.json")
            self.assertIn("2026-11-21",
                          salida.read_text(encoding="utf-8"))

    def test_sincronizacion_determinista(self):
        with tempfile.TemporaryDirectory() as tmp:
            research = Path(tmp) / "research"
            research.mkdir()
            self._escribir_informe(research)
            salida = Path(tmp) / "medicion-ultima.md"
            sm.sincronizar(research_dir=research, salida=salida)
            primera = salida.read_bytes()
            sm.sincronizar(research_dir=research, salida=salida)
            self.assertEqual(salida.read_bytes(), primera)

    def test_sin_informe_falla_con_mensaje_claro(self):
        with tempfile.TemporaryDirectory() as tmp:
            research = Path(tmp) / "research"
            research.mkdir()
            salida = Path(tmp) / "medicion-ultima.md"
            with self.assertRaises(sm.SyncError) as ctx:
                sm.sincronizar(research_dir=research, salida=salida)
            self.assertIn("no se encontró ningún informe", str(ctx.exception))
            self.assertFalse(salida.exists())
            # Y por CLI: exit 2, sin traza.
            err = io.StringIO()
            with contextlib.redirect_stderr(err):
                codigo = sm.main(["--research-dir", str(research),
                                  "--salida", str(salida), "--quiet"])
            self.assertEqual(codigo, 2)
            self.assertIn("no se encontró ningún informe", err.getvalue())
            self.assertNotIn("Traceback", err.getvalue())

    def test_json_invalido_falla_sin_romper(self):
        with tempfile.TemporaryDirectory() as tmp:
            research = Path(tmp) / "research"
            research.mkdir()
            (research / "medicion-2026-11-21.json").write_text(
                "{ esto no es json", encoding="utf-8")
            salida = Path(tmp) / "medicion-ultima.md"
            with self.assertRaises(sm.SyncError) as ctx:
                sm.sincronizar(research_dir=research, salida=salida)
            self.assertIn("no es un JSON válido", str(ctx.exception))
            self.assertFalse(salida.exists())

    def test_informe_sin_estructura_falla_con_mensaje_claro(self):
        with tempfile.TemporaryDirectory() as tmp:
            research = Path(tmp) / "research"
            research.mkdir()
            (research / "medicion-2026-11-21.json").write_text(
                json.dumps({"fecha": "2026-11-21"}), encoding="utf-8")
            salida = Path(tmp) / "medicion-ultima.md"
            with self.assertRaises(sm.SyncError) as ctx:
                sm.sincronizar(research_dir=research, salida=salida)
            self.assertIn("falta la clave", str(ctx.exception))

    def test_fmt_num(self):
        self.assertEqual(sm.fmt_num(222), "222")
        self.assertEqual(sm.fmt_num(60.0), "60")
        self.assertEqual(sm.fmt_num(14.5), "14,5")
        self.assertEqual(sm.fmt_num(10.09), "10,09")
        self.assertEqual(sm.fmt_num(1.0), "1")
        self.assertEqual(sm.fmt_num(None), "s/d")

    def test_resumen_real_valido_y_fuera_del_indice(self):
        """El resumen sincronizado existe, cita su fuente y no rompe el
        índice de experimentos (no es un experimento)."""
        resumen = REPO / "experiments" / "medicion-ultima.md"
        self.assertTrue(resumen.is_file())
        self.assertEqual(val.validate_medicion_summary(REPO), [])
        self.assertEqual(val.validate_experiments_index(REPO), [])
        texto = resumen.read_text(encoding="utf-8")
        self.assertIn("222 likes", texto)
        self.assertIn("10,09x", texto)

    def test_resumen_sin_fuente_falla_validacion(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            exp = root / "experiments"
            exp.mkdir()
            (exp / "medicion-ultima.md").write_text(
                "# Resumen sin fuente\n\n222 likes.\n", encoding="utf-8")
            errors = val.validate_medicion_summary(root)
            self.assertTrue(any("informe fuente" in e for e in errors),
                            errors)


class TestValidacionCompleta(unittest.TestCase):
    def test_todo_el_repo_valido(self):
        self.assertEqual(val.validate_all(REPO), [])


if __name__ == "__main__":
    unittest.main()
