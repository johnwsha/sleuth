import os
from flask import Flask, request, render_template, jsonify, redirect, url_for
# import final_once.py
from final_while import main
import json

app = Flask(__name__, static_url_path='', template_folder="static")

global data
data = []

@app.route('/', methods=['GET'])
def root():
	# File should be in 'static' directory
	return app.send_static_file('index.html')

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
	return render_template('register.html')

@app.route('/partyinput', methods=['GET', 'POST'])
def partyinput():
	# ename = session.get('email', None)\

	return render_template('partyinput.html')

@app.route('/partyinfo', methods=['GET', 'POST'])
def partyinfo():
	grouped = main(read_json('groups.json'))
	meeting1 = grouped['meetarray'][0]
	return render_template('partyinfo.html', meeting1=meeting1)

@app.route('/grouping', methods=['GET', 'POST'])
def grouping():

	# need these here atm or else error
	# these will reset data and ename to empty every time /pickaparty is refreshed
	# we want to replace this with reading from database (fixes resetting data problem)
	# in database, if no data or ename, set as {} (empty dictionary)
	ename = "John"

	# append new data into data
	# save as txt file

	if request.method == 'POST':
		print("post request")

		print(request.json)
		if 'data' in request.json:
			data.append(request.json['data']) # pulling the data from post request

			with open("groups.json", "w") as f:
				f.write(json.dumps(data, indent=4))

		# if 'ename' in request.json:
		# 	ename = request.json['ename']
		# else:
		# 	ename = {}
	print("data:", data)

	return render_template('pickaparty.html', data=data, ename=ename) # this is temp

@app.route('/kNN')
def kNN():
	grouped = main(read_json('groups.json'))
	print("kNN grouped", grouped)
	# return grouped
	return jsonify(grouped=grouped)

@app.route('/show_data')
def show_data():
	return jsonify(data=data)

@app.route('/delete')
def delete():
	data = []
	clear_text()
	return jsonify(data=data)

def read_json(json_file):
    with open(json_file) as j_file:
        data = json.load(j_file)
    # pp.pprint(data)
    return data

def clear_text():
	data = []
	with open("groups.json", "w") as f:
		f.write(json.dumps(data, indent=4))


# @app.before_first_request
# def activate_job():
# 	"""
# 	Runs before first request.
# 	Creates new thread for run_job()
# 	run_job is used to call a recurring background task
# 	Runs kNN at regular intervals in the background
# 	"""
# 	def run_job():
# 		time.sleep(30) # run every 30 seconds
# 		while True:
# 			print("Run recurring task")
#
# 			# read from file
# 			data = read_json("groups.json")
# 			final_once.main(data)
#
# 			# clear data .txt file
# 			clear_text()
#
# 			print("waiting")
# 			time.sleep(300) # pause 5 minutes
#
# 		thread = threading.Thread(target=run_job)
# 		thread.start()

# Run the app
if __name__ == '__main__':
	app.run(debug=True)
