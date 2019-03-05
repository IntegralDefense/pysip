# pysip
A thin wrapper around requests to interact with the Simple Intel Platform (SIP).

## Usage

	from pysip import Client

	sip_client = Client('localhost:4443', verify=False)
	sip_client.login('user', 'password')

	print(sip_client.get('indicators/status'))
