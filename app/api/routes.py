# app/api/main.py

from fastapi import APIRouter


router = APIRouter(tags=['Volley GO! API'])


@router.get('/')
def root():
    return 'Volley Go! API v1.0   |   by Caiqui Viera'
