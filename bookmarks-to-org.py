#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2014 Alexey Kutepov a.k.a. rexim

# Modified by Fabio Rinaldi 2018, see explanation at:
# https://github.com/fabiorinaldi/bookmarks2org

# ------------------------------------------------------------

# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import codecs
import locale
import sys
import json

# Initial nestedness level
# 0: to have the top level folders in the json file 
#    become top level in org 
# 1: to put the top level folders in the json file under a new 
#    top level entry in the org file (original behavior)
TOPLEVEL=1

sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout)

def export_bookmarks(bookmarks, fp, matchtitle=None):

    # Output the node according to its type and the current level
    def print_bookmarks_place(bookmarks,level):
        fp.write('%s - [[%s][%s]]\n' % (' ' * (level - 1),
                                        bookmarks['uri'],
                                        bookmarks['title']))


    # Output the node according to its type and the current level
    def print_bookmarks_container(bookmarks,level,title="bookmarks"):
        if bookmarks['title'] != "":
            title = bookmarks['title'] 
        fp.write('%s %s\n' % ('*' * level, title))


    # The inner recursive function which does the main work
    def export_bookmarks_impl(bookmarks, level, matchtitle):
        # matchtitle can have 2 values: 
        #  None: no string required, print always, 
        #  the string to be matched: don't print until matched

        if bookmarks.has_key('children'):
            # Due to the nature of org-mode format, it is important to
            # export not folder nodes first. So they are guaranteed to
            # be children of the current node.

            if not matchtitle:
                # condition is true only when matchtitle is None
                for child in bookmarks['children']:
                    if child['type'] == 'text/x-moz-place':
                        print_bookmarks_place(child, level + 1)

            for child in bookmarks['children']:
                if child['type'] == 'text/x-moz-place-container':
                    if not matchtitle or child['title'] == matchtitle:
                        print_bookmarks_container(child, level + 1)
                        export_bookmarks_impl(child, level + 1, None)

                    else:
                        # matchtitle contains a string AND
                        #   that string does not match matchtitle
                        # recurse only
                        export_bookmarks_impl(child, level, matchtitle)                        

    if not matchtitle and TOPLEVEL>0:
        print_bookmarks_container(bookmarks, TOPLEVEL)

    export_bookmarks_impl(bookmarks, TOPLEVEL, matchtitle)

if __name__ == '__main__':
    # Reading JSON from stdin
    bookmarks = json.load(sys.stdin)

    args=sys.argv[1:]

    if len(args) == 0:
        export_bookmarks(bookmarks, sys.stdout, None)

    else:
        while len(args) > 0:

            # Writing org-mode to stdout, starting at the bookmark identified by the argument
            export_bookmarks(bookmarks, sys.stdout, args[0])

            args = args[1:]

