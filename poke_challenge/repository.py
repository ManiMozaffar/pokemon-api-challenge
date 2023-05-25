from typing import List, Tuple
import json
import os
import sqlite3
import asyncio


import httpx
from tortoise import Tortoise
from tortoise.functions import Count


from poke_challenge.schema import PokemonTypes, PokemonTypeCounter
from poke_challenge.constants import POKEMON_NAMES, BASE_API_URL
from poke_challenge.models import PokemonModel
from poke_challenge.abstract import (
    APIHandlerABC,
    DatabaseHandlerABC,
    JsonFileHandlerABC
)


class APIHandler(APIHandlerABC):
    def __init__(self):
        self._data = None

    async def get_single_pokemon_data(
        self, client: httpx.AsyncClient, name: str
    ) -> Tuple[list, str]:
        resp = await client.get(f"{BASE_API_URL}/pokemon/{name}")
        return (resp.json()["types"], name)

    async def get_data_from_api(self) -> List[PokemonTypes]:
        if self._data is not None:
            return self._data
        temp = {}
        self._data = []
        async with httpx.AsyncClient() as client:
            tasks = [
                self.get_single_pokemon_data(client, name)
                for name in POKEMON_NAMES
            ]
            responses = await asyncio.gather(*tasks)
            for resp, name in responses:
                temp[name] = list(name["type"]["name"] for name in resp)
            for key, value in temp.items():
                for item in value:
                    self._data.append(
                        PokemonTypes(pokemon_name=key, pokemon_type=item)
                    )
        return self._data


class DatabaseHandler(DatabaseHandlerABC):
    _db_path: str = "./database.db"

    async def tortoise_up(self) -> None:
        TORTOISE_ORM = {
            "connections": {
                "default": {
                    "engine": "tortoise.backends.sqlite",
                    "credentials": {
                        "file_path": self._db_path
                    }
                }
            },
            "apps": {
                "models": {
                    "models": ["poke_challenge.models"],
                    "default_connection": "default"
                }
            }
        }
        await Tortoise.init(config=TORTOISE_ORM)
        await Tortoise.generate_schemas()
        return None

    async def store_result(self, result: List[PokemonTypes]) -> None:
        await PokemonModel.bulk_create(
            [PokemonModel(**item.dict()) for item in result]
        )
        return None

    async def all_pokemons(self) -> List[PokemonTypes.dict]:
        return await PokemonModel.all().values_list(
            "pokemon_name", "pokemon_type"
        )

    async def start_database(self) -> None:
        conn = sqlite3.connect(self._db_path)
        conn.executescript("""
        PRAGMA foreign_keys = ON;
        DROP TABLE IF EXISTS pokemon_types;
        """)
        conn.close()
        await self.tortoise_up()
        return None

    async def close(self) -> None:
        await Tortoise.close_connections()
        return None

    async def query_counter(self) -> List[PokemonTypeCounter]:
        result = await PokemonModel.all().annotate(
            type_count=Count('pokemon_type')
        ).group_by("pokemon_type").values("pokemon_type", "type_count")
        return [
            PokemonTypeCounter(**item) for item in result
        ]


class JsonFileHandler(JsonFileHandlerABC):
    def pydantic_to_json(self, result: List[PokemonTypeCounter]):
        json_data = json.dumps(
            {counter.pokemon_type: counter.type_count for counter in result}
        )
        return json_data

    def save_to_file(self, data):
        file_path = os.path.join(os.getcwd(), "result.json")

        try:
            with open(file_path, "w") as file:
                file.write(data)
            print(f"Data saved to {file_path} successfully.")
        except IOError as error:
            print(
                "An error occurred while saving the data to"
                f"{file_path}: {error}"
            )
