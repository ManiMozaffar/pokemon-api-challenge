from typing import List
from abc import ABC, abstractmethod

import httpx

from poke_challenge.schema import PokemonTypes, PokemonTypeCounter


class APIHandlerABC(ABC):
    @abstractmethod
    async def get_single_pokemon_data(
        client: httpx.AsyncClient, name: str
    ): ...

    @abstractmethod
    def get_data_from_api(self) -> List[PokemonTypes]: ...


class JsonFileHandlerABC(ABC):
    @abstractmethod
    def pydantic_to_json(self, result: dict): ...
    @abstractmethod
    def save_to_file(self, data: dict): ...


class DatabaseHandlerABC(ABC):
    @abstractmethod
    async def query_counter(self) -> List[PokemonTypeCounter]: ...
    @abstractmethod
    async def start_database(self) -> None: ...
    @abstractmethod
    async def close(self) -> None: ...
    @abstractmethod
    async def store_result(self, result: List[PokemonTypes]) -> None: ...
    @abstractmethod
    async def all_pokemons(self) -> List[PokemonTypes.dict]: ...
    @abstractmethod
    async def tortoise_up(self) -> None: ...


class ControllerABC(ABC):
    database_handler: DatabaseHandlerABC
    josn_handler: JsonFileHandlerABC
    api_handler: APIHandlerABC

    @abstractmethod
    async def store_all_results(self, result: List[PokemonTypes]) -> None: ...

    @abstractmethod
    async def print_all_results_from_db(
        self, result: List[PokemonTypes]
    ) -> None: ...
    @abstractmethod
    async def query_for_count(self, ) -> List[PokemonTypeCounter]: ...
    @abstractmethod
    async def save_results_json(self) -> None: ...
    @abstractmethod
    async def exit(self) -> None: ...
