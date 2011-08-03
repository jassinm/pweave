"""
This module defines the LegacyDefaultProcessor class for use with pweave.

2011-02-11, Mark Edgington

"""
# this plugin module is only imported by pweave.py
import __main__ as pweave
CodeProcessor = pweave.CodeProcessor

import os
import StringIO
import matplotlib.pyplot as plt

#TODO: make more general (e.g. not specific to LaTeX) -- just a "put x before
#      and y after" plugin.


class LegacyDefaultProcessor(CodeProcessor):
    """Processor which maintains pweave stable release backward compatibility.
    
    The "default" processor included with the stable version of pweave performs
    a couple different functions, including code-evaluation and inclusion in the
    output document, as well as graphics capturing and inclusion.
    
    The following code-block options are accepted:
    
    Code Evaulation and Display
    ---------------------------
    
    *echo* -- Echo the code chunk contents in the output document. If False the
              source code will be hidden.  Default is True.
            
    *evaluate* -- Evaluate the code chunk. If False the chunk won't be
                  executed.  Default is True.
                
    *results* -- The output format of the evaluated-code results. 'verbatim'
                 for literal block, rst for reST output or 'tex' for latex
                 output.  Default is 'verbatim'.
                
    *term* -- If True the output emulates a terminal session i.e. the code
              chunk and the output will be printed as a doctest block. Can also
              be used in latex documents, where the output will formatted as
              verbatim.
            

    Figure Generation
    -----------------
                
    *fig* -- Whether a matplotlib plot produced by the code chunk should be
             included in the file. The figure will be added with the 
             ".. image::" directive in .rst documents, and the \includegraphics
             command in .tex documents. See the 'caption' option if you want to
             use a figure environment.  Default is False.
            
    *width* -- The width of the used figure in reST or Sphinx document (using
               reST markup). It can be set in % like '80 %', or using units
               like cm.  Default is '15 cm'.
            
    *caption* -- A string providing a caption for the figure produced in the
                 code chunk. Can only be used with 'fig = True' option. If a
                 caption is provided the figure will be added in the .rst
                 document with the '..  figure::' directive and as a figure
                 float in Latex.
    
    """
    def __init__(self, all_processors):
        super(LegacyDefaultProcessor, self).__init__(all_processors)
        self.nfig = 1
    
    def name(self):
        "Return a string representing the name of this code-processor"
        return 'legacydefault'

    def default_block_options(self):
        "Return a dictionary containing the processor's default block-options."
        option_defaults = {
                           "echo": 'True',
                           "results": 'verbatim',
                           "fig": 'False',
                           "evaluate": 'True',
                           "width": '15 cm',
                           "caption": '',
                           "term": 'False',
                          }
        
        return option_defaults

    def process_code(self, codeblock, codeblock_options):
        outbuf = StringIO.StringIO() # temporary file obj for storing text
        blockoptions = codeblock_options
        
        # Format specific options for tex or rst
        if self.settings['format'] == 'tex':
            codestart = '\\begin{verbatim}\n' 
            codeend = '\\end{verbatim}\n'
            outputstart = '\\begin{verbatim}\n'
            outputend = '\\end{verbatim}\n' 
            codeindent = ''
        elif self.settings['format'] == 'rst':
            codestart = '::\n\n' 
            codeend = '\n\n'
            outputstart = '::\n\n' 
            outputend = '\n\n' 
            codeindent = '  '
        elif self.settings['format'] == 'sphinx':
            codestart = '::\n\n' 
            codeend = '\n\n'
            outputstart = '::\n\n' 
            outputend = '\n\n' 
            codeindent = '  '
        
        #Output in doctests mode
        #print dtmode
        if blockoptions['term'].lower() == 'true':
            outbuf.write('\n')
            if self.settings['format']=="tex": outbuf.write(codestart)
            
            for x in codeblock.splitlines():
                outbuf.write('>>> ' + x + '\n')
                result = self.exec_code(x)
                if len(result) > 0:
                    outbuf.write(result)
            
            outbuf.write(codeend)
        else:
            result = ''
            #include source in output file?
            if blockoptions['echo'].lower() == 'true':
                outbuf.write(codestart)
                for x in codeblock.splitlines():
                    outbuf.write(codeindent + x + '\n')
                outbuf.write(codeend)

            #evaluate code and include results in output file?
            if blockoptions['evaluate'].lower() == 'true':
                if blockoptions['fig'].lower() == 'true':
                    #A placeholder for figure options
                    #import matplotlib
                    #matplotlib.rcParams['figure.figsize'] = (6, 4.5)
                    pass
                
                result = self.exec_code(codeblock).splitlines()
        
            #If we get results they are printed
            if len(result) > 0:
                indent = codeindent # default indentation
                
                if blockoptions['results'] == "verbatim":
                    outbuf.write(outputstart)
                elif blockoptions['results'] in ['rst', 'tex']:
                    indent = ''
                
                for x in result:
                    outbuf.write(indent + x + '\n')
                outbuf.write('\n')
                
                if blockoptions['results'] == "verbatim":
                    outbuf.write(outputend)
        
        #Save and include a figure?
        if blockoptions['fig'].lower() == 'true':
            figname = os.path.join(self.settings['imgfolder_path'],'Fig' +str(self.nfig) \
                    + self.settings['img_format'])
            plt.savefig(figname, dpi = 200)
            
            #TODO: why can't we just set 'img_format' for sphinx like we do for
            #      tex and rst?
            if self.settings['format'] == 'sphinx':
                figname2_base = os.path.join(self.settings['imgfolder_path'], 'Fig' + str(self.nfig)) 
                figname2 = figname2_base + self.settings['sphinxteximg_format']
                figname2_base_rel = \
                    os.path.relpath(figname2_base, self.settings['base_output_path'])
                plt.savefig(figname2)
            plt.clf()
            if self.settings['format'] == 'rst':
                if blockoptions['caption']:
                    #If the image has a caption, use Figure directive
                    outbuf.write('.. figure:: ' + figname + '\n')
                    outbuf.write('   :width: ' + blockoptions['width'] + '\n\n')
                    outbuf.write('   ' + blockoptions['caption'] + '\n\n')
                else:
                    outbuf.write('.. image:: ' + figname + '\n')
                    outbuf.write('   :width: ' + blockoptions['width'] + '\n\n')
            elif self.settings['format'] == 'sphinx':
                if blockoptions['caption']:
                    outbuf.write('.. figure:: ' + figname2_base_rel + '.*\n')
                    outbuf.write('   :width: ' + blockoptions['width'] + '\n\n')
                    outbuf.write('   ' + blockoptions['caption'] + '\n\n')
                else:
                    outbuf.write('.. image:: ' + figname2_base_rel + '.*\n')
                    outbuf.write('   :width: ' + blockoptions['width'] + '\n\n')
            elif self.settings['format'] == 'tex':
                if blockoptions['caption']:
                    outbuf.write('\\begin{figure}\n')
                    outbuf.write('\\includegraphics{'+ figname + '}\n')
                    outbuf.write('\\caption{' + blockoptions['caption'] + '}\n')
                    outbuf.write('\\end{figure}\n')
                else:
                    outbuf.write('\\includegraphics{'+ figname + '}\n\n')

            self.nfig += 1
        
        document_text = outbuf.getvalue()
        outbuf.close()
        
        return (document_text, codeblock) # document_text, code_text
