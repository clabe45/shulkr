from gradle.project import Project


def test_gradle_build(project: Project) -> None:
	"""
	Run a gradle build
	"""

	project.gradle.build()
