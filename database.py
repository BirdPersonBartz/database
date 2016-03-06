import sqlite3 as sql
import pandas as pd 


city_table = 'cities'
weather_table = 'weather'

city_colc = 'city'
city_colw = 'cityname'
state_col = 'state'
year_col = 'year'
w_month = 'warm_month'
c_month = 'cold_month'
avg_high = 'avg_high'
text_type = 'text'
integer_type = 'integer'

citiesinput = (('NYC','NY'),
				('Boston','MA'),
				('Chicago','IL'),
				('Miami','FL'),
				('Dallas','TX'),
				('Seattle','WA'))
weatherinput = (('NYC',2013,'July','Jan',62),
				('Boston',2013,'July','Jan',59),
				('Chicago',2013,'July','Jan',59),
				('Miami',2013,'Aug','Jan',84),
				('Dallas',2013,'July','Jan',77),
				('Seattle',2013,'July','Jan',61))
citiesstmt = "INSERT INTO cities VALUES (?,?);"
weatherstmt = "INSERT INTO weather VALUES (?,?,?,?,?);"


con = sql.connect('getting_started.db')

with con:
	cur = con.cursor()
	cur.execute("DROP TABLE IF EXISTS cities")
	cur.execute("DROP TABLE IF EXISTS weather")
	cur.execute('CREATE TABLE {tn} ({fn1} {ft1}, {fn2} {ft1})'\
		.format(tn=city_table, fn1=city_colc, ft1=text_type, fn2=state_col))
	cur.execute('CREATE TABLE {tn} ({fn1} {ft1}, {fn2} {ft2}, {fn3} {ft1}, {fn4} {ft1}, {fn5} {ft1})'\
		.format(tn=weather_table, fn1=city_colw, ft1=text_type, fn2=year_col,ft2=integer_type,fn3=w_month,fn4=c_month,fn5=avg_high))
	cur.executemany(citiesstmt, citiesinput)
	cur.executemany(weatherstmt, weatherinput)
	cur.execute("SELECT cityname, state, warm_month FROM weather INNER JOIN cities ON (city=cityname) WHERE warm_month ='July';")
	rows=cur.fetchall()
	cols = [desc[0] for desc in cur.description]
	df = pd.DataFrame(rows, columns=cols)
	print('The cities warmest in July are %s' % ', '.join(df['cityname']))