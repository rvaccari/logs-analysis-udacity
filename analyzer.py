import psycopg2
from psycopg2._psycopg import ProgrammingError

view_logs = "CREATE VIEW view_logs AS " \
            "    SELECT  " \
            "		path, " \
            "		ip, " \
            "		method, " \
            "		status, " \
            "		date(time) as date, " \
            "		id " \
            "    FROM log "

view_log_total = " CREATE VIEW view_log_total AS " \
                 "	select lo.date " \
                 "	,count(lo.id) as total " \
                 "	,(select count(view_logs.id) " \
                 "    from view_logs " \
                 "    where date(view_logs.date)=date(lo.date) " \
                 "    and view_logs.status != '200 OK') as com_erro " \
                 "	,(select count(view_logs.id) " \
                 "    from view_logs " \
                 "    where date(view_logs.date)=date(lo.date) " \
                 "    and view_logs.status = '200 OK') as sem_erro " \
                 "	from view_logs lo " \
                 "	group by lo.date "


def cria_views(cur):
    cur.execute(view_logs)
    cur.execute(view_log_total)


def check_views(cur):
    try:
        sql = 'select * from view_log_total limit 1'
        cur.execute(sql)
    except ProgrammingError as e:
        cria_views(cur)


def questao_1(cur):
    sql = "SELECT ar.title, COUNT(ar.id) total " \
          "FROM articles ar " \
          "LEFT JOIN log AS lo " \
          "  ON (lo.path =  CONCAT('/article/',ar.slug)) " \
          "GROUP BY ar.title " \
          "ORDER BY total DESC " \
          "LIMIT 3 "
    cur.execute(sql)
    top_3 = cur.fetchall()
    for top in top_3:
        print(f'{top[0]} - {top[1]} views')


def questao_2(cur):
    sql = "SELECT au.name, COUNT(au.id) total  " \
          "FROM articles ar  " \
          "LEFT JOIN log AS lo  " \
          "  ON (lo.path =  CONCAT('/article/',ar.slug)) " \
          "LEFT JOIN authors as au " \
          "  on (au.id = ar.author) " \
          "GROUP BY au.name  " \
          "ORDER BY total DESC  "

    cur.execute(sql)
    authors = cur.fetchall()
    for author in authors:
        print(f'{author[0]} - {author[1]} views')


def questao_3(cur):
    sql = " select lt.date " \
          " ,ROUND(cast((lt.com_erro * 100) as decimal) / lt.total, 2) as percent_erro " \
          " from view_log_total lt " \
          " where (cast((lt.com_erro * 100) as decimal) / lt.total) > 1 "

    cur.execute(sql)
    authors = cur.fetchall()
    for author in authors:
        print(f'{author[0]} - {author[1]}% errors')


def conexao(db_name='news'):
    con = psycopg2.connect(
        dbname=db_name,
        user='vagrant',
        host='127.0.0.1')
    con.autocommit = True
    cur = con.cursor()
    return con, cur


if __name__ == '__main__':
    con, cur = conexao()
    check_views(cur)
    while True:
        print('0. Exit')
        print('1. Quais são os três artigos mais populares de todos os tempos?')
        print('2. Quem são os autores de artigos mais populares de todos os tempos?')
        print('3. Em quais dias mais de 1% das requisições resultaram em erros?')
        option = int(input('Opção: '))
        print()
        if option == 0:
            break
        elif option == 1:
            questao_1(cur)
        elif option == 2:
            questao_2(cur)
        else:
            questao_3(cur)
        print()
    con.close()
