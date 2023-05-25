# poke-challenge

Short API challenge, implemented using MVC SOLID design.


### Tasks
1. Get the types for each pokemon from API
e.g. bulbasaur is grass and poison

2. Store the data in SQLite3
e.g.
```sql
pokemon_name    |   type
--------------------------
bulbasaur       |   grass
bulbasaur       |   poison
charmander      |   fire
```

3. Print all the rows from database

4. Query the count of pokemon per type e.g.
```sql
type      |   count
-----------------------
Fire      |   3
Water     |   2
Normal    |   4
```

5. Save a json file in output with the result e.g.
```json
{
    "Fire": 3,
    "Water": 2,
    "Normal": 4
}
```

### To run

To install: 
```bash
make init
```

To run: 
```bash
make deploy
```
