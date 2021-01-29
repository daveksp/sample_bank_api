def get_schema_required_fields(schema):
    return [k for k, v in schema._declared_fields.items()
            if v.required and not v.dump_only]
