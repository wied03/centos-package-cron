#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import socket
import sys
from email_producer import EmailProducer
from db_session_fetcher import db_session_fetcher
import smtplib
from email.mime.text import MIMEText

__VERSION__ = '1.0.3.1'

def main():
    args = parse_args()    
    repos_to_exclude_list = []
    if args.disablerepo != None:
        repos_to_exclude_list = args.disablerepo.split(',')
    repos_to_include_list = []
    if args.enablerepo != None:
        repos_to_include_list = args.enablerepo.split(',')
        
    producer = EmailProducer(repos_to_exclude_list, repos_to_include_list, args.skipold, args.skip_sqlite_file_path)
    email_content = producer.produce_email()

    if email_content != '':
        server = smtplib.SMTP('localhost')        
        message = MIMEText(email_content.encode('utf-8'), 'plain', 'utf-8')
        message['Subject'] = args.email_subject
        message['From'] = args.email_from
        message['To'] = args.email_to
        server.sendmail(from_addr=args.email_from, to_addrs=[args.email_to], msg=message.as_string())
        server.quit
                            
def parse_args():
    parser = argparse.ArgumentParser(description="Emails administrators with CentOS security updates and changelogs of non-security updates. Version %s" % __VERSION__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument('-e', '--email_to',
    type=str,
    required=True,
    help='Email following user with the output')    

    parser.add_argument('-f', '--email_from',
    type=str,
    default="CentOS Update Check on %s <noreply@centos.org>" %(socket.gethostname()),
    help='Send the email from this user.')    

    parser.add_argument('-s', '--email_subject',
    type=str,
    default="CentOS Update Check on %s" %(socket.gethostname()),
    help='Send the email using this subject') 
    
    parser.add_argument('-dr','--disablerepo',
    type=str,
    help='List of comma separated repos to exclude when dealing with Yum')
    
    parser.add_argument('-er','--enablerepo',
    type=str,
    help='List of comma separated repos to include when dealing with Yum')
    
    parser.add_argument('-so','--skipold',
    type=bool,
    default=True,
    help='Only annoys the person with 1 email for a given advisory/package update notice.')
    
    parser.add_argument('-db','--skip-sqlite-file-path',
    type=str,
    default=db_session_fetcher.DEFAULT_DB_PATH,
    help='The location of the Sqlite DB used to track which notifications you have already received.')
    
    return parser.parse_args()

if __name__ == '__main__':
    sys.exit(main())
