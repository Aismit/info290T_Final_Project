from flask import Flask, jsonify, request, Response, render_template, url_for
from flask_api import status
from MySQLdb import _mysql
import mysql.connector
import numpy as np
import os, json, requests
import pandas as pd
import shutil
import matplotlib.pyplot as plt

app = Flask(__name__)

query_parts = {}

# with app.app_context(), app.test_request_context():
# 	print(url_for('static', filename='css/selection.css', _external =True), flush=True)

@app.route('/', methods=["GET"])
def get_selection_page():
	#with app.app_context(), app.test_request_context():
		#print(url_for('static', filename='css/selection.css', _external =True), flush=True)
	return render_template('selection.html')

# @app.route('/police', methods=["POST"]):
# def get_police_page():
# 	path = request.form()
# 	return 

def contains_helper(val, val_to_search):
	print(list(val), flush=True)
	for elem in val:
		print(elem, flush=True)
		if val_to_search in val.get(elem):
			return val.get(elem)
	return False



@app.route('/visualize', methods=["POST"])
def visualize():
	#print("hjsdfsdfs", flush=True)
	#val = request.form['value']
	global query_parts
	count = 0
	val_to_add = []
	if request.form.get('start_year_value') != "":
		val_to_add += ['Time > ' + str(request.form.get('start_year_value'))]
		count += 1 
	if request.form.get('end_year_value') != "":
		val_to_add += ["Time < " + str(request.form.get('end_year_value'))]
		count += 1
	if request.form.get("description_text") != "":
		val_to_add += ["VictimDescription like %{" + str(request.form.get("description_text")) + "!= }%"]
		count += 1
	if request.form.get("precincts_entered") != "":
		precincts = request.form.get("precincts_entered").split(",")
		temp = ""
		if len(precincts) > 1:
			for elem in precincts:
				temp += "Precinct like %'" + elem + "'' OR "
		temp = temp[:-4]
		val_to_add += ["(" + temp + ")"]
		count += 1
	temp = contains_helper(request.form, "weapons:")
	print(temp, flush=True)
	if temp:
		#weapons = request.form.get(temp)
		#print(weapons, flush=True)
		col_index = temp.find(":")
		weapons = temp[col_index + 1:]
		weapons = weapons.split(",") 
		print(weapons, flush=True)
		temp = ""
		if len(weapons) > 1:
			for elem in weapons:
				temp += "Weapon like '%" + elem + "%' OR "
		temp = temp[:-4]
		val_to_add += ["(" + temp + ")"]
		count += 1
	if count > 0:
		sql = "Select * from final_dataset where City = '" + str(query_parts['location']) + "'"
		for val in val_to_add:
			sql += " AND " + val
		#sql = sql[:-5]
		sql = sql + ";"
		print(sql, flush=True) 
	else:
		sql = "Select * from final_dataset where City = '" + str(query_parts['location']) + "' ;"
	#print(request.form['value1'], flush=True)
	#sql = 'select * from crime2 where City="BOS" and Weapon like "%FIREARM%"'
	query_parts["sql"] = sql
	cursor.execute(sql)
	data = pd.DataFrame(cursor.fetchall())
	print(sql, flush=True)
	print(data.count, flush=True)
	#data.to_csv('boston.csv',index=False) 
	data.to_html('tempdata.html')
	print(os.listdir(), flush=True)
	#print(os.getcwd(), flush=True)
	#print(os.listdir(), flush=True)
	shutil.move('tempdata.html', 'templates/tempdata.html')
	print(os.listdir(), flush=True)
	print(request.form, flush=True)
	return render_template('visualize.html')

@app.route('/gbl', methods=["GET", "POST"])
def gbl():
	global query_parts
	sql = query_parts["sql"]
	count = sql.find("*")
	sql = sql[:count] + "Location, count(*)" + sql[count + 1: -1] + " group by Location;"
	print(sql, flush=True)
	cursor.execute(sql)
	data = pd.DataFrame(cursor.fetchall())
	print(list(data.columns), flush=True)
	plt.clf()
	df = pd.DataFrame({'location':list(data[1].values)}, index = list(data[0].values))
	print(df.count, flush=True)
	ax = df.plot(kind="bar",use_index=True, rot=90)
	#bar(rot=90)
	fig = ax.get_figure()
	print(os.listdir(), flush=True)
	fig.savefig("temp2.png", dpi=100, bbox_inches = 'tight')
	#plt.show()
	#plt.xticks(rotation=90)
	#plt.savefig("temp.png")
	plt.clf()

	print(os.listdir(), flush=True)
	shutil.move('temp2.png', 'static/temp2.png')
	#os.chdir("static")
	#print(os.listdir(), flush=True)
	return render_template('showgraph.html')

@app.route('/groupbylocation', methods=["GET", "POST"])
def groupbylocation():
	global query_parts
	sql = query_parts["sql"]
	count = sql.find("*")
	sql = sql[:count] + "Location, count(*)" + sql[count + 1: -1] + " group by Location;"
	print(sql, flush=True)
	return render_template('nyc.html')

@app.route('/data', methods=["GET", "POST"])
def data():
	global query_parts
	query_parts['info'] = 'crimes'
	print("YESS", flush=True)
	return render_template('crimez.html')
	

@app.route('/crimes', methods=["GET", "POST"])
def crimes():
	global query_parts
	query_parts['info'] = 'crimes'
	print("YESS", flush=True)
	return render_template('crimez.html')

@app.route('/showdata', methods=["GET","POST"])
def showdata():
	global query_parts
	query_parts['info'] = 'crimes'
	print("YESS", flush=True)
	return render_template('tempdata.html')

@app.route('/offenders', methods=["GET"])
def offenders():
	global query_parts
	query_parts['info'] = 'offenders'
	return render_template('offenders.html')


@app.route('/nyc', methods=["GET"])
def nyc():
	global query_parts
	query_parts['location'] = 'NYC'
	return render_template('nyc.html')

@app.route('/bos', methods=["GET"])
def bos():
	global query_parts
	query_parts['location'] = 'BOS'
	return render_template('nyc.html')


@app.route('/atl', methods=["GET"])
def atl():
	global query_parts
	query_parts['location'] = 'ATL'
	return render_template('atl.html')

@app.route('/aus', methods=["GET"])
def aus():
	global query_parts
	query_parts['location'] = 'AUS'
	return render_template('aus.html')

@app.route('/chi', methods=["GET"])
def chi():
	global query_parts
	query_parts['chi'] = 'CHI'
	return render_template('chi.html')

@app.route('/journalist', methods=["GET"])
def journalist():
	return render_template('journalist.html')

if __name__ == '__main__':
    db = mysql.connector.connect(host='db290tproj', user='root', passwd='pw', database='db290TProj')
    cursor = db.cursor(buffered=True)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)