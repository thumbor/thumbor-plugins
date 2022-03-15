import os.path

from tornado.testing import gen_test

from thumbor_plugins.test_helpers.engine import EngineCase


class GIFVTest(EngineCase):
    optimizer = "thumbor_plugins.optimizers.gifv"
    fixtures_path = os.path.join(os.path.dirname(__file__), "imgs")

    @gen_test
    async def test_gifv(self):
        response = await self.http_client.fetch(
            self.get_url("/unsafe/filters:gifv()/animated.gif")
        )
        self.assertEqual(response.code, 200)
        self.assertEqual(response.headers["Content-Type"], "video/mp4")

    @gen_test
    async def test_gifv_with_background(self):
        response = await self.http_client.fetch(
            self.get_url("/unsafe/filters:gifv(mp4):background_color(ff00ff)/animated.gif")
        )
        self.assertEqual(response.code, 200)
        self.assertEqual(response.headers["Content-Type"], "video/mp4")

    @gen_test
    async def test_gifv_webm(self):
        response = await self.http_client.fetch(
            self.get_url("/unsafe/filters:gifv(webm)/animated.gif")
        )
        self.assertEqual(response.code, 200)
        self.assertEqual(response.headers["Content-Type"], "video/webm")
