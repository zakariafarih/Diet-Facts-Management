# -*- coding: utf-8 -*-
from odoo import fields, models

class NutrientTemplate(models.Model):
    _name = 'nutrient.template'
    _description = "Nutrient"

    name = fields.Char("Nutrient Name", required=True)
    uom_id = fields.Many2one("uom.uom", string="Unit of Measure")
    description = fields.Text("Description")
