Graphical Base64 encoder and decoder
===================
<p align="center"><img width="65%" alt="GUI Interface" src="https://raw.githubusercontent.com/Aayush-Security/Base64-encoder-decoder/master/Screenshot%20from%202018-06-23%2016-58-44.png"></p>

A simple base64 encoder and decoder for files, written in python. 
Works as both a command-line utility and as a graphical application for those 
who have PyGTK available.

Takes a file (binary or text) as an input and encodes it to a base64 text file.
The reverse operation is also possible, by taking a text file and decoding it
back to the original format.

To run GUI

```
 python main.py
```
If you get error

Traceback (most recent call last):
  File "main.py", line 24, in <module>
    import gtk
ImportError: No module named gtk
  
  Install python-gtk2
  
```
 sudo apt-get install python-gtk2
```



