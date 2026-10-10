import dis

import fastapi


router = fastapi.APIRouter(prefix="/decompiler", tags=["decompiler"])

@router.get("/dis/{dis_query}")
def dis_decompiler(dis_query: str) -> fastapi.Response:
    """ Probably not safe decompilation for python instructions sent from the UI """
    decompiled = dis.dis(dis_query)
    return decompiled