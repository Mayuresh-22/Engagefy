from langflow.template import Input, Output
from langflow.custom import Component
# from langflow.field_typing import Text
from langflow.schema.message import Message
import requests


class DBReadComponent(Component):
    display_name = "Database Read Component"
    description = "Reads data from an Astra DB table."
    name = "DBReadComponent"
    icon = "code"
    PAGE_SIZE = 10

    inputs = [
        Input(
            name="Message",
            display_name="Message",
            field_type="Message",
            required=False,
            info="The message to be stored in the database.",
            input_type="text",
        ),
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
            name="fields",
            display_name="Field Names",
            info="The field names (comma seperated) for the table.",
            value="",
            required=True,
        ),
        Input(
            name="primary_key",
            display_name="Primary Key Values (WHERE clause)",
            info="The primary key values for the WHERE clause.",
            required=True,
        )
    ]

    outputs = [
        Output(
            display_name="DB Results",
            name="results",
            method="get_rows",
        ),
    ]

    def build_url(self) -> str:
        DB_ID = self.db_id
        DB_REGION = self.db_region
        keyspace = self.keyspace
        table_name = self.table_name
        fields = self.fields
        primary_key = self.primary_key

        return f"https://{DB_ID}-{DB_REGION}.apps.astra.datastax.com/api/rest/v2/keyspaces/{keyspace}/{table_name}/{primary_key}?{fields if fields else ''}&page-size={self.PAGE_SIZE}&raw=true&count=DESC"

    def get_rows(self) -> Message:
        db_url = self.build_url()
        db_token = self.db_token
        headers = {
            "accept": "application/json",
            "X-Cassandra-Token": db_token
        }
        resp = requests.get(db_url, headers=headers)
        if resp.status_code != 200:
            raise Exception("error")
        return Message(text=str(resp.json()))


# # Define how to use the inputs and outputs
# component = DBReadComponent()
