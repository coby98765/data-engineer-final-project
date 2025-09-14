from fastapi import FastAPI, Query
from typing import Optional
from src.shared.dal.elastic import get_es

app = FastAPI(title="Public API")

@app.get("/healthz")
def healthz():
    return {"ok": True}

@app.get("/search")
def search(locality: str, street: str, house: Optional[int] = Query(None)):
    es = get_es()
    must = [{"term":{"locality.keyword": locality}}, {"term":{"street.keyword": street}}]
    if house is not None:
        must.append({"term":{"house_number": house}})
    body = {"query":{"bool":{"must": must}}, "size": 1}
    res = es.search(index="eligibility_v1", body=body)
    hits = res.get("hits",{}).get("hits",[])
    if not hits:
        return {"found": False}
    doc = hits[0]["_source"]
    return {"found": True, "eligible": doc.get("eligible"), "lat": doc.get("lat"), "lon": doc.get("lon")}
