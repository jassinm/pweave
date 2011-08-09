"""
This module defines a Matplotlib-figure processor class for use with pweave.

2011-01-14, Mark Edgington

"""
# this plugin module is only imported by pweave.py
import __main__ as pweave
CodeProcessor = pweave.CodeProcessor

from string import Template
import os
import matplotlib.pyplot as plt

class MatplotlibFigureProcessor(CodeProcessor):
    """Processor for generating (LaTeX) figures from matplotlib plots.

    Given a code-block containing sourcecode required to generate a matplotlib
    figure, a PDF file of this figure will be stored, and the LaTeX snippet
    required for including the image in a LaTeX figure will be generated.

    The following code-block options are accepted:

    *output_folder* -- specifies the folder (relative to the pweave source
                       file if not given as an absolute path) which should be
                       used for storing the generated image pdf files. This
                       folder will be created if it doesn't already exist. The
                       default folder is 'images'.

    *filename* -- specifies the basename of the pdf file which will be stored
                  in *output_folder*.  By default this will be "FigureNNN",
                  where NNN is some number.

    *width* -- specifies (in any valid LaTeX units) the image
               width.  The default is "0.9\linewidth".

    *height* -- specifies (in any valid LaTeX units) the image height
                If height is not specified, only width is used.

    *center* -- should the figure be centered? (true/false). Default=true

    *caption* -- the figure caption. (Defaults to "")

    *label* -- the name of the LaTeX label to use (if not provided, no label
               will be associated with the figure).

    *where* -- string indicating where to place the figure (default='h').

    TODO: other formatting options

    """
    def __init__(self, processors):
        super(MatplotlibFigureProcessor, self).__init__(processors)
        self.figure_number = 1 # counter used for autogenerating figure-names

    def name(self):
        return "mplfig"

    def default_block_options(self):
        "Return a dictionary containing the processor's default block-options."
        option_defaults = {
                            'output_folder': None, # to override global default
                            'filename': None,
                            'width': None,
                            'height': None,
                            'center': 'true',
                            'caption': '',
                            'label': None,
                            'where': 'h',
                            'echo': 'false',
                          }

        return option_defaults


    def output_template_str(self):
        return r'''
\begin{figure}[$where]
 $centering
 \includegraphics[$dimensions]{$imgfile_abspath}
 \caption{$caption}
 $label
\end{figure}
'''

    def get_image_abspath(self, outfolder):
        "Autogenerate and return an absolute image path."
        infile = self.settings['sourcefile_path']
        basename, infile_ext = os.path.splitext(infile)
        fname = basename + "_mpl_image_%03d.pdf" % self.figure_number
        imgpath = os.path.abspath(os.path.join(outfolder, fname))

        return imgpath


    def get_substitution_dict(self, codeblock_options):
        "populate variables for substitution"
        o = codeblock_options
        s = substitution_vars = {}

        for k in ['width', 'caption', 'where']:
            s[k] = o[k]


        #r'0.9\linewidth',
        dimensions = []
        heightset = (o['height'] is not None)
        widthset = (o['width'] is not None)

        if widthset:
            dimensions.append('width=' + o['width'])
        if heightset:
            dimensions.append('height=' + o['height'])
        if not widthset and not heightset:
            dimensions.append(r'width=0.9\linewidth')

        s['dimensions'] = ",".join(dimensions)

        if o['label'] is not None:
            s['label'] = r'\label{' + o['label'] + '}\n'
        else:
            s['label'] = ''

        if o['center'].lower() == 'true':
            s['centering'] = r'\centering'
        else:
            s['centering'] = ''

        if o['output_folder'] is not None:
            outfolder = os.path.join(self.settings['base_output_path'],
                                     o['output_folder'])
        else:
            # use globally set default output-image folder
            outfolder = self.settings['imgfolder_path']

        if o['filename'] is not None:
            s['imgfile_abspath'] = os.path.join(outfolder, o['filename'])
        else:
            # auto-generate filename
            s['imgfile_abspath'] = self.get_image_abspath(outfolder)

        s['imgfile_relpath'] = os.path.relpath(s['imgfile_abspath'],
                                               self.settings['base_output_path']
                                              )

        return substitution_vars

    def write_figure(self, filename):
        "Write (and clear) the matplotlib fig as a pdf to the specified file."
        plt.savefig(filename, dpi = 200)
        plt.clf()


    def process_code(self, codeblock, codeblock_options):
        substitution_vars = self.get_substitution_dict(codeblock_options)

        # execute the codeblock, storing results in self.execution_namespace
        self.exec_code(codeblock)

        capt = codeblock_options['caption']
        if capt in self.execution_namespace:
            caption = self.execution_namespace[capt]
            substitution_vars['caption'] = caption
        # a bit ugly... (passing info here via substitution_vars dict)
        self.write_figure(substitution_vars['imgfile_abspath'])

        document_text = \
            Template(self.output_template_str()).substitute(substitution_vars)

        # by default, don't echo the codeblock to the output document
        if codeblock_options['echo'].lower() == 'true':
            code_text = codeblock
        else:
            code_text = ''

        self.figure_number += 1

        return (document_text, code_text)
