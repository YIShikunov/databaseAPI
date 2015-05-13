import MySQLdb as mDB
from forumDB.functions.database import Database

def get_user_details(value, type, cursor):
    if cursor is None:
        db = mDB.connect(Database.host, Database.user, Database.password, Database.database, init_command='SET NAMES UTF8')
        new_cursor = db.cursor()
    else:
        new_cursor = cursor

    query = """select about, email, Users.id, isAnonymous, name, username, group_concat(thread) from Users
              left join Subscriptions on Users.id = Subscriptions.u_id where Users.""" + type + "= %s "
    new_cursor.execute(query, (value, ))
    result = new_cursor.fetchone()

    #######
    if result is None:
        raise RequestError("No such post exists", 1)
    #######

    if result[6] is not None:
        subscriptions = map(int, result[6].split(','))
    else:
        subscriptions = []

    if type == 'email':
        value = result[2]
    query = 'select email from Followers f join Users u on u.id = f.follower where followee = %s'
    new_cursor.execute(query, (value, ))
    followers = new_cursor.fetchall()

    query = 'select email from Followers f join Users u on u.id = f.followee where follower = %s'
    new_cursor.execute(query, (value, ))
    following = new_cursor.fetchall()

    followers = [i[0] for i in followers]
    following = [i[0] for i in following]

    if cursor is None:
        new_cursor.close()
        db.close()

    return {
        'about': result[0],
        'email': result[1],
        'id': result[2],
        'isAnonymous': result[3],
        'name': result[4],
        'username': result[5],
        'subscriptions': subscriptions,
        'followers': followers,
        'following': following
    }


def get_list_followers2(required_params, optional_params):

    if required_params['type'] == 'follower':
        column = 'followee'
    if required_params['type'] == 'followee':
        column = 'follower'

    db = mDB.connect(Database.host, Database.user, Database.password, Database.database, init_command='SET NAMES UTF8')
    cursor = db.cursor()

    query = "select " + required_params['type'] + " from Followers f join Users u on f." + column + \
            "=u.id where u.email= %s"
    query_params = [required_params['user']]

    if optional_params['since_id'] is not None:
        query += ' and ' + required_params['type'] + ' >= %s '
        query_params.append(int(optional_params['since_id']))

    if optional_params['order'] is not None:
        query += ' order by u.name ' + optional_params['order']
    else:
        query += ' order by u.name desc '

    if optional_params['limit'] is not None:
        query += ' limit ' + optional_params['limit']

    cursor.execute(query, query_params)
    users = cursor.fetchall()
    result = []
    if len(users) != 0:
        for row in users:
            result.append(get_user_details(row[0], 'id', cursor))

    cursor.close()
    db.close()
    return result


def get_forum_user_list(required_params, optional_params):
    db = mDB.connect(Database.host, Database.user, Database.password, Database.database, init_command='SET NAMES UTF8')
    cursor = db.cursor()

    cursor.execute('select id from Forums where short_name = %s', (required_params['forum'], ))
    f_id = cursor.fetchone()[0]

    query = """select distinct u_id
        from Posts p inner join Users u on u.id = p.u_id
        where p.f_id = %s """
    query_params = [f_id]

    if optional_params is not None:
        if optional_params['since_id'] is not None:
            query += ' and u_id >= %s '
            query_params.append(optional_params['since_id'])

        if optional_params['order'] is not None:
            query += ' order by u.name ' + optional_params['order']
        else:
            query += ' order by u.name desc '

        if optional_params['limit'] is not None:
            query += ' limit ' + optional_params['limit']

    list = []
    cursor.execute(query, query_params)
    result = cursor.fetchall()
    for element in result:
        list.append(get_user_details(element[0], 'id', cursor))

    cursor.close()
    db.close()
    return list