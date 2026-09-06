"""Les règles de remplacement des carrousels du mercredi, testées sans Metricool."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import publier  # noqa: E402

MERCREDI = "2026-09-09T18:00:00"


def _post(pid, dt=MERCREDI, media=1, type_="POST", draft=True, auto=False, status="PENDING"):
    return {"id": pid, "draft": draft, "autoPublish": auto,
            "publicationDate": {"dateTime": dt},
            "media": [f"https://cdn/{pid}-{i}.jpg" for i in range(media)],
            "instagramData": {"type": type_},
            "providers": [{"network": "instagram", "status": status}]}


def test_carrousels_existants_se_reconnaissent_au_creneau_et_au_nombre_de_medias():
    posts = [_post(1, media=3), _post(2, media=1), _post(3, dt="2026-09-09T12:00:00", media=4)]
    assert [p["id"] for p in publier.carrousels_existants(posts, MERCREDI)] == [1]


def test_poste_du_jour_ne_remplace_que_le_post_simple_en_brouillon():
    posts = [
        _post(1),                                  # post feed simple en brouillon : remplaçable
        _post(2, type_="REEL"),                    # un reel coûte un tournage : jamais
        _post(3, type_="STORY"),                   # une story ne consomme pas le quota feed
        _post(4, media=3),                         # déjà un carrousel
        _post(5, draft=False, auto=True),          # validé par le client : lui appartient
        _post(6, status="PUBLISHED"),              # déjà parti
        _post(7, media=0),                         # sans média : remplaçable aussi
    ]
    assert [p["id"] for p in publier.poste_du_jour(posts)] == [1, 7]


def test_normaliser_accepte_les_formes_de_reponse_connues(monkeypatch):
    monkeypatch.setenv("METRICOOL_TOKEN", "t")
    reponses = iter([
        "https://cdn/normalisee.jpg",
        {"data": "https://cdn/data.jpg"},
        {"result": {"url": "https://cdn/result.jpg"}},
        {"autre": 1},
    ])
    monkeypatch.setattr(publier, "_req", lambda *a, **k: next(reponses))
    assert publier.normaliser("https://src/1.jpg") == "https://cdn/normalisee.jpg"
    assert publier.normaliser("https://src/1.jpg") == "https://cdn/data.jpg"
    assert publier.normaliser("https://src/1.jpg") == "https://cdn/result.jpg"
    assert publier.normaliser("https://src/1.jpg") == "https://src/1.jpg"


def test_blog_ids_sont_uniques():
    assert len(set(publier.BLOG_IDS.values())) == len(publier.BLOG_IDS)
