from frictionless import Package
from sqlalchemy import create_engine, Table, Column, Integer, String, DateTime, text, MetaData, UniqueConstraint

def create_db(resource_name):
    engine = create_engine(f'sqlite:///data-raw/{resource_name}/db.sqlite')
    metadata = MetaData()
    table = Table(
            resource_name, metadata,
            Column('id', Integer, primary_key=True),
            Column('code', Integer, nullable=False),
            Column('seq', Integer, nullable=False),
            Column('name', String),
            Column('title', String),
            Column('description', String),
            Column('valid_from', String, nullable=False),
            Column('valid_to', String, nullable=False),
            Column('created_at', DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP')),
            Column('updated_at', DateTime, server_default=text('CURRENT_TIMESTAMP')),
            UniqueConstraint('code', 'seq', name='uix_1')
        )
    metadata.create_all(engine)

package = Package('datapackage.yaml')

for resource_name in package.resource_names:
    create_db(resource_name)