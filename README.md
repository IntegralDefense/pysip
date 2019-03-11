# pysip
A thin wrapper around requests to interact with the Simple Intel Platform (SIP).

## Usage

	from pysip import Client

	sip_client = Client('localhost:4443', '11111111-1111-1111-1111-111111111111', verify=False)

	print(sip_client.get('indicators/status'))
