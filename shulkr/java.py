from typing import Dict, List, Tuple, Union

import javalang
from javalang.ast import Node
from javalang.tokenizer import Identifier, tokenize
from javalang.tree import MemberReference, VariableDeclaration


class JavaAnalyzationError(Exception):
	pass


def _ast_nodes_equal(
	node1: Node,
	node2: Node,
	recursive: bool,
	matches: List[Tuple[any, any]],
	_first_level=True
) -> bool:

	# Non-recursive comparison; we're done now that the first node has been
	# processed
	if not recursive and not _first_level:
		return True

	if type(node1) is not type(node2):
		return False

	if type(node1) is list:
		if len(node1) != len(node2):
			return False

		for i in range(len(node1)):
			if not _ast_nodes_equal(node1[i], node2[i], recursive, matches, False):
				return False

		return True

	elif isinstance(node1, Node):
		ignored_attrs = [
			attrs for a, b, attrs in matches if node1 in (a, b) or node2 in (a, b)
		]
		for attr in node1.attrs:
			if attr in ignored_attrs:
				continue

			attr1 = getattr(node1, attr)
			attr2 = getattr(node2, attr)

			if not _ast_nodes_equal(attr1, attr2, recursive, matches, False):
					return False

		return True

	else:
		# if node1 != node2:
			# print('XD', node1, node2, '\n')
		return node1 == node2


def ast_nodes_equal(
	node1: Node,
	node2: Node,
	recursive=True,
	matches: List[Tuple[any, any]] = tuple()
) -> bool:

	return _ast_nodes_equal(node1, node2, recursive, matches)


def ast_paths_equal(
	path1: List[Union[Node, List[Node]]],
	path2: List[Union[Node, List[Node]]],
	matches: List[Tuple[any, any]] = tuple()
) -> bool:
	"""
	Determine if two AST node paths are equal, ignoring other parts of the file

	Args:
		path1 (List[Union[Node, List[Node]]]): [description]
		path2 (List[Union[Node, List[Node]]]): [description]
		matches (List[Tuple[any, any]], optional): List of node pairs to
			consider equal. Defaults to tuple().

	Returns:
		bool: [description]
	"""

	if len(path1) != len(path2):
		return False

	# Skip list entries in the path (because they contain irrelevant parts)
	for i in range(len(path1)):
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
			yield from _filter_ast_node(
				getattr(node, attr),
				t,
				_path=_path + [node, attr]
			)


def filter_ast_node(node: Node, t: type) -> List[Union[Node, str]]:
	return _filter_ast_node(node, t)


def chunk_ast_nodes_by_path(
	nodes: List[Tuple[List, Node]]
) -> List[Tuple[List, List[Node]]]:

	chunks = []
	curr_path = None
	curr_chunk = None
	for path, node in nodes:
		if path != curr_path:
			if curr_path is not None:
				chunks.append((curr_path, curr_chunk))

			curr_path = path
			curr_chunk = []

		curr_chunk.append(node)

	if curr_path is not None:
		chunks.append((curr_path, curr_chunk))

	return chunks


def _have_same_references(
	a_var: str,
	b_var: str,
	a_refs: List[Tuple],
	b_refs: List[Tuple],
	matches: List[Tuple]
) -> bool:

	ar = [
		(path, ref)
		for path, refs in a_refs
		for ref in refs
		if ref.member == a_var
	]

	br = [
		(path, ref)
		for path, refs in b_refs
		for ref in refs
		if ref.member == b_var
	]

	if len(ar) != len(br):
		return False

	for i in range(len(ar)):
		a_ref_path, a_ref_node = ar[i]
		b_ref_path, b_ref_node = br[i]
		ref_match = (a_ref_node, b_ref_node, 'name')

		if not ast_paths_equal(
			a_ref_path,
			b_ref_path,
			matches=matches + [ref_match]
		):
			return False

	return True


