import numpy as np
import pandas as pd
import sys
from typing import Any, Literal


def sys_print(*args:Any, sep:str = '\n'):
	sys.stdout.write(sep.join(map(str, args)) + '\n')
	sys.stdout.flush()


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


def drop_row_by_row_integer(df:pd.DataFrame, row_integer:int) -> pd.DataFrame:
	return df.drop(index=row_integer)  #type:ignore


def drop_row_by_row_index(df:pd.DataFrame, row_index:int) -> pd.DataFrame:
	return df.drop(df.index[row_index])  #type:ignore


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
