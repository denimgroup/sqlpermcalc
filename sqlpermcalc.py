#!/usr/bin/python

import logging
import sqlparse
from sqlparse.sql import Identifier, IdentifierList
from sqlparse.tokens import Keyword, DML
import sys


sqlparse_version = 0.1
logging.basicConfig(level=logging.DEBUG)


def merge_map(main_map, table_name, column_list):
	"""Merge a new set of columns for a table into an existing set of permissions.

	Keyword arguments:
	main_map -- the map into which the new permissions will be merged
	table_name -- string name for the table permissions apply to
	column_list -- list of strings for the columns

	"""
	logging.debug("Adding table %s with columns %s to map with existing keys %s", \
						table_name, ",".join(column_list), ",".join(main_map.keys()))

	if table_name in main_map:
		logging.debug("Already have a map for table %s. Adding to it", table_name)
		table_map = main_map[table_name]
	else:
		logging.debug("No map for table %s. Creating", table_name)
		table_map = { }
		main_map[table_name] = table_map

	for column in column_list:
		table_map[column] = 1


class PermissionsModel():
	SELECT_MAP = { }
	"""Map containing SELECT permissions

	This map has string keys representing table names that point to maps. The inner maps
	contain string keys representing column names that point to a constant (1) simply
	to indicate the presence of that permission for the column.

	"""
	INSERT_MAP = { }
	"""Map containing INSERT permissions

	This map has string keys representing table names that point to maps. The inner maps
	contain string keys representing column names that point to a constant (1) simply
	to indicate the presence of that permission for the column.

	"""
	DELETE_MAP = { }
	"""Map containing DELETE permissions

	This map has string keys representing table names that point to a constant (1) simply
	to indicate the presence of that permission for the table.

	"""
	UPDATE_MAP = { }
	"""Map containing SELECT permissions

	This map has string keys representing table names that point to maps. The inner maps
	contain string keys representing column names that point to a constant (1) simply
	to indicate the presence of that permission for the column.

	"""


	# TOFIX - This method signature will need to be updated as the SELECT handling is
	# made more sophisticated because a single SELECT statement could indicate the need
	# for SELECT permissions to a number of tables and columns within those tables
	def merge_select(self, table_name, column_list):
		"""Merge new SELECT permissions.

		Keyword arguments:
		table_name -- string name for the table that will get additional permissions
		column_list -- list of string names for the columns the permisisons apply to

		"""
		merge_map(self.SELECT_MAP, table_name, column_list)

	def merge_update(self, table_name, column_list):
		"""Merge new UPDATE permissions.

		Keyword arguments:
		table_name -- string name for the table that will get additional permissions
		column_list -- list of string names for the columns the permisisons apply to

		"""
		merge_map(self.UPDATE_MAP, table_name, column_list)


	def merge_insert(self, table_name, column_list):
		"""Merge new INSERT permissions.

		Keyword arguments:
		table_name -- string name for the table that will get additional permissions
		column_list -- list of string names for the columns the permisisons apply to

		"""
		merge_map(self.INSERT_MAP, table_name, column_list)
		

	def merge_delete(self, table_name):
		"""Merge new DELETE permissions.

		Keyword arguments:
		table_name -- string name for the table that will get additional permissions

		"""
		self.DELETE_MAP[table_name] = 1

	def print_stuff(self):
		"""Print a list of all the permissions in the PermissionModel in a human-readable format."""
		logging.debug('Database permission model')
		logging.debug("DELETE: %s", ",".join(self.DELETE_MAP.keys()))
		for table_name in self.INSERT_MAP.keys():
			column_map = self.INSERT_MAP[table_name]
			logging.debug("INSERT: Table: %s, Columns: %s", table_name, ",".join(column_map.keys()))
		for table_name in self.UPDATE_MAP.keys():
			column_map = self.UPDATE_MAP[table_name]
			logging.debug("UPDATE: Table: %s, Columns: %s", table_name, ",".join(column_map.keys()))
		for table_name in self.SELECT_MAP.keys():
			column_map = self.SELECT_MAP[table_name]
			logging.debug("SELECT: Table: %s, Columns: %s", table_name, ",".join(column_map.keys()))

	def __init__(self):
		self.data = []


def analyze_parsed_sql(sql_line):
	logging.debug(">>>> SQL fragment |%s|", sql_line)
	logging.debug(">>>> Token count: %d", len(sql_line.tokens))
	i = 0
	for token in sql_line.tokens:
		logging.debug(">>>> Token[%d]: |%s| is of type |%s|", i, token, type(token))
		i = i + 1

def extract_all_identifiers(identifier_stuff):
	logging.debug("Extracting identifiers from %s", identifier_stuff)
	result = []
	# When checking for Identifiers you also have to check for Keywords because of a bug
	# in the parsing library that treats Identifiers with names that match Keywords as
	# Keywords
	if isinstance(identifier_stuff, list):
		logging.debug("Found a list: %s", identifier_stuff)
		for item in identifier_stuff:
			logging.debug("Extracting identifiers for list item %s", item)
			result.extend(extract_all_identifiers(item))
	elif isinstance(identifier_stuff, IdentifierList):
		logging.debug("Found an IdentifierList: %s. Going to break into a list and process", \
						identifier_stuff)
		result.extend(extract_all_identifiers(identifier_stuff.get_identifiers()))
	elif isinstance(identifier_stuff, Identifier) or identifier_stuff.ttype is Keyword:
		logging.debug("Found an Identifier: %s. Adding to result list: |%s|", \
							identifier_stuff, identifier_stuff)
		result.append(str(identifier_stuff))
	else:
		logging.debug("Ignoring item %s of type %s", identifier_stuff, type(identifier_stuff))

	return result


