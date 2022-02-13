import os.path

from shutil import which

from tornado.testing import AsyncHTTPTestCase

from thumbor.app import ThumborServiceApp
from thumbor.config import Config
from thumbor.context import Context, ServerParameters
from thumbor.importer import Importer


class EngineCase(AsyncHTTPTestCase):
    def get_app(self):
        cfg = Config(SECURITY_KEY="ACME-SEC")
        server_params = ServerParameters(None, None, None, None, None, None, debug=True)
        server_params.gifsicle_path = which("gifsicle")

        cfg.DETECTORS = []
        cfg.STORAGE = "thumbor.storages.no_storage"
        cfg.LOADER = "thumbor.loaders.file_loader"
        cfg.FILE_LOADER_ROOT_PATH = getattr(self, "fixtures_path", None)
        cfg.ENGINE = "thumbor.engines.pil"
        cfg.USE_GIFSICLE_ENGINE = True
        cfg.FFMPEG_PATH = which("ffmpeg")
        cfg.ENGINE_THREADPOOL_SIZE = 10
        cfg.OPTIMIZERS = [
            getattr(self, "optimizer", None),
        ]
        if not cfg.ENGINE:
            return None

        importer = Importer(cfg)
        importer.import_modules()
        ctx = Context(server_params, cfg, importer)
        application = ThumborServiceApp(ctx)

        return application

    def assert_result_smaller_than_original(self, request, original_image):
        original_image_size = os.path.getsize(
            os.path.join(self.fixtures_path, original_image)
        )
        self.assertLess(int(request.headers["Content-Length"]), original_image_size)
