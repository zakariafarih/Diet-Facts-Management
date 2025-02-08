from odoo import http
from odoo.http import request, content_disposition
from odoo.addons.portal.controllers.portal import CustomerPortal

class NutritionFactsController(CustomerPortal):

    @http.route(['/nutrition/facts/<int:product_id>/pdf'], type='http', auth="user")
    def download_nutrition_facts(self, product_id, **kw):
        """Download nutrition facts PDF report."""
        try:
            # Get the product
            product = request.env['product.template'].sudo().browse(product_id)
            if not product.exists():
                return request.not_found()

            # Generate PDF
            pdf, _ = request.env['ir.actions.report'].sudo()._render_qweb_pdf(
                'diet_facts_management.report_nutrition_facts',
                [product_id]
            )

            # Create response
            pdfhttpheaders = [
                ('Content-Type', 'application/pdf'),
                ('Content-Length', len(pdf)),
                ('Content-Disposition', f'attachment; filename="{product.name}_nutrition_facts.pdf"'),
            ]
            return request.make_response(pdf, headers=pdfhttpheaders)

        except Exception as e:
            return request.not_found()