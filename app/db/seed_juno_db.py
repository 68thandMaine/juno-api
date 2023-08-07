import asyncio
from anyio import Path

from app.lib.utils.log import logger

from app.db.db import get_session

from csv import DictReader

from typing import List
from app.models.all import Bill, BillCreate
from pydantic import ValidationError

file_path = Path("./app/db/example-data.csv")


class InsensitiveDictReader(DictReader):
    """
    This class overrides the fieldnames property in order to strip whitespace from fieldnames
    and to make all fieldnames lower case.
    """

    @property
    def fieldnames(self):
        fieldnames = super(InsensitiveDictReader, self).fieldnames
        if fieldnames is None:
            return None
        return [self.mutate_field(field) for field in fieldnames]
\
    def mutate_field(self, field):
        return field.strip().lower()


def csv_rows():
    """Synchronously open example CSVs and return rows as dicts."""
    with open(file_path) as seed_file:
        reader = InsensitiveDictReader(seed_file)
        return [row for row in reader]


async def seed_bill_rows(model_data: List[BillCreate]):
    import pdb
    db_session = get_session()
    for model in model_data:
        logger(db_session)
        pdb.set_trace()
        new_bill = Bill.from_orm(model)

        # db_session.add(new_bill)
        # await db_session.commit()
        # await db_session.refresh(new_bill)
    # try:

    # except Exception as e:
    #     logger(model)
    #     logger(f"Seeding failed: \n\n{e}")


async def read_seed_rows():
    if not await file_path.exists():
        raise FileNotFoundError("example data CSV not found.")

    rows = await asyncio.to_thread(csv_rows)
    return rows


async def seed_db():
    entity_rows = await read_seed_rows()
    # logger(f"Creating {len(entity_rows)} bills")
    await seed_bill_rows(entity_rows)
    # Use this line to call a method to create a batch of bills (or bill one at a time).


async def run_seed():
    try:
        await seed_db()
    except ValidationError as err:
        print(err)


if __name__ == "__main__":
    asyncio.run(run_seed())
