#!/usr/bin/env python3

from pysip import Client

sip_client = Client('localhost:4443', verify=False)
sip_client.login('mwilson', 'asdfasdfasdf')

print(sip_client.get('indicators/status'))
