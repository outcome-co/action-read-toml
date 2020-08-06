from unittest.mock import Mock, call, patch

from src import main


@patch('src.main.get_read_toml_args', autospec=True)
def test_switch_called_before_read(mock_get_args: Mock):
    m = Mock()
    with patch('outcome.read_toml.bin.read_toml', new=m.read):
        with patch('src.main.switch_working_directory', new=m.switch):
            mock_get_args.return_value = ['arg']
            main.main()
            assert m.mock_calls == [call.switch(), call.read(['arg'])]


@patch('outcome.read_toml.bin.say', autospec=True)
@patch('src.main.os.chdir', autospec=True)
class TestSwitch:
    @patch.dict('os.environ', {'GITHUB_WORKSPACE': '/workspace'})
    def test_switch(self, mock_chdir: Mock, mock_say: Mock):
        main.switch_working_directory()
        mock_chdir.assert_called_once_with('/workspace')

    @patch.dict('os.environ', {}, clear=True)
    def test_no_switch(self, mock_chdir: Mock, mock_say: Mock):
        main.switch_working_directory()
        mock_chdir.assert_not_called()


@patch('outcome.read_toml.bin.read_toml', autospec=True)
class TestGithubActions:
    @patch.dict('os.environ', {'GITHUB_ACTIONS': '1'})
    def test_github_actions(self, mock_read_toml: Mock):
        main.main()
        mock_read_toml.assert_called_once()
        args, kwargs = mock_read_toml.call_args
        assert '--github-actions' in args[0]

    @patch.dict('os.environ', {}, clear=True)
    def test_no_github_actions(self, mock_read_toml: Mock):
        main.main()
        mock_read_toml.assert_called_once()
        args, kwargs = mock_read_toml.call_args
        assert '--github-actions' not in args[0]
