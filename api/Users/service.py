from .model import Users
from fastapi import Depends, Form, HTTPException, status
from utils.base.database_session import AsyncDatabase
from utils.auth import service as auth_utils
from utils.base.service import BaseRepository
from sqlalchemy import select

class UsersService(BaseRepository):
    model = Users


    
    async def check_user_registered_fields(self, user_data):
        username = user_data.get("username")
        email = user_data.get("email")

        fields_to_check = {
            Users.username: username,
            Users.email: email,
        }
        used_fields = []
        for field, value in fields_to_check.items():
            if value:
                query = select(Users).where(field == value)
                result = await self.session.scalars(query)
                user = result.first()
                if user:
                    field_name = field.name
                    used_fields.append(field_name)

        if used_fields:
            raise HTTPException(404, f"Fields already in use: {','.join(used_fields)}")
        else:
            return True


    async def register(self, user_data):
        await self.check_user_registered_fields(user_data=user_data)
        user_data['role'] = 'user'
        user = Users(**user_data)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        return user


async def get_user_service(session=Depends(AsyncDatabase.get_session)):
    return UsersService(session)


user_service: UsersService = Depends(get_user_service)

