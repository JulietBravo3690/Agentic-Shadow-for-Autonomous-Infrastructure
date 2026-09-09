import os
os.environ["DATABASE_URL"]="sqlite:///./test.db"
import pytest
from fastapi.testclient import TestClient
from app.database.db import engine
from app.database.models import Base
from app.main import app
@pytest.fixture
def client():
 Base.metadata.drop_all(engine); Base.metadata.create_all(engine)
 with TestClient(app) as value: yield value
