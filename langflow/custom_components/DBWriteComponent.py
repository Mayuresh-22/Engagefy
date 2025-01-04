from langflow.template import Input, Output
from langflow.custom import Component
# from langflow.field_typing import Text


class DBWriteComponent(Component):
    display_name = "Database Read Component"
    description = "Reads data from an Astra DB table."
    name = "DBWriteComponent"
    icon = "code"
    PAGE_SIZE = 10

    inputs = [
        Input(
            name="db_token",
            display_name="Astra DB Token",
            required=True,
            placeholder="Enter application token",
            multiline=False,
            info="This is the application token for the Astra DB.",
        ),
        Input(
            name="db_id",
            display_name="Astra DB id",
            required=True,
            multiline=False,
            info="This is the id for the Astra DB.",
        ),
        Input(
            name="db_region",
            display_name="Astra DB Region",
            required=True,
            multiline=False,
            info="This is the region for the Astra DB.",
        ),
        Input(
            name="keyspace",
            display_name="Keyspace",
            info="Table Keyspace (or AstraDB namespace).",
            required=True,
        ),
        Input(
            name="keyspace",
            display_name="Keyspace",
            info="Table Keyspace (or AstraDB namespace).",
            required=True,
        ),
        Input(
            name="table_name",
            display_name="Table Name",
            info="The name of the table (or AstraDB collection) where vectors will be stored.",
            load_from_db=True,
            required=True,
        ),
        Input(
            name="data_to_write",
            display_name="Data to Write",
            field_type="Data",
            required=False,
            info="The Data with dict {data: [<records to store>]} to write to the database.",
            input_type=["Data"],
        ),
    ]

    outputs = [
        Output(
            display_name="DB response",
            name="results",
            method="process_data",
        ),
    ]

    def build_url(self) -> str:
        DB_ID = self.db_id
        DB_REGION = self.db_region
        keyspace = self.keyspace
        table_name = self.table_name
        primary_key = self.primary_key

        return f"https://{DB_ID}-{DB_REGION}.apps.astra.datastax.com/api/rest/v2/keyspaces/{keyspace}/{table_name}/{primary_key}"

    def process_data(self) -> list[dict[str, any]]:
        pass


# # Define how to use the inputs and outputs
# component = DBWriteComponent()
