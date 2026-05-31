from typer.testing import CliRunner

from citeevidence.cli import app


def test_cli_help_smoke() -> None:
    runner = CliRunner()

    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "Evidence-grounded citation function analysis CLI scaffold." in result.stdout


def test_final_results_help_smoke() -> None:
    result = CliRunner().invoke(app, ["analysis", "final-results", "--help"])

    assert result.exit_code == 0
    assert "--phase2" in result.stdout
