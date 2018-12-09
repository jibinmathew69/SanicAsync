import pytest
import json
from main import make_app

@pytest.yield_fixture
def app():
    app = make_app()
    yield app

@pytest.fixture
def test_cli(loop, app, test_client):

    return loop.run_until_complete(test_client(app))



async def test_upload_api(test_cli):
    data = {
	"urls" : [
				"https://images.homedepot-static.com/productImages/a810e8c9-9c40-44f9-a01c-eeaa5ac9c88d/svn/stencil-ease-commercial-stencils-cc0081m-64_1000.jpg",
                "https://cdn.psychologytoday.com/sites/default/files/styles/article-inline-half/public/field_blog_entry_images/2018-02/cloned_dogs_mdorottya_123rf.png",
                "https://ithemes.com/wp-content/uploads/2016/10/Free-High-Quality-Images-Death-to-the-Stock-Photo.jpg",
                "https://images.pexels.com/photos/789380/pexels-photo-789380.jpeg",
                "https://images.pexels.com/photos/280204/pexels-photo-280204.jpeg"
		]
    }
    response = await test_cli.post('/v1/images/upload',data=json.dumps(data))

    assert response.status == 200

async def test_status(test_cli):

    response = await test_cli.get('/v1/images')

    assert response.status == 200

