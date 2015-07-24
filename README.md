# thumbor-plugins
[![Build Status](https://travis-ci.org/thumbor/thumbor-plugins.svg?branch=master)](https://travis-ci.org/thumbor/thumbor-plugins)

## Install 
```
pip install https://github.com/thumbor/thumbor-plugins/archive/master.zip
```

## Usage

### thumbor_plugins.optimizers.jpegrecompress

This optimizer uses the tool [JPEG-Archive](https://github.com/danielgtaylor/jpeg-archive) to reduce the image size but keep the image visually the same. The process is lossy (**not** lossless) and similar to [JPEGmini](http://www.jpegmini.com/).

> Compress JPEGs by re-encoding to the smallest JPEG quality while keeping perceived visual quality the same and by making sure huffman tables are optimized. This is a lossy operation, but the images are visually identical and it usually saves 30-70% of the size for JPEGs coming from a digital camera, particularly DSLRs. By default all EXIF/IPTC/XMP and color profile metadata is copied over, but this can be disabled to save more space if desired.

Images should be kept on the highest quality settings to achieve best results.

```ini
QUALITY = 100
JPEGRECOMPRESS_PATH = '/usr/bin/jpeg-recompress'
OPTIMIZERS = [
  'thumbor.optimizers.jpegtran'
]
```

Result:
```
root@a08db5748d10:/data# thumbor /usr/local/bin/thumbor -p 9000 -c /etc/thumbor.conf -l debug
2015-07-24 17:49:19 root:DEBUG thumbor running at 0.0.0.0:9000
2015-07-24 17:49:21 thumbor:DEBUG STATSD: storage.hit:1|c
2015-07-24 17:49:21 thumbor:DEBUG No image format specified. Retrieving from the image extension: .jpg.
2015-07-24 17:49:21 thumbor:DEBUG Content Type of image/jpeg detected.
2015-07-24 17:49:21 thumbor:DEBUG [JPEG-RECOMPRESS] running: /usr/bin/jpeg-recompress --strip --accurate --loops 10 /tmp/tmphFS4Uc /tmp/tmp__CwVY
ssim at q=67 (40 - 95): 0.963943
ssim at q=81 (68 - 95): 0.977207
ssim at q=88 (82 - 95): 0.984416
ssim at q=92 (89 - 95): 0.989077
ssim at q=94 (93 - 95): 0.991773
ssim at q=95 (95 - 95): 0.992719
ssim at q=96 (96 - 95): 0.994757
ssim at q=96 (97 - 95): 0.994757
ssim at q=96 (97 - 95): 0.994757
Final optimized ssim at q=96: 0.994763
New size is 57% of original (saved 45 kb)
2015-07-24 17:49:22 tornado.access:INFO 200 GET /unsafe/test.jpg (192.168.59.3) 1246.18ms
```
