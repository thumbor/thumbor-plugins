import os.path

from tornado.testing import gen_test

from thumbor_plugins.test_helpers.engine import EngineCase

class PILTest(EngineCase):
    optimizer = "thumbor_plugins.optimizers.gifv"
    fixtures_path = os.path.join(
        os.path.dirname(__file__), "imgs"
    )

    @gen_test
    async def test_gifv(self):
        await self.http_client.fetch(self.get_url("/unsafe/filters:gifv()/animated.gif"))
