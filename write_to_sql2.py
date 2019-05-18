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





