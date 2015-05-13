from forumDB.functions.database import Database
from forumDB.functions.thread.getters import thread_to_json
from forumDB.functions.user.getters import get_user_details
import MySQLdb as mDB


def get_forum_details(short_name, related, cursor):
    if cursor is None:
        db = mDB.connect(Database.host, Database.user, Database.password, Database.database, init_command='SET NAMES UTF8')
        new_cursor = db.cursor()
    else:
        new_cursor = cursor

    new_cursor.execute('select id, name , short_name , user, u_id  from Forums where short_name = %s', (short_name,))
    forum = new_cursor.fetchone()

    #######
    if forum is None:
        raise RequestError("No such post exists", 1)
    #######

    info = forum_to_json(forum)
    if related is not None:
        if 'user' in related:
            info['user'] = get_user_details(forum[4], 'id', new_cursor)

    if cursor is None:
        new_cursor.close()
        db.close()
    return info


def forum_to_json(forum):
    return {
        'id': int(forum[0]),
        'name': forum[1],
        'short_name': forum[2],
        'user': forum[3]
    }


def get_list_posts(forum_shortname, optional_params):
    from forumDB.functions.post.getters import post_to_json

    db = mDB.connect(Database.host, Database.user, Database.password, Database.database, init_command='SET NAMES UTF8')
    cursor = db.cursor()

    cursor.execute('select id from Forums where short_name = %s', (forum_shortname, ))
    result = cursor.fetchone()

    #######
    if result is None:
        raise RequestError("No such forum exists", 1)
    #######


    f_id = result[0]
    forum = forum_shortname

    post_parameters = """p.date , p.dislikes , p.forum , p.id , p.isApproved , p.isDeleted , p.isEdited ,
        p.isHighlighted , p.isSpam , p.likes , p.message , p.parent , p.points , p.thread , p.user"""

    query = ' select ' + post_parameters

    condition = ' from Posts as p where p.f_id = %s '

    if optional_params['related'] is not None:
        if 'forum' in optional_params['related']:
            forum = get_forum_details(forum_shortname, [], cursor)

        if 'thread' in optional_params['related']:
            thread_parameters = """ t.date, t.dislikes , t.forum , t.id , t.isClosed , t.isDeleted , t.likes ,
            t.message , t.points , t.posts, t.slug , t.title , t.user"""
            query += ' , ' + thread_parameters
            condition = """ from Posts as p
                        inner join Threads as t on p.thread = t.id where p.f_id = %s"""


    query += condition

    query_params = [f_id]
    if optional_params['since'] is not None:
        query += ' and p.date >= %s '
        query_params.append(optional_params['since'])

    if optional_params['order'] is not None:
        query += ' order by p.date ' + optional_params['order']
    else:
        query += ' order by p.date desc '

    if optional_params['limit'] is not None:
        query += ' limit ' + str(optional_params['limit'])

    cursor.execute(query, query_params)

    list = cursor.fetchall()
    result = []

    for row in list:
        row_json = post_to_json(row[0:15])
        row_json['forum'] = forum
        if optional_params['related'] is not None:
            if 'thread' in optional_params['related']:
                row_json['thread'] = thread_to_json(row[15:28])

            if 'user' in optional_params['related']:
                row_json['user'] = get_user_details(row_json['user'], 'email', cursor)
        result.append(row_json)
    cursor.close()
    db.close()
    return result


def get_list_threads(required_params, optional_params):

    db = mDB.connect(Database.host, Database.user, Database.password, Database.database, init_command='SET NAMES UTF8')
    cursor = db.cursor()

    related = optional_params['related']
    value = required_params['forum']

    if related is not None and 'forum' in related:
        forum = get_forum_details(value, [], cursor)
    else:
        forum = value

    cursor.execute('select id from Forums where short_name = %s', (value,))
    value = cursor.fetchone()[0]

    query = """select date, dislikes , forum , id , isClosed , isDeleted , likes , message ,points , posts, slug ,
            title, user from Threads where f_id = %s """
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

    result = []
    for row in list:
        row_json = thread_to_json(row)
        row_json['forum'] = forum
        if related is not None and 'user' in related:
            row_json['user'] = get_user_details(row_json['user'], 'email', cursor)
        result.append(row_json)

    cursor.close()
    db.close()
    return result