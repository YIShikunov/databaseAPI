from forumDB.functions.database import Database
import MySQLdb as mDB

def create_forum(required_params):
    db = mDB.connect(Database.host, Database.user, Database.password, Database.database, init_command='SET NAMES UTF8')
    cursor = db.cursor()

    query = """select id from Users where email = %s """
    cursor.execute(query, (required_params['user'], ))
    id = cursor.fetchone()[0]

    cursor.execute('insert into Forums (name , short_name , user, u_id ) values (%s , %s , %s, %s )',
                                         (required_params['name'], required_params['short_name'],
                                          required_params['user'], id ,))
    db.commit()
    id = cursor.lastrowid
    cursor.close()
    db.close()
    return {
        'name': required_params['name'],
        'short_name': required_params['short_name'],
        'user': required_params['user'],
        'id': id
    }
