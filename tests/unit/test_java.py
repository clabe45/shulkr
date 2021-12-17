from javalang.tree import CompilationUnit, ClassDeclaration, Literal, MethodDeclaration

from shulkr.java import ast_nodes_equal, filter_ast_node, get_renamed_variables, undo_variable_renames


def wrap_in_class(code: str) -> str:
	return """package foo;

	class Foo {
		public static void main(String[] args) {
			%s
		}
	}
	""" % code


def test_ast_nodes_equal_with_equal_ints_returns_true():
	assert ast_nodes_equal(1, 1, recursive=False)


def test_ast_nodes_equal_recursive_with_equal_ints_returns_true():
	assert ast_nodes_equal(1, 1)


def test_ast_nodes_equal_with_different_ints_returns_true():
	assert not ast_nodes_equal(1, 2, recursive=False)


def test_ast_nodes_equal_recursive_with_different_ints_returns_true():
	assert not ast_nodes_equal(1, 2)


def test_ast_nodes_equal_with_equal_nodes_returns_true():
	node1 = Literal(value='hello')
	node2 = Literal(value='hello')
	assert ast_nodes_equal(node1, node2, recursive=False)


def test_ast_nodes_equal_recursive_with_equal_nodes_returns_true():
	node1 = Literal(value='hello')
	node2 = Literal(value='hello')
	assert ast_nodes_equal(node1, node2)


def test_ast_nodes_equal_with_inequal_nodes_returns_false():
	node1 = Literal(value='hello')
	node2 = Literal(value='bye')
	assert not ast_nodes_equal(node1, node2, recursive=True)


def test_ast_nodes_equal_recursive_with_inequal_nodes_returns_false():
	node1 = Literal(value='hello')
	node2 = Literal(value='bye')
	assert not ast_nodes_equal(node1, node2)


def test_ast_nodes_equal_recursive_with_equal_nodes_wrapped_in_lists_returns_true():
	node1 = Literal(value='hello')
	node2 = Literal(value='hello')
	assert ast_nodes_equal([node1], [node2])


def test_ast_nodes_equal_recursive_with_inequal_nodes_wrapped_in_lists_returns_false():
	node1 = Literal(value='hello')
	node2 = Literal(value='bye')
	assert not ast_nodes_equal([node1], [node2])


def test_ast_nodes_equal_recursive_with_inequal_nodes_and_the_inequal_part_ignored_returns_true():
	# The following doesn't make any sense, but it's just to test our code, calm
	# down
	node1 = Literal(value='hello')
	node2 = Literal(value='bye')
	node3 = Literal(value=node1)
	node4 = Literal(value=node2)
	assert ast_nodes_equal(node3, node4, matches=[(node1, node2, 'value')])


def test_filter_ast_node_with_no_matching_children_returns_empty_list():
	node = Literal(value='hello')
	assert list(filter_ast_node(node, CompilationUnit)) == []


def test_get_renamed_variables_identical_code_with_single_declaration_with_intialization_returns_empty_list():
	renamed_variables = get_renamed_variables(
		wrap_in_class('int x = 0;'),
		wrap_in_class('int x = 0;')
	)

	assert renamed_variables == []


def test_get_renamed_variables_identical_code_with_two_declarations_without_initializations_returns_empty_list():
	renamed_variables = get_renamed_variables(
		wrap_in_class('int x; int y;'),
		wrap_in_class('int x; int y;')
	)

	assert renamed_variables == []


def test_get_renamed_variables_identical_code_with_one_declaration_with_two_variables_without_initializations_returns_empty_list():
	renamed_variables = get_renamed_variables(
		wrap_in_class('int x, y;'),
		wrap_in_class('int x, y;')
	)

	assert renamed_variables == []


def test_get_renamed_variables_single_declaration_with_intialization_returns_the_mapping():
	renamed_variables = get_renamed_variables(
		wrap_in_class('int x = 0;'),
		wrap_in_class('int y = 0;')
	)

	assert [v for path, v in renamed_variables] == [[('x', 'y')]]


