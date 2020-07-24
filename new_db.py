import os, pymysql

target_db_name = 'zigbang'

sqlusr = 'root'

# 각자 비밀번호 입력
sqlpwd = ''

app = [
    'map'
]

def migrating():

    conn = pymysql.connect(
            host='localhost',
            user= sqlusr,
            password=sqlpwd,
            db=target_db_name,
            charset='utf8mb4'
        )

    curs = conn.cursor()

    curs.execute('drop database '+ target_db_name)
    curs.execute('create database ' + target_db_name + ' character set utf8mb4 collate utf8mb4_general_ci')
    conn.close()

    os.system('find . -path "*/migrations/*.py"')
    os.system('find . -path "*/migrations/*.py" -not -name "__init__.py" -delete')

    os.system('python manage.py makemigrations')
    os.system('python manage.py migrate')

    return
    

migrating()

os.system('python ./initialize_total_database.py')
