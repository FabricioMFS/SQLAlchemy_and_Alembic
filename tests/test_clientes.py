from attr import dataclass
import pytest
from pydantic import UUID4
from .fixtures import create_one_client




class TestClients:
    data = {
        'name': 'Fabricio',
        'email': 'fabricio_menezes@live.com'
    }

    @pytest.mark.asyncio
    async def test_create_cliente_(self, apply_migrations):
        from ..db.crud.clients import RpClient

        res =  await RpClient.create(value=self.data)

        assert res.get('status')
        assert res.get('content').id

    @pytest.mark.asyncio
    async def test_update_fields(self, create_one_client):
        from ..db.crud.clients import RpClient
        id = create_one_client.id

        res =  await RpClient.modify(id=id, values=self.data)
        assert res.get('status')

        client =  await RpClient.search_by_id(id=id)        
        assert client.get('status')

        client = client.get('content')
        assert client.name == self.data['name']