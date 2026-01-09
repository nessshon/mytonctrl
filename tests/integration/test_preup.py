from pytest_mock import MockerFixture

from mytonctrl import mytonctrl


def test_warnings(cli, monkeypatch, mocker: MockerFixture):
    monkeypatch.setattr(mytonctrl, 'CheckMytonctrlUpdate', lambda *_: None)
    monkeypatch.setattr(mytonctrl, 'check_installer_user', lambda *_: None)
    monkeypatch.setattr(mytonctrl, 'check_vport', lambda *_: None)

    # test check_ubuntu_version

    monkeypatch.setattr(mytonctrl.os.path, 'exists', lambda _: True)
    res = '''
PRETTY_NAME="Ubuntu 22.04.4 LTS"
NAME="Ubuntu"
VERSION_ID="22.04"
VERSION="22.04.4 LTS (Jammy Jellyfish)"
VERSION_CODENAME=jammy
ID=ubuntu
'''
    mock = mocker.mock_open(read_data=res)
    monkeypatch.setattr('builtins.open', mock)
    output = cli.run_pre_up()
    assert 'Ubuntu' not in output

    monkeypatch.setattr(mytonctrl.os.path, 'exists', lambda _: True)
    res = '''
    PRETTY_NAME="Ubuntu 24.04.4 LTS"
    NAME="Ubuntu"
    VERSION_ID="24.04"
    VERSION="24.04.3 LTS (Noble Numbat)"
    VERSION_CODENAME=noble
    ID=ubuntu
    '''
    mock = mocker.mock_open(read_data=res)
    monkeypatch.setattr('builtins.open', mock)
    output = cli.run_pre_up()
    assert 'Ubuntu' not in output

    res = '''
PRETTY_NAME="Ubuntu 20.04.4 LTS"
NAME="Ubuntu"
VERSION_ID="20.04"
VERSION="20.04.4 LTS (Focal Fossa)"
VERSION_CODENAME=focal
ID=ubuntu
'''
    mock = mocker.mock_open(read_data=res)
    monkeypatch.setattr('builtins.open', mock)
    output = cli.run_pre_up()
    assert 'Ubuntu version must be 22.04 or 24.04. Found 20.04.' in output

    res = '''
PRETTY_NAME="Debian GNU/Linux 12 (bookworm)"
NAME="Debian GNU/Linux"
VERSION_ID="12"
VERSION="12 (bookworm)"
VERSION_CODENAME=bookworm
ID=debian
'''
    mock = mocker.mock_open(read_data=res)
    monkeypatch.setattr('builtins.open', mock)
    output = cli.run_pre_up()
    assert 'Ubuntu' not in output

    # todo: other warnings
