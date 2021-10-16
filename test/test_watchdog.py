import os
import unittest
from unittest import mock


def mockenv(**envvars):
    return mock.patch.dict(os.environ, envvars)


class MyTestCase(unittest.TestCase):
    @mockenv(SERVERS_PATH="../app/servers_paths.txt")
    def test_creating_settings(self):
        # dummy test
        # given
        min_len = 1
        # when
        from app.config import Settings  # leave it here as it needs os path

        settings = Settings()
        paths_length = len(settings.paths)

        # then
        self.assertGreaterEqual(paths_length, 1)


if __name__ == '__main__':
    unittest.main()
