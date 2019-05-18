import streets
import MySQLdb

if __name__ == '__main__':
    filename = 'config.txt'
    lineList = list()
    with open(filename) as f:
        for line in f:
            lineList.append(line)

    mydbhost = lineList[0]
    mydbhost = mydbhost.rstrip()

    mydbname = lineList[1]
    mydbname = mydbname.rstrip()

    mydbuser = lineList[2]
    mydbuser = mydbuser.rstrip()

    mydbpass = lineList[3]
    mydbpass = mydbpass.rstrip()
    db = MySQLdb.connect(host=mydbhost,
                         database=mydbname,
                         user=mydbuser,
                         password=mydbpass)
    db.autocommit(True)
    db.set_character_set('utf8')
    cur = db.cursor()

    # path_to_streets = "highway-line_ekb_str.geojson"
    # streets_dict = streets.streets_dict(path_to_streets)
    # street_insert_query = "INSERT INTO streets (name, len) VALUES ('%s', %.3f)"
    # i = 0
    # for street in streets_dict:
    #     query = street_insert_query % (street, streets_dict[street])
    #     print(query, i / len(streets_dict))
    #     cur.execute(query)
    myjson = """"
    {
"type": "FeatureCollection",
"name": "academ",
"crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } },
"features": [
{ "type": "Feature", "properties": { "id": 1 }, "geometry": { "type": "MultiPolygon", "coordinates": [ [ [ [ 60.153728474861133, 56.85551463932228 ], [ 60.336011355380947, 56.852726008377552 ], [ 60.33921692161875, 56.788806480071123 ], [ 60.239536187787976, 56.824108896974948 ], [ 60.157889442721135, 56.788941199676039 ], [ 60.129584096887527, 56.822843841725486 ], [ 60.153728474861133, 56.85551463932228 ] ] ] ] } }
]
}
    """
    dname = "Веер"
    #@f'Hello, {name}!'
    query = f'INSERT INTO districts (name, points) VALUES ({dname}, {myjson})'
    print(query)
    cur.execute(query)








