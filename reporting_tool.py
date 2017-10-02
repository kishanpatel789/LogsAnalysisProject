#!/usr/bin/env python2.7

import psycopg2
import string


def get_query(query):
    """
    Connect to the database, execute query, and return results
    """
    c = psycopg2.connect("dbname=news")
    cursor = c.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    c.close()
    return results


def top_articles():
    """
    Output top 3 articles in descending order
    """
    output_title = 'Most Popular Articles \n'
    output_format = '   $article -- $views views \n'
    query = "SELECT articles.title, record.views as views \
            FROM articles, \
            (SELECT path, count(*) as views \
            FROM log \
            GROUP BY path) as record \
            WHERE record.path = '/article/' || articles.slug \
            ORDER BY views DESC LIMIT 3;"

    query_results = get_query(query)

    top_articles = []
    for row in query_results:
        top_articles.append({'article': str(row[0]), 'views': str(row[1])})

    show_results(output_title, output_format, top_articles)


def top_authors():
    """
    Output top authors in descending ORDER
    """
    output_title = 'Most Popular Authors \n'
    output_format = '   $author -- $views views \n'
    query = "SELECT authors.name, count(name) as views \
            FROM articles, authors, log \
            WHERE articles.author = authors.id \
               AND log.path = '/article/' || articles.slug \
            GROUP BY authors.name \
            ORDER BY views DESC;"

    query_results = get_query(query)

    top_authors = []
    for row in query_results:
        top_authors.append({'author': str(row[0]), 'views': str(row[1])})

    show_results(output_title, output_format, top_authors)


def top_error_days():
    """
    Output days on which more than 1 percent of requests led to errors
    """
    output_title = 'Days on Which More Than 1% of Requests Led to Errors \n'
    output_format = '   $month $day, $year -- $percent_of_error% errors \n'
    query = "SELECT EXTRACT(YEAR FROM log.time) as year, \
            EXTRACT(MONTH FROM log.time) as month, \
            EXTRACT(DAY FROM log.time) as day, \
            ROUND(errors.num*100/requests.num::numeric, 3) as percent_of_err \
            FROM log, \
            (SELECT date_trunc('day', log.time) as date, count(*) as num \
            FROM log \
            GROUP BY date) as requests, \
            (SELECT date_trunc('day', log.time) as date, count(*) as num \
            FROM log \
            WHERE status LIKE '%404%' \
            GROUP BY date) as errors \
            WHERE date_trunc('day', log.time) = requests.date AND \
            	    date_trunc('day', log.time) = errors.date AND \
                    errors.num*100/requests.num::float >= 1 \
            GROUP BY year, month, day, errors.num, requests.num \
            ORDER BY year, month, day;"

    query_results = get_query(query)

    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
              'August', 'September', 'October', 'November', 'December']
    month_converter = {num: month for num, month in enumerate(months, 1)}

    top_error_days = []
    for row in query_results:
        top_error_days.append({'year': str(int(row[0])),
                               'month': month_converter[int(row[1])],
                               'day': str(int(row[2])),
                               'percent_of_error': str(float(row[3]))})

    show_results(output_title, output_format, top_error_days)


def show_results(output_title, output_format, results):
    """
    Format and return results
    """
    output = output_title
    template = string.Template(output_format)
    for entry in results:
        output += template.safe_substitute(entry)

    print output


top_articles()
top_authors()
top_error_days()
