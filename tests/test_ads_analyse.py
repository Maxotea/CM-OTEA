"""La lecture chiffrée des campagnes : statistiques justes, verdicts alignés sur le skill cm-meta-ads."""

import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import ads_analyse as aa  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent

SPEC = {
    "client": "otea-production",
    "slug": "essai",
    "titre": "Essai",
    "objectif": "OUTCOME_ENGAGEMENT",
    "budget": {"type": "total", "montant_eur": 42, "debut": "2026-11-16", "fin": "2026-11-22"},
    "kpi": {"cout_par_lead_cible_eur": {"moyen": 42, "bien": 21, "wow": 14}},
}


def ligne(nom, depense, impressions, clics, resultats=0, reach=None, frequency=None):
    l = {"id": nom, "name": nom, "amount_spent": str(depense), "impressions": str(impressions),
         "clicks": str(clics), "results": {"indicator": "x", "values": [{"value": resultats}]},
         "reach": str(reach if reach is not None else impressions // 2)}
    if frequency is not None:
        l["frequency"] = frequency
    return l


def test_nombre_accepte_toutes_les_formes_meta():
    assert aa.nombre("12,5") == 12.5
    assert aa.nombre({"values": [{"value": "3"}]}) == 3
    assert aa.nombre(None) == 0
    assert aa.nombre("n/a") == 0


def test_releve_brut_du_connecteur():
    brut = {"ad_entities": json.dumps([ligne("A", 1, 100, 2)])}
    assert aa.lignes_du_releve(brut)[0]["name"] == "A"


def test_wilson_encadre_la_proportion():
    bas, haut = aa.wilson(20, 1000)
    assert bas < 0.02 < haut
    assert 0.012 < bas < 0.014 and 0.029 < haut < 0.032


def test_taille_echantillon_classique():
    # 1,5 % contre 1,95 % : de l'ordre de 13 000 impressions par pub (formule à deux proportions)
    n = aa.taille_echantillon(0.015, 0.30)
    assert 12500 < n < 13800


def test_proba_meilleure_tranche_un_ecart_net():
    a = aa.pub_depuis_ligne(ligne("A", 10, 5000, 150))
    b = aa.pub_depuis_ligne(ligne("B", 10, 5000, 60))
    pa, pb = aa.proba_meilleure([a, b])
    assert pa > 0.99 and abs(pa + pb - 1) < 1e-9


def test_apprentissage_on_ne_touche_a_rien():
    d = aa.diagnostic(SPEC, [ligne("A", 5, 900, 10)], date(2026, 11, 17), reperes={})
    assert d["phase"] == "apprentissage"
    assert d["actions"][0].startswith("NE RIEN TOUCHER")


def test_surdepense_coupe_d_office():
    # jour 2 sur 7 : 12 € prévus à date, 20 € dépensés
    d = aa.diagnostic(SPEC, [ligne("A", 20, 3000, 30)], date(2026, 11, 17), reperes={})
    assert any(a.startswith("COUPER") for a in d["actions"])


def test_aucune_diffusion_demande_les_erreurs():
    d = aa.diagnostic(SPEC, [ligne("A", 0, 0, 0)], date(2026, 11, 18), reperes={})
    assert any("ads_get_errors" in a for a in d["actions"])


def test_lassitude_au_dela_de_trois():
    d = aa.diagnostic(SPEC, [ligne("A", 20, 4000, 40, frequency=3.6)], date(2026, 11, 20), reperes={})
    assert any(a.startswith("REMPLACER") for a in d["actions"])


def test_decision_sans_prospects_reclame_la_donnee():
    d = aa.diagnostic(SPEC, [ligne("A", 40, 6000, 60)], date(2026, 11, 22), reperes={})
    assert d["phase"] == "decision"
    assert d["actions"][0].startswith("DONNÉE MANQUANTE")


def test_decision_paliers_de_la_spec():
    lignes = [ligne("A", 42, 6000, 60)]
    wow = aa.diagnostic(SPEC, lignes, date(2026, 11, 22), prospects=3, reperes={})
    assert "palier wow" in wow["actions"][0] and "+20 %" in wow["actions"][0]
    bien = aa.diagnostic(SPEC, lignes, date(2026, 11, 22), prospects=2, reperes={})
    assert "palier bien" in bien["actions"][0]
    zero = aa.diagnostic(SPEC, lignes, date(2026, 11, 22), prospects=0, reperes={})
    assert zero["actions"][0].startswith("COUPER")


def test_campagne_terminee_ne_propose_pas_de_hausse():
    d = aa.diagnostic(SPEC, [ligne("A", 42, 6000, 60)], date(2026, 11, 30), prospects=3, reperes={})
    assert d["phase"] == "terminee"
    assert "+20 %" not in d["actions"][0]


def test_repere_ctr_ne_juge_qu_en_decision():
    rep = {"otea-production": {"ctr_min": 0.02, "source": "test"}}
    faible = [ligne("A", 40, 8000, 40)]  # 0,5 %
    assert not any("REMPLACER" in a for a in aa.diagnostic(SPEC, faible, date(2026, 11, 19), reperes=rep)["actions"])
    assert any("REMPLACER" in a for a in aa.diagnostic(SPEC, faible, date(2026, 11, 22), reperes=rep)["actions"])


def test_reperes_du_depot_sont_sources():
    reperes = json.loads((ROOT / "campagnes/reperes.json").read_text(encoding="utf-8"))["reperes"]
    for client, r in reperes.items():
        assert r.get("source"), f"{client} : un repère sans source n'a rien à faire dans reperes.json"
