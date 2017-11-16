from cerberus import Validator
import yaml

class MetadataValidator():
    def __init__(self, schema_filename):
        with open(schema_filename, 'r') as schema_file:
            schema = yaml.load(schema_file)
            self.validator = Validator(schema=schema)
            self.validator.allow_unknown = True

    def validate_data(self, data, schema_key):
        document = {}
        document[schema_key] = data
        if not self.validator.validate(document=document):
            print(self.validator.errors)
            return False

        return True
