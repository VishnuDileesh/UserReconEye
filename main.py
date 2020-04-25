import os
import shutil
from sys import argv
from tqdm import tqdm
from pyfiglet import Figlet
from helium import *
import dominate
import click
import tldextract
import http.server
import socketserver
from dominate.tags import *
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


    render_report(username)

enum_report = {}


def reconsearch(site, username):


    start_chrome(site, headless=True)

    site_name = tldextract.extract(site)

    src_name = 'screenshots/{}/{}.png'.format(username, site_name.domain)


    get_driver().save_screenshot(src_name)

    enum_report[site_name.domain] = [site, src_name]

    kill_browser()



def render_report(username):
    
    doc = dominate.document(title='Enumeration Report : {}'.format(username))

    click.echo('Generating report of {}'.format(username))

    for k, v in tqdm(enum_report.items()):

        site_link = v[0]

        with doc.body:
            with a(href=site_link):
                img(src='screenshots/{}/{}.png'.format(username, k))

    with open('{}_report.html'.format(username), 'w') as f:
        f.write(doc.render())

    PORT = 4700
    Handler = http.server.SimpleHTTPRequestHandler

 

    try: 
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            click.echo('Report Generated Successfuly')
            click.echo('Open report at http://localhost:{}/{}_report.html'.format(PORT, username))

            httpd.serve_forever()

    except:
        print('Port is busy, switching port')
        PORT += 3
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            click.echo('Report Generated Successfuly')
            click.echo('Open report at http://localhost:{}/{}.html'.format(PORT, username))
            httpd.serve_forever()


if __name__ == "__main__":
    main()
