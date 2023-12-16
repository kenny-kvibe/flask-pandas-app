# Docs:  https://pandas.pydata.org/docs/
import pandas as pd

import functions as f


def main(cols_count:int = 1, rows_count:int = 1, value_low:int = 0, value_high:int = 1) -> pd.DataFrame:
	return pd.DataFrame({
		f'rand-{i}': pd.Series(f.get_random_ints_array(value_low, value_high, rows_count))
		for i in range(cols_count)
	})


def test(df:pd.DataFrame):
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

	f.create_save_dataframe_plot(df, show_plot=True, save_plot_png=False)


if __name__ == '__main__':
	test(main(4, 7, 100, 999))
	raise SystemExit(0)
