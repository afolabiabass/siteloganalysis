import psycopg2
import datetime

# What are the most popular three articles of all time?

db = psycopg2.connect("dbname=news")
c = db.cursor()

query = "select a.title, count(a.title) as total  from (select title, CONCAT('/article/', slug) as articlepath" \
        " from articles) as a left join log on a.articlepath = log.path group by a.title order by total desc limit 3"

c.execute(query)
rows = c.fetchall()

print "What are the most popular three articles of all time?"
for row in rows:
    print row[0] + ' - ' + str(int(row[1])) + ' views'

db.close()

# Who are the most popular article authors of all time?

db = psycopg2.connect("dbname=news")
c = db.cursor()

query = "select a.authorname, count(a.title) as total  from (select title, CONCAT('/article/', slug) as articlepath, authors.name as authorname" \
        " from articles, authors where articles.author = authors.id ) as a left join log on a.articlepath = log.path group by a.authorname order by total desc limit 3"

c.execute(query)
rows = c.fetchall()

print "Who are the most popular article authors of all time?"
for row in rows:
    print row[0] + ' - ' + str(int(row[1])) + ' views'

db.close()

# On which days did more than 1% of requests lead to errors?

db = psycopg2.connect('dbname=news')
c = db.cursor()

query = "select * from (select a.badtime as t, ((cast(a.badtotal as float) / cast(b.alltotal as float)) * 100) as percent from " \
        "(select cast(time as date) as badtime, count(cast(time as date)) as badtotal from log where status != '200 OK' group by cast(time as date)) as a " \
        "left join (select cast(time as date) as alltime, count(cast(time as date)) as alltotal from log group by cast(time as date)) as b " \
        "on a.badtime = b.alltime order by percent desc) as c where percent > 1"

c.execute(query)
rows = c.fetchall()

print "On which days did more than 1% of requests lead to errors?"
for row in rows:
    print row[0].strftime('%B %d, %Y') + ' - ' + str(float(row[1])) + '%'
    # print row
db.close()
