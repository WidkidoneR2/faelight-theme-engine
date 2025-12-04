"""
Command-line interface for Faelight Theme Engine.
"""

import click

@click.group()
@click.version_option(version="0.1.0")
def cli():
    """Faelight Theme Engine - Generate themes from wallpapers."""
    pass

@cli.command()
def hello():
    """Test command - will be replaced in v2.8.2"""
    click.echo("🎨 Faelight Theme Engine v0.1.0")
    click.echo("✅ Structure complete! Ready for implementation.")

if __name__ == '__main__':
    cli()
