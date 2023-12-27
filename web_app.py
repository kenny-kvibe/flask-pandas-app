#pyright: reportUnusedFunction=none
# Docs:  https://flask.palletsprojects.com/
import pandas as pd
from flask import Blueprint, Flask, render_template, request
from waitress import serve
from werkzeug.exceptions import HTTPException

import constants as c
import functions as f



def run(name: str, port: int = 80, df: pd.DataFrame | None = None, serve_locally: bool = True) -> int:
	""" Initialize the `Flask` app and run it using `DataFrame` data """
	app = init_app(name)
	register_routes(app, pd.DataFrame() if df is None else df)

	try:
		host = f.get_local_ipv4() if serve_locally else '0.0.0.0'
		run_app(app, host, port, c.DEV_MODE)
	except KeyboardInterrupt:
		return 1
	return 0


def run_app(app: Flask, host: str = '127.0.0.1', port: int = 5000, dev_mode: bool = False):
	""" Run the `Flask` app """
	if dev_mode is True:
		app.run(
			host=host,
			port=port,
			debug=dev_mode,
			use_debugger=dev_mode,
			use_reloader=dev_mode)
		return
	serve(app, host=host, port=port)


def init_app(name: str = __name__) -> Flask:
	""" Initialize the `Flask` app """
	return Flask(name)


def send_error_response(title: str, code: int, error_html: str) -> tuple[str, int]:
	""" Send an error response """
	return (
		render_template(
			'error.html',
			page_title=title,
			head_title='Error',
			error_code=code,
			error_html=error_html),
		code)


def register_routes(app: Flask, df: pd.DataFrame):
	""" Register the `Flask` routes """
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
			py_version=f.python_version(),
			dict_table=df.to_dict())

	# === page: data ==================
	@view.route('/data', methods=['GET', 'POST'])
	def page_data():
		toggle_dir_arg = 'vertical'
		table, number_arg = df, ''
		number_count = 0

		if request.method == 'POST':
			toggle_dir_arg = request.form.get('input-table-direction-toggle', '')
			if toggle_dir_arg == '':
				toggle_dir_arg = request.form.get('input-table-direction', 'vertical')
			else:
				toggle_dir_arg = 'horizontal' if toggle_dir_arg == 'vertical' else 'vertical'

			number_arg = request.form.get('number-input', '')
			if not number_arg.isdigit():
				number_arg = ''
			else:
				number_count = df[df.columns].applymap(lambda x: x == int(number_arg)).sum().sum()

				# table = df.copy()
				# for col in table.columns:
				# 	table[col] = table[col].where(table[col] == int(number_arg), '--')
				# if not isinstance(table, pd.DataFrame):
				# 	table = table.to_frame()
				# table.fillna('--', inplace=True)

		return render_template(
			'page-data.html',
			number_count=number_count,
			number_arg=number_arg,
			page_title=title,
			head_title='Data',
			table_direction=toggle_dir_arg,
			dict_table=table.to_dict())

	# === error handler ==================
	@app.errorhandler(HTTPException)
	def error_handler(error):
		return send_error_response(title, error.code, error.name)

	app.register_blueprint(view)
