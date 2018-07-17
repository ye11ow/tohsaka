from click.testing import CliRunner
from cli import list_spells
from cli import list_mystic_codes
from cli import show_mystic_code


class TestCli:

    def test_list_spells(self):
        runner = CliRunner()
        result = runner.invoke(list_spells, [])
        assert result.exit_code == 0

        assert 'Forum' in result.output
        assert 'REST' in result.output

    def test_list_mystic_codes(self):
        runner = CliRunner()
        result = runner.invoke(list_mystic_codes, [])
        assert result.exit_code == 0

        assert 'Stock' in result.output
        assert 'Weather' in result.output

    def test_show_mystic_code(self):
        runner = CliRunner()
        result = runner.invoke(show_mystic_code, ['weather'])
        assert result.exit_code == 0

        assert 'Weather' in result.output
        assert 'appid' in result.output

