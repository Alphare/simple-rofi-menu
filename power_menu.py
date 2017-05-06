#!/usr/bin/python3
"""
Simple power menu for rofi.
"""
import sys
import subprocess
from collections import OrderedDict


class MenuItem:
    def __init__(self, name, command):
        super().__init__()
        self.name = str(name)
        self.command = str(command)

    def __str__(self):
        return self.name


class MenuGroup:
    def __init__(self, *items, **kwargs):
        super().__init__()
        self.visible = kwargs.get('visible', True)
        self.menu_items = OrderedDict()
        for item in items:
            self.add_item(item)

    def add_item(self, item):
        assert isinstance(item, MenuItem)
        self.menu_items[item.name] = item.command

    def __str__(self):
        return "\n".join(self.menu_items)


class MenuChoices:
    groups = []
    separator = '----'

    @property
    def number_of_items(self):
        return sum([len(menu_items) for menu_items in [group.menu_items for group in self.groups]])

    def __init__(self, *groups, **kwargs):
        super().__init__()
        self.numbered = kwargs.get('numbered', False)
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
            new_items = OrderedDict()
            for index, (name, command) in enumerate(group.menu_items.items()):
                new_items["{} {}".format(self.number_of_items + index, name)] = command
            group.menu_items = new_items
        self.groups.append(group)

    def __getitem__(self, name):
        for group in self.groups:
            attr = group.menu_items.get(name)
            if attr:
                return attr
        raise KeyError(name)


def power_menu():
    menu_choices = MenuChoices(
        MenuGroup(
            MenuItem('Lock screen', "/home/raphael/.config/i3/block_lock.sh"),
            MenuItem('Logout', "i3-msg exit"),
        ),
        MenuGroup(
            MenuItem('Switch user', "gdmflexiserver"),
            MenuItem('Reboot', "reboot"),
            MenuItem('Shutdown', "init 0"),
        ),
        numbered=True,
    )
    try:
        # Commands might be multiple words long
        arguments = sys.argv[1:]
        choice = " ".join(arguments)
        split_bash_command = menu_choices[choice].split()

        # Popen ensures the child process still live even if rofi exits
        subprocess.Popen(split_bash_command, stdout=subprocess.PIPE)

    except (KeyError, IndexError):
        # Fine for this program's purposes
        # Will trigger if no arguments are provided or if they are not in `menu_choices`
        print(menu_choices)


if __name__ == '__main__':
    power_menu()
