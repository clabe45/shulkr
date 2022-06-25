import os

from shulkr.config import Config, init_config


class TestConfig:
	def test_save_opens_config_file_for_writing(self, mocker):
		# 1. Create a new configuration
		config = Config(
			repo_path='foo',
			mappings='mojang',
			message_template='{}',
			tag=True,
			undo_renamed_vars=False
		)

		# 2. Mock open()
		open_ = mocker.patch('shulkr.config.open')

		# 3. Try to save the configuration to the disk
		config.save()

		# 4. Make sure open() was called currectly
		config_path = os.path.join('foo', '.shulkr')
		open_.assert_called_once_with(config_path, 'w+')


def test_init_config_creates_new_configuration_with_provided_arguments_if_config_file_is_not_found(mocker, empty_repo):
	# 1. Spy on Config constructor
	Config_ = mocker.patch('shulkr.config.Config')

	# 2. Patch os.path.exists to return False
	mocker.patch('shulkr.config.os.path.exists', return_value=False)

	# 3. Call init_config
	init_config(
		repo_path='foo',
		mappings='mojang',
		message_template='{}',
		tag=True,
		undo_renamed_vars=False
	)

	# 4. The Config constructor should have been called with the specified
	# path and mappings
	Config_.assert_called_once_with('foo', 'mojang', '{}', True, False)


def test_init_config_commits_config_when_creating_new_one(mocker, empty_repo):
	# 1. Stub out Config class
	mocker.patch('shulkr.config.Config')

	# 2. Mock 'git commit'
	mocker.patch.object(empty_repo.git, 'commit')

	# 3. No existing config should be found
	mocker.patch('shulkr.config.os.path.exists', return_value=False)

	# 4. Call init_config
	init_config(
		repo_path='foo',
		mappings='mojang',
		message_template='{}',
		tag=True,
		undo_renamed_vars=False
	)

	# 5. "git commit --message 'add .shulkr' .shulkr"
	empty_repo.git.add.assert_called_once_with('.shulkr')
	empty_repo.git.commit.assert_called_once_with(message='add .shulkr')


def test_init_config_loads_existing_config_if_config_file_is_found(mocker):
	# 1. Stub out the Config constructor
	Config_ = mocker.patch('shulkr.config.Config')

	# 2. Add a fake config
	# 2a. Patch os.path.exists to return True
	mocker.patch('shulkr.config.os.path.exists', return_value=True)

	# 2b. Stub out open()
	mocker.patch('shulkr.config.open')

	# 2c. Patch toml.load to return a dummy config file
	raw_config = {
		'mappings': 'yarn',
		'message': 'Minecraft {}',
		'tag': False,
		'experimental': {
			'undo_renamed_vars': True
		}
	}
	mocker.patch('shulkr.config.toml.load', return_value=raw_config)

	# 3. Call init_config
	init_config(
		repo_path='foo',
		mappings='mojang',
		message_template='{}',
		tag=True,
		undo_renamed_vars=False
	)

	# 4. The Config constructor should have been called with the path and
	# mappings from the existing config
	Config_.assert_called_once_with(
		repo_path='foo',
		mappings='yarn',
		message_template='Minecraft {}',
		tag=False,
		undo_renamed_vars=True
	)
