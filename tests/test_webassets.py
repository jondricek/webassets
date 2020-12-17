# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

from codecs import open
import hashlib
import locale
from pathlib import Path
from shutil import rmtree
from tempfile import mkdtemp
import unittest

from pelican import Pelican
from pelican.settings import read_settings
from pelican.tests.support import module_exists, mute, skipIfNoExecutable

HERE = Path(__name__).parent / 'tests'
THEME_DIR = HERE / 'test_data'
CSS_REF = open(THEME_DIR / 'static' / 'css' / 'style.min.css').read()
CSS_HASH = hashlib.md5(CSS_REF.encode()).hexdigest()[0:8]

@unittest.skipUnless(module_exists("webassets"), "webassets isn't installed")
@skipIfNoExecutable(["sass", "-v"])
@skipIfNoExecutable(["cssmin", "--version"])
class TestWebAssets(unittest.TestCase):
    """Base class for testing webassets."""

    def setUp(self, override=None):
        from pelican.plugins import webassets

        self.temp_path = mkdtemp(prefix="pelicantests.")
        settings = {
            "ASSET_CONFIG": [("sass_bin", "scss")],
            "PATH": THEME_DIR,
            "OUTPUT_PATH": self.temp_path,
            "PLUGINS": [webassets],
            "THEME": THEME_DIR,
            "LOCALE": locale.normalize("en_US"),
            "CACHE_CONTENT": False,
        }
        if override:
            settings.update(override)

        self.settings = read_settings(override=settings)
        pelican = Pelican(settings=self.settings)
        mute(True)(pelican.run)()

    def tearDown(self):
        rmtree(self.temp_path)

    def check_link_tag(self, css_file, html_file):
        """Check the presence of `css_file` in `html_file`."""

        link_tag = '<link rel="stylesheet" href="{css_file}">'.format(css_file=css_file)
        with open(html_file) as html:
            self.assertRegex(html.read(), link_tag)


class TestWebAssetsRelativeURLS(TestWebAssets):
    """Test pelican with relative urls."""

    def setUp(self):
        TestWebAssets.setUp(self, override={"RELATIVE_URLS": True})

    def test_jinja2_ext(self):
        # Test that the Jinja2 extension was correctly added.

        from webassets.ext.jinja2 import AssetsExtension

        self.assertIn(AssetsExtension, self.settings["JINJA_ENVIRONMENT"]["extensions"])

    def test_compilation(self):
        # Compare the compiled css with the reference.
        gen_file = Path(
            self.temp_path) / 'theme' / 'gen' / 'style.{}.min.css'.format(CSS_HASH)
        self.assertTrue(gen_file.is_file())

        with open(gen_file) as css_new:
            self.assertEqual(css_new.read(), CSS_REF)

    def test_template(self):
        # Look in the output files for the link tag.

        css_file = "./theme/gen/style.{0}.min.css".format(CSS_HASH)
        html_files = ["index.html", "archives.html", "this-is-a-super-article.html"]
        for f in html_files:
            self.check_link_tag(css_file, Path(self.temp_path) / f)

        self.check_link_tag(
            "../theme/gen/style.{0}.min.css".format(CSS_HASH),
            Path(self.temp_path) / 'category' / 'yeah.html',
        )


class TestWebAssetsAbsoluteURLS(TestWebAssets):
    """Test pelican with absolute urls."""

    def setUp(self):
        TestWebAssets.setUp(
            self, override={"RELATIVE_URLS": False, "SITEURL": "http://localhost"}
        )

    def test_absolute_url(self):
        # Look in the output files for the link tag with absolute url.

        css_file = "http://localhost/theme/gen/style.{0}.min.css".format(CSS_HASH)
        html_files = ["index.html", "archives.html", "this-is-a-super-article.html"]
        for f in html_files:
            self.check_link_tag(css_file, Path(self.temp_path) / f)
