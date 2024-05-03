import os
from gradle.command import Gradle


class TestGradle:
    def test__init__without_gradlew(self, mocker):
        """
        Gradle constructor
        """

        Command__init__ = mocker.patch("gradle.command.Command.__init__")
        mocker.patch("gradle.command.os.path.exists", return_value=False)

        Gradle(".", capture_output=True)

        Command__init__.assert_called_once_with(
            "gradle", working_dir=".", capture_output=True
        )

    def test__init__with_gradlew(self, mocker):
        """
        Gradle constructor
        """

        gradlew_path = "path/to/gradlew.bat" if os.name == "nt" else "path/to/gradlew"

        Command__init__ = mocker.patch("gradle.command.Command.__init__")
        mocker.patch("gradle.command.os.path.exists", return_value=True)
        mocker.patch("gradle.command.os.path.join", return_value=gradlew_path)

        Gradle(".", capture_output=True)

        Command__init__.assert_called_once_with(
            # Mocking `os.name` causes pytest to crash on unix, so we have to
            # check the os name
            gradlew_path,
            working_dir=".",
            capture_output=True,
        )
