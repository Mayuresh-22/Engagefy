import asyncio
import uuid
import httpx
from langflow.helpers.data import data_to_text
from langflow.schema.message import Message
from langflow.template import Input, Output
from langflow.custom import Component
from langflow.schema import Data


class DBWriteComponent(Component):
    display_name = "Database Write Component"
    description = "Writes data to an Astra DB table."
    name = "DBWriteComponent"
    icon = "database"
    PAGE_SIZE = 10
    processed_data: list[dict[str, any]] = []

    inputs = [
        Input(
            name="db_token",
            display_name="Astra DB Token",
            required=True,
            placeholder="Enter application token",
            multiline=False,
            info="The application token for the Astra DB.",
        ),
        Input(
            name="db_id",
            display_name="Astra DB ID",
            required=True,
            multiline=False,
            info="The ID for the Astra DB.",
        ),
        Input(
            name="db_region",
            display_name="Astra DB Region",
            required=True,
            multiline=False,
            info="The region for the Astra DB.",
        ),
        Input(
            name="keyspace",
            display_name="Keyspace",
            required=True,
            info="The keyspace (or namespace) of the Astra DB table.",
        ),
        Input(
            name="table_name",
            display_name="Table Name",
            required=True,
            info="The name of the table where data will be written.",
        ),
        Input(
            name="data_to_write",
            display_name="Data to Write",
            field_type="Message",
            required=True,
            info="A list of records to store in the database. Format: {'data': [<records>]}",
            input_types=["text"]
        ),
    ]

    outputs = [
        Output(
            display_name="DB Response",
            name="results",
            method="process_data",
        ),
    ]

    def build_url(self) -> str:
        """
        Constructs the Astra DB API URL based on the provided inputs.
        """
        return (
            f"https://{self.db_id}-{self.db_region}.apps.astra.datastax.com/"
            f"api/rest/v2/keyspaces/{self.keyspace}/{self.table_name}"
        )

    async def write_row(self, client: httpx.AsyncClient, row: dict) -> dict:
        """
        Writes a single row to the database and returns the result.
        """
        row["id"] = str(uuid.uuid4())  # Ensure the row has a unique ID
        url = self.build_url()
        headers = {
            "accept": "application/json",
            "X-Cassandra-Token": self.db_token,
            "Content-Type": "application/json",
        }

        try:
            response = await client.post(url, headers=headers, json=row)
            response.raise_for_status()
            return {"status": "success", "value": response.json()}
        except httpx.RequestError as e:
            return {"status": "error", "value": str(e)}
        except httpx.HTTPStatusError as e:
            return {"status": "error", "value": response.json() if response else str(e)}

    async def write_rows(self, rows: list[dict]) -> list[dict]:
        """
        Writes multiple rows to the database concurrently and returns the results.
        """
        async with httpx.AsyncClient() as client:
            tasks = [self.write_row(client, row) for row in rows]
            return await asyncio.gather(*tasks)

    def process_data(self) -> Message:
        """
        Processes the input data and writes rows to the database.
        """
        if not isinstance(self.data_to_write, Message):
            return Message(text="error")
        rows_to_write = eval(self.data_to_write.text)
        # Execute asynchronous database writes
        write_response = asyncio.run(self.write_rows(rows_to_write))
        # return error response if more than 50% of the writes failed
        error_count = sum(1 for response in write_response if response["status"] == "error")
        if error_count > len(write_response) / 2:
            return Message(text="error")
        return Message(text="success")
