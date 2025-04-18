import click
import carousel

@click.command()
def cmd():
    carousel.main()

if __name__ == "__main__":
    cmd()
