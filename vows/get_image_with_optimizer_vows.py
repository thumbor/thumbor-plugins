#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/globocom/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com timehome@corp.globo.com
from os.path import abspath, join, dirname

from pyvows import Vows, expect
from tornado_pyvows.context import TornadoHTTPContext

from thumbor.app import ThumborServiceApp
from thumbor.config import Config
from thumbor.importer import Importer
from thumbor.context import Context, ServerParameters
from thumbor.utils import which
from thumbor.engines.pil import Engine as PILEngine


storage_path = abspath(join(dirname(__file__), 'fixtures/'))


class BaseContext(TornadoHTTPContext):
    def __init__(self, *args, **kw):
        super(BaseContext, self).__init__(*args, **kw)


@Vows.batch
class GetImageWithPngcrush(BaseContext):
    def get_app(self):
        cfg = Config(SECURITY_KEY='ACME-SEC', PNGCRUSH_PATH=which('pngcrush'))
        cfg.LOADER = "thumbor.loaders.file_loader"
        cfg.FILE_LOADER_ROOT_PATH = storage_path
        cfg.OPTIMIZERS = [
            'thumbor_plugins.optimizers.pngcrush',
        ]

        importer = Importer(cfg)
        importer.import_modules()
        server = ServerParameters(8889, 'localhost', 'thumbor.conf', None, 'info', None)
        server.security_key = 'ACME-SEC'
        ctx = Context(server, cfg, importer)
        application = ThumborServiceApp(ctx)

        self.engine = PILEngine(ctx)

        return application

    class ShouldBePngcrush(BaseContext):
        def topic(self):
            return self.get('/unsafe/test.png')

        def should_be_ok(self, response):
            expect(response.code).to_equal(200)


@Vows.batch
class GetImageWithOptipng(BaseContext):
    def get_app(self):
        cfg = Config(SECURITY_KEY='ACME-SEC', OPTIPNG_PATH=which('optipng'), OPTIPNG_LEVEL=1)
        cfg.LOADER = "thumbor.loaders.file_loader"
        cfg.FILE_LOADER_ROOT_PATH = storage_path
        cfg.OPTIMIZERS = [
            'thumbor_plugins.optimizers.optipng',
        ]

        importer = Importer(cfg)
        importer.import_modules()
        server = ServerParameters(8889, 'localhost', 'thumbor.conf', None, 'info', None)
        server.security_key = 'ACME-SEC'
        ctx = Context(server, cfg, importer)
        application = ThumborServiceApp(ctx)

        self.engine = PILEngine(ctx)

        return application

    class ShouldBeOptipng(BaseContext):
        def topic(self):
            return self.get('/unsafe/test.png')

        def should_be_ok(self, response):
            expect(response.code).to_equal(200)
