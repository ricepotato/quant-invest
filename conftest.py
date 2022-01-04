import pytest
import dotenv
from repository import MongodbRepository


@pytest.fixture
def mongo_repo():
    dotenv.load_dotenv()
    return MongodbRepository()
