# Introduction

Since Snapchat imposes few restrictions on what data can be uploaded (i.e.,
not just images), I've taken to using it as a system to send files to
myself and others.

Snapchat FS is the tool that allows this. It provides a simple command line
interface for uploading arbitrary files into Snapchat, managing them, and
downloading them to any other computer with access to this package.

Uploading the file is simple:

```
$ sfs upload some_file.pdf
Uploading file some_file.pdf
```

Downloading is just as simple:

```
$ sfs download directory_to_put_files
Downloading snap file.txt
Downloading snap file.txt but filename is not unique; downloading as: file.txt-1a55ff534e03d25b5a489da83c2ae32ad9bc70fc6e07df4e7b0e82f028cb531f
```

Snapchat FS supports some other features, such as listing the files
currently maintained in Snapchat using the Snapchat FS utility:

```
$ sfs list
Filename      Content hash
some_file.pdf fc7f9f7fd935c8f34...7df
cow.mov       1a55ff534e03d25b5...31f
```


# Features

* [x] Uploading files via command line
* [x] Downloading all the files all at once to an arbitrary file
* [ ] Downloading one file at a time
* [ ] Deleting files from Snapchat's server using the command line (to delete it you must "view" it in the app)
* [ ] Encrypting data with something other than the Snapchat default
* [ ] FUSE integration (yes yes I know I know)


# Configuration

`sfs` will boot up and look for the file `~/.snapchat_fs`, which is a config file that we will use to store things like username and password. If it doesn't find the file, it will prompt you for your username and password. After you enter these things, it will create the config file and populate it with this information (NOTE: password is in PLAINTEXT).

This looks something like so:

```
Looks like you haven't used Snapchat FS before.
We're going to ask for a username and a password; you can
change these later by messing with the file /Users/alex/.snapchat_fs
Please enter a username:
bobby_murphy
Please enter your password (NOTE: STORED IN PLAINTEXT):

```

The `sfs` config file will then look something like this:

```
USERNAME=bobby_murphy
PASSWORD=iheartsnapchat
```

To add more to this config file, all you need to do is follow that format. Currently `sfs` is feature-sparse, so the only settings only include `USERNAME` and `PASSWORD`, but eventually it will allow you to do things like specify the encryption protocol to use when encrypting your data and sending it to the Snapchat servers.


# Installation

The `sfs` file is a Python script that currently sits in the root directory and never moves, because there's no installation script. You can run it with a command like `./sfs`. If you want to move into `bin/` or something, you'll have to do it yourself.

Someday this will be `pip`-installable or something.


# Authors

| Author        | GitHub username                                | Personal Site | Contribution |
|:--------------|:----------------------------------------------:|:-------------|:-------------|
| **Chad Brubaker** | [@pencilo](https://github.com/pencilo)     | -            | wrote some of `snapchat_core`. See his [pysnapchat](https://github.com/pencilo/pysnapchat) repot for a very similar implementation. (All work used with permission.)
| **Alex Clemmer**  | [@hausdorff](https://github.com/hausdorff/)| [nullspace](http://blog.nullspace.io/) | wrote everything else. |
| **Michael Rosenberg**  | [@doomrobo](https://github.com/doomrobo)| - | bug fixes, better login mechanisms |
| -  | [@anshukla](https://github.com/anshukla)| - | added `requirements.txt` |


# LICENSE

Distributed under MIT, which basically means that if you should use this code for anything, you just have to keep a note saying we wrote the code. That said, God help you should you actually decide to use this code.


## MIT License

Copyright (C) [Alex Clemmer](http://nullspace.io/) ([@hausdorff](https://github.com/hausdorff)) and Chad Brubaker ([@pencilo](https://github.com/pencilo))

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
