import asyncio
from anyio import Path
from app.lib.utils.log import logger
from app.db.juno_tables import JunoTables

from csv import DictReader
from typing import List
from app.models.all import Bill


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

    def mutate_field(self, field):
        return field.strip().lower()


def csv_rows():
    """Synchronously open example CSVs and return rows as dicts."""
    with open(file_path, encoding="utf-8-sig") as seed_file:
        reader = InsensitiveDictReader(seed_file)
        return [row for row in reader]


async def seed_bill_rows(model_data: List[Bill]):
    async with JunoTables() as session:
        try:
            for model in model_data:
                new_bill = Bill(**model)
                session.add(new_bill)
                await session.commit()
                await session.refresh(new_bill)
        except Exception as e:
            logger(f"Seeding failed: \n\n{e}")


async def read_seed_rows():
    if not await file_path.exists():
        raise FileNotFoundError("example data CSV not found.")

    rows = await asyncio.to_thread(csv_rows)
    return rows


async def seed_db():
    entity_rows = await read_seed_rows()
    logger(f"Creating {len(entity_rows)}s bills")
    await seed_bill_rows(entity_rows)


if __name__ == "__main__":
    asyncio.run(seed_db())
