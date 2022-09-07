def test_displays_error_for_no_versions(run):
	assert 'No versions selected' in run.output