def find_the_identifiers_in_list(sql_part):
	result = []
	for identifier in sql_part.get_identifiers():
		if isinstance(identifier, Identifier):
			result.append(str(identifier))
	return result


def find_the_identifiers(sql_part):
	# logging.debug("sql_part is of type %s", type(sql_part))
	result = []
	for token in sql_part:
		# logging.debug("Token |%s| is of type |%s|", token, type(token))
		if isinstance(token, Identifier):
			# logging.debug("Found an Identifier: |%s|", token)
			result.append(str(token))
		elif isinstance(token, IdentifierList):
			# logging.debug("Found an IdentifierList: |%s|", token)
			result.extend(find_the_identifiers_in_list(token))
	return result


def parse_column_names_update(sql_part):
	# logging.debug("Parsing column names from |%s|", sql_part)
	# analyze_parsed_sql(sql_part)
	result = find_the_identifiers(sql_part)
	return result


def handle_update(sql_line, model):
	logging.debug("Parse UPDATE for |%s|", sql_line)
	table_name = str(sql_line.tokens[2])
	column_names = parse_column_names_update(sql_line.tokens[3:])
	logging.info("UPDATE permission required for table |%s|", table_name)
	logging.info("UPDATE permissions required for columns |%s|", ",".join(column_names))

	model.merge_update(table_name, column_names)


def handle_delete(sql_line, model):
	logging.debug("Parse DELETE for |%s|", sql_line)
	table_name = str(sql_line.tokens[4])
	logging.info("DELETE permission required for table |%s|", table_name)

	model.merge_delete(table_name)


def handle_select(sql_line, model):
	# TOFIX - This only handles VERY basic SELECT queries and needs to be updated
	# to deal with nested queries and joins
	logging.debug("Parse SELECT for |%s|", sql_line)
	analyze_parsed_sql(sql_line)

	# Find the 'FROM' or skip the line
	from_index = 0
	from_found = False
	for item in sql_line.tokens:
		if item.ttype is Keyword and item.value.upper() == 'FROM':
			from_found = True
			break;
		from_index = from_index + 1
	if not from_found:
		logging.info("Bad SELECT statement. No FROM found in %s", sql_line)
		# TODO - Better error handling
		return

	column_tokens = sql_line.tokens[2:from_index-1]
	column_names = extract_all_identifiers(column_tokens)
	logging.debug("column_names looks to be: %s", column_names)
	table_name = str(sql_line.tokens[from_index+2])
	logging.info("SELECT permission required for table |%s|", table_name)
	logging.info("SELECT permissions required for columns |%s|", ",".join(column_names))
	
	model.merge_select(table_name, column_names)

def parse_column_names_insert(sql_part):
	# logging.debug("Parsing column names from |%s|", sql_part)
	# analyze_parsed_sql(sql_part)
	result = []
	for token in sql_part.tokens:
		# logging.debug("Token |%s| is of type |%s|", token, type(token))
		if isinstance(token, Identifier):
			# logging.debug("Found an Identifier: |%s|", token)
			result.append(str(token))
	return result


def handle_insert(sql_line, model):
	logging.debug("Parse INSERT for |%s|", sql_line)
	insert_target = sql_line.tokens[4]
	table_name = str(insert_target.tokens[0])
	column_names = parse_column_names_insert(insert_target.tokens[2])
	logging.info("INSERT permission required for table |%s|", table_name)
	logging.info("INSERT permissions required for columns |%s|", ",".join(column_names))

	model.merge_insert(table_name, column_names)


def handle_line(line, model):
	"""Take a SQL statement in a string and add the appropriate permissions to the model.

	Keyword arguments:
	line -- string containing a single SQL statement
	model -- PermissionsModel containing the current set of permissions

	"""
	logging.debug("Going to handle line |%s|", line)

	sql_line = sqlparse.parse(line)[0]
	stmt_type = sql_line.get_type()
	logging.debug("Statement type is |%s|", stmt_type)

	# analyze_parsed_sql(sql_line)

	if stmt_type == 'INSERT':
		handle_insert(sql_line, model)
	elif stmt_type == 'SELECT':
		handle_select(sql_line, model)
	elif stmt_type == 'DELETE':
		handle_delete(sql_line, model)
	elif stmt_type == 'UPDATE':
		handle_update(sql_line, model)

def main():
	logging.info('Starting sqlparse version %s', sqlparse_version)

	# Open input file and setup permission model

	# TOFIX - Create permission model objects
	# TODO - Add exception/error handling

	if len(sys.argv) < 2:
		logging.error('No SQL file specified.')
		logging.error('usage: ./sqlpermcalc.py <sql_filename>')
		sys.exit(-1)

	sql_filename = sys.argv[1]
	logging.debug('SQL filename is %s', sql_filename)
	sql_file = open(sql_filename, 'r')

	# For each statement in file add to permission model

	the_model = PermissionsModel()

	for line in sql_file:
		line = line.rstrip()
		handle_line(line, the_model)

	# Print out permission model

	the_model.print_stuff()

	# TODO - Print out permission model

	logging.info('sqlparse finished')


if __name__ == '__main__':
	main()

