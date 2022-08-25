from fileinput import filename
from multiprocessing import context
from typing import List
from django.http import HttpResponse
from django.utils import timezone
from django.utils.crypto import get_random_string

from django.template.loader import render_to_string
import logging
from django.http import HttpResponse
from urllib.parse import quote
from io import BytesIO

import xhtml2pdf.default
from xhtml2pdf import pisa
from urllib.parse import quote



class PDFGenerator:
    logger = logging.getLogger("app.pdf")
    logger_x2p = logging.getLogger("app.pdf.xhtml2pdf")

    def __init__(self, for_model,
                 fields: List, from_file: str,
                 to_file: str = "Employment-letter.pdf"):

        self.model = for_model
        self.template_name = from_file
        self.pdf_file = to_file
        self.fields = fields
        self.rendered_template = None
        self.context = {}

    def render_context_data(self):
        self.get_context_data()

        self.rendered_template = render_to_string(
            template_name=self.template_name,
            context=self.context)

    def get_context_data(self):
        for field in self.fields:
            if hasattr(self.model, field):
                attr = getattr(self.model, field)
                self.context[field] = attr

    def html_to_pdf(self, content, encoding="utf-8", link_callback=None, **kwargs):

        src = BytesIO(content.encode(encoding))
        dest = BytesIO()

        pdf = pisa.pisaDocument(src, dest, encoding=encoding, link_callback=link_callback, **kwargs)
        if pdf.err:
            self.logger.error("Error rendering PDF document")
            for entry in pdf.log:
                if entry[0] == xhtml2pdf.default.PML_ERROR:
                    self.logger_x2p.error("line %s, msg: %s, fragment: %s", entry[1], entry[2], entry[3])
            raise Exception("Errors rendering PDF", content=content, log=pdf.log)

        if pdf.warn:
            for entry in pdf.log:
                if entry[0] == xhtml2pdf.default.PML_WARNING:
                    self.logger_x2p.warning("line %s, msg: %s, fragment: %s", entry[1], entry[2], entry[3])

        return dest.getvalue()

    def encode_filename(self, filename):
        quoted = quote(filename)
        if quoted == filename:
            return "filename=%s" % filename
        else:
            return "filename*=UTF-8''%s" % quoted

    def FileResponse(self, content_type="application/pdf"):
        self.render_context_data()
        content = self.html_to_pdf(content=self.rendered_template)
        response = HttpResponse(content, content_type=content_type)
        if filename is not None:
            response["Content-Disposition"] = "attachment; %s" % self.encode_filename(self.pdf_file)
        return response
