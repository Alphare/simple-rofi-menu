================
Simple Rofi menu
================
What started as a < 20 lines script to make a simple power menu to use with Rofi_.

Screenshot
==========
.. image:: screenshot.png

Usage
=====
To use the menu with rofi, use::

    rofi -show <name> -modi <name>:<path>/simple_rofi_menu.py.

The script will then fetch your :code:`srm_config.<extension>` file, in the same folder as :code:`simple_rofi_menu.py`. You can find examples in the :code:`example_configs/` folder.

As of now, SRM supports YAML and JSON formats. SRM will look for the YAML one first, then the JSON one. If you intend on using a YAML configuration file, you will need to have PyYAML_ installed.

Note: since this script uses :code:`/usr/bin/python3`, you can do so using :code:`pip3 install PyYAML --user` to use your general Python environment, or just change the shebang line to whatever virtualenv you want to use, as long as it's based on Python 3.

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
