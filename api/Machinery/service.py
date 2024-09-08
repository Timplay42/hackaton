from fastapi import Depends
from utils.base.database_session import AsyncDatabase
from utils.base.service import BaseRepository
from .model import SafetyMachinery



class MachineSafetyService(BaseRepository):
    model = SafetyMachinery


async def get_machine_safety_service(session=Depends(AsyncDatabase.get_session)):
    return MachineSafetyService(session)

machine_safety_service: MachineSafetyService = Depends(get_machine_safety_service)

