# Navi

A vim plugin that provides hyperlinks for text files (a la textlink) and a browsing history. Written mainly in Python.

# Installation

Unix-type operating systems:
  Place navi.vim and navi.py in your global vim plugin directory or 
  in ~/.vim/plugin/navi to install just for your own user account.

  If you are using git you can simply 
  git clone https://github.com/alexvoss/navi.git
  You might want to watch the repository to be notified of updates.

Windows:
  Place navi.vim and navi.py in ... or in ...

# Usage

The simplest usage is to create a link to a section in the current file. Links
are delimited by the caret character (^) and can contain arbitrary text. The
plugin will search the current file for this string from the top (ignoring the
links of course). For example, here is a link to ^USAGE^, the section heading
above. It is up to you, the user, to provide suitable target that are unique
within the file. With the default key mapping, in command mode, place the 
cursor over the link above and hit the backquote character (`) on your keyboard
in normal mode. The cursor should jump to the heading of this section.

Links can also go to external files, which will be opened in a vertical split window
The plugin will detect if the file is already open and switch to the corresponding 
window.  For example, here is a link to the python source for the plugin:

^@navi.py^

To open a specific section of this file, add the string to search for in front
of the at sign (@) in the above. For example, to link to the findLink() function
in the python source, use a link like this:

^def findLink@navi.py^

Navi keeps a history of locations, so it is possible to switch back to a previous
location. The is done using the tilde character (~) on your keyboard in normal
mode. If you have closed the window you activated a link from then the location
is removed from the history without switching windows. If you have more than one
window for a file, then one of them is used but not necessarily the one you used
to activate the link. (fix this?)

# WHY?

Navi is inspired by Robert KellyIV's textlink plugin [1]. It does feature
some additional functionality, a syntax that I find nicer but as mainly witten
as an exercise in writing vim plugins in python. 

I had a look at VimScript and turned away with horror (there is a reason the 
standard work on this is called "Learn VimScript the Hard Way" [2]. So why 
stick with vim? The answer is muscle memory [3] as well as the fact that vim 
is still one of the few text editors that allow you to get your work done without 
having to use the mouse (ot touch your screen), which does improve efficiency.

# Footnotes

[1]: http://www.vim.org/scripts/script.php?script_id=347
[2]: http://learnvimscriptthehardway.stevelosh.com/
[3]: http://lifehacker.com/5799234/how-muscle-memory-works-and-how-it-affects-your-success


