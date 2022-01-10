import pytest

@pytest.mark.asyncio
@pytest.fixture(scope='function')
async def create_one_client(apply_migrations):
    from db.crud.clients import RpClient
    from faker import Faker
    seeds_generation = Faker() 

    data = {
        'name': seeds_generation.pystr(max_chars=50),
        'email': seeds_generation.pystr(max_chars=50)
    }

    res = await RpClient.create(value=data)
    assert res.get('status')    
    return res.get('content')