# Logs Analysis Project

## System Requirements
* Python
* psycopg2
* Postgresql
* Virtual Machine Setup

## Project Questions
1. What are the most popular three articles of all time?
  Which articles have been accessed the most?
  Present this information as a sorted list with the most popular article at the top
2. Who are the most popular article authors of all time?
  That is, when you sum up all of the articles each author has written, which authors get the most page views?
  Present this as a sorted list with the most popular author at the top.
3. On which days did more than 1% of requests lead to errors?
  The log table includes a column status that indicates the HTTP status code that the news site sent to the user's browser.


* Download the data
You will need to unzip the newsdata file after downloading it. The file inside is called newsdata.sql. Put this file into the vagrant directory, which is shared with your virtual machine.  To build the reporting tool, you'll need to load the site's data into your local database.

* Load data onto the database
```sql
psql -d news -f newsdata.sql
```
* Connect to database
```sql
psql -d news
```
* Create the views listed below while connected to the DB
* Run python3 YanalLogsAnalysis.py after existing DB

### Create Views
```sql
CREATE VIEW author_details AS
SELECT authors.name, articles.title, articles.slug
FROM articles
join authors on (articles.author = authors.id)
ORDER BY authors.name;
```

```sql
CREATE VIEW log_path_total_views AS
SELECT path, COUNT(*) AS view
FROM log
GROUP BY path
ORDER BY path;
```

```sql
CREATE VIEW art_total_views AS
SELECT author_details.name, author_details.title, log_path_total_views.view
FROM author_details join log_path_total_views
ON (substring(log_path_total_views.path, 10) = author_details.slug)
ORDER BY log_path_total_views.view DESC;
```

```sql
CREATE VIEW total_daily_view AS
SELECT date(time), COUNT(*) AS views
FROM log
GROUP BY date(time)
ORDER BY date(time);
```

```sql
CREATE VIEW error_daily_view AS
SELECT date(time), COUNT(*) AS errors
FROM log WHERE status like '4%'
GROUP BY date(time)
ORDER BY date(time);
```

```sql
CREATE VIEW daily_error_rate AS
SELECT total_daily_view.date, (100.0*error_daily_view.errors/total_daily_view.views) AS percentage
FROM total_daily_view join error_daily_view
ON (total_daily_view.date = error_daily_view.date)
ORDER BY total_daily_view.date;
```
## Authors

* **Yanal Altidoka**
