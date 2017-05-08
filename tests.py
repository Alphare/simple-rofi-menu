import json
from io import StringIO
from textwrap import dedent

import pytest
import yaml
from hypothesis import given
from hypothesis.strategies import text

from simple_rofi_menu import import_menu_from_config, Menu, MenuGroup, MenuItem, run_selected_item


@pytest.fixture
def valid_yaml_config_file():
    menu_string = """\
    separator: "----"
    index_start: 1
    index_format: "{item_index}: {item_name}"
    numbered: True
    groups:
    - items:
      - name: Lock screen
        command: "i3 lock"
      - name: Logout
        command: i3-msg exit
    - items:
      - name: Switch user
        command: gdmflexiserver
      - name: Reboot
        command: reboot
      - name: Shutdown
        command: init 0"""

    # Because our code will load a file, we use a StringIO
    # instead of a string in case of a regression between
    # yaml.load() and yaml.loads()
    return yaml.load(StringIO(dedent(menu_string)))


@pytest.fixture
def valid_json_config_file():
    menu_string = """\
    {
        "separator": "----",
        "index_start": 1,
        "index_format": "{item_index}: {item_name}",
        "numbered": true,
        "groups": [
            {
                "items": [
                    {
                        "name": "Lock screen",
                        "command": "i3lock"
                    },
                    {
                        "name": "Logout",
                        "command": "i3-msg exit"
                    }
                ]
            },
            {
                "items": [
                    {
                        "name": "Switch user",
                        "command": "gdmflexiserver"
                    },
                    {
                        "name": "Reboot",
                        "command": "reboot"
                    },
                    {
                        "name": "Shutdown",
                        "command": "init 0"
                    }
                ]
            }
        ]
    }"""

    # Because our code will load a file, we use a StringIO
    # instead of a string in case of a regression between
    # json.load() and json.loads()
    return json.load(StringIO(dedent(menu_string)))


@pytest.fixture(params=['valid_yaml_config_file', 'valid_json_config_file'])
def valid_config_file_metafixture(request):
    """
    Parametrizes test with multiple fixtures 
    """
    return request.getfuncargvalue(request.param)


class TestEquality:
    @pytest.mark.parametrize('first_menu, second_menu, equal', [
        (Menu(), Menu(), True),
        (Menu(MenuGroup()), Menu(), False),
        (Menu(MenuGroup()), Menu(MenuGroup()), True),
        (Menu(MenuGroup(MenuItem('lmjg', 'lkjg'))), Menu(MenuGroup()), False),
        (Menu(MenuGroup(MenuItem('lmjg', 'lkjg'))), Menu(MenuGroup(MenuItem('lmjg', 'lkjg'))), True),
        (Menu(numbered=True), Menu(), False),
        (Menu(separator=""), Menu(), False),
        (Menu(index_start=3), Menu(), False),
        (Menu(index_format=""), Menu(), False),
    ])
    def test_Menu(self, first_menu, second_menu, equal):
        assert (first_menu == second_menu) == equal
        assert (second_menu == first_menu) == equal


def test_import_menu_from_config(valid_config_file_metafixture):
    menu = import_menu_from_config(valid_config_file_metafixture)

    expected_menu = Menu(
        MenuGroup(
            MenuItem(
                name='Lock screen',
                command='i3lock'
            ),
            MenuItem(
                name='Logout',
                command='i3-msg exit'
            )
        ),
        MenuGroup(
            MenuItem(
                name='Switch user',
                command='gdmflexiserver'
            ),
            MenuItem(
                name='Reboot',
                command='reboot'
            ),
            MenuItem(
                name='Shutdown',
                command='init 0'
            )
        ),
        numbered=True,
        index_format="{item_index}: {item_name}",
        index_start=1,
        separator='----',
    )

    assert menu == expected_menu


def test_menu_str(valid_config_file_metafixture):
    menu = import_menu_from_config(valid_config_file_metafixture)
    assert str(menu) == dedent("""\
    1: Lock screen
    2: Logout
    ----
    3: Switch user
    4: Reboot
    5: Shutdown""")


@pytest.mark.parametrize('sys_argv', [
    ['test', 'bad_argument'],
    ['test', 'multiple', 'bad', 'arguments'],
    ['test'],  # No arguments
])
def test_invalid_run_menu(sys_argv):
    menu = Menu()

    with pytest.raises(KeyError):
        run_selected_item(menu, sys_argv, dry_run=True)


@given(text())
def test_successful_run_menu(item_name):
    menu = Menu(
        MenuGroup(
            MenuItem(
                name=item_name, command="whatever"
            ),
        ),
        MenuGroup(
            MenuItem(
                name="whatever_1", command="whatever"
            ),
            MenuItem(
                name="whatever_2", command="whatever"
            ),
        ),
    )

    run_selected_item(menu, ['test', item_name], dry_run=True)
