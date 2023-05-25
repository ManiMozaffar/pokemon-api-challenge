from tortoise.models import Model
from tortoise import fields


class PokemonModel(Model):
    id = fields.IntField(pk=True)
    pokemon_name = fields.CharField(max_length=200)
    pokemon_type = fields.CharField(max_length=200)

    class Meta:
        table = "pokemon_types"
