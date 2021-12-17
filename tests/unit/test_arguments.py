from shulkr.arguments import parse_args


def test_parse_args_with_no_arguments_exits_with_return_code_of_2(mocker):
	sys_exit = mocker.patch('sys.exit')
	parse_args([])
	assert sys_exit.called_once_with(2)


def test_parse_args_with_one_version_has_correct_version():
	assert parse_args(['1.18']).version == ['1.18']


def test_parse_args_with_one_version_has_default_repo():
	assert parse_args(['1.18']).repo == '.'


def test_parse_args_with_one_version_has_default_message():
	assert parse_args(['1.18']).message == 'version {}'


def test_parse_args_with_one_version_sets_undo_renamed_vars_to_false():
	assert not parse_args(['1.18']).undo_renamed_vars


def test_parse_args_with_one_version_sets_tag_to_true():
	assert parse_args(['1.18']).tag


def test_parse_args_with_one_version_and_no_tags_sets_tag_to_false():
	assert not parse_args(['--no-tags', '1.18']).tag
