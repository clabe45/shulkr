from gradle.command import Gradle


class Project:
    def __init__(self, project_dir: str, capture_output=False) -> None:
        self.project_dir = project_dir
        self.gradle = Gradle(self.project_dir, capture_output=capture_output)

    @staticmethod
    def init(project_dir: str, capture_output=False) -> "Project":
        """
        Create a new gradle project
        """

        project = Project(project_dir, capture_output=capture_output)
        project.gradle.init()
        return project
