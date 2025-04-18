import click
import carousel

@click.command()
def cli():
    carousel.main()

if __name__ == "__main__":
    cli()
