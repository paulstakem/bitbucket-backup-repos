#!/usr/bin/env python

import argparse
import json
import netrc
import requests

def get_netrc_login_info(netrc_machine=None):
    username = None
    password = None

    try:
        info = netrc.netrc().authenticators(netrc_machine)
        if info is not None:
            username = info[0]
            password = info[2]
        else:
            raise netrc.NetrcParseError('No authenticators for {}'.format(netrc_machine))
    except (IOError, netrc.NetrcParseError) as err:
        print('error parsing .netrc: {}'.format(err))

    return username, password

def get_bitbucket_repos(user):
    """Retrieves all bitbucket repos, handles pagination"""

    repos = []
    url = "https://api.bitbucket.org/2.0/repositories/{}".format(user)
    headers = {'Content-Type': 'application/json'}

    username, password = get_netrc_login_info('api.bitbucket.org')
    r = requests.get(url, auth=(username, password), headers=headers)
    page_result = json.loads(r.text)
    repos += page_result['values']

    while 'next' in page_result:
        url = page_result['next']
        r = requests.get(url, auth=(username, password), headers=headers)
        page_result = json.loads(r.text)
        repos += page_result['values']

    return repos


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--bitbucket', action='store_true', help='list bitbucket repos', default=True)
    parser.add_argument('-u', '--user', help='the user or team to get repos for', default='vmdb')
    parser.add_argument('-j', '--json', action='store_true', help='output in json', default=True)

    args = parser.parse_args()

    repos = []
    repos = get_bitbucket_repos(args.user)

    for repo in repos:
        if args.json:
            print(json.dumps(repo))
        else:
            print(repo)


if __name__ == '__main__':
    main()
