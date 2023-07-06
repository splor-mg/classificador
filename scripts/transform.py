from pathlib import Path
import yaml
from sqlalchemy import select, update, and_
from datetime import datetime
import pytz
from scripts.db import metadata, engine
import logging

logger = logging.getLogger(__name__)

def transform_resource(resource_name: str):
    table = metadata.tables[resource_name]
    path = Path(f'data-raw/{resource_name}')
    
    for file in path.glob('*.yaml'):
        with open(file, 'r') as file:
            classification = yaml.safe_load(file)

        for item in classification:
            for key in ['name', 'title', 'description']:
                if key not in item:
                    item[key] = None

            with engine.begin() as connection:
                    # Fetch existing row
                    stmt = select(table).where((table.c.code == item['code']) & (table.c.seq == item['seq']))
                    existing_row = connection.execute(stmt).fetchone()

                    if existing_row is not None:
                        # Check if relevant columns have changed
                        if existing_row.name != item['name'] or \
                        existing_row.title != item['title'] or \
                        existing_row.description != item['description'] or \
                        existing_row.valid_from != item['valid_from'] or \
                        existing_row.valid_to != item['valid_to']:
                            # If so, perform update and set updated_at to current time
                            now = datetime.now(pytz.utc)
                            stmt = (
                                update(table).
                                where(and_(table.c.code == item['code'], table.c.seq == item['seq'])).
                                values(
                                    name=item['name'],
                                    title=item['title'],
                                    description=item['description'],
                                    valid_from=item['valid_from'],
                                    valid_to=item['valid_to'],
                                    updated_at=now
                                )
                            )
                            connection.execute(stmt)
                    else:
                        # If row does not exist, perform insert
                        stmt = (
                            table.insert().
                            values(
                                code=item['code'],
                                seq=item['seq'],
                                name=item['name'],
                                title=item['title'],
                                description=item['description'],
                                valid_from=item['valid_from'],
                                valid_to=item['valid_to'],
                            )
                        )
                        connection.execute(stmt)
