# Webassets: A Plugin for Pelican

[![Build Status](https://img.shields.io/github/workflow/status/pelican-plugins/webassets/build)](https://github.com/pelican-plugins/webassets/actions)
[![PyPI Version](https://img.shields.io/pypi/v/pelican-webassets)](https://pypi.org/project/pelican-webassets/)
![License](https://img.shields.io/pypi/l/pelican-webassets?color=blue)

Use the [`webassets` module](https://github.com/miracle2k/webassets) to manage assets such as CSS and JS files

## Installation

This plugin can be installed via:

```shell-session
python -m pip install pelican-webassets
```

## Usage

The Webassets module allows you to perform a number of useful asset management
functions, including:

* CSS minifier (`cssmin`, `yui_css`, ...)
* CSS compiler (`less`, `sass`, ...)
* JS minifier (`uglifyjs`, `yui_js`, `closure`, ...)

Others filters include CSS URL rewriting, integration of images in CSS via data
URIs, and more. Webassets can also append a version identifier to your asset
URL to convince browsers to download new versions of your assets when you use
far-future expires headers. Please refer to the [Webassets documentation](http://webassets.readthedocs.org/en/latest/builtin_filters.html) for
more information.

When used with Pelican, Webassets is configured to process assets in the
`OUTPUT_PATH/theme` directory. You can use Webassets in your templates by
including one or more template tags. The Jinja variable `{{ ASSET_URL }}` can
be used in templates and is relative to the `theme/` url. The
`{{ ASSET_URL }}` variable should be used in conjunction with the
`{{ SITEURL }}` variable in order to generate URLs properly. For example:

```html+jinja
{% assets filters="cssmin", output="css/style.min.css", "css/inuit.css", "css/pygment-monokai.css", "css/main.css" %}
    <link rel="stylesheet" href="{{ SITEURL }}/{{ ASSET_URL }}">
{% endassets %}
```

... will produce a minified css file with a version identifier that looks like:

```html
<link href="http://example.com/theme/css/style.min.css?b3a7c807" rel="stylesheet">
```

These filters can be combined. Here is an example that uses the SASS compiler
and minifies the output:

```html+jinja
{% assets filters="sass,cssmin", output="css/style.min.css", "css/style.scss" %}
    <link rel="stylesheet" href="{{ SITEURL }}/{{ ASSET_URL }}">
{% endassets %}
```

Another example for Javascript:

```html+jinja
{% assets filters="uglifyjs", output="js/packed.js", "js/jquery.js", "js/base.js", "js/widgets.js" %}
    <script src="{{ SITEURL }}/{{ ASSET_URL }}"></script>
{% endassets %}
```

The above will produce a minified JS file:

```html
<script src="http://example.com/theme/js/packed.js?00703b9d"></script>
```

Pelican's debug mode is propagated to Webassets to disable asset packaging
and instead work with the uncompressed assets.

If you need to create named bundles (for example, if you need to compile SASS
files before minifying with other CSS files), you can use the `ASSET_BUNDLES`
variable in your settings file. This is an ordered sequence of 3-tuples, where
the 3-tuple is defined as `(name, args, kwargs)`. This tuple is passed to the
[environment's `register()` method](http://webassets.readthedocs.org/en/latest/environment.html#registering-bundles). The following will compile two SCSS files
into a named bundle, using the `pyscss` filter:

```python
ASSET_BUNDLES = (
    ("scss", ["colors.scss", "main.scss"], {"filters": "pyscss"}),
)
```

Many of Webasset's available compilers have additional configuration options
(i.e. `Less`, `Sass`, `Stylus`, `Closure_js`).  You can pass these options to
Webassets using the `ASSET_CONFIG` in your settings file.

The following will handle Google Closure's compilation level and locate
LessCSS's binary:

```python
ASSET_CONFIG = (
    ("CLOSURE_COMPRESSOR_OPTIMIZATION", "WHITESPACE_ONLY"),
    ("LESS_BIN", "lessc.cmd"),
)
```

If you wish to place your assets in locations other than the theme output
directory, you can use `ASSET_SOURCE_PATHS` in your settings file to provide
webassets with a list of additional directories to search, relative to the
theme's top-level directory:

```python
ASSET_SOURCE_PATHS = [
    "vendor/css",
    "scss",
]
```

## Contributing

Contributions are welcome and much appreciated. Every little bit helps. You can contribute by improving the documentation, adding missing features, and fixing bugs. You can also help out by reviewing and commenting on [existing issues][].

To start contributing to this plugin, review the [Contributing to Pelican][] documentation, beginning with the **Contributing Code** section.

[existing issues]: https://github.com/pelican-plugins/webassets/issues
[Contributing to Pelican]: https://docs.getpelican.com/en/latest/contribute.html

## License

This project is licensed under the AGPL-3.0 license.