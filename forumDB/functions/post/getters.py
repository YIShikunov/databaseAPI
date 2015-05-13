from forumDB.functions.database import Database
from forumDB.functions.forum.getters import forum_to_json

from forumDB.functions.thread.getters import thread_to_json
from forumDB.functions.user.getters import get_user_details
import MySQLdb as mDB

from forumDB.functions.common import RequestError, ResponseCodes


def post_to_json(post):
    parent = post[11]
    if parent == 'null':
        parent = None
    return {
        'date': str(post[0]),
        'dislikes': int(post[1]),
        'forum': post[2],
        'id': int(post[3]),
        'isApproved': bool(post[4]),
        'isDeleted': bool(post[5]),
        'isEdited': bool(post[6]),
        'isHighlighted': bool(post[7]),
        'isSpam': bool(post[8]),
        'likes': int(post[9]),
        'message': post[10],
        'parent': parent,
        'points': int(post[12]),
        'thread': int(post[13]),
        'user': post[14]
    }


def get_post_details(post, related, cursor):
    if cursor is None:
        db = mDB.connect(Database.host, Database.user, Database.password, Database.database, init_command='SET NAMES UTF8')
        new_cursor = db.cursor()
    else:
        new_cursor = cursor

    thread_parameters = """ t.date, t.dislikes, t.forum, t.id, t.isClosed, t.isDeleted, t.likes, t.message, t.points,
                      t.posts, t.slug, t.title, t.user """

    post_parameters = """ p.date, p.dislikes, p.forum, p.id, p.isApproved, p.isDeleted, p.isEdited,
                                 p.isHighlighted, p.isSpam, p.likes, p.message, p.parent, p.points, p.thread, p.user """

    forum_parameters = """ f.id, f.name, f.short_name, f.user """

    columns = "select " + post_parameters
    tables = " from Posts p "
    forum_in_related = False
    if related is not None:
        if 'forum' in related:
            columns += ", " + forum_parameters
            tables += "join Forums f on p.f_id = f.id "
            forum_in_related = True
        if 'thread' in related:
            columns += ", " + thread_parameters
            tables += " join Threads t on p.thread = t.id "

    query = columns + tables + " where p.id = %s"

    new_cursor.execute(query, (int(post),))
    result = new_cursor.fetchone()

    #######
    if result is None:
        raise RequestError("No such post exists", 1)
    #######


    info = post_to_json(result[0:15])
    if related is not None:
        if 'user' in related:
            info['user'] = get_user_details(info['user'], 'email', new_cursor)
        if 'forum' in related:
            info['forum'] = forum_to_json(result[15:19])
        if 'thread' in related:
            if forum_in_related:
                info['thread'] = thread_to_json(result[19:32])
            else:
                info['thread'] = thread_to_json(result[15:28])

    if cursor is None:
        new_cursor.close()
        db.close()
    return info


def get_post_list(required_params, optional_params):
    db = mDB.connect(Database.host, Database.user, Database.password, Database.database, init_command='SET NAMES UTF8')
    cursor = db.cursor()
    query_params = []
    if required_params['type'] == 'user':
        type = 'u_id'
        cursor.execute('select id from Users where email= %s', (required_params['user'],))
        value = cursor.fetchone()[0]
    if required_params['type'] == 'forum':
        type = 'f_id'
        cursor.execute('select id from Forums where short_name= %s', (required_params['forum'],))
        value = cursor.fetchone()[0]
    if required_params['type'] == 'thread':
        type = 'thread'
        value = required_params['thread']

    query = """select date , dislikes , forum , id , isApproved , isDeleted , isEdited ,
    isHighlighted , isSpam , likes , message , parent , points , thread , user from Posts where """ \
            + type + " = %s"
    query_params.append(value)

    if optional_params['since'] is not None:
        query += ' and date >= %s '
        query_params.append(optional_params['since'])

    if optional_params['order'] is not None:
        query += ' order by date ' + optional_params['order']
    else:
        query += ' order by date desc '

    if optional_params['limit'] is not None:
        query += ' limit ' + optional_params['limit']

    cursor.execute(query, query_params)
    list = cursor.fetchall()
    array = []
    for row in list:
        array.append(post_to_json(row))

    cursor.close()
    db.close()
    return array
