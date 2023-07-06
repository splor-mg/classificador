from frictionless import Package, steps, transform
import petl as etl
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def transform_resource(resource_name: str, output_path: Path, descriptor: str = 'datapackage.yaml'):
    logger.info(f'Transforming resource {resource_name}')
    package = Package(descriptor)
    resource = package.get_resource(resource_name)
    target = transform(resource, steps=[steps.table_normalize()])
    table = target.to_petl()
    for field in resource.schema.fields:
        if field.custom.get('target'):
            table = etl.rename(table, field.name, field.custom['target'])
    etl.tocsv(table, output_path, encoding='utf-8')
