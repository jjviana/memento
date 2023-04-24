import string
import os
class IncludeTemplate(string.Template):
    # A subclass of string.Template that supports including other templates
    # using the syntax ${include:filename}
    idpattern = r'(?a:[_a-z][_a-z0-9:.]*)'
    
    def __init__(self, template):
        # Initialize the template with the given string
        super().__init__(template)
        # Find the directory of this script
        self.TEMPLATE_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.TEMPLATE_BASE_DIR=os.path.join(self.TEMPLATE_BASE_DIR,"templates")

    def substitute(self, mapping=None, **kwargs):
    
        # Override the substitute method to handle include directives
        if mapping is None:
            mapping = kwargs
        else:
            mapping = dict(mapping, **kwargs)
        # Loop through all the placeholders in the template
        matches = self.pattern.findall(self.template)
        for _, _, name, _ in matches:
            # If the name starts with "include:", treat it as an include directive
            if name.startswith("include:"):
                # Get the filename from the name
                filename = name[len("include:"):]
                # Read the file and create a new template from it
                with open(os.path.join(self.TEMPLATE_BASE_DIR, filename)) as f:
                    included_template = IncludeTemplate(f.read())
                # Substitute the included template with the same mapping
                included_content = included_template.substitute(mapping)
                # Replace the placeholder with the included content
                self.template = self.template.replace("${" + name + "}", included_content)
        # Call the original substitute method on the modified template
        return super().substitute(mapping)
