#!/usr/bin/env python3
"""
A simple menu for rofi.
"""
import os.path
import sys
import subprocess
from collections import OrderedDict

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE_NAME = 'srm_config'


def import_menu_from_config(config):
    groups = []
    for group in config['groups']:
        items = []
        for item in group['items']:
            items.append(MenuItem(**item))
        groups.append(MenuGroup(*items))
    del config['groups']
    return Menu(*groups, **config)


def create_menu():
    """
    Tries to open the yaml file first. If found, we assume PyYAML is installed and continue.
    Else, we try opening the json file.
    """
    try:
        with open(os.path.join(BASE_DIR, "{}.yaml").format(CONFIG_FILE_NAME), encoding='utf-8', mode='r') as f:
            import yaml
            config = yaml.load(f)
    except FileNotFoundError:
        with open(os.path.join(BASE_DIR, "{}.json").format(CONFIG_FILE_NAME), encoding='utf-8', mode='r') as f:
            import json
            config = json.load(f)

    return import_menu_from_config(config)


class MenuItem:
    def __init__(self, name, command):
        super().__init__()
        self.name = str(name)
        self.command = str(command)

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name and self.command == other.command


class MenuGroup:
    def __init__(self, *items):
        super().__init__()
        self.menu_items = OrderedDict()
        for item in items:
            self.add_item(item)

    def add_item(self, item):
        assert isinstance(item, MenuItem)
        self.menu_items[item.name] = item.command

    def __str__(self):
        return "\n".join(self.menu_items)

    def __eq__(self, other):
        if len(self.menu_items) != len(other.menu_items):
            return False
        return all([item == other_item for item, other_item in zip(self.menu_items, other.menu_items)])


class Menu:
    @property
    def number_of_items(self):
        return sum([len(menu_items) for menu_items in [group.menu_items for group in self.groups]])

    def __init__(self, *groups, **kwargs):
        super().__init__()
        self.numbered = kwargs.get('numbered', False)
        self.index_start = kwargs.get('index_start', 0)
        self.index_format = kwargs.get('index_format', "{item_index} {item_name}")
        self.separator = kwargs.get('separator', '---')
        self.groups = []
        for group in groups:
            self.add_group(group)

    def __str__(self):
        return_values = []
        is_first_loop = True

        for group in self.groups:
            if not is_first_loop:
                return_values.append(self.separator)
            return_values.append(str(group))
            is_first_loop = False

        return "\n".join(return_values)

    def add_group(self, group):
        assert isinstance(group, MenuGroup)
        if self.numbered:
            # Change the key to all MenuItems in the group using `self.index_format` which must define {item_index} and {item_name}
            # starts at `self.index_start`
            new_items = OrderedDict()
            for index, (name, command) in enumerate(group.menu_items.items(), start=self.index_start):
                new_items[self.index_format.format(item_index=self.number_of_items + index, item_name=name)] = command
            group.menu_items = new_items
        self.groups.append(group)

    def __getitem__(self, name):
        # Look for the MenuItem with this name in each group
        for group in self.groups:
            attr = group.menu_items.get(name)
            if attr:
                return attr
        raise KeyError(name)

    def __eq__(self, other):
        if not self.groups and not other.groups:
            groups_are_equal = True
        elif len(self.groups) != len(other.groups):
            return False
        else:
            groups_are_equal = all([group == other_group for group, other_group in zip(self.groups, other.groups)])
        return all([
            groups_are_equal,
            self.index_format == other.index_format,
            self.index_start == other.index_start,
            self.numbered == other.numbered,
            self.separator == other.separator,
        ])


def run_selected_item(menu, sys_argv, dry_run=False):
    # Commands might be multiple words long
    arguments = sys_argv[1:]
    choice = " ".join(arguments)
    split_bash_command = menu[choice].split()
    # Popen ensures the child process still live even if rofi exits
    if not dry_run:
        subprocess.Popen(split_bash_command, stdout=subprocess.PIPE)


def run_menu(menu):
    try:
        # sys.argv passed to the function for easier testing
        run_selected_item(menu, sys.argv)
    except KeyError:
        # Fine for this program's purposes
        # Will trigger if no arguments are provided or if they are not in `menu`
        print(menu)


def main():
    menu = create_menu()
    assert isinstance(menu, Menu)

    run_menu(menu)


if __name__ == '__main__':
    main()
