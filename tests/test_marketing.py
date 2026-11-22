"""Suite del ecosistema de marketing y comunicación.

Solo stdlib. Se corre desde la raíz del repo:

    python3 -m unittest discover -s tests -v

Cubre: esquema de perfiles, integridad del índice de experimentos,
plantillas completas (campaña, estrategia, calendario), biblioteca
(12 ganchos, 11 formatos) y ausencia de secretos en el contenido.
"""

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

import validate as val  # noqa: E402


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


class TestValidacionCompleta(unittest.TestCase):
    def test_todo_el_repo_valido(self):
        self.assertEqual(val.validate_all(REPO), [])


if __name__ == "__main__":
    unittest.main()
