from typing import Dict, List, Tuple, Union

import javalang
from javalang.ast import Node
from javalang.tree import MemberReference, VariableDeclaration


class JavaAnalyzationError(Exception):
	pass


def _ast_nodes_equal(node1: Node, node2: Node, recursive: bool, matches: List[Tuple[any, any]], _first_level=True) -> bool:
	# Non-recursive comparison; we're done now that the first node has been processed
	if not recursive and not _first_level:
		return True

	if type(node1) is not type(node2):
		# print('XA', type(node1), type(node2), '\n')
		return False

	if type(node1) is list:
		if len(node1) != len(node2):
			# print('XB', '\n'.join([str(type(n)) for n in node1]), '\n' + '\n'.join([str(type(n)) for n in node2]), '\n')
			return False

		for i in range(len(node1)):
			if not _ast_nodes_equal(node1[i], node2[i], recursive, matches, False):
				# print('XC', type(node1[i]), type(node2[i]), '\n')
				return False

		return True

	elif isinstance(node1, Node):
		ignored_attrs = [attrs for a, b, attrs in matches if node1 in (a, b) or node2 in (a, b)]
		for attr in node1.attrs:
			if attr in ignored_attrs:
				continue

			attr1 = getattr(node1, attr)
			attr2 = getattr(node2, attr)

			if not _ast_nodes_equal(attr1, attr2, recursive, matches, False):
					# print('XC', type(attr1), type(attr2), '\n')
					return False

		return True

	else:
		# if node1 != node2:
			# print('XD', node1, node2, '\n')
		return node1 == node2


def ast_nodes_equal(node1: Node, node2: Node, recursive=True, matches: List[Tuple[any, any]] = tuple()) -> bool:
	return _ast_nodes_equal(node1, node2, recursive, matches)


def ast_paths_equal(path1: List[Union[Node, List[Node]]], path2: List[Union[Node, List[Node]]], matches: List[Tuple[any, any]] = tuple()) -> bool:
	"""
	Determine if two AST node paths are equal, ignoring other parts of the file

	Args:
		path1 (List[Union[Node, List[Node]]]): [description]
		path2 (List[Union[Node, List[Node]]]): [description]
		matches (List[Tuple[any, any]], optional): List of node pairs to consider equal. Defaults to tuple().

	Returns:
		bool: [description]
	"""

	if len(path1) != len(path2):
		return False

	for i in range(len(path1)):  # Skip list entries in the path (because they contain irrelevant parts)
		if not ast_nodes_equal(path1[i], path2[i], recursive=False, matches=matches):
			return False

	return True


def _filter_ast_node(node: Node, t: type, _path=[]) -> List[Union[Node, str]]:
	if node is None:
		return

	elif type(node) is list:
		for item in node:
			for path, child in _filter_ast_node(item, t, _path=_path):
				yield path, child

	elif isinstance(node, Node):
		if isinstance(node, t):
			yield _path, node

		for attr in node.attrs:
			for path, child in _filter_ast_node(getattr(node, attr), t, _path=_path + [node, attr]):
				yield path, child


def filter_ast_node(node: Node, t: type) -> List[Union[Node, str]]:
	return _filter_ast_node(node, t)


def get_renamed_variables(source_code: str, target_code: str) -> Dict[str, str]:
	try:
		source_tree = javalang.parse.parse(source_code)
		target_tree = javalang.parse.parse(target_code)
	except javalang.parser.JavaSyntaxError as e:
		return None

	source_declarations = list(filter_ast_node(source_tree, VariableDeclaration))
	target_declarations = list(filter_ast_node(target_tree, VariableDeclaration))

	source_var_names = [declarator.name for path, declaration in source_declarations for declarator in declaration.declarators]
	target_var_names = [declarator.name for path, declaration in target_declarations for declarator in declaration.declarators]

	source_references = list(filter_ast_node(source_tree, MemberReference))
	target_references = list(filter_ast_node(target_tree, MemberReference))

	renamed_var_names = []
	matches = []

	# Find all the semantically equalivalent variables that have different
	# names. For the variable declarations a and b to be semantically
	# equalivalent:
	#
	# - They must have be in the same semantic section of the file
	# - They must have the same references and assignments

	for source_dec_path, source_dec_node in source_declarations:
		for target_dec_path, target_dec_node in target_declarations:
			# 1. Make sure paths would be equal if source_node (a) and
			#	 target_node (b) were the same.

			# 1a. Must be in the same part of the file
			# First get all previously discovered renamed variables
			prev_matches_here = [(old, new, attrs) for path, v in matches for old, new, attrs in v if path == target_dec_path]
			# Now make sure the paths are equal (ignoring the previously found
			# renamed variables and the declarations themselves)
			if not ast_paths_equal(source_dec_path, target_dec_path, matches=prev_matches_here + [(source_dec_node, target_dec_node, ['type', 'declarators'])]):
				continue

			for source_declarator in source_dec_node.declarators:
				# 1b. (Must have different names)
				if source_declarator.name in target_var_names:
					continue

				for target_declarator in target_dec_node.declarators:
					# 1c. All attributes except the name should be equal
					declarator_match = (source_declarator, target_declarator, 'name')
					if not ast_nodes_equal(source_declarator, target_declarator, recursive=True, matches=prev_matches_here + [declarator_match]):
						continue

					# 1c. Must have the same references
					sr = [(path, ref) for path, ref in source_references if ref.member == source_declarator.name]
					tr = [(path, ref) for path, ref in target_references if ref.member == target_declarator.name]
					if len(sr) != len(tr):
						continue

					refs_match = True
					for i in range(len(sr)):
						source_ref_path, source_ref_node = sr[i]
						target_ref_path, target_ref_node = tr[i]
						ref_match = (source_ref_node, target_ref_node, 'name')
						if not ast_paths_equal(source_ref_path, target_ref_path, matches=prev_matches_here + [ref_match]):
							refs_match = False
							break

						for path, mappings in matches:
							if path == target_ref_path:
								for old, new in mappings:
									break

								mappings.append(ref_match)

						else:
							matches.append((target_ref_path, [ref_match]))

					if not refs_match:
						continue

					print(source_declarator.name, target_declarator.name)
					# 1d. (The function cannot return multiple mappings
					#     containing the same variable at the same path)
					other_renames_at_path = False
					never_used = True
					for path, mappings in renamed_var_names:
						if path != target_dec_path:
							continue

						for old, new in mappings:
							if old == source_declarator.name or new == target_declarator.name:
								never_used = False
								break

						if not never_used:
							break

						mappings.append((source_declarator.name, target_declarator.name))
						other_renames_at_path = True
						break

					if not never_used:
						continue

					if not other_renames_at_path:
						mappings = [(source_declarator.name, target_declarator.name)]
						renamed_var_names.append((target_dec_path, mappings))

					for path, v in matches:
						if path == target_dec_path:
							for old, new, _ in v:
								if old == source_declarator:
									raise JavaAnalyzationError(f'duplicate declarator in source: {old}')

								if new == target_declarator:
									raise JavaAnalyzationError(f'duplicate declarator in target: {new}')

							v.append(declarator_match)

					else:
						matches.append((target_dec_path, [declarator_match]))

	return renamed_var_names
