from langflow.template import Input, Output
from langflow.custom import Component
from concurrent.futures import ThreadPoolExecutor
import requests
import os


class DBWriteComponent(Component):
    display_name = "Database Read Component"
    description = "Reads data from an Astra DB table."
    name = "DBWriteComponent"
    icon = "code"
    PAGE_SIZE = 10
    processed_data: list[dict[str, any]] = []

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
        return f"https://{DB_ID}-{DB_REGION}.apps.astra.datastax.com/api/rest/v2/keyspaces/{keyspace}/{table_name}"

    def process_data(self) -> list[dict[str, any]]:
        pass

    def write_row(self, row: dict) -> bool:
        db_url = self.build_url()
        db_token = self.db_token
        headers = {
            "accept": "application/json",
            "X-Cassandra-Token": db_token
        }
        body = row
        try:
            resp = requests.post(db_url, headers=headers, data=body)
            if resp.status_code != 200:
                raise Exception("error")
            return True
        except Exception as e:
            print(e)
            return False

    def write_rows(self, rows: list[dict]) -> list[bool]:
        MAX_THREADS = min(os.cpu_count(), len(rows))  # max threads to use
        with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
            resp_list = list(executor.map(self.write_row, rows))
        # if 50% of the rows are written, return True
        success_rate_list = [1 if resp else 0 for resp in resp_list]
        if sum(success_rate_list) >= len(rows) / 2:
            return True
        return False


# # Define how to use the inputs and outputs
# component = DBWriteComponent()
