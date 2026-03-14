# Building the Documentation

This guide explains how to build the vdsxarray Sphinx documentation.

## Prerequisites

Install documentation dependencies:

```bash
cd docs
pip install -r source/requirements.txt
```

Or using the project's package manager:

```bash
uv sync --group dev
```

## Building

### HTML Documentation

To build the HTML documentation:

**On Linux/macOS:**
```bash
cd docs
make html
```

**On Windows:**
```bash
cd docs
make.bat html
```

The built documentation will be in `docs/build/html/`. Open `docs/build/html/index.html` in your browser.

### Other Formats

Sphinx supports multiple output formats:

```bash
make html       # HTML pages
make latexpdf   # PDF (requires LaTeX)
make epub       # EPUB ebook
make man        # Man pages
make text       # Plain text
```

## Cleaning Build Files

To remove all built documentation:

```bash
make clean
```

## Live Preview

For live preview during development, install `sphinx-autobuild`:

```bash
pip install sphinx-autobuild
```

Then run:

```bash
sphinx-autobuild docs/source docs/build/html
```

Open http://127.0.0.1:8000 in your browser. The page will auto-reload when you save changes.

## Documentation Structure

The documentation follows the Diátaxis framework:

- **Tutorials** (learning-oriented): Step-by-step lessons for beginners
- **How-To Guides** (problem-oriented): Solutions to specific tasks
- **Reference** (information-oriented): Technical API documentation
- **Explanation** (understanding-oriented): Conceptual discussions
- **AI Agents**: Dedicated section for AI coding agents

## File Organization

```
docs/
  source/
    conf.py                 # Sphinx configuration
    index.rst               # Main documentation page
    installation.rst        # Installation guide
    quickstart.rst          # Quick start guide
    tutorials/              # Tutorial pages
    howto/                  # How-to guides
    reference/              # API reference
    explanation/            # Conceptual documentation
    ai-agents/              # AI agent documentation
    _static/                # Static files (CSS, images)
      custom.css            # Custom styles
    _templates/             # Custom templates (if any)
  build/                    # Generated documentation (gitignored)
  Makefile                  # Build commands (Unix)
  make.bat                  # Build commands (Windows)
```

## Writing Documentation

### RST Files

Most documentation is in reStructuredText (`.rst`) format:

```rst
Section Title
=============

Subsection
----------

Paragraph text with **bold** and *italic*.

.. code-block:: python

   # Python code example
   import xarray as xr
   ds = xr.open_dataset("file.vds", engine="vds")

.. note::
   This is a note admonition.
```

### Markdown Files

Some files use Markdown (`.md`) via MyST parser:

```markdown
# Section Title

## Subsection

Paragraph text with **bold** and *italic*.

```python
# Python code example
import xarray as xr
ds = xr.open_dataset("file.vds", engine="vds")
```

```note
This is a note admonition.
```
```

## Tips

1. **Check for warnings**: Sphinx warnings often indicate broken links or formatting issues
2. **Test locally**: Always build and review documentation before committing
3. **Follow Diátaxis**: Place content in the appropriate category
4. **Use consistent formatting**: Follow existing documentation style
5. **Include code examples**: Show, don't just tell

## Troubleshooting

### "sphinx-build not found"

Install Sphinx:
```bash
pip install sphinx
```

### Import errors when building

Make sure the package is installed:
```bash
pip install -e .
```

### Missing dependencies

Install all documentation dependencies:
```bash
pip install -r docs/source/requirements.txt
```

### Warnings about missing references

Check that all referenced files exist and cross-references use correct syntax:
```rst
:doc:`path/to/document`      # Link to document
:ref:`label-name`            # Link to label
:class:`ClassName`           # Link to class
:func:`function_name`        # Link to function
```

## GitHub Pages Deployment

The documentation can be automatically deployed to GitHub Pages via GitHub Actions.

See `.github/workflows/docs.yml` for the deployment configuration (if it exists).

## Contributing to Documentation

When contributing documentation:

1. Follow the Diátaxis framework
2. Use clear, concise language
3. Include code examples
4. Test all code examples
5. Build locally and check for warnings
6. Ensure cross-references work

For more details, see the [Contributing Guide](../CONTRIBUTING.md).
