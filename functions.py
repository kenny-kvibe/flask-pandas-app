import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import psutil
import socket
import sys
import uuid
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from typing import Any, Literal

import constants as c


def sys_print(*args:Any, sep:str = ' ', end:str = '\n'):
	""" Print to `sys.stdout` """
	sys.stdout.write(sep.join(map(str, args)) + end)
	sys.stdout.flush()


def python_version() -> str:
	""" Get the Python version """
	return '.'.join(str(n) for n in sys.version_info[:3])


def print_df_col_value(df:pd.DataFrame, col_idx:int, row_i:int, row_by:Literal['idx', 'num'] = 'idx') -> Any|None:
	""" Print a value from a pandas `DataFrame` column """
	col_value = get_column_value_by(df, str(df.columns[col_idx]), row_i, row_by)
	sys_print(f'{row_by} {row_i} col {col_idx} : {col_value}')


def print_df_table(df:pd.DataFrame, max_rows:int = 6, max_columns:int = 10):
	""" Print a pandas `DataFrame` table """
	pd.set_option('display.max_rows', max_rows)
	pd.set_option('display.max_columns', max_columns)

	table = str(df).split('\n')
	table_head = table[0]
	table_sep = '–'*len(table_head)
	table[0] = f'n {table_head[2:]}'
	table.insert(1, table_sep)

	sys_print(table_sep, *table, table_sep, sep='\n')


def get_column_value_by_row_num(df:pd.DataFrame, column_name:str, row_number:int) -> Any|None:
	value = None
	try:
		value = df.loc[row_number, column_name]
		if pd.isna(value):
			value = df[column_name][row_number]
			if pd.isna(value):
				value = None
	except KeyError:
		value = None
	return value


def get_column_value_by_row_idx(df:pd.DataFrame, column_name:str, row_index:int) -> Any|None:
	value = None
	try:
		value = df.iloc[row_index][column_name]
		if pd.isna(value):
			value = df[column_name].iloc[row_index]
			if pd.isna(value):
				value = None
	except KeyError:
		value = None
	return value


def get_column_value_by(df:pd.DataFrame, column_name:str, row_i:int, row_by:Literal['idx', 'num'] = 'idx') -> Any|None:
	return (get_column_value_by_row_idx(df, column_name, row_i)
			if row_by == 'idx' else
			get_column_value_by_row_num(df, column_name, row_i))


def drop_row_by_row_num(df:pd.DataFrame, row_number:int) -> pd.DataFrame:
	return df.drop(index=row_number)


def drop_row_by_row_idx(df:pd.DataFrame, row_index:int) -> pd.DataFrame:
	return df.drop(df.index[row_index])  #type:ignore


def drop_row_by(df:pd.DataFrame, row_i:int, row_by:Literal['idx', 'num'] = 'idx') -> pd.DataFrame:
	return (drop_row_by_row_idx(df, row_i)
			if row_by == 'idx' else
			drop_row_by_row_num(df, row_i))


def read_df_from_file(
	file_name:str,
	dir_path:str = c.DATAFRAME_DIR_PATH,
	file_type:Literal['csv', 'pkl'] = 'csv',
	**read_kwargs
) -> pd.DataFrame | None:
	""" Read a pandas `DataFrame` from a file. """
	file_path = os.path.join(dir_path, file_name)
	if not os.path.exists(file_path):
		return None
	if file_type == 'csv':
		return pd.read_csv(file_path, **read_kwargs)
	if file_type == 'pkl':
		return pd.read_pickle(file_path, **read_kwargs)
	return None


def save_df_to_file(
	df:pd.DataFrame,
	file_name:str,
	dir_path:str = c.DATAFRAME_DIR_PATH,
	file_type:Literal['csv', 'pkl'] = 'csv',
	**write_kwargs
):
	""" Save a pandas `DataFrame` to a file, overwriting any existing file. """
	file_path = os.path.join(dir_path, file_name)
	if os.path.exists(file_path):
		os.remove(file_path)

	if dir_path not in ('', '.', '..') and not os.path.exists(dir_path):
		os.makedirs(dir_path)

	if file_type == 'csv':
		with open(file_path, 'w') as fp:
			df.to_csv(fp, **write_kwargs)
		del fp
		return

	if file_type == 'pkl':
		with open(file_path, 'wb', ) as fp:
			df.to_pickle(fp, **write_kwargs)
		del fp
		return


