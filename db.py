import sqlite3


def check_client(client_id):
    connection = sqlite3.connect('db.sqlite')
    cursor = connection.cursor()
    cursor.execute('SELECT client_id FROM conversation WHERE client_id=?', (client_id,))
    connection.commit()
    client = cursor.fetchall()
    try:
        client = client[0][0]
        return True
    except IndexError:
        return False


def add_topic(client_name, client_id, topic):
    connection = sqlite3.connect('db.sqlite')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO conversation (client_name, client_id, topic) VALUES (?,?,?)',
                       (client_name, client_id, topic,))
    connection.commit()


def new_operator(name, id):
    connection = sqlite3.connect('db.sqlite')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO operators (name, telegram_id, busy) VALUES (?,?,0)',
                       (name, id,))
    connection.commit()


def delete_operator(id):
    connection = sqlite3.connect('db.sqlite')
    cursor = connection.cursor()
    cursor.execute("DELETE FROM operators WHERE telegram_id=?", (id,))
    connection.commit()


def get_operators():
    connection = sqlite3.connect('db.sqlite')
    cursor = connection.cursor()
    cursor.execute('SELECT telegram_id FROM operators WHERE busy=0')
    connection.commit()
    operators = cursor.fetchall()
    print(operators)
    operators = operators[0]
    return operators


def add_operator(operator, topic):
    connection = sqlite3.connect('db.sqlite')
    cursor = connection.cursor()
    cursor.execute('UPDATE conversation SET operator = ? WHERE topic=?', (operator, topic))
    cursor.execute('UPDATE operators SET busy = 1 WHERE telegram_id = ?', (operator,))
    connection.commit()


def get_client(operator):
    connection = sqlite3.connect('db.sqlite')
    cursor = connection.cursor()
    cursor.execute('SELECT client_id FROM conversation WHERE operator=?', (operator,))
    connection.commit()
    client = cursor.fetchall()
    return client[0][0]


def get_conversations():
    connection = sqlite3.connect('db.sqlite')
    cursor = connection.cursor()
    cursor.execute('SELECT client_name, topic FROM conversation WHERE operator is NULL')
    connection.commit()
    conversations = cursor.fetchall()
    return conversations


def get_operator(client):
    connection = sqlite3.connect('db.sqlite')
    cursor = connection.cursor()
    cursor.execute('SELECT operator FROM conversation WHERE client_id=?', (client,))
    connection.commit()
    operator = cursor.fetchall()
    return operator[0][0]


def stop_conv(client, operator):
    connection = sqlite3.connect('db.sqlite')
    cursor = connection.cursor()
    cursor.execute("DELETE FROM conversation WHERE client_id=?", (client,))
    cursor.execute('UPDATE operators SET busy = 0 WHERE telegram_id = ?', (operator,))
    connection.commit()


if __name__ == '__main__':
    connection = sqlite3.connect('db.sqlite')
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE operators (id INTEGER PRIMARY_KEY, name TEXT, telegram_id INTEGER, busy INTEGER)')
    connection.commit()
    connection = sqlite3.connect('db.sqlite')
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE conversation (id INTEGER PRIMARY_KEY, client_name TEXT, '
                       'client_id INTEGER, operator INTEGER, topic TEXT)')
    connection.commit()
