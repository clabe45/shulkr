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

	for a, b in matches:
		if (node1 == a and node2 == b) or (node1 == b and node2 == a):
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
		for attr in node1.attrs:
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

	renamed_variables = []
	matches = []

	# Find all the semantically equalivalent variables that have different
	# names. For the variable declarations a and b to be semantically
	# equalivalent:
	#
	# - They must have be in the same semantic section of the file
	# - They must have the same references and assignments

	for source_path, source_node in source_declarations:
		for target_path, target_node in target_declarations:
			# print('A')
			# 1. Make sure paths would be equal if source_node (a) and
			#	target_node (b) were the same.

			# 1a. Must be in same part of the file
			prev_matches_here = [(old, new) for path, v in matches for old, new in v if path == target_path]
			if not ast_paths_equal(source_path, target_path, matches=prev_matches_here + [(source_node, target_node)]):
				continue

			for source_declarator in source_node.declarators:
				# 1b. (Must have different names)
				if source_declarator.name in target_var_names:
					continue

				for target_declarator in target_node.declarators:
					# print('C', source_declarator.name, target_declarator.name, prev_matches_here)

					# 1c. Must have same initializer
					if not ast_nodes_equal(source_declarator.initializer, target_declarator.initializer, recursive=True, matches=prev_matches_here + [(source_node, target_node)]):
						continue

					# 1c. Must have the same references
					sr = [(path, ref) for path, ref in source_references if ref.member == source_declarator.name]
					tr = [(path, ref) for path, ref in target_references if ref.member == target_declarator.name]
					# print('D', source_declarator.name, len(sr), target_declarator.name, len(tr))
					if len(sr) != len(tr):
						continue

					refs_match = True
					for i in range(len(sr)):
						source_ref_path, source_ref_node = sr[i]
						target_ref_path, target_ref_node = tr[i]
						if not ast_paths_equal(source_ref_path, target_ref_path, matches=prev_matches_here + [(source_node, target_node), (source_ref_node, target_ref_node)]):
							refs_match = False
							break

						for path, v_node in matches:
							if path == target_ref_path:
								for old, new in v_node:
									break

								v_node.append((source_ref_node, target_ref_node))

						else:
							v_node = [(source_ref_node, target_ref_node)]
							matches.append((target_ref_path, v_node))

					if not refs_match:
						continue

					print(source_declarator.name, target_declarator.name)
					# print('E', source_declarator.name, target_declarator.name)
					for path, v_name in renamed_variables:
						if path != target_path:
							continue

						for old, new in v_name:
							if old == source_declarator.name:
								raise JavaAnalyzationError(f'duplicate declarator name in source: {old}')

							if new == target_declarator.name:
								raise JavaAnalyzationError(f'duplicate declarator name in target: {new}')

						v_name.append((source_declarator.name, target_declarator.name))
						break

					else:
						v_name = [(source_declarator.name, target_declarator.name)]
						renamed_variables.append((target_path, v_name))

					for path, v_node in matches:
						if path == target_path:
							for old, new in v_node:
								if old == source_declarator:
									raise JavaAnalyzationError(f'duplicate declarator in source: {old}')

								if new == target_declarator:
									raise JavaAnalyzationError(f'duplicate declarator in target: {new}')

							v_node.append((source_declarator, target_declarator))

					else:
						v_node = [(source_declarator, target_declarator)]
						matches.append((target_path, v_node))

	return renamed_variables
