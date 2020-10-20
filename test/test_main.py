import functools
from pathlib import Path
from unittest.mock import Mock, call, patch

import pytest
from typer.testing import CliRunner

from src import main


@pytest.fixture
def mock_console_write():
    with patch('src.main.console.write', autospec=True) as mocked_write:
        yield mocked_write


@pytest.mark.usefixtures('mock_console_write')
def test_switch_called_before_read():
    m = Mock()
    with patch('outcome.read_toml.bin.read_toml', new=m.read):
        with patch('src.main.switch_working_directory', new=m.switch):
            main.run(github_actions=True, key='key', path='file')
            assert m.mock_calls == [call.switch(), call.read(key='key', path='file')]


@patch('src.main.os.chdir', autospec=True)
class TestSwitch:
    @patch.dict('os.environ', {'GITHUB_WORKSPACE': '/workspace'})
    def test_switch(self, mock_chdir: Mock):
        main.switch_working_directory()
        mock_chdir.assert_called_once_with('/workspace')

    @patch.dict('os.environ', {}, clear=True)
    def test_no_switch(self, mock_chdir: Mock):
        main.switch_working_directory()
        mock_chdir.assert_not_called()


@pytest.fixture
def without_switch_working_directory():
    with patch('src.main.switch_working_directory', autospec=True):
        yield


@pytest.fixture
def runner_invoke():
    runner = CliRunner()
    return functools.partial(runner.invoke, main.build())


@pytest.mark.usefixtures('without_switch_working_directory')
class TestCalls:
    @patch('outcome.read_toml.bin.read_toml', autospec=True)
    def test_single_key(self, mock_read_toml: Mock, runner_invoke):
        mock_read_toml.return_value = 'value'
        result = runner_invoke(['--path', 'file.toml', '--key', 'key_to_read'])

        assert result.exit_code == 0
        assert result.stdout.strip() == 'value'
        mock_read_toml.assert_called_once_with(path=Path('file.toml'), key='key_to_read', check_only=False, default=None)

    @patch('outcome.read_toml.bin.read_toml', autospec=True)
    def test_multiple_keys(self, mock_read_toml: Mock, runner_invoke):
        mock_read_toml.side_effect = ['v1', 'v2']
        result = runner_invoke(['--path', 'file.toml', '--key', 'key_to_read\nother_key_to_read'])

        assert mock_read_toml.call_count == 2

        assert result.exit_code == 0
        assert result.stdout.strip() == 'v1\nv2'

        assert mock_read_toml.call_args_list == [
            call(path=Path('file.toml'), key='key_to_read', check_only=False, default=None),
            call(path=Path('file.toml'), key='other_key_to_read', check_only=False, default=None),
        ]

    @patch('outcome.read_toml.bin.read_toml', autospec=True)
    def test_multiple_keys_trailing_newline(self, mock_read_toml: Mock, runner_invoke):
        mock_read_toml.side_effect = ['v1', 'v2']
        result = runner_invoke(['--path', 'file.toml', '--key', 'key_to_read\nother_key_to_read\n'])

        assert mock_read_toml.call_count == 2

        assert result.exit_code == 0
        assert result.stdout.strip() == 'v1\nv2'

        assert mock_read_toml.call_args_list == [
            call(path=Path('file.toml'), key='key_to_read', check_only=False, default=None),
            call(path=Path('file.toml'), key='other_key_to_read', check_only=False, default=None),
        ]

    @patch('outcome.read_toml.bin.read_toml', autospec=True)
    def test_check_only(self, mock_read_toml: Mock, runner_invoke):
        mock_read_toml.return_value = '1'
        result = runner_invoke(['--path', 'file.toml', '--key', 'key_to_read', '--check-only'])

        assert result.exit_code == 0
        assert result.stdout.strip() == '1'
        mock_read_toml.assert_called_once_with(path=Path('file.toml'), key='key_to_read', check_only=True, default=None)


@pytest.mark.usefixtures('without_switch_working_directory')
@patch('outcome.read_toml.bin.read_toml', autospec=True)
class TestGithubActions:
    def test_github_actions(self, mock_read_toml: Mock, runner_invoke):
        mock_read_toml.return_value = 'value'
        result = runner_invoke(['--path', 'file.toml', '--key', 'key-to-read', '--github-actions'])

        assert result.exit_code == 0
        assert result.stdout.strip() == '::set-output name=key_to_read::value'
        mock_read_toml.assert_called_once_with(path=Path('file.toml'), key='key-to-read', check_only=False, default=None)