def test_get_renamed_variables_single_declaration_with_intialization_returns_correct_path():
	renamed_variables = get_renamed_variables(
		wrap_in_class('int x = 0;'),
		wrap_in_class('int y = 0;')
	)

	actual = [type(node) for path, v in renamed_variables for node in path]
	expected = [CompilationUnit, str, ClassDeclaration, str, MethodDeclaration, str]
	assert actual == expected


def test_get_renamed_variables_two_declarations_without_intializations_returns_both_mappings():
	renamed_variables = get_renamed_variables(
		wrap_in_class('int x; int a;'),
		wrap_in_class('int y; int b;')
	)

	assert [v for path, v in renamed_variables] == [[('x', 'y'), ('a', 'b')]]


def test_get_renamed_variables_two_declarations_with_intializations_returns_both_mappings():
	renamed_variables = get_renamed_variables(
		wrap_in_class('int x = 0; int a = 1;'),
		wrap_in_class('int y = 0; int b = 1;')
	)

	assert [v for path, v in renamed_variables] == [[('x', 'y'), ('a', 'b')]]


def test_get_renamed_variables_one_declaration_with_different_intializations_returns_empty_list():
	renamed_variables = get_renamed_variables(
		wrap_in_class('int x = 0;'),
		wrap_in_class('int y = 1;')
	)

	assert renamed_variables == []


def test_get_renamed_variables_single_declaration_without_intialization_returns_the_mapping():
	renamed_variables = get_renamed_variables(
		wrap_in_class('int x;'),
		wrap_in_class('int y;')
	)

	assert [v for path, v in renamed_variables] == [[('x', 'y')]]


def test_get_renamed_variables_single_declaration_with_one_identical_reference_returns_the_mapping():
	renamed_variables = get_renamed_variables(
		wrap_in_class('int x; System.out.println(x);'),
		wrap_in_class('int y; System.out.println(y);')
	)

	assert [v for path, v in renamed_variables] == [[('x', 'y')]]


def test_get_renamed_variables_single_declaration_with_one_different_reference_returns_empty_list():
	renamed_variables = get_renamed_variables(
		wrap_in_class('int x; System.out.println(x);'),
		wrap_in_class('int y; System.out.println(y + "...");')
	)

	assert renamed_variables == []


def test_get_renamed_variables_one_declaration_without_initialization_in_each_branch_of_if_statement_returns_the_mapping():
	renamed_variables = get_renamed_variables(
		wrap_in_class('if (true) { int x; } else { int x; }'),
		wrap_in_class('if (true) { int y; } else { int y; }')
	)

	assert [v for path, v in renamed_variables] == [[('x', 'y')], [('x', 'y')]]


def test_undo_variable_renames_with_one_declaration_and_no_renames_returns_identical_code():
	code = 'int x;'
	renamed_variables = []

	assert undo_variable_renames(code, renamed_variables) == code


def test_undo_variable_renames_with_one_renamed_declaration_updates_code():
	renamed_variables = [(None, [('x', 'y')])]

	assert undo_variable_renames('int y;', renamed_variables) == 'int x;'


def test_undo_variable_renames_with_one_declaration_with_one_renamed_variable_and_one_unchanged_variable_updates_renamed_variable():
	renamed_variables = [(None, [('x', 'y')])]

	assert undo_variable_renames('int a, y;', renamed_variables) == 'int a, x;'


def test_undo_variable_renames_with_one_renamed_declaration_with_one_reference_updates_declaration_and_reference():
	renamed_variables = [(None, [('x', 'y')])]

	assert undo_variable_renames('int y = 0; int a = y;', renamed_variables) == 'int x = 0; int a = x;'


def test_undo_variable_renames_with_one_renamed_declaration_set_to_string_with_same_text_only_updates_identifier():
	renamed_variables = [(None, [('x', 'y')])]

	assert undo_variable_renames('int y = "y";', renamed_variables) == 'int x = "y";'
