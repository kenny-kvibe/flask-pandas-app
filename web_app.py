#pyright: reportUnusedFunction=none
# Docs:  https://flask.palletsprojects.com/
import pandas as pd
import psutil
import socket
from flask import Blueprint, Flask, render_template, request
from werkzeug.exceptions import HTTPException

import constants as c
import functions as f


def init_app(name:str = __name__) -> Flask:
	return Flask(name)


def send_error_response(title:str, code:int, error_html:str) -> tuple[str, int]:
	return (
		render_template(
			'error.html',
			page_title=title,
			head_title='Error',
			error_code=code,
			error_html=error_html),
		code)


def register_routes(app:Flask, df:pd.DataFrame):
	title = 'Flask App'

	view = Blueprint(
		'view',
		__name__,
		url_prefix='/',
		static_folder=c.FLASK_STATIC_DIR_PATH,
		template_folder=c.FLASK_TEMPLATES_DIR_PATH)

	# === index ==================
	@view.route('/', methods=['GET'])
	def index():
		return render_template(
			'home.html',
			page_title=title,
			head_title='Home',
			dict_table=df.to_dict())

	# === page data ==================
	@view.route('/page-data', methods=['GET', 'POST'])
	def page_data():
		table = df.copy()

		if request.method == 'POST':
			number_arg = request.form.get('number-input', '')

			if number_arg != '' and number_arg.isdigit():
				number_arg = int(number_arg)
				for col in table.columns:
					table[col] = table[col].where(table[col] == number_arg, '–')
				if not isinstance(table, pd.DataFrame):
					table = table.to_frame()
				table = table.fillna('–')

				f.sys_print(f'Number: {number_arg}')

		else:
			number_arg = ''

		# f.print_df_table(df)

		return render_template(
			'page-data.html',
			number_arg=number_arg,
			page_title=title,
			head_title='Data',
			dict_table=table.to_dict())


	# === error handler ==================
	@app.errorhandler(HTTPException)
	def error_handler(error):
		return send_error_response(title, error.code, error.name)

	app.register_blueprint(view)


def main(name:str, port:int = 80, df:pd.DataFrame|None = None, serve_locally:bool = True) -> int:
	""" Initialize the `Flask` app and run it using `DataFrame` data """
	flask_app = init_app(name)
	register_routes(flask_app, pd.DataFrame() if df is None else df)

	try:
		flask_app.run(
			host=get_local_ipv4() if serve_locally else '0.0.0.0',
			port=port,
			debug=c.DEV_MODE,
			use_debugger=c.DEV_MODE,
			use_reloader=c.DEV_MODE)
	except KeyboardInterrupt:
		return 1
	return 0


def get_local_ipv4() -> str:
	""" Get the first IPv4 address that starts with `192.168.` or get `127.0.0.1` """
	interfaces = psutil.net_if_addrs().values()

	for ifs in interfaces:
		for addr in ifs:
			if addr.family == socket.AF_INET and addr.address.startswith('192.168.'):
				return addr.address

	return '127.0.0.1'