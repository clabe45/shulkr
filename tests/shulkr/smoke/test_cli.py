def test_exits_with_status_code_of_zero(run):
    print("Exitted with non-zero status code:")
    print(run.error)
    assert run.exit_code == 0


def test_displays_error_for_no_versions(run):
    assert "No versions selected" in run.output
