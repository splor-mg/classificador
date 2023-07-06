from pathlib import Path
import yaml
from sqlalchemy import create_engine, text
from datetime import datetime
import pytz
import logging

logger = logging.getLogger(__name__)

def extract_resource(resource_name: str):
    
    engine = create_engine(f'sqlite:///data-raw/{resource_name}/db.sqlite')
    
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
                    stmt = text(f'SELECT * FROM {resource_name} WHERE code = :code AND seq = :seq')
                    existing_row = connection.execute(stmt, {"code": item['code'], "seq": item['seq']}).fetchone()

                    if existing_row is not None:
                        # Check if relevant columns have changed
                        if existing_row.name != item['name'] or \
                        existing_row.title != item['title'] or \
                        existing_row.description != item['description'] or \
                        existing_row.valid_from != item['valid_from'] or \
                        existing_row.valid_to != item['valid_to']:
                            # If so, perform update and set updated_at to current time
                            now = datetime.now(pytz.utc)
                            stmt = text(
                                f"""
                                UPDATE {resource_name}
                                SET name=:name, title=:title, description=:description,
                                valid_from=:valid_from, valid_to=:valid_to, updated_at=:updated_at
                                WHERE code=:code AND seq=:seq
                                """
                            )

                            connection.execute(
                                stmt,
                                {
                                    "name": item['name'],
                                    "title": item['title'],
                                    "description": item['description'],
                                    "valid_from": item['valid_from'],
                                    "valid_to": item['valid_to'],
                                    "updated_at": now,
                                    "code": item['code'],
                                    "seq": item['seq']
                                }
                            )
                    else:
                        # If row does not exist, perform insert
                        stmt = text(
                            f"""
                            INSERT INTO {resource_name} (code, seq, name, title, description, valid_from, valid_to)
                            VALUES (:code, :seq, :name, :title, :description, :valid_from, :valid_to)
                            """
                        )

                        connection.execute(
                            stmt,
                            {
                                "code": item['code'],
                                "seq": item['seq'],
                                "name": item['name'],
                                "title": item['title'],
                                "description": item['description'],
                                "valid_from": item['valid_from'],
                                "valid_to": item['valid_to']
                            }
                        )
