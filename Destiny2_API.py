import requests


def call_API(endpoint, **kwargs):
    # Create url for the request
    url = 'https://www.bungie.net/Platform'  # Base url
    if endpoint == 'SearchDestinyPlayer':
        membershipType = kwargs['membershipType']
        displayName = kwargs['displayName']
        url += f'/Destiny2/SearchDestinyPlayer/{membershipType}/{displayName}/'
    elif endpoint == 'GetProfile':
        membershipType = kwargs['membershipType']
        destinyMembershipId = kwargs['destinyMembershipId']
        components = '?components=' + str(kwargs['components'])
        url += f'/Destiny2/{membershipType}/Profile/{destinyMembershipId}/{components}'
    elif endpoint == 'GetCharacter':
        membershipType = kwargs['membershipType']
        destinyMembershipId = kwargs['destinyMembershipId']
        characterId = kwargs['characterId']
        components = '?components=' + str(kwargs['components'])
        url += f'/Destiny2/{membershipType}/Profile/{destinyMembershipId}/Character/{characterId}/{components}'
    else:
        print('Endpoint not found')
        return -1

    # Send the request
    response = requests.get(
        url,
        headers={'x-api-key': '5aa40b3bb4804c2d9199187a7730c4f4'},
    )

    # TO DO make some error checking on the response

    # Return the response
    json = response.json()
    return json['Response']
