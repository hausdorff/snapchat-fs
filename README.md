
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

Snapchat FS supports many other features, such as listing the files
currently maintained in Snapchat using the Snapchat FS utility:

```
$ sfs list
Filename      Content hash
some_file.pdf fc7f9f7fd935c8f34...7df
cow.mov       1a55ff534e03d25b5...31f
```


# Authors

| Author        | GitHub username                            | Contribution |
|:--------------|-------------------------------------------:|:------------:|
| Chad Brubaker | [@pencilo](https://github.com/pencilo)     | wrote some of `snapchat_core`. See his [pysnapchat](https://github.com/pencilo/pysnapchat) repot for a very similar implementation. (All work used with permission.)
| Alex Clemmer  | [@hausdorff](https://github.com/hausdorff/)| wrote everything else. |


# LICENSE

Distributed under MIT, which basically means that if you should use this code for anything, you just have to keep a note saying we wrote the code. That said, God help you should you actually decide to use this code.


## MIT License

Copyright (C) Alex Clemmer (@hausdorff) and Chad Brubaker (@pencilo)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.