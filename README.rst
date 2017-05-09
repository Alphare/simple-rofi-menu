================
Simple Rofi menu
================
What started as a < 20 lines script to make a simple power menu to use with Rofi_.

Screenshot
==========
.. image:: screenshot.png

Install
=======
Simply download :code:`simple_rofi_menu.py` and an example config file to the same directory. Soon, you will be able to use a custom path for your config file.

Usage
=====
To use the menu with rofi, use::

    rofi -show <name> -modi <name>:<path>/simple_rofi_menu.py.

The script will then fetch your :code:`srm_config.<extension>` file, in the same folder as :code:`simple_rofi_menu.py`. You can find examples in the :code:`example_configs/` folder.

As of now, SRM supports YAML and JSON formats. SRM will look for the YAML one first, then the JSON one. If you intend on using a YAML configuration file, you will need to have PyYAML_ installed.

Note: This script uses :code:`#!/usr/bin/env python3`, it will fetch your current Python environment and look for Python 3. You can do :code:`pip3 install PyYAML --user` to install PyYAML in your general Python environment.

Documentation
=============

Menu
----

| **Positional arguments**: :code:`*groups`
| **Type:** MenuGroup_
| As many groups as you want.

----------

| **Keyword argument:** :code:`numbered`
| **Type**: Boolean
| **Default**: :code:`False`
| Auto-numbering of all menu items.

----------

| **Keyword argument:** :code:`index_start`
| **Type**: Integer
| **Default**: :code:`0`
| Index of the first menu item if :code:`numbered` is :code:`True`.

----------

| **Keyword argument:** :code:`index_format`
| **Type**: String
| **Default**: :code:`"{item_index} {item_name}"`
| Format for updating each :code:`MenuItem` if :code:`numbered` is :code:`True`, which must define :code:`{item_index}` and :code:`{item_name}`.

----------

| **Keyword argument:** :code:`separator`
| **Type**: String
| **Default**: :code:`"---"`
| Separates menu groups.


MenuGroup
---------
| **Positional arguments**: :code:`*items`
| **Type**: MenuItem_
| As many items as you want.

MenuItem
--------
| **Argument**: :code:`name`
| **Type**: String
| Name to be displayed in the menu.

----------

| **Argument**: :code:`command`
| **Type**: String
| Command to be executed upon selecting this item


.. _Rofi: https://davedavenport.github.io/rofi/
.. _PyYAML: https://pypi.python.org/pypi/PyYAML
