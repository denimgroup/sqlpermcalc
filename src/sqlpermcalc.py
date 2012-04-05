#!/usr/bin/python

import logging
import sqlparse
from sqlparse.sql import Identifier, IdentifierList, Parenthesis, Token, TokenList, Where
from sqlparse.tokens import Keyword, DML, Name, Wildcard
import sys
import traceback


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

	if len(column_list) == 0:
		logging.error("Trying to merge permissions for table %s with no permissions. Going to raise Exception", table_name)
		raise Exception("Trying to merge permissions for table %s with no permissions" % table_name)

	if table_name in main_map:
		logging.debug("Already have a map for table %s. Adding to it", table_name)
		table_map = main_map[table_name]
	else:
		logging.debug("No map for table %s. Creating", table_name)
		table_map = { }
		main_map[table_name] = table_map

	for column in column_list:
		table_map[column] = 1


def print_helper(table_map, permission_name):
	if len(table_map) > 0:
		# There are table permissions to display
		tables = sorted(table_map.keys())
		for table_name in tables:
			column_map = table_map[table_name];
			if '*' in column_map:
				column_list = ('*')
			else:
				column_list = sorted(column_map.keys())
			logging.debug("%s: Table: %s, Columns: %s", permission_name, table_name, ",".join(column_list))


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
		if len(self.DELETE_MAP.keys()) > 0:
			logging.debug("DELETE: %s", ",".join(sorted(self.DELETE_MAP.keys())))

		print_helper(self.INSERT_MAP, "INSERT")
		print_helper(self.UPDATE_MAP, "UPDATE")
		print_helper(self.SELECT_MAP, "SELECT")



	def __init__(self):
		self.data = []


def analyze_parsed_sql(sql_line):
	logging.debug(">>>> SQL fragment |%s| is of type |%s| and ttype |%s|", sql_line, type(sql_line), sql_line.ttype)
	logging.debug(">>>> Token count: %d", len(sql_line.tokens))
	i = 0
	for token in sql_line.tokens:
		logging.debug(">>>> Token[%d]: |%s| is of type |%s| and ttype |%s|", i, token, type(token), token.ttype)
		i = i + 1

def extract_all_identifiers(identifier_stuff):
	logging.debug("Extracting identifiers from %s", identifier_stuff)
	result = []
	# When checking for Identifiers you also have to check for Keywords and Builtins because of a bug
	# in the parsing library that treats Identifiers with names that match Keywords as
	# Keywords (ditto Builtins)
	if isinstance(identifier_stuff, list):
		logging.debug("Found a list: %s", identifier_stuff)
		for item in identifier_stuff:
			logging.debug("Extracting identifiers for list item %s", item)
			result.extend(extract_all_identifiers(item))
	elif identifier_stuff.ttype is Wildcard:
		logging.debug("Found a Wildcard: %s. Adding to result list: |%s|", \
							identifier_stuff, identifier_stuff)
		result.append('*')
	elif isinstance(identifier_stuff, Identifier) or identifier_stuff.ttype is Keyword or identifier_stuff.ttype is Name.Builtin:
		logging.debug("Found an Identifier: %s. Adding to result list: |%s|", \
							identifier_stuff, identifier_stuff)
		result.append(str(identifier_stuff))
	# elif isinstance(identifier_stuff, IdentifierList):
	elif isinstance(identifier_stuff, TokenList):
		logging.debug("Found a TokenList: %s. Going to break into a list and process", \
						identifier_stuff)
		result.extend(extract_all_identifiers(identifier_stuff.tokens))
	else:
		logging.debug("Ignoring item %s of type %s and ttype %s",
						identifier_stuff, type(identifier_stuff), identifier_stuff.ttype)

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



def remove_string_from_list_ignore_case(the_list, string_to_remove):
	index = 0
	for list_item in the_list:
		if list_item.lower() == string_to_remove.lower():
			del the_list[index]
			# Decrement because we're going to increment in just a second and we need to stay in the same place
			index = index - 1
		index = index + 1
			


