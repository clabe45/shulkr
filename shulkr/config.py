class Config:
	def __init__(self) -> None:
		self.repo_path = None


def get_config():
	return config


config = Config()
