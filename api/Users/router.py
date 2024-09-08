from fastapi import APIRouter, Depends
from .schema import UsersBase, UsersCreate
from .service import user_service
from utils.auth.service import get_me, validate_auth_user

user_router = APIRouter()


@user_router.post(path='/register', name='register')
async def register_user(user: UsersCreate, users=user_service):
    return await users.register(user)

@user_router.get(path='/all', name='get all users')
async def get_users(users=user_service):
    return await users.all()

