# Code from http://destinydevs.github.io/BungieNetPlatform/docs/Manifest
# with some minor edits

import requests
import zipfile
import os
import pickle
import json
import sqlite3


def get_manifest():
    manifest_url = 'https://www.bungie.net/Platform/Destiny2/Manifest/'

    # get the manifest location from the json
    r = requests.get(manifest_url)
    manifest = r.json()
    mani_url = 'https://www.bungie.net' + \
        manifest['Response']['mobileWorldContentPaths']['en']

    # Download the file, write it to 'MANZIP'
    r = requests.get(mani_url)
    with open("MANZIP", "wb") as zip:
        zip.write(r.content)
    print("Download Complete!")

    # Extract the file contents, and rename the extracted file
    # to 'Manifest.content'
    with zipfile.ZipFile('MANZIP') as zip:
        name = zip.namelist()
        zip.extractall()
    os.rename(name[0], 'Manifest.content')
    print('Unzipped!')


def build_dict(hash_dict):
    # connect to the manifest
    con = sqlite3.connect('Manifest.content')
    print('Connected')
    # create a cursor object
    cur = con.cursor()

    all_data = {}
    # for every table name in the dictionary
    for table_name in hash_dict.keys():
        # get a list of all the jsons from the table
        cur.execute('SELECT json from '+table_name)
        print('Generating '+table_name+' dictionary....')

        # this returns a list of tuples: the first item in each tuple is our json
        items = cur.fetchall()

        # create a list of jsons
        item_jsons = [json.loads(item[0]) for item in items]

        # create a dictionary with the hashes as keys
        # and the jsons as values
        item_dict = {}
        hash = hash_dict[table_name]
        for item in item_jsons:
            item_dict[item[hash]] = item

        # add that dictionary to our all_data using the name of the table
        # as a key.
        all_data[table_name] = item_dict
    print('Dictionary Generated!')
    return all_data


def init_manifest():
    # check if pickle exists, if not create one.
    if os.path.isfile(r'Manifest.content') == False:
        get_manifest()
        manifest = build_dict(hashes)
        with open('manifest.pickle', 'wb') as data:
            pickle.dump(manifest, data)
            print("'manifest.pickle' created!\nDONE!")
    else:
        print('Pickle Exists')

    with open('manifest.pickle', 'rb') as data:
        manifest = pickle.load(data)

    return manifest


hashes = {
    'DestinyClassDefinition': 'hash',
    'DestinyInventoryItemDefinition': 'hash',
    'DestinyTalentGridDefinition': 'hash',
    'DestinyHistoricalStatsDefinition': 'statId',
    'DestinyStatDefinition': 'hash',
    'DestinySandboxPerkDefinition': 'hash',
    'DestinyStatGroupDefinition': 'hash',
    'DestinyInventoryBucketDefinition': 'hash'
}
