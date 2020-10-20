from unittest.mock import Mock, call, patch

import pytest

from src import main


@patch('src.main.get_read_toml_args', autospec=True)
def test_switch_called_before_read(mock_get_args: Mock):
    m = Mock()
    with patch('outcome.read_toml.bin.read_toml', new=m.read):
        with patch('src.main.switch_working_directory', new=m.switch):
            mock_get_args.return_value = [{'path': 'file'}]
            main.main()
            assert m.mock_calls == [call.switch(), call.read(path='file')]


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


@pytest.mark.usefixtures('without_switch_working_directory')
@patch.dict('os.environ', {}, clear=True)
class TestCalls:
    @patch('outcome.read_toml.bin.read_toml', autospec=True)
    def test_single_key(self, mock_read_toml: Mock):
        with patch('src.main.sys', autospec=True) as mocked_sys:
            mocked_sys.argv = ['exe', '--path', 'file.toml', '--key', 'key_to_read']

            main.main()

            mock_read_toml.assert_called_once_with(path='file.toml', key='key_to_read')

    @patch('outcome.read_toml.bin.read_toml', autospec=True)
    def test_multiple_keys(self, mock_read_toml: Mock):
        with patch('src.main.sys', autospec=True) as mocked_sys:
            mocked_sys.argv = ['exe', '--path', 'file.toml', '--key', 'key_to_read\nother_key_to_read']

            main.main()

            assert mock_read_toml.call_count == 2
            assert mock_read_toml.call_args_list == [
                call(path='file.toml', key='key_to_read'),
                call(path='file.toml', key='other_key_to_read'),
            ]

    @patch('outcome.read_toml.bin.read_toml', autospec=True)
    def test_multiple_keys_trailing_newline(self, mock_read_toml: Mock):
        with patch('src.main.sys', autospec=True) as mocked_sys:
            mocked_sys.argv = ['exe', '--path', 'file.toml', '--key', 'key_to_read\nother_key_to_read\n']

            main.main()

            assert mock_read_toml.call_count == 2
            assert mock_read_toml.call_args_list == [
                call(path='file.toml', key='key_to_read'),
                call(path='file.toml', key='other_key_to_read'),
            ]


@patch('outcome.read_toml.bin.read_toml', autospec=True)
class TestGithubActions:
    @patch.dict('os.environ', {'GITHUB_ACTIONS': '1'})
    def test_github_actions(self, mock_read_toml: Mock):
        with patch('src.main.sys', autospec=True) as mocked_sys:
            mocked_sys.argv = ['exe', '--path', 'file.toml', '--key', 'key_to_read']

            main.main()

            mock_read_toml.assert_called_once()
            args, kwargs = mock_read_toml.call_args
            assert kwargs['github_actions']

    @patch.dict('os.environ', {}, clear=True)
    def test_no_github_actions(self, mock_read_toml: Mock):
        with patch('src.main.sys', autospec=True) as mocked_sys:
            mocked_sys.argv = ['exe', '--path', 'file.toml', '--key', 'key_to_read']

            main.main()

            mock_read_toml.assert_called_once()
            args, kwargs = mock_read_toml.call_args
            assert not kwargs.get('github_actions', False)
