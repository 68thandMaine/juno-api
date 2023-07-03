from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.juno_tables import JunoTables
from dotenv import load_dotenv

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """async function ensures async connections use the same event loop as the app"""
    # * execute before startup
    services = {}
    services["juno_tables"] = JunoTables()
    await services["juno_tables"].create_tables()

    yield
    # * clean up and release resources on shutdown
    await services["juno_tables"].close()


app = FastAPI(title="Juno API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"hello": "world"}
