import json
import pytest
import asyncio

from poke_challenge.controller import PokemonController
from poke_challenge.schema import PokemonTypes


@pytest.fixture
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    asyncio.set_event_loop(loop)
    return loop


@pytest.fixture
def repo(event_loop):
    repo = PokemonController()
    event_loop.run_until_complete(repo.database_handler.start_database())
    event_loop.run_until_complete(repo.store_all_results())
    yield repo
    event_loop.run_until_complete(repo.database_handler.close())


@pytest.mark.asyncio
async def test_store_all_results(repo: PokemonController):
    await repo.store_all_results()
    api_data = await repo.api_handler.get_data_from_api()
    db_data = await repo.database_handler.all_pokemons()
    db_data = [
        PokemonTypes(pokemon_name=item[0], pokemon_type=item[1])
        for item in db_data
    ]

    assert len(api_data) == len(db_data)
    assert all([data in api_data for data in db_data])


@pytest.mark.asyncio
async def test_query_for_count(repo: PokemonController):
    api_data = await repo.api_handler.get_data_from_api()
    api_count = {}
    for data in api_data:
        api_count[data.pokemon_type] = api_count.get(data.pokemon_type, 0) + 1
    result_count = await repo.query_for_count()
    result_count_dict = {
        counter.pokemon_type: counter.type_count for
        counter in result_count
    }
    assert api_count == result_count_dict


@pytest.mark.asyncio
async def test_save_results_json(repo: PokemonController):
    await repo.save_results_json()
    with open('result.json', 'r') as file:
        file_data = json.load(file)
    result_count = {
        counter.pokemon_type: counter.type_count
        for counter in repo.results
    }
    assert file_data == result_count
