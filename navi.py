# ----------------------------------------------------------------------------
#
#   navi.py - pyton code for the navi plugin. 
#
#   See README.md for the documentation. Some notes on the python code below.
# 
#   Copyright 2016 Alexander Voss
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ----------------------------------------------------------------------------
#
#   Some notes on the code:
#   - yes, I know some stuff in there is not "pythonic", don't care.
#   - anything that is an actual issue I am happy to learn about!
#   - unit tests are interspersed with the code since I like to see
#     the test and the code it is testing at the same time
#   - code to mock up vim for tests is at ^MOCKING^
# 
#   Table of Contents:
#     ^def followLink^
#     ^def findLink^
#     ^def followLocalLink^
#     ^def followFileLink^
#     ^def makeFilenameAbsolute^
#     ^def isWindowOpenFor^
#     ^switchToWindowForFile^
# 
# ----------------------------------------------------------------------------

import re
import os

# if we cannot import the vim module, assume that we are running nose tests
testing = False
try:
    import vim
except ImportError:
    testing = True
    from nose.tools import assert_equal

# history of windows and locations 
breadcrumbs = []

# ----------------------------------------------------------------------------
def followLink():
    """
    try to find a link in the current line and follow it to the notes,
    open a vertical split window for them if one is not already open.
    """
    (section,file) = findLink()
    if file is None:
        if section is not None:
            followLocalLink(section)
    else:
        if section is not None:
            followFileLink(section, file)

# ----------------------------------------------------------------------------
def findLink():
    """
    Find a link of the form ^section@filename^, ^@filename^ or ^section^ and return
    a tuple (filename, section) where either can be None or (None, None) if no link
    is found.
    """
    line = vim.current.line
    # try section@filename match
    matches = re.search("\^(.+)@(.+)\^", line)
    if matches is None:
        # try filename only
        matches = re.search("\^@(.+)\^", line)
        if matches is not None:
            return (None, matches.group(1))
        else:
            # section only
            matches= re.search("\^(.+)\^", line)
            if matches is not None:
                return (matches.group(1), None)
            else:
                return (None, None)
    return (matches.group(1), matches.group(2))

def findLink_FindsSectionFileLink_Test():
    vim.current.line = "Blah Blah ^BREAKING@NEWS.MD^ Blah"
    assert_equal(findLink(), ("BREAKING", "NEWS.MD"))

def findLink_FindsSectionOnly_Test():
    vim.current.line = "Blah Blub ^BREAKING^ Waffle"
    assert_equal(findLink(), ("BREAKING", None))

def findLink_FindsFilenameOnly_Test():
    vim.current.line = "Waffle Blah '^@NEWS.MD^' Blub"
    assert_equal(findLink(), (None, "NEWS.MD"))

# ----------------------------------------------------------------------------
targetRegex1 = "\(^\|[^\^]\)" # the start of line or character != caret
targetRegex2 = "\($\|[^\^]\)" # the end of line or character != caret

def followLocalLink(section):
    """
    Search for the given string from the top of the file, ignoring instances
    here it appears as part of a link. 
    """
    vim.command("normal 1G")
    vim.command("/\m" + targetRegex1 + section + targetRegex2)

# ----------------------------------------------------------------------------
def followFileLink(section, file):
    """
    If a window is already open for file then switches to it, otherwise opens
    a new one using vsplit.
    """
    absfile = makeFilenameAbsolute(file)
    if isWindowOpenFor(absfile):
        switchToWindowForFile(absfile)
    else:
        vim.command("vsplit "+absfile)
    if(section is not None):
        followLocalLink(section)

# ----------------------------------------------------------------------------
def makeFilenameAbsolute(file):
    """
    If the given filename is not already absolute the it is taken as being
    relative to the path of the file in the current buffer. Returns the 
    abolute path to the resulting filename.
    """
    if os.path.isabs(file):
        return file
    currentFile = vim.current.buffer.name
    return os.path.dirname(currentFile)+"/"+file

# ----------------------------------------------------------------------------
def isWindowOpenFor(file):
    """
    Check if there is an open window for the given file.
    """
    for window in vim.windows:
        buffer = window.buffer
        print buffer.name
        if buffer.name == file:
            return True
    return False

# ----------------------------------------------------------------------------
def switchToWindowForFile(file):
    for i in range(1, len(vim.windows)):
        vim.command("exe "+str(i)+" . \"wincmd w\"")
        if(vim.current.window.buffer.name == file):
            return

# ----------------------------------------------------------------------------
# MOCKING up vim for the unit tests
# ----------------------------------------------------------------------------

# small helper class to simulate vim.* during testing using a dict
class dotdict(dict):
    def __getattr__(self, attr):
        return self.get(attr)
    __setattr__= dict.__setitem__
    __delattr__= dict.__delitem__

if testing:
    vim = dotdict()
    vim.current = dotdict()
    vim.current.line = ""

