import pytest

from db_connection.db_connection import DbClient

class BaseCase:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, config):
        self.db, self.url = config