def parse_column_names_where(where_clause):
	"""Retrieve column names used in a WHERE clause

	Keyword arguments:
	where_clause --- Instance of sqlparse.sql.Where we will extract column names from

	Keyword return:
	List of strings containing column names found in the WHERE clause

	"""
	logging.debug("Parsing column names from WHERE clause |%s|", where_clause)
	analyze_parsed_sql(where_clause)
	# Strip off the first token because it is a WHERE token which is a keyword that would be flagged by
	# extract_all_identifiers
	tokens = where_clause.tokens
	tokens = tokens[1:]
	column_names = extract_all_identifiers(tokens)
	logging.debug("Column names found in WHERE clause |%s| were |%s|", where_clause, ",".join(column_names))
	# Need to clean out ANDs and ORs
	remove_string_from_list_ignore_case(column_names, "AND")
	remove_string_from_list_ignore_case(column_names, "OR")
	return column_names


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
		logging.error("Bad SELECT statement. No FROM found in %s", sql_line)
		raise Exception("Bad SELECT statement. No FROM found in %s" % sql_line)

	column_tokens = sql_line.tokens[2:from_index-1]
	column_names = extract_all_identifiers(column_tokens)
	logging.debug("column_names looks to be: %s", column_names)
	table_name = str(sql_line.tokens[from_index+2])
	logging.info("SELECT permission required for table |%s|", table_name)
	logging.info("SELECT permissions required for columns |%s|", ",".join(column_names))

	# Also need to check the WHERE clause for additional SELECT column privs
	tokens_after_from = sql_line.tokens[from_index:]
	for token in tokens_after_from:
		if isinstance(token, Where):
			# Found our WHERE - pull the columns required
			where_column_names = parse_column_names_where(token)
			model.merge_select(table_name, where_column_names)
	
	model.merge_select(table_name, column_names)

def parse_column_names_insert(sql_part):
	logging.debug("Parsing column names from |%s|", sql_part)
	result = extract_all_identifiers(sql_part)
	return result


def handle_insert(sql_line, model):
	logging.debug("Parse INSERT for |%s|", sql_line)
	analyze_parsed_sql(sql_line)

	insert_target = sql_line.tokens[4]

	logging.debug("insert_target is |%s|", insert_target)
	analyze_parsed_sql(insert_target)

	if isinstance(insert_target, Identifier):
		table_name = str(insert_target)
		column_names = ('*')
	else:
		table_name = str(insert_target.tokens[0])
		# This is a bit of a hack, but deals with situations where there is no space in the query - ie:
		# INSERT INTO MyTable(column1,column2,column3)VALUES(1,2,3)
		if isinstance(insert_target.tokens[1], Parenthesis):
			check_index = 1
		else:
			check_index = 2
		column_names = parse_column_names_insert(insert_target.tokens[check_index])

	logging.info("INSERT permission required for table |%s|", table_name)
	logging.info("INSERT permissions required for columns |%s|", ",".join(column_names))

	model.merge_insert(table_name, column_names)


def handle_line(line, model):
	"""Take a SQL statement in a string and add the appropriate permissions to the model.

	Keyword arguments:
	line -- string containing a single SQL statement
	model -- PermissionsModel containing the current set of permissions
	
	Keyword return:
	True if the line was processed correctly, False if an error occurred

	"""
	logging.debug("Going to handle line |%s|", line)
	error_detected = False

	try:
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
	except Exception as inst:
		error_detected = True
		logging.error("Error parsing line |%s|", line)
		logging.error("Error type is |%s|", type(inst))
		logging.error("Error args are |%s|", inst.args)
		logging.error("Error string representation: |%s|", str(inst))
		traceback.print_exc()

	return (not error_detected)

def main():
	logging.info('Starting sqlparse version %s', sqlparse_version)

	# Open input file and setup permission model

	if len(sys.argv) < 2:
		logging.error('No SQL file specified.')
		logging.error('usage: ./sqlpermcalc.py <sql_filename>')
		sys.exit(-1)

	sql_filename = sys.argv[1]
	logging.debug('SQL filename is %s', sql_filename)
	sql_file = open(sql_filename, 'r')

	# For each statement in file add to permission model

	the_model = PermissionsModel()

	lines_attempted = 0
	errors = 0

	for line in sql_file:
		line = line.rstrip()
		lines_attempted = lines_attempted + 1
		status = handle_line(line, the_model)
		if not status:
			errors = errors + 1

	logging.info("%d errors from %d lines processed", errors, lines_attempted)

	# Print out permission model

	the_model.print_stuff()

	# TODO - Print out permission model

	logging.info('sqlparse finished')


if __name__ == '__main__':
	main()

