.. Pweave - literate programming with Python documentation master file, created by
   sphinx-quickstart on Thu Mar  4 14:50:07 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. warning:: This documentation is out-of-date.  It is in the process of being
          updated, and was originally based on the version of pweave available
          at `<http://mpastell.com/pweave>`_.  The actual version of pweave
          which you have, however, has been significantly refactored, and
          extended in its functionality and flexibility with respect to the
          original version.  The newer version is available at
          `<http://bitbucket.org/edgimar/pweave/src>`_.  For a short up-to-date
          description of this version, see the :ref:`README <README>` file in the
          repository's root folder.

Welcome
------------
Pweave is a literate programming tool for Python that is developed after `Sweave <http://www.stat.uni-muenchen.de/~leisch/Sweave/>`_. And like Sweave it uses the `noweb <http://www.cs.tufts.edu/~nr/noweb/>`_ syntax. Pweave is a single python script that is able to weave a python code between “<<>>=” and “@” blocks and include the results in the document. Pweave is good for creating dynamic reports and tutorials. This documentation has been created using `Sphinx <http://sphinx.pocoo.org>`_.

Features
__________

* **Execute python code** in the chunks and **capture input and ouput** to a literate environment using  either `reStructuredText <http://docutils.sourceforge.net/rst.html>`_ or Latex source. Using reST enables conversion of the documents to several formats (html, latex, pdf, odt).
* **Use hidden code blocks**, i.e. code is executed, but not printed in the output file.
* **Capture matplotlib graphics**.


Download
_________
You can checkout the latest version of the code with mercurial:

::
 
 hg clone https://bitbucket.org/edgimar/pweave

Install
_____________
To install **pweave** simply copy (or symlink to) the "pweave.py" file in a directory in your path, and make it executable e.g. using:

::

 cp pweave.py /usr/local/bin/pweave
 chmod a+xr /usr/local/bin/pweave

Secondly, copy the files in `pweave_plugins` into `$HOME/.pweave_plugins`, or
create a symbolic link::

 ln -s pweave_plugins $HOME/.pweave_plugins 

Get started
______________

.. Browse the `Pweave help <usage.html>`_ to get you started!

**The up-to-date README contents:**

.. toctree::
    
    README
    
**The old (still being updated) documentation:**

.. toctree::
    
    docs
