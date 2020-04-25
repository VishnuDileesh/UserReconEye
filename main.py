from sys import argv
from tqdm import tqdm
from pyfiglet import Figlet
from helium import *
import click
from platforms_list import platforms

f = Figlet(
        font='slant',
        width=80
        )

__author__ = 'vishnu_dileesh'

click.echo(click.style(f.renderText('UserReconEye'), bold=True, fg='cyan'))
click.echo(click.style((f'Author: vishnu_dileesh'), fg='cyan'))

@click.command()
@click.argument('username')
def main(username):
    click.echo('name is {}'.format(username))



if __name__ == "__main__":
    main()
