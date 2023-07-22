from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.db.juno_tables import JunoTables
from dotenv import load_dotenv
from uuid import UUID

# from app.api.v1_routes import api_router

from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.bill import Bill, BillCreate
from sqlmodel import select
from app.db.db import get_session, init_db

load_dotenv()


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     """async function ensures async connections use the same event loop as the app"""
#     # * execute before startup
#     services = {}
#     services["juno_tables"] = JunoTables()
#     # await services["juno_tables"].drop_tables()
#     await services["juno_tables"].create_tables()
#     yield
#     # * clean up and release resources on shutdown
#     await services["juno_tables"].close()


# app = FastAPI(title="Juno API", lifespan=lifespan)
app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await init_db()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(api_router)


@app.get("/bills")
async def get_bills(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Bill))
    bills = result.scalars().all()
    return [Bill(name=bill.name, id=bill.id) for bill in bills]


@app.post("/bills")
async def add_bill(bill: BillCreate, session: AsyncSession = Depends(get_session)):
    new_bill = Bill(
        name=bill.name,
        amount=bill.amount,
        due_date=bill.due_date,
        frequency=bill.frequency,
        recurring=bill.recurring,
        category=bill.category,
        status=bill.status,
        notes=bill.notes,
    )
    session.add(new_bill)
    await session.commit()
    await session.refresh(new_bill)
    return new_bill
