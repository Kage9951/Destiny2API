import Destiny2_API
import Destiny2_Manifest

# Init local python dict manifest
manifest = Destiny2_Manifest.init_manifest()

# Get Player
destinyPlayer = Destiny2_API.call_API('SearchDestinyPlayer', membershipType=4,
                                      displayName='Kage%2312572')[0]

# Get Profile
profile = Destiny2_API.call_API('GetProfile',
                                membershipType=destinyPlayer['membershipType'],
                                destinyMembershipId=destinyPlayer['membershipId'],
                                components='Profiles')

# Get Characters
characters = []
for characterId in profile['profile']['data']['characterIds']:
    characters.append(Destiny2_API.call_API('GetCharacter',
                                            membershipType=profile['profile']['data']['userInfo']['membershipType'],
                                            destinyMembershipId=profile['profile']['data']['userInfo']['membershipId'],
                                            characterId=characterId,
                                            components='Characters,CharacterInventories,CharacterEquipment'))

# Print Character Class and Equipped Items
for char in characters:
    class_manifest = manifest['DestinyClassDefinition'][char['character']
                                                        ['data']['classHash']]
    print(f'\n{class_manifest["displayProperties"]["name"]}:')
    for item in char['equipment']['data']['items']:
        bucket_manifest = manifest['DestinyInventoryBucketDefinition'][item['bucketHash']]
        item_manifest = manifest['DestinyInventoryItemDefinition'][item['itemHash']]
        print(
            f' {bucket_manifest["displayProperties"]["name"]}: {item_manifest["displayProperties"]["name"]}')
