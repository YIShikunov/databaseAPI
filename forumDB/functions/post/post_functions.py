from forumDB.functions.database import exec_insert_update_delete_query, Database, exec_select
from forumDB.functions.common import RequestError
from forumDB.functions.post.getters import post_to_json
import MySQLdb as mDB


def create_post(required_parameters, optional_parameters):
    info = {
        'date': required_parameters['date'],
        'thread': required_parameters['thread'],
        'message': required_parameters['message'],
        'user': required_parameters['user'],
        'forum': required_parameters['forum'],
    }
    db = mDB.connect(Database.host, Database.user, Database.password, Database.database, init_command='SET NAMES UTF8')
    cursor = db.cursor()

    cursor.execute('select id from Users where email = %s', (required_parameters['user'],))
    u_id = cursor.fetchone()[0]

    cursor.execute('select id from Forums where short_name = %s', (required_parameters['forum'],))
    f_id = cursor.fetchone()[0]

    query = 'insert into Posts (date , thread , message , user , forum, u_id, f_id '
    values = "( %s , %s , %s , %s , %s , %s, %s  "
    query_parameters = [required_parameters['date'], required_parameters['thread'],
                        required_parameters['message'], required_parameters['user'],
                        required_parameters['forum'], u_id, f_id]
    for parameter in optional_parameters:
        if optional_parameters[parameter] is not None:
            query += ',' + parameter
            values += ', %s '
            query_parameters.append(optional_parameters[parameter])
            info[parameter] = optional_parameters[parameter]

    query += ') values ' + values + ')'
    cursor.execute(query, query_parameters)
    db.commit()
    info['id'] = cursor.lastrowid
    cursor.execute('update Threads set posts = posts + 1 where id = %s', (required_parameters['thread'],))
    db.commit()
    cursor.close()
    db.close()

    return info


def post_vote(required_params):
    db = mDB.connect(Database.host, Database.user, Database.password, Database.database, init_command='SET NAMES UTF8')
    cursor = db.cursor()

    if required_params['vote'] == 1:
        cursor.execute(
            'update Posts set likes = likes + 1 , points = points + 1 where id = %s', (required_params['post'],))
    if required_params['vote'] == -1:
        cursor.execute(
            'update Posts set dislikes = dislikes + 1, points = points - 1 where id = %s',
            (required_params['post'],))
    db.commit()

    cursor.execute('select date , dislikes , forum , id , isApproved , isDeleted , isEdited , '
                                   'isHighlighted , isSpam , likes , message , parent , points , thread , user from Posts'
                                   ' where id = %s ', (required_params['post'],))
    post = cursor.fetchone()
    cursor.close()
    db.close()
    return post_to_json(post)




def post_update(required_params):
    db = mDB.connect(Database.host, Database.user, Database.password, Database.database, init_command='SET NAMES UTF8')
    cursor = db.cursor()

    cursor.execute("update Posts set message = %s where id = %s",
                                    (required_params['message'], required_params['post'],))
    db.commit()
    cursor.execute('select date , dislikes , forum , id , isApproved , isDeleted , isEdited , '
                                   'isHighlighted , isSpam , likes , message , parent , points , thread , user from Posts'
                                   ' where id = %s ', (required_params['post'],))
    post = cursor.fetchone()
    cursor.close()
    db.close()
    return post_to_json(post)


def post_remove_restore(required_params, type):
    id = required_params['post']
    if type == 'remove':
        result = exec_select("select isDeleted from Posts where id = %s", (id,))
        if (result is None or len(result) == 0):
            raise RequestError("No such post exists.", 1)
        if (result[0][0] == 0):
            exec_insert_update_delete_query("update Posts set isDeleted = 1 where id = %s", (id,))
            exec_insert_update_delete_query("update Threads t inner join Posts p on p.thread = t.id set t.posts = t.posts-1 where p.id = %s", (id,))            
    if type == 'restore':
        result = exec_select("select isDeleted from Posts where id = %s", (id,))
        if (result[0][0] == 1):
            exec_insert_update_delete_query("update Posts set isDeleted = 0 where id = %s", (id,))
            exec_insert_update_delete_query("update Threads t inner join Posts p on p.thread = t.id set t.posts = t.posts+1 where p.id = %s", (id,)) 
    return {'post': id}