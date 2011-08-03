"""
This module defines a HelloWorld class for use with pweave.  It serves as a
simple example of how to write a processor.  To use the processor, run pweave
on a file that looks like the following::
    
    Well, friends, can you guess what the following block will be
    replaced by?
    
    <<p=helloworld>>=
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec iaculis
    augue ut augue porttitor nec molestie nibh congue. Aliquam erat volutpat.
    Suspendisse urna tortor, tristique et elementum scelerisque, posuere sed
    dolor. Fusce in facilisis odio. Vivamus ut ornare arcu. Sed.
    @
    
    The End.

Now, eagerly open up the generated files, and be filled with glee.

"""
# this plugin module is only imported by pweave.py

# The following two lines are required.
import __main__ as pweave
CodeProcessor = pweave.CodeProcessor


class HelloWorldProcessor(CodeProcessor):
    """Processor example which can be used as a template.
    
    This processor "converts" (replaces) all of the text in the code-block to "Hello
    World!", and also generates python output containing "print 'Hello
    World!'".
    
    Exciting, isn't it?
    
    The following code-block options are accepted:
    
    *hello_text* -- (optional) specifies what text should replace the
                    code-block. Defaults to "Hello World!"
    
    
    """
    def __init__(self, processors):
        # If you need to initialize your processor, *first* call the __init__()
        # method of the parent class:
        super(HelloWorldProcessor, self).__init__(processors)
        #
        # add any additional initialization needed by the processor here.
        #
    
    def name(self):
        return "helloworld"
    
    def default_block_options(self):
        "Return a dictionary containing the processor's default block-options."
        option_defaults = {
                            'hello_text': 'Hello World!',
                          }
        
        return option_defaults
    
    def process_code(self, codeblock, codeblock_options):
        document_text = codeblock_options['hello_text']
        code_text = "print '%s'" % codeblock_options['hello_text']
        
        return (document_text, code_text)
