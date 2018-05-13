#!/usr/bin/env python

import psycopg2
import datetime


def db_connect():
	""" 
	Creates and returns a connection to the database defined by DBNAME,
	as well as a cursor for the database.
	Returns:
		db, c - a tuple. The first element is a connection to the database.
				The second element is a cursor for the database.
	"""
	db = psycopg2.connect("dbname=news")
	return db.cursor()


def execute_query(query):
	"""
	execute_query takes an SQL query as a parameter. 
	Executes the query and returns the results as a list of tuples.
	args:
	query - an SQL query statement to be executed.

	returns:
	A list of tuples containing the results of the query.
	"""
	try:
		c = db_connect()
		c.execute(query)
		return c.fetchall()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)


def print_top_articles():
	"""Prints out the top 3 articles of all time."""
	query = """SELECT a.title, count(a.title) AS total
		FROM (
		SELECT title, CONCAT('/article/', slug) AS articlepath
			FROM articles
		) AS a
		LEFT JOIN log
		ON a.articlepath = log.path
		GROUP BY a.title
		ORDER BY total DESC
		LIMIT 3;"""
	results = execute_query(query)

	print "What are the most popular three articles of all time?"
	for row in results:
		print row[0] + ' - ' + str(int(row[1])) + ' views'


def print_top_authors():
	"""Prints a list of authors ranked by article views."""
	query = """SELECT a.authorname, count(a.title) AS total
		FROM (
			SELECT title, CONCAT('/article/', slug) AS articlepath,
			authors.name AS authorname
			FROM articles, authors
			WHERE articles.author = authors.id
		) AS a
		LEFT JOIN log
		ON a.articlepath = log.path
		GROUP BY a.authorname
		ORDER BY total desc
		LIMIT 3;"""
	results = execute_query(query)

	print "Who are the most popular article authors of all time?"
	for row in results:
		print row[0] + ' - ' + str(int(row[1])) + ' views'


def print_errors_over_one():
	"""Prints out the days where more than 1% of logged access requests were errors."""
	query = """SELECT *
		FROM (
			SELECT a.badtime AS t,
			((cast(a.badtotal AS float) / cast(b.alltotal AS float)) * 100) AS percent
			FROM (
				SELECT cast(time AS date) AS badtime, count(cast(time AS date)) AS badtotal
				FROM log
				WHERE status != '200 OK'
				GROUP BY cast(time AS date)
			) AS a
			LEFT JOIN (
				SELECT cast(time AS date) AS alltime, count(cast(time AS date)) AS alltotal
				FROM log
				GROUP BY cast(time as date)
			) AS b
			ON a.badtime = b.alltime
			ORDER BY percent DESC
		) AS c
		WHERE percent > 1"""
	results = execute_query(query)

	print "On which days did more than 1% of requests lead to errors?"
	for row in results:
		print row[0].strftime('%B %d, %Y') + ' - ' + str(float(row[1])) + '%'


if __name__ == '__main__':
	print_top_articles()
	print_top_authors()
	print_errors_over_one()





