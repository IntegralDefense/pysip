# pysip
A thin wrapper around requests to interact with the Simple Intel Platform (SIP).

## Usage

	import pysip

    # Connect to SIP
	sip_client = pysip.Client('localhost:4443', '11111111-1111-1111-1111-111111111111', verify=False)
	
	# Example GET request
	print(sip_client.get('indicators/status'))
	
	# Adding an indicator and ignoring any 409 Conflict error if the indicator already exists.
	try:
	    data = {'type': 'IP', 'value': '127.0.0.1'}
	    sip_client.post('indicators', data)
	except pysip.ConflictError:
	    pass
