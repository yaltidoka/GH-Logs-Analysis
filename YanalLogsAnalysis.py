#!/usr/bin/env python3
# Log Analysis project

import psycopg2


def main():
    # Database connection
    conn = psycopg2.connect("dbname=news")
    # Open a cursor database functions
    cur = conn.cursor()
    # 1 - select title and # of views for each title
    most_popular_articles = """
      SELECT art_total_views.title, art_total_views.view
      FROM art_total_views
      ORDER BY art_total_views.view DESC
      LIMIT 3;
    """
    cur.execute(most_popular_articles)
    print("1. What are the most popular three articles of all time?")
    for (title, view) in cur.fetchall():
        print("    {} - {} views".format(title, view))
    print("********************************************************")
    # 2 - select author and sum up all the views for each of their articles
    most_popular_authors = """
    SELECT art_total_views.name, SUM(art_total_views.view) AS author_view
    FROM art_total_views
    GROUP BY art_total_views.name
    ORDER BY author_view DESC;
    """
    cur.execute(most_popular_authors)
    print("2. Who are the most popular article authors of all time?")
    for (name, view) in cur.fetchall():
        print("    {} - {} views".format(name, view))
    print("********************************************************")
    # 3 - select the daily error rate, but only show the ones greater than 1%
    more_than_one_percent_errors = """
    SELECT *
    FROM daily_error_rate
    WHERE daily_error_rate.percentage > 1
    ORDER BY daily_error_rate.percentage DESC;
    """
    cur.execute(more_than_one_percent_errors)
    print("3. On which days did more than 1% of requests lead to errors?")
    for (date, percentage) in cur.fetchall():
        print("    {} - {:0.2f}% errors".format(date, percentage))
    print("**********************************************************")

    # Close database
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
