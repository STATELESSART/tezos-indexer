from unittest import IsolatedAsyncioTestCase

import cootoo


class ExampleTest(IsolatedAsyncioTestCase):
    async def test_example(self):
        assert cootoo