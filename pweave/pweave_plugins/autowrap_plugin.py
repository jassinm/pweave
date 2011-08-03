"""
This module defines the AutoWrapProcessor class for use with pweave.

2011-01-28, Mark Edgington

"""
# this plugin module is only imported by pweave.py
import __main__ as pweave
CodeProcessor = pweave.CodeProcessor

from string import Template
import re
import sys

#TODO: make more general (e.g. not specific to LaTeX) -- just a "put x before
#      and y after" plugin.

class AutoWrapProcessor(CodeProcessor):
    """Processor to automatically wrap different items with a LaTeX command.
    
    This processor takes a list of commands and for each command, a
    corresponding set of text-fragments.  The code-block is searched for these
    fragments, and when they are encountered, they are replaced by a 'wrapped'
    version of the fragment, where the command surrounds the fragment (e.g.
    "\mathbf{<string>}" could replace <string>). 
    
    Beware of defining conflicting (overlapping) text-fragments, since if a
    part of the code-block matches more than one text-fragment, the behavior
    may not be as you expect it. 
    
    The following code-block options are accepted:
    
    *<cmdname>_wrapped* -- any option having this form (e.g. "textbf_wrapped")
                           will be interpreted as a list of text-fragments that
                           should be wrapped with the specified command.
                           The list has the form "<fragment0>#<fragment1>...".
    
    *list_delimiter* -- (optional) specifies what character is used to delimit
                        the text-fragment lists.  The default value is '#'.
                        
    *escape_delimiter* -- (optional) specifies a *two-character sequence* to
                          be used to escape text in the codeblock.  If text in
                          the codeblock is preceeded by these two characters,
                          the text will *NOT* be substituted, and the two
                          characters will be removed from the passed-through
                          text.  The default value is '!!'.  Note, that the
                          two-character requirement is due to a limitation
                          imposed by using a negative lookbehind in a regular
                          expression pattern.
    
    """
    def name(self):
        return "autowrap"
    
    def default_block_options(self):
        "Return a dictionary containing the processor's default block-options."
        option_defaults = {
                            'list_delimiter': '#',
                            'escape_delimiter': '!!',
                          }
        
        return option_defaults

    def process_code(self, codeblock, codeblock_options):
        # build a dictionary of 'frag':'command' mappings
        fragment_dict = {}
        for k,v in codeblock_options.iteritems():
            if k.endswith("_wrapped"):
                cmd = k[0:-8] # chop off '_wrapped'
                for frag in v.split(codeblock_options['list_delimiter']):
                    fragment_dict[frag] = cmd
        
        substitution_vars = {}
        # build substitution dictionary (allows for more general substitutions
        # in the future), at the same time replacing fragments with a 
        # substitution-variable.
        
        esc = codeblock_options['escape_delimiter']

        i=0
        placeholder_root = "autowrap_"
        placeholder_tmp_root = esc + esc.join(list(placeholder_root)) + esc 
        for frag,cmd in fragment_dict.iteritems():
            repl_str = '\\' + cmd + '{' + frag + '}'
            placeholder = placeholder_root + str(i)
            
            # temp-placeholder needed to prevent substituting parts of the
            # placeholders during the substitution loop.
            placeholder_tmp = placeholder_tmp_root + str(i)
            
            substitution_vars[placeholder] = repl_str
            
            escapedfrag = re.escape(frag)
            # only replace when frag is not immediately preceded by '!!' or '${'.
            # uses a "negative lookbehind" assertion: (?<!....)
            pattern = r'(?<!\$\{|'+re.escape(esc)+')' + escapedfrag
            codeblock = re.sub(pattern, r'${' + placeholder_tmp + r'}', codeblock)
            
            i += 1
            
        # now all autowrap comamnd substitutions are finished -- replace
        # escaped placeholders with 'legal' placeholders so Template()
        # likes the placeholder names.
        codeblock = codeblock.replace(placeholder_tmp_root, placeholder_root)
            
        # loop once more, this time removing '!!' preceeding fragments
        for frag,cmd in fragment_dict.iteritems():
            pattern = re.escape(esc) + re.escape(frag)
            codeblock = re.sub(pattern, re.escape(frag), codeblock) 
        
        # add any additional items to substitution_vars dict here...
        
        # perform substitutions
        try:
            document_text = \
                Template(codeblock).substitute(substitution_vars)
        except ValueError, e:
            print e, ':'
            print codeblock
            sys.exit(1)
        
        code_text = ''
        
        return (document_text, code_text)
