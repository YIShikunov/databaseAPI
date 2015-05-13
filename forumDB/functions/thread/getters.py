from forumDB.functions.database import Database
from forumDB.functions.user.getters import get_user_details
from forumDB.functions.common import RequestError, ResponseCodes
import MySQLdb as mDB

def thread_to_json(thread):
    return {
        'date': str(thread[0]),
        'dislikes': int(thread[1]),
        'forum': thread[2],
        'id': int(thread[3]),
        'isClosed': bool(thread[4]),
        'isDeleted': bool(thread[5]),
        'likes': int(thread[6]),
        'message': thread[7],
        'points': int(thread[8]),
        'posts': int(thread[9]),
        'slug': thread[10],
        'title': thread[11],
        'user': thread[12]
    }


def get_thread_details(thread, related, cursor):
    from forumDB.functions.forum.getters import forum_to_json
    thread_parameters = ' date, dislikes , forum , Threads.id , isClosed , isDeleted , likes , message ,points , posts, slug , title ,Threads.user '
    #0-12
    if related is not None and 'forum' in related:
        forum_parameters = 'Forums.id, name , short_name , Forums.user '
    #12-16
        query = 'select ' + thread_parameters + ',' + forum_parameters + \
                "from Threads inner join Forums on Threads.f_id = Forums.id where Threads.id = %s"
    else:
        query = "select " + thread_parameters + " from Threads where id = %s"

    if cursor is None:
        db = mDB.connect(Database.host, Database.user, Database.password, Database.database, init_command='SET NAMES UTF8')
        new_cursor = db.cursor()
    else:
        new_cursor = cursor

    new_cursor.execute(query, (thread,))
    result = new_cursor.fetchone()



    #######
    if result is None:
        raise RequestError("No such post exists", 1)
    #######

    info = thread_to_json(result)

    if (related is not None and [x for x in related if x not in ['user', 'forum']]):
        raise RequestError("One of related values is incorrect." + str(related), ResponseCodes.INVALID_REQUEST)

        
    if related is not None:
        if 'user' in related:
            info['user'] = get_user_details(info['user'], 'email', new_cursor)
        if 'forum' in related:
            info['forum'] = forum_to_json(result[13:17])

    if cursor is None:
        new_cursor.close()
        db.close()
    return info


def get_list(what, value, optional_params):
    db = mDB.connect(Database.host, Database.user, Database.password, Database.database, init_command='SET NAMES UTF8')
    cursor = db.cursor()

    if what == 'user':
        cursor.execute('select id from Users where email = %s', (value,) )
        value = cursor.fetchone()[0]
        query = """select date, dislikes , forum , id , isClosed , isDeleted , likes , message ,points , posts, slug , title ,
                user from Threads where u_id = %s """
    if what == 'forum':
        cursor.execute('select id from Forums where short_name = %s', (value,) )
        value = cursor.fetchone()[0]
        query = """select date, dislikes , forum , id , isClosed , isDeleted , likes , message ,points , posts, slug , title ,
                user from Threads where f_id = %s """
    query_params = [value]

    if optional_params['since'] is not None:
        query += ' and date >= %s '
        query_params.append(optional_params['since'])

    if optional_params['order'] is not None:
        query += ' order by date ' + optional_params['order']
    else:
        query += ' order by date desc '

    if optional_params['limit'] is not None:
        query += ' limit ' + str(optional_params['limit'])

    cursor.execute(query, query_params)
    list = cursor.fetchall()
    array = []
    for row in list:
        array.append(thread_to_json(row))

    cursor.close()
    db.close()
    return array