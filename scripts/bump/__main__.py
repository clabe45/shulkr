from mint.repo import Repo
import keepachangelog


def current_version():
	changes = keepachangelog.to_dict('CHANGELOG.md')
	return sorted(changes.keys())[-1]


def main():
	repo = Repo('.')

	old_version = current_version()

	# Release to get predicted version
	keepachangelog.release('CHANGELOG.md')
	predicted_version = current_version()

	# Confirm version
	user_input = input('New version [{}]: '.format(predicted_version))
	new_version = user_input or predicted_version

	# Undo temporary release
	repo.git.restore('CHANGELOG.md')

	# Release with confirmed version
	keepachangelog.release('CHANGELOG.md', new_version)

	# Update setup.py
	with open('setup.py', 'r') as setuppy:
		setuppy_code = setuppy.read()
	new_setuppy_code = setuppy_code.replace(old_version, new_version)
	with open('setup.py', 'w') as setuppy:
		setuppy.write(new_setuppy_code)

	# Commit to git
	commit_message = f'chore: release version {new_version}\n\nBump version {old_version} → {new_version}'
	repo.git.commit('CHANGELOG.md', 'setup.py', message=commit_message)
	repo.git.tag(f'v{new_version}', annotate=True, message=f'version {new_version}')

	print(f'Bumped version {old_version} → {new_version}')


if __name__ == '__main__':
	main()
