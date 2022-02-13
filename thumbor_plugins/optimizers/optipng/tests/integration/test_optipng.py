import os.path

from tornado.testing import gen_test

from thumbor_plugins.test_helpers.engine import EngineCase

class OptiPNG(EngineCase):
    optimizer = "thumbor_plugins.optimizers.optipng"
    fixtures_path = os.path.join(
        os.path.dirname(__file__), "imgs"
    )

    @gen_test(timeout=30)
    async def test_optipng(self):
        result = await self.http_client.fetch(self.get_url("/unsafe/bend.png"))
        self.assert_result_smaller_than_original(result, "bend.png")
