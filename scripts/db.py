from frictionless import Package
from sqlalchemy import create_engine, Table, Column, Integer, String, DateTime, text, MetaData, UniqueConstraint

engine = create_engine('sqlite:///data-raw/db.sqlite')

metadata = MetaData()

def create_table(name):
    return Table(
        name, metadata,
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

package = Package('datapackage.yaml')

tables = {resource_name: create_table(resource_name) for resource_name in package.resource_names}

metadata.create_all(engine)
