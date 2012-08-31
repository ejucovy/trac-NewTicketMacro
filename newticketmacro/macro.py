# vim: expandtab
import re, time
from StringIO import StringIO

from genshi.builder import tag

from trac.core import *
from trac.ticket.api import TicketSystem
from trac.util import TracError
from trac.util.text import to_unicode
from trac.web.chrome import Chrome, add_stylesheet, ITemplateProvider
from trac.wiki.api import parse_args, IWikiMacroProvider
from trac.wiki.formatter import format_to_html, format_to_oneliner
from trac.wiki.macros import WikiMacroBase
from trac.wiki.model import WikiPage
from trac.wiki.web_ui import WikiModule

class NewTicketMacro(WikiMacroBase):
    """A macro to add scrippets to a page. Usage:
    """
    implements(IWikiMacroProvider,ITemplateProvider)

    defaults = (
        ('heading', None),
        ('subheading', None),
        ('summary_placeholder', 'Short summary of your problem'),
        ('summary_description', ('Describe your problem in more detail here. '
                                 'What were you doing when it happened? ' 
                                 'What did you expect would occur? '
                                 'What happened instead?')),
        ('container_class', ''),
        ('description_rows', '5'),
        ('form_fields', ''),
        ('hidden_fields', ''),
        )

    def expand_macro(self, formatter, name, content, args):
        data = parse_args(content)[1]
        if data.has_key("id"):
            data["form"] = "new-ticket-form-%s" % data["id"]
        else:
            data["form"] = "new-ticket-form"

        for default in self.defaults:
            data.setdefault(default[0], default[1])
        data['form_fields'] = [i.strip() for i in data['form_fields'].split()
                               if i.strip()]
        data['hidden_fields'] = [i.strip() for i in data['hidden_fields'].split()
                                 if i.strip()]
        
        _form_fields = []
        if len(data['form_fields']):
            fields = dict((i['name'], i) for i in TicketSystem(self.env).get_ticket_fields())
            for field in data['form_fields']:
                if '%s_placeholder' % field in data:
                    fields[field]['placeholder'] = data['%s_placeholder' % field]
                else:
                    fields[field]['placeholder'] = fields[field]['label']
                if field == 'owner':
                    TicketSystem(self.env).eventually_restrict_owner(fields[field])
                _form_fields.append(fields[field])
        data['form_fields'] = _form_fields

        if len(data['hidden_fields']):
            data['hidden_fields'] = [i.split("=") for i in data['hidden_fields']]

        self.log.debug("EXPAND ARGUMENTS: %s " % data)
        req = formatter.req
        template = Chrome(self.env).load_template('newticketmacro_form.html',method='xhtml')
        data = Chrome(self.env).populate_data(req, data)
        
        rendered_result = template.generate(**data)

        add_stylesheet(req, 'newticketmacro/form.css')

        return rendered_result
    
    # ITemplateProvider methods
    def get_templates_dirs(self):
        from pkg_resources import resource_filename
        return [resource_filename('newticketmacro', 'templates')]

    def get_htdocs_dirs(self):
        from pkg_resources import resource_filename
        return [('newticketmacro', resource_filename(__name__, 'htdocs'))] 

