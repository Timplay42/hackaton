import asyncio
import uvicorn
from fastapi import FastAPI, APIRouter
from starlette.middleware.cors import CORSMiddleware
from utils.base.config import settings
from utils.middlewares.api_doc_auth_middleware import ApidocBasicAuthMiddleware

from api.Users.router import user_router
from api.File.router import file_router
from api.Machinery.router import machinery_router
from api.Material.router import material_router
from api.SafetyVioleiton.router import safety_violetion_router
from api.Tools.router import tools_router

service_title = settings.api.title
app = FastAPI(title="hackaton",
              docs_url=f'/hackaton/api/docs',
              swagger_ui_parameters={
                  'docExpansion': 'none',
                  'persistAuthorization': 'true',
                  'defaultModelRendering': 'model'
              })
app.add_middleware(ApidocBasicAuthMiddleware)



origins = ["http://localhost:3000"]

app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*", "OPTIONS"],
                   allow_headers=["*"], max_age=3600)

router = APIRouter()

router.include_router(user_router, prefix='/users', tags=['User | Users'])
router.include_router(file_router, prefix='/file', tags=['File | Files'])
router.include_router(machinery_router, prefix='/machine_safety', tags=['MachineSafety | MachinesSafety'])
router.include_router(safety_violetion_router, prefix='/safety_violetion', tags=['SafetyVioletion | SafetyVioletions'])
router.include_router(tools_router, prefix='/tool', tags=['Tool | Tools'])
router.include_router(material_router, prefix='/material', tags=["Material | Materials"])



@router.get("/ping", tags=["Server"])
async def ping_server():
    return "pong"


app.include_router(router, prefix='/hackaton/api/v1')

if __name__ == "__main__":
    uvicorn.run("app:app", host='0.0.0.0', port=8020, reload=True)
