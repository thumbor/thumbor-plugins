import os.path

from tornado.testing import gen_test

from thumbor_plugins.test_helpers.engine import EngineCase


class PNGQuantTest(EngineCase):
    optimizer = "thumbor_plugins.optimizers.pngquant"
    fixtures_path = os.path.join(os.path.dirname(__file__), "imgs")

    @gen_test
    async def test_pngquant(self):
        result = await self.http_client.fetch(self.get_url("/unsafe/bend.png"))
        self.assert_result_smaller_than_original(result, "bend.png")
