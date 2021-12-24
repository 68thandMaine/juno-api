from fastapi import APIRouter, Depends, Query
import os

# from juno_api.controller.loupe_controller import LoupeController

router = APIRouter()


@router.get("/accounts/")
async def plasmid_index_search():
    print('hiiiii')