def get_renamed_variables(
	source_code: str,
	target_code: str
) -> Dict[str, str]:

	try:
		source_tree = javalang.parse.parse(source_code)
		target_tree = javalang.parse.parse(target_code)
	except javalang.parser.JavaSyntaxError:
		return None

	source_declarations = chunk_ast_nodes_by_path(
		filter_ast_node(source_tree, VariableDeclaration)
	)

	target_declarations = chunk_ast_nodes_by_path(
		filter_ast_node(target_tree, VariableDeclaration)
	)

	target_var_names = [
		declarator.name
		for path, declarations in target_declarations
		for declaration in declarations
		for declarator in declaration.declarators
	]

	source_references = chunk_ast_nodes_by_path(
		filter_ast_node(source_tree, MemberReference)
	)

	target_references = chunk_ast_nodes_by_path(
		filter_ast_node(target_tree, MemberReference)
	)

	renamed_var_names = []
	matches = []

	# Find all the semantically equalivalent variables that have different
	# names. For the variable declarations a and b to be semantically
	# equalivalent:
	#
	# - They must have be in the same semantic section of the file
	# - They must have the same references and assignments

	# Iterate over every pair of chunks, including the pair of the same chunk.
	for i in range(len(source_declarations)):
		source_decn_path, source_decn_nodes = source_declarations[i]
		for j in range(i, len(target_declarations)):
			target_decn_path, target_decn_nodes = target_declarations[j]

			# 1. Make sure paths would be equal if source_node (a) and
			# target_node (b) were the same.

			# 1a. Must be in the same part of the file
			# First get all previously discovered renamed variables
			prev_matches_here = [
				(old, new, attrs)
				for path, v in matches
				for old, new, attrs in v
				if path in (source_decn_path, target_decn_path)
			]

			# Now make sure the paths are equal (ignoring the previously found
			# renamed variables and the declarations themselves)
			if not ast_paths_equal(
				source_decn_path,
				target_decn_path,
				matches=prev_matches_here
			):
				continue

			for k in range(len(source_decn_nodes)):
				source_decn_node = source_decn_nodes[k]
				for m in range(len(source_decn_node.declarators)):
					source_declarator = source_decn_node.declarators[m]
					# 1b. Must have different names
					if source_declarator.name in target_var_names:
						continue

					sr = [
						(path, ref)
						for path, refs in source_references
						for ref in refs
						if ref.member == source_declarator.name
					]

					for n in range(k, len(target_decn_nodes)):
						target_decn_node = target_decn_nodes[n]
						for q in range(len(target_decn_node.declarators)):
							target_declarator = target_decn_node.declarators[q]
							# 1c. All attributes except the name should be equal
							declarator_match = (source_declarator, target_declarator, 'name')
							if not ast_nodes_equal(
								source_declarator,
								target_declarator,
								recursive=True,
								matches=prev_matches_here + [declarator_match]
							):
								continue

							# 1d. Must have the same references
							if not _have_same_references(
								source_declarator.name,
								target_declarator.name,
								source_references,
								target_references,
								prev_matches_here
							):
								continue

							tr = [
								(path, ref)
								for path, refs in target_references
								for ref in refs
								if ref.member == target_declarator.name
							]

							# (sr and tr have the same length, so we can do this safely)
							for i in range(len(sr)):
								source_ref_path, source_ref_node = sr[i]
								target_ref_path, target_ref_node = tr[i]
								ref_match = (source_ref_node, target_ref_node, 'name')

								for path, mappings in matches:
									if path == target_ref_path:
										mappings.append(ref_match)

								else:
									matches.append((target_ref_path, [ref_match]))

							# 1d. (The function cannot return multiple mappings
							# containing the same variable at the same path)
							other_renames_at_path = False
							never_used = True
							for path, mappings in renamed_var_names:
								if path != target_decn_path:
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
								renamed_var_names.append((target_decn_path, mappings))

							for path, v in matches:
								if path == target_decn_path:
									for old, new, _ in v:
										if old == source_declarator:
											raise JavaAnalyzationError(f'duplicate declarator in source: {old}')

										if new == target_declarator:
											raise JavaAnalyzationError(f'duplicate declarator in target: {new}')

									v.append(declarator_match)

							else:
								matches.append((target_decn_path, [declarator_match]))

	return renamed_var_names


def undo_variable_renames(code: str, renamed_var_names: List[Tuple]) -> str:
	lines = code.split('\n')
	tokens = tokenize(code)

	for token in tokens:
		if not isinstance(token, Identifier):
			continue

		for path, mappings in renamed_var_names:
			for old, new in mappings:
				if token.value == new:
					line, col = token.position
					line -= 1
					col -= 1
					lines[line] = lines[line][:col] + old + lines[line][col + len(new):]

	return '\n'.join(lines)
