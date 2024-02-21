import click
from pql import PQL

# Create a PQL instance for the CLI
pql = PQL("notes", "logs")

@click.group()
def cli():
    """PQL command-line interface."""
    pass

# ... (Other commands using the PQL object)

@cli.command()
@click.argument("image_path")
@click.option("--name", help="Optional name for the note")
def push_image(image_path, name):
    """Stores an image as a note."""
    pql.push_image(image_path, name)

if __name__ == "__main__":
    cli()
