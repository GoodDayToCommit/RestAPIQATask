import json
import logging
from os.path import join, dirname
from jsonschema import validate


def assert_valid_schema(data, schema_file):
    schema = _load_json_schema(schema_file)
    logging.info("JSONSchema: verification started")
    return validate(data, schema)


def _load_json_schema(filename):
    relative_path = join('schemas', filename)
    absolute_path = join(dirname(__file__), relative_path)

    with open(absolute_path) as schema_file:
        return json.loads(schema_file.read())
