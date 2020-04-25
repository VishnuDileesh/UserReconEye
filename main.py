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
#from platforms_list import platforms
from test_list import platforms

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

    with doc.head:
        style(
                """\

                h1, h6, h4{
                margin: 0px !important;
                }

                p{
                margin: 0px !important;
                }

                div.gallery{
                margin: 5px;
                border: 1px solid #ccc;
                float: left;
                width: 180px;
                }

                div.gallery img{
                width: 100%;
                height: auto;
                }
                """
                )

    click.echo('Generating report of {}'.format(username))
    
    with doc.body:
        h1('UserReconEye')
        h4('__author__ : vishnu_dileesh')
        h4('An open source osint username social media enumeration tool')

        br()
        br()

        h4('Click on reconed image with positive result to visit the profile')

        br()

    for k, v in tqdm(enum_report.items()):

        site_link = v[0]

        with doc:

            with div(cls='gallery'):
                with a(href=site_link, target='_blank'):
                    img(src='screenshots/{}/{}.png'.format(username, k))
        
        #with a(href=site_link):
        #    img(src='screenshots/{}/{}.png'.format(username, k))
        #    hr()

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
            click.echo('Open report at http://localhost:{}/{}_report.html'.format(PORT, username))
            httpd.serve_forever()


if __name__ == "__main__":
    main()
