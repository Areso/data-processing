import json

with open('academ.geojson') as json_file:
    data = json.load(json_file)
    for p in data['features']:
        a = (p['geometry'])
        for tArray in a['coordinates']:
            print(tArray)
            print(type(tArray))
            print(len(tArray))
            print(' ')

