# Docs:  https://pandas.pydata.org/docs/
import matplotlib as mpl
import matplotlib.pyplot as plt
import os
import pandas as pd
from matplotlib.axes import Axes
from matplotlib.figure import Figure

import constants as c
import functions as f



def main(cols_count:int = 1, rows_count:int = 1, value_low:int = 0, value_high:int = 1) -> pd.DataFrame:
	return pd.DataFrame({
		f'rand_col_{i}': pd.Series(f.get_random_ints_array(value_low, value_high, rows_count))
		for i in range(cols_count)
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


def test(df:pd.DataFrame):
	f.print_df_table(df)
	f.print_get_col_value(df, 0, 0, 'int')
	f.print_get_col_value(df, 0, 0, 'idx')
	f.print_get_col_value(df, 0, 1, 'int')
	f.print_get_col_value(df, 0, 1, 'idx')

	df = f.drop_row_by_row_integer(df, 0)
	df = f.drop_row_by_row_index(df, 0)

	f.print_df_table(df)
	f.print_get_col_value(df, 0, 0, 'int')
	f.print_get_col_value(df, 0, 0, 'idx')
	f.print_get_col_value(df, 0, 2, 'int')
	f.print_get_col_value(df, 0, 2, 'idx')

	create_save_dataframe_plot(df)


if __name__ == '__main__':
	test(main(3, 5, 100, 999))
	raise SystemExit(0)
