# Django-HTML-template-to-PDF



So I built this multipurpose PdfGenerator that takes any model instance, a list of fields, an HTML template and optionally a pdf file name. It then generate a a pdf from the HTML templates and the Fields accessed in the templates. It then returns an HTTP FileResponse of the pdf generated.

There is this package [django-easy-pdf](https://github.com/nigma/django-easy-pdf) that is supported by django 1. To 2.. 

Took off some snippets from it, Joined it with mine, performed some abracadabra and we have a PDFGenerator class.

