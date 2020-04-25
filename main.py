import os
import shutil
from sys import argv
from tqdm import tqdm
from pyfiglet import Figlet
from helium import *
import click
import tldextract
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
    click.echo('Enumerating {}'.format(username))

    try:
        os.mkdir('screenshots/{}'.format(username))
    except:
        shutil.rmtree('screenshots/{}'.format(username))

        os.mkdir('screenshots/{}'.format(username))


    for k, v in tqdm(platforms.items()):

        if v['up']:

            site = 'https://' + username + v['url']

            reconsearch(site, username)

        else:

            site = v['url'] + username

            reconsearch(site, username)



def reconsearch(site, username):


    start_chrome(site, headless=True)

    site_name = tldextract.extract(site)

    src_name = 'screenshots/{}/{}.png'.format(username, site_name.domain)


    get_driver().save_screenshot(src_name)


    kill_browser()


if __name__ == "__main__":
    main()
