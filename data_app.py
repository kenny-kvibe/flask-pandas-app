import numpy as np
import pandas as pd

import functions as f


FILE_NAME_CSV = 'df-data.csv'
FILE_NAME_PKL = 'df-data.pkl'


def get_df(
	cols_count:int = 1,
	rows_count:int = 1,
	min_value:int = 0,
	max_value:int = 1,
	df_dtype:type = np.uint16,
	force_df_generate:bool = False,
	uuid_df_cols:bool = True
) -> pd.DataFrame:
	""" [Pandas Docs](https://pandas.pydata.org/docs/)
	"""
	if not force_df_generate:
		df = f.read_df_from_file(FILE_NAME_PKL, file_type='pkl')
		if isinstance(df, pd.DataFrame):
			return df

		df = f.read_df_from_file(FILE_NAME_CSV, file_type='csv')
		if isinstance(df, pd.DataFrame):
			return df

	df = f.generate_df(cols_count, rows_count, min_value, max_value, df_dtype, uuid_df_cols)
	f.save_df_to_file(df, FILE_NAME_CSV, file_type='csv')
	f.save_df_to_file(df, FILE_NAME_PKL, file_type='pkl')
	return df


def main() -> int:
	df = get_df(5, 7, 0, 9, force_df_generate=True, uuid_df_cols=False)

	# f.sys_print('-----\nDataFrame\n'             + str(df))
	# f.sys_print('-----\nDataFrame Values\n'      + str(df.values))
	# f.sys_print('-----\nDataFrame Head Dict\n'   + str(df.head(2).to_dict()))
	# f.sys_print('-----\nDataFrame Values Mean\n' + str(df.values.mean()))

	df_dtype: np.dtype = df.iloc[0, 0].dtype
	df_filtered_result = df.where(df%2 == 0, df_dtype.type(0))
	df_filtered_result = df[df%2 == 0].fillna(df_dtype.type(0))
	df_first_col_rows3 = df_filtered_result.iloc[:, 0].head(3)
	f.sys_print(df_first_col_rows3)

	f.print_df_table(df)
	f.print_df_col_value(df, 0, 0, 'idx')
	f.print_df_col_value(df, 0, 0, 'num')
	f.print_df_col_value(df, 0, 1, 'idx')
	f.print_df_col_value(df, 0, 1, 'num')

	df = f.drop_row_by(df, 0, 'num')
	df = f.drop_row_by(df, 0, 'idx')

	f.print_df_table(df)
	f.print_df_col_value(df, 0, 0, 'idx')
	f.print_df_col_value(df, 0, 0, 'num')
	f.print_df_col_value(df, 0, 2, 'idx')
	f.print_df_col_value(df, 0, 2, 'num')

	i = df.index[0]
	f.sys_print(f'== row idx {i}: {df.iloc[i].values}')
	f.sys_print(f'== row num {i}: {df.loc[i].values}')

	c = df.columns[0]
	f.sys_print(f'== col {c}: {df[c].values}')

	f.create_save_dataframe_plot(
		df,
		cell_font_size=20,
		window_width=1920,
		show_plot=True,
		save_plot_png=False)

	return 0


if __name__ == '__main__':
	raise SystemExit(main())
