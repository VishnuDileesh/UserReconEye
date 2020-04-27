import os
import shutil
from sys import argv
from tqdm import tqdm
from pyfiglet import Figlet
from helium import *
import dominate
import click
import tldextract
import time
from dominate.tags import *
from platforms_list import platform_users, users_platform


f = Figlet(
        font='slant',
        width=80
        )

__author__ = 'vishnu_dileesh'

click.echo(click.style(f.renderText('UserReconEye'), bold=True, fg='cyan'))
click.echo(click.style((f'Author: vishnu_dileesh'), fg='cyan'))

@click.command()
@click.argument('username')
@click.option('--wait', '-w')
def main(username, wait):

    """
    Running tool:
    python3 main.py vishnu_dileesh

    Running tool with 3 seconds delay:
    python3 main.py -w 3 vishnu_dileesh

    """

    click.echo('\nEnumerating {}\n'.format(username))

    try:
        os.mkdir('screenshots/{}'.format(username))
    except:
        shutil.rmtree('screenshots/{}'.format(username))

        os.mkdir('screenshots/{}'.format(username))

    try:
        os.mkdir('reports')
    except:
        pass


    if wait == None:
        wait = 0

    for p_u in tqdm(platform_users):

        site = ''.join((p_u, username))

        reconsearch(site, username, wait)


    for u_p in tqdm(users_platform):

        site = ''.join(('https://', username, u_p))

        reconsearch(site, username, wait)

    render_report(username)




def reconsearch(site, username, wait):


    start_chrome(site, headless=True)

    site_name = tldextract.extract(site)

    src_name = ''.join(('screenshots/', username, '/', site_name.domain, '.png'))


    time.sleep(float(wait))


    get_driver().save_screenshot(src_name)


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

    click.echo('\nGenerating report of {}'.format(username))
    
    with doc.body:
        h1('UserReconEye')
        h4('__author__ : vishnu_dileesh')
        h4('An open source osint username social media enumeration tool')

        br()
        br()

        h4('Click on reconed image with positive result to visit the profile')

        br()



    for pu in platform_users:
        sitename = tldextract.extract(pu)
        with doc:
            with div(cls='gallery'):
                with a(href='{}{}'.format(pu, username), target='_blank'):
                    img(src='../screenshots/{}/{}.png'.format(username, sitename.domain))
    
    for up in users_platform:
        sitename = tldextract.extract(up)
        with doc:
            with div(cls='gallery'):
                with a(href='https://{}{}'.format(username, up), target='_blank'):
                    img(src='../screenshots/{}/{}.png'.format(username, sitename.domain))

    

    with open('reports/{}_report.html'.format(username), 'w') as f:
        f.write(doc.render())


    current_dir = os.getcwd()

    start_chrome('file:///{}/reports/{}_report.html'.format(current_dir, username))
    
    click.echo('\nReport Successfully generated')



if __name__ == "__main__":
    main()
