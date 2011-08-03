
Pweave Help
===========

.. index:: features

Features
________

`Pweave <http://mpastell.com/pweave>`_ is a literate programming tool for Python that is developed
after `Sweave <http://www.stat.uni-muenchen.de/~leisch/Sweave/>`_. And
like Sweave it uses the `noweb <http://www.cs.tufts.edu/~nr/noweb/>`_
syntax. Pweave is a single python script that is able to weave a
python code between “<<>>=” and “@” blocks and include the results in
the document. Pweave is good for creating dynamic reports and
tutorials. 

**With Pweave you can:**

* Execute python code in the blocks and capture input and ouput to a literate environment using  either `reStructuredText <http://docutils.sourceforge.net/rst.html>`_, `Sphinx <http://sphinx.pocoo.org>`_ or Latex markup. Using reST or Sphinx enables conversion of the documents to several formats (html, latex, pdf, odt).
* Use hidden code blocks, i.e. code is executed, but not printed in the output file.
* Capture matplotlib graphics.

.. index:: source document, output document

Document types
______________

.. describe:: Source document

   Contains a mixture of documentation and code chunks. Pweave will evaluate the code and leave the documentation chunks as they are. The documentation chunks can be written either with reST or Latex. The source document is processed using *Pweave*, which gives us the formatted output document.

.. describe:: Weaved document

   Is produced by Pweave from the source document. Contains the documentation, original code, the captured outputof the code and optionally captured `matplotlib <http://matplotlib.sourceforge.net/>`_ figures.

.. describe:: Source code

   Is produced by Pweave from the source document. Contains the source code extracted from the code chunks.    

.. index::  syntax, code chunk, documentation chunk

Pweave syntax
_____________
Pweave uses noweb syntax for defining the code chunks and documentation chunks, just like `Sweave <http://www.stat.uni-muenchen.de/~leisch/Sweave/>`_. 

.. describe:: Code chunk

   start with a line marked with <<>>= or <<option>>= and end with line marked with @. The code between the start and end markers is executed and the output is captured to the output document.

.. describe:: Documentation chunk

   Are the rest of the document (between @ and <<>>= lines) and can be written using either reST or Latex.

.. index:: options, figures

Code Chunk Options
__________________

Pweave currently has the following options for processing the code chunks.

.. envvar:: fig = True or (False)
   
   Whether a matplotlib plot produced by the code chunk should be included in the file. The figure will be added with '.. image::' directive in .rst and \\includegraphics tag in .tex documents. See the 'caption' option if you want to use figure environment.  

.. envvar:: width = '15 cm'
  
   The width of the used figure in reST or Sphinx document (using reST markup). Default is '15 cm', it can also be set in % like width = '80 %'. 

.. envvar:: echo = True or (False)

   Echo the python code in the output document. If False the source code will be hidden.

.. envvar:: evaluate = True or (False).

   Evaluate the code chunk. If False the chunk won't be executed.

.. envvar:: results = 'verbatim'

  The output format of the printed results. 'verbatim' for literal block, rst for reST output or 'tex' for latex output.

.. envvar:: caption = ''

   A string providing a caption for the figure produced in the code chunk. Can only be used with 'fig = True' option. If a caption is provided the figure will be added in the .rst document with the '.. figure::' directive and as a figure float in Latex.  

.. versionadded:: 0.12

.. envvar:: term = False or (True)

   If True the output emulates a terminal session i.e. the code chunk and the output will be printed as a  `doctest block <http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html#doctest-blocks>`_. Can also be used in latex documents, where the output will formatted as verbatim.

.. versionadded:: 0.12

Example
--------

A code chunk that saves and displays a 12 cm wide image and hides the source code:

::

 <<fig = True, width = '12 cm', echo = False>>=
 from pylab import *
 plot(arange(10))
 show()
 @

Weaving Pweave Documents
________________________

Weaving a Pweave source file produces too output files: .rst document or .tex document that contains the weaved code together with its evaluated output and .py file that contains the python code extracted from the document. All of the produced figures are placed in the 'images/' folder as a default.

**Pweave documents are weaved from the shell with the command:**

.. describe:: Pweave [options] sourcefile

Options:

.. program:: Pweave

.. cmdoption:: --version

   show the version number and exit

.. cmdoption:: -h, --help

   show help message and exit

.. cmdoption:: -f FORMAT, --format FORMAT

   The output format: 'sphinx' (default), 'rst' or 'tex'

.. cmdoption::  -m MPLOTLIB, --matplotlib=MPLOTLIB
   
   Do you want to use matplotlib true (default) or false

.. cmdoption::  -g FIGFMT, --figure-format=FIGFMT

   Figure format for matplolib graphics: Defaults to 'png' for rst and Sphinx html documents and 'pdf' for tex

.. cmdoption::  -d FIGDIR, --figure-directory=FIGDIR

   Directory path for matplolib graphics: Default                        'images/'


Example
--------

Weave a document with default options (Sphinx with png figures)

::

  $ Pweave ma.Pnw
  Output written to ma.rst
  Code extracted to ma.py

Weave a Latex document with png figures:

:: 

  Pweave -f tex -g png source.Pnw

Get options:

::

  Pweave --help

