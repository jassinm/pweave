
.. index:: LaTeX example

LaTeX example
-------------

`Here <_static/ma.pdf>`_ is a simple example of a Pweave file (`ma.tex_pweave <_static/ma.tex_pweave>`_) that uses LaTeX as the documentation markup. The file demonstrates basic usage of Pweave and how it can easily be used to add dynamic figures and tables. 

.. literalinclude:: ma.tex_pweave

The file was processed with Pweave using:

:: 

  Pweave -f tex ma.tex_pweave

And as result we get the LaTex document `ma.tex <_static/ma.tex>`_ (shown below).  

.. literalinclude:: ma.tex


Processing the example with pdflatex produces `this pdf <_static/ma.pdf>`_
