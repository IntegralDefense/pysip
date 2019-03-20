# pysip
A thin wrapper around requests to interact with the Simple Intel Platform (SIP).

## Usage

	import pysip

    # Connect to SIP
	sip_client = pysip.Client('localhost:4443', '11111111-1111-1111-1111-111111111111', verify=False)
		
	# Example POST request
	# Add an indicator and ignore any 409 Conflict error if the indicator already exists.
	try:
	    data = {'type': 'IP', 'value': '127.0.0.1'}
	    sip_client.post('/api/indicators', data)
	except pysip.ConflictError:
	    pass

    # Example GET request
    # Get all of the indicators with the "Analyzed" status in "bulk" mode.
    indicators = sip_client.get('/api/indicators?status=Analyzed&bulk=true')
    
    # Example PUT request
    # Update an indicator's status.
    data = {'status': 'Informational'}
    result = sip_client.put('/api/indicators/1', data)
    
    # Example DELETE request
    # Delete an indicator.
    result = sip_client.delete('/api/indicators/1')