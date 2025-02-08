from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class NutritionFactTemplate(models.Model):
    _name = "nutritionfact.template"
    _description = "Nutrition Fact"

    nutrient_id = fields.Many2one('nutrient.template', string="Nutrient", required=True)
    product_id = fields.Many2one('product.template', string="Product", ondelete='cascade')
    value = fields.Float('Nutrient Value', default=0.0)
    dailypercent = fields.Float("Daily %", default=0.0)
    uom = fields.Char(string="Unit of Measure", compute='_compute_uom', store=True)

    @api.depends('nutrient_id')
    def _compute_uom(self):
        for rec in self:
            rec.uom = rec.nutrient_id.uom_id.name if rec.nutrient_id.uom_id else ''

    def action_print_report(self):
        """Generate URL to download the nutrition facts report."""
        self.ensure_one()
        if not self.product_id:
            return False

        return {
            'type': 'ir.actions.act_url',
            'url': f'/nutrition/facts/{self.product_id.id}/pdf',
            'target': 'new',
        }