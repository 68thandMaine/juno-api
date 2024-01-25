import asyncio
import re
from csv import DictReader

from anyio import Path

from app.db.juno_db import JunoDB
from app.models.all import Bill, Category

ENTITY_CSV_PATH = Path("./app/db/seed_data/bill_seed.csv")
CATEGORY_CSV_PATH = Path("./app/db/seed_data/category_seed.csv")


class InsensitiveDictReader(DictReader):
    @property
    def fieldnames(self):
        fieldnames = super(InsensitiveDictReader, self).fieldnames
        return (
            [self.mutate_field(field) for field in fieldnames] if fieldnames else None
        )

    def mutate_field(self, field):
        return field.strip().lower()


async def read_csv_rows(file_path):
    if not await file_path.exists():
        raise FileNotFoundError(f"CSV file not found: {file_path}")

    with open(file_path, "r", encoding="utf-8-sig") as seed_file:
        reader = InsensitiveDictReader(seed_file)
        return [row for row in reader]


async def seed_model_rows(model_class, model_data):
    async with JunoDB() as session:
        try:
            for model in model_data:
                model = {
                    key: float(value) if re.match(r"^[-+]?\d*\.?\d+$", value) else value
                    for key, value in model.items()
                }
                new_model = model_class(**model)
                session.add(new_model)
            await session.commit()
            await session.refresh(new_model)
        except Exception as e:
            raise Exception(e)


async def seed_db():
    db = JunoDB()
    await db.create_tables()
    entity_rows = await read_csv_rows(ENTITY_CSV_PATH)
    category_rows = await read_csv_rows(CATEGORY_CSV_PATH)

    await seed_model_rows(Bill, entity_rows)
    await seed_model_rows(Category, category_rows)


if __name__ == "__main__":
    asyncio.run(seed_db())
