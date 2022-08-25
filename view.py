lass EmploymentLetterView(View):

    def get(self, request, u_id):
        staff = get_object_or_404(Staff, u_id=u_id)
        fields = ["get_full_name", "adress", "pay_interval", "pay_rate", "position", "office_ext", "employed_on",
                  "manager"]
        template_name = "flatpages/employment-letter.html",
        pdf_file = PDFGenerator(staff, fields=fields, from_file=template_name)
        return pdf_file.FileResponse()