def generate_uuid(uuid_version:Literal[1, 3, 4, 5] = 4, uppercase:bool = False) -> str:
	""" Generate a new UUID string. """
	if uuid_version == 1:
		uuid_string = str(uuid.uuid1())
	else:
		uuid4 = uuid.uuid4()
		if uuid_version == 3:
			uuid_string = str(uuid.uuid3(uuid.NAMESPACE_OID, str(uuid4)))
		elif uuid_version == 4:
			uuid_string = str(uuid4)
		elif uuid_version == 5:
			uuid_string = str(uuid.uuid5(uuid.NAMESPACE_OID, str(uuid4)))
		else:
			raise ValueError(f'Invalid UUID version: uuid{uuid_version}')
	if uppercase:
		return uuid_string.upper()
	return uuid_string


def generate_df(
	rows:int = 1,
	cols:int = 1,
	min_value:int | None = None,
	max_value:int | None = None,
	dtype:type = np.uint16,
	uuid_col_names:bool = True
) -> pd.DataFrame:
	""" Generates a pandas `DataFrame` """
	if min_value is None:
		min_value = 0
	else:
		min_value = max(0, min_value)

	dtype_max = np.iinfo(dtype).max
	if max_value is None:
		max_value = dtype_max
	else:
		max_value = max(
			min_value+1,
			min(dtype_max, max_value+1))

	return pd.DataFrame({
		(
			generate_uuid(uppercase=True) if uuid_col_names else f'col{i}'
		):  pd.Series(
				np.random.randint(min_value, max_value, rows, dtype),
			dtype=dtype)
		for i in range(cols)
	})


def create_save_dataframe_plot(
	df:pd.DataFrame,
	window_title:str = 'DataFrame',
	window_width:int = 512,
	window_height:int = 256,
	cell_font_size:float = 10.0,
	cells_border_size:float = 0.5,
	cells_border_color:str = '#000000',
	header_row_fg_color:str = '#000000',
	header_row_bg_color:str = '#FFBB00',
	values_row_fg_color:str = '#EFEFEF',
	values_row_bg_color:str = '#0033FF',
	save_plot_png:bool = True,
	show_plot:bool = False,
):
	""" Create a plot of a pandas `DataFrame`,
	optionally show it or/and save it to a '.png' file. """
	mpl.rcParams['toolbar'] = 'None'

	ax:Axes
	fig:Figure
	fig, ax = plt.subplots()

	fig_mgr = fig.canvas.manager
	if fig_mgr:
		fig_mgr.set_window_title(window_title)

	rows_count = len(df)
	columns_count = len(df.columns)

	cell_height = 1/(rows_count+1)
	cell_width = 1/columns_count

	cell_font_name = 'Consolas' if 'Consolas' in c.TTF_FONTS else 'Monospace'

	ax.axis('off')
	ax.set_position((0, 0, 1, 1))
	ax.set_aspect('auto')

	table = ax.table(
		colLabels   = tuple(df.columns),
		colColours  = tuple([header_row_bg_color]*columns_count),
		cellText    = tuple(tuple(str(col) for col in row) for row in df.values),
		cellColours = tuple([values_row_bg_color]*columns_count for _ in range(rows_count)),
		loc         = 'center')

	table_cells = table.get_celld()

	for cell_key, cell in table_cells.items():
		row, _col = cell_key
		is_first_row = row == 0

		cell.set_width(cell_width)
		cell.set_height(cell_height)
		cell.set_linewidth(cells_border_size)
		cell.set_edgecolor(cells_border_color)

		cell_text = cell.get_text()
		cell_text.set_rotation(0)
		cell_text.set_fontsize(cell_font_size)
		cell_text.set_fontweight('bold' if is_first_row else 'normal')
		cell_text.set_fontstyle('normal')
		cell_text.set_fontfamily(cell_font_name)
		cell_text.set_verticalalignment('center_baseline')
		cell_text.set_horizontalalignment('center' if is_first_row else 'left')
		cell_text.set_color(header_row_fg_color if is_first_row else values_row_fg_color)

	fig.set_size_inches(window_width/fig.dpi, window_height/fig.dpi)

	if save_plot_png:
		plt.savefig(os.path.join(c.DATAFRAME_DIR_PATH, f'{window_title}.png'))
	if show_plot:
		plt.show(block=True)
	plt.close(fig)


def get_local_ipv4() -> str:
	""" Get the first IPv4 address that starts with `192.168.` or get `127.0.0.1` """
	interfaces = psutil.net_if_addrs().values()

	for ifs in interfaces:
		for addr in ifs:
			if addr.family == socket.AF_INET and addr.address.startswith('192.168.'):
				return addr.address

	return '127.0.0.1'