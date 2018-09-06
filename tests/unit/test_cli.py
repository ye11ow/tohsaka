import json

from unittest.mock import patch
from click.testing import CliRunner
from cli import list_mystic_codes
from cli import show_mystic_code
from cli import run
from cli import load


class TestCli:

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


    @patch('cli.Tohsaka.__init__', return_value=None)
    @patch('cli.Tohsaka.go', return_value=None)
    def test_run_wizard(self, go, __init__):
        runner = CliRunner()
        result = runner.invoke(run, ['stock'], input='splk\nsplk.json\n')
        assert result.exit_code == 0

        __init__.assert_called_once_with('stock', {
            'symbol': 'splk',
            'output_file': 'splk.json'
        })
        go.assert_called_once()

    @patch('cli.Tohsaka.__init__', return_value=None)
    @patch('cli.Tohsaka.go', return_value=None)
    def test_run_wizard_default(self, go, __init__):
        runner = CliRunner()
        result = runner.invoke(run, ['stock'], input='splk\n\n')
        assert result.exit_code == 0

        __init__.assert_called_once_with('stock', {
            'symbol': 'splk',
            'output_file': 'stock'
        })
        go.assert_called_once()


    @patch('cli.Tohsaka.__init__', return_value=None)
    @patch('cli.Tohsaka.go', return_value=None)
    @patch('cli.Tohsaka.load_mystic_code', return_value={})
    def test_run_no_param(self, load_mystic_code, go, __init__):
        runner = CliRunner()
        result = runner.invoke(run, ['stock'], input='splk\n\n')
        assert result.exit_code == 0

        load_mystic_code.assert_called_once_with('stock')
        __init__.assert_called_once_with('stock', {})
        go.assert_called_once()

    @patch('cli.Tohsaka.__init__', return_value=None)
    @patch('cli.Tohsaka.go', return_value=None)
    def test_load(self, go, __init__):
        runner = CliRunner()

        profile = {
            'mystic': 'my_mystic',
            'options': 'options'
        }

        with runner.isolated_filesystem():
            with open('profile', 'w') as f:
                f.write(json.dumps(profile))

            result = runner.invoke(load, ['profile'])

            __init__.assert_called_once_with('my_mystic', {'options': 'options'})
            go.assert_called_once()