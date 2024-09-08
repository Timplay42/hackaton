import io
import tempfile
import zipfile
import datetime

from fastapi.responses import FileResponse
from .model import File, FileChildren
from fastapi import Depends, Form, HTTPException, status
from utils.base.database_session import AsyncDatabase
from utils.base.service import BaseRepository
from sqlalchemy import select
import os
from moviepy.editor import *
import boto3
from utils.base.s3amazon import S3Client

from utils.base.config import settings

class FilesService(BaseRepository):
    model = File
    s3 = S3Client()

    async def upload(self, file):

        parent_file = File(name=file.filename,
                            mime_type='mp4',
                            time_stamp={})
        self.session.add(parent_file)
        await self.session.commit()

        await self.s3.upload(file=await file.read(), object_name=f'{parent_file.id}.mp4')
        file_url = f'https://{settings.s3.bucket_name}.s3.amazonaws.com/{parent_file.id}.mp4'
        parent_file.file_url = file_url
        await self.session.commit()
        await self.session.refresh(parent_file)

        return parent_file

    async def create_clip(self, name: str, time_stamp: dict, file_id: str):
        
        file_parent = await self.get_parent_file(file_id)
        try:
            clips = []
            video = VideoFileClip(file_parent.original_path)
            counter = 0
            for key, value in time_stamp.items():
                clip = video.subclip(value[0], value[1])
                temp_file = tempfile.NamedTemporaryFile(suffix='.mp4')
                clip.write_videofile(temp_file.name)
                temp_file.seek(0)
                await self.s3.upload(file=temp_file, object_name=f"{file_parent.id}_{counter}.mp4")
                clips.append(f"https://s3.timeswb.com/{settings.s3.bucket_name}/{file_parent.id}_{counter}.mp4")
                counter += 1
                temp_file.close()
            
            for item in range(len(clips)):
                children_file = FileChildren(queue=item,
                                            name=f'{file_parent.id}_{counter}.mp4',
                                            original_path=clips[item],
                                            mime_type='mp4',
                                            parent_file_id=file_id)
                

                self.session.add(children_file)
            await self.session.commit()
            await self.session.refresh(children_file)
                

            return await self.get_parent_file(self, parent_id=file_parent.id)
        except Exception as e:
            raise e


    async def get_parent_file(self, parent_id):
        file = await self.id(parent_id)
        if file is None:
            raise HTTPException(400, detail='file is None')
        return file

    async def get_file(self, file_id):
        file = self.id(file_id)
        if file is None:
            raise HTTPException(401, 'file not found')
        response = await self.s3.get_file(f'{file.id}.mp4')
        file_content = response['Body'].read()
        return file_content



async def get_files_service(session=Depends(AsyncDatabase.get_session)):
    return FilesService(session)

files_service: FilesService = Depends(get_files_service)

