from poke_challenge.controller import PokemonController


async def main():
    repo = PokemonController()
    await repo.store_all_results()
    await repo.print_all_results_from_db()
    await repo.query_for_count()
    await repo.save_results_json()
    await repo.exit()
