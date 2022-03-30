Specification 2
====================

This package allows user to apply a variety of modifications to selected image(s) and then save it in the desired
folder.

Usage
--------------
In order to use the program, user needs to run main.py file and follow the given instructions in the user interface
program.

Firstly, select image(s) which you want to modify and folder where you want to save modified image(s). Then, select
resize method, enter width and height if needed. You can also choose filter which you want to apply to image(s).
After that, just click "Save" button to save modified image(s).

Note:
--------------
* You cannot resize image's width or height values to bigger than originals. Otherwise, program will use the original
image's size values.
* JPEG file format does not support "RGBA" format, so the program converts all transparent pixels into white pixels.