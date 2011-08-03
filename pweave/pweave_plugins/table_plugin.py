"""
This module defines a TableProcessor class for use with pweave.

2011-01-11, Mark Edgington

"""
# this plugin module is only imported by pweave.py
import __main__ as pweave
CodeProcessor = pweave.CodeProcessor

from string import Template

class TableProcessor(CodeProcessor):
    """Processor for generating (LaTeX) tables.
    
    This processor generates a table from a nested-list.
    
    The following code-block options are accepted:
    
    *table_list_name* -- (optional) specifies the name of a nested list which
                         the code-block will create that contains the contents
                         of the table.  Each sublist in the list represents one
                         row of the table, and can contain either string or
                         numeric values.  By default, this option is set to
                         "table_rows". 
    
    *column_labels* -- (optional) specifies the name of a list which contains
                       the column labels. 
    
    *row_labels* -- (optional) specifies the name of a list which contains the
                    row labels.
    
    TODO: other formatting options
    
    """
    def name(self):
        return "table"
    
    def default_block_options(self):
        "Return a dictionary containing the processor's default block-options."
        option_defaults = {
                            'caption': '',
                            'center': 'true',
                            'table_list_name': 'tablerows',
                            'column_labels': None,
                            'row_labels': None,
                            'echo': 'false',
                          }
        
        return option_defaults


    def output_template_str(self):
        return r'''
\begin{table}
\caption{$caption}
\begin{center}
\begin{tabular}{$tabular_format}
\hline
$columnlabels

$rows
\hline
\end{tabular}
\end{center}
\end{table}
'''
    
    def col_label_str(self, col_labels):
        "Return LaTeX code for column labels"
        if len(col_labels) == 0:
            return ''

        bold_labels = [r'\textbf{' + str(label) + r'}' for label in col_labels]
        
        s = r' & '.join(bold_labels) + r'\\ \hline' + "\n"
        
        return s
    
    def rows_str(self, table_rows, row_labels=None):
        "Return LaTeX code for all rows"
        
        s = ''
        for i,row in enumerate(table_rows):
            latex_row_elems = [str(elem) for elem in row]
            if row_labels is not None:
                latex_row_elems.insert(0, r'\textbf{' + str(row_labels[i]) + r'}')
            
            s += r' & '.join(latex_row_elems) + r'\\' + "\n"
        
        s += r'\hline' + "\n"
        
        return s
    
    def tabular_format_str(self, table_rows, row_labels=None):
        "Return LaTeX 'tabular' environment format string"
 
        row_length = len(table_rows[0])
        if row_labels is not None:
            row_length += 1
        
        #TODO: don't hardcode to all 'c' elems
        format_elems = ['c'] * row_length
        
        s = "|" + "|".join(format_elems) + "|"
        
        return s
        #return "|l | c |"
        
    
    def process_code(self, codeblock, codeblock_options):
        substitution_vars = {}

        # execute the codeblock, storing results in self.execution_namespace
        self.exec_code(codeblock)
        # extract object from exec_code()'s namespace:
        table_rows = self.execution_namespace['tablerows']
        
        if codeblock_options['column_labels'] is not None:
            col_labels = self.execution_namespace[codeblock_options['column_labels']]
            substitution_vars['columnlabels'] = self.col_label_str(col_labels)
        else:
            substitution_vars['columnlabels'] = ''
        
        if codeblock_options['row_labels'] is not None:
            row_labels = self.execution_namespace[codeblock_options['row_labels']]
        else:
            row_labels = None
        
        substitution_vars['rows'] = self.rows_str(table_rows, row_labels)
        substitution_vars['tabular_format'] = self.tabular_format_str(table_rows, row_labels)
        substitution_vars['caption'] = codeblock_options['caption']

        document_text = \
            Template(self.output_template_str()).substitute(substitution_vars)
        
        # by default, don't echo the codeblock to the output document
        if codeblock_options['echo'].lower() == 'true':
            code_text = codeblock
        else:
            code_text = ''
        
        return (document_text, code_text)
