import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import sys
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from typing import Any, Literal

import constants as c


def sys_print(*args:Any, sep:str = '\n'):
	sys.stdout.write(sep.join(map(str, args)) + '\n')
	sys.stdout.flush()


def print_get_col_value(df:pd.DataFrame, col_idx:int, row_i:int, row_by:Literal['idx', 'int'] = 'idx') -> Any|None:
	column_name = str(df.columns[col_idx])
	sys_print('{} {} col {} : {}'.format(
		row_by,
		row_i,
		col_idx,
		(get_column_value_by_row_idx(df, column_name, row_i)
		 if row_by == 'idx' else
		 get_column_value_by_row_int(df, column_name, row_i))
	))


def print_df_table(df:pd.DataFrame):
	table = str(df).split('\n')
	table_head = table[0]
	table_sep = '–'*len(table_head)
	table[0] = f'n {table_head[2:]}'
	table.insert(1, table_sep)
	sys_print(table_sep, *table, table_sep)


def get_random_ints_array(
	low:int,
	high:int,
	rows_count:int = 1
) -> np.ndarray[str, np.dtype[np.uint64]]:
	return np.random.default_rng().integers(
		low, high,
		size=[max(1, rows_count)],
		dtype=np.uint64)


def get_column_matching_values(df:pd.DataFrame, column_name:str, column_value:Any) -> pd.Series:
	return df[df[column_name] == column_value]


def get_column_values(df:pd.DataFrame, column_name:str) -> pd.Series:
	return df[column_name].values


def get_column_value_by_row_int(df:pd.DataFrame, column_name:str, row_integer:int) -> Any|None:
	value = None
	try:
		value = df.loc[row_integer, column_name]
		if pd.isna(value):
			value = df[column_name][row_integer]
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


def drop_row_by_row_int(df:pd.DataFrame, row_integer:int) -> pd.DataFrame:
	return df.drop(index=row_integer)  #type:ignore


def drop_row_by_row_idx(df:pd.DataFrame, row_index:int) -> pd.DataFrame:
	return df.drop(df.index[row_index])  #type:ignore


def drop_row_by(df:pd.DataFrame, row_i:int, row_by:Literal['idx', 'int'] = 'idx') -> pd.DataFrame:
	if row_by == 'int':
		return drop_row_by_row_int(df, row_i)
	return drop_row_by_row_idx(df, row_i)


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
	show_plot:bool = False,
	save_plot_png:bool = True,
):
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

	values_row_bg_colors = [[values_row_bg_color]*columns_count for _ in range(rows_count)]
	header_row_bg_colors = [header_row_bg_color]*columns_count

	cell_font_name = 'Consolas' if 'Consolas' in c.TTF_FONTS else 'Monospace'

	ax.axis('off')
	ax.set_position((0, 0, 1, 1))
	ax.set_aspect('auto')

	table_plt = ax.table(
		colLabels=tuple(df.columns),
		colColours=header_row_bg_colors,
		cellText=tuple(tuple(str(col) for col in row) for row in df.values),
		cellColours=values_row_bg_colors,
		loc='center',
	)

	# table_plt.scale(1, 1)
	table_cells = table_plt.get_celld()

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
		plt.savefig(os.path.join(c.ROOT_PATH, f'{window_title}.png'))
	if show_plot:
		plt.show()
	plt.close(fig)