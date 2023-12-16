# Docs:  https://pandas.pydata.org/docs/
import pandas as pd

import functions as f



def main(cols_count:int = 1, rows_count:int = 1, value_low:int = 0, value_high:int = 1) -> pd.DataFrame:
	return pd.DataFrame({
		f'rand_col_{i}': pd.Series(f.get_random_ints_array(value_low, value_high, rows_count))
		for i in range(cols_count)
	})


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

	f.create_save_dataframe_plot(df)


if __name__ == '__main__':
	test(main(3, 5, 100, 999))
	raise SystemExit(0)
