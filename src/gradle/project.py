from gradle.command import Gradle


class Project:
	"""
	A gradle project
	"""

	def __init__(self, project_dir: str) -> None:
		"""
		Initialize a gradle project
		"""

		self.project_dir = project_dir
		self.gradle = Gradle(self.project_dir)

	@staticmethod
	def init(project_dir: str) -> 'Project':
		"""
		Create a new gradle project
		"""

		project = Project(project_dir)
		project.gradle.init()
		return project
