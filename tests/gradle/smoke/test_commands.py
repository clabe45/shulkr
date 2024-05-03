from gradle.project import Project


def test_gradle_build(project: Project) -> None:
    """
    Run a gradle build
    """

    assert project.gradle.build() is None
