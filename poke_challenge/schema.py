from pydantic import BaseModel


class PokemonTypes(BaseModel):
    pokemon_name: str
    pokemon_type: str


class PokemonTypeCounter(BaseModel):
    pokemon_type: str
    type_count: int
