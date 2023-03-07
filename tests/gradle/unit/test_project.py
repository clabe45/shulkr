from gradle.project import Project


class TestProject:
	def test__init__creates_gradle_instance(self, mocker):
		"""
		Test Project constructor
		"""

		Gradle = mocker.patch('gradle.project.Gradle')

		Project('.', capture_output=True)

		Gradle.assert_called_once_with('.', capture_output=True)

	def test__init__sets_project_dir(self, mocker):
		"""
		Test Project constructor
		"""

		mocker.patch('gradle.project.Gradle')

		project = Project('.')

		assert project.project_dir == '.'
