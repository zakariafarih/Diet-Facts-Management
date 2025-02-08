# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class DietAllergen(models.Model):
    _name = 'diet.allergen'
    _description = "Food Allergen"

    name = fields.Char("Allergen Name", required=True)
    description = fields.Text("Description")

class ResPartner(models.Model):
    _inherit = 'res.partner'

    allergen_ids = fields.Many2many(
        'diet.allergen',
        'partner_allergen_rel',
        'partner_id',
        'allergen_id',
        string="Allergens"
    )

class MealTemplateInheritAllergen(models.Model):
    _inherit = 'meal.template'

    @api.onchange('item_ids')
    def _onchange_check_allergens(self):
        """
        Onchange to warn user if a meal item has an allergen
        that the user is allergic to.
        """
        for meal in self:
            if not meal.user_id or not meal.item_ids:
                continue
            # All allergens for the meal's user
            partner = meal.user_id.partner_id
            if not partner:
                continue
            user_allergens = partner.allergen_ids
            if not user_allergens:
                continue

            # Check each item
            for line in meal.item_ids:
                product_allergens = line.item_id.allergen_ids
                # intersection = raise a warning
                if user_allergens & product_allergens:
                    raise ValidationError(
                        "Warning: Meal '{}' contains allergens ({}) for user '{}'!".format(
                            meal.name,
                            ", ".join(a.name for a in (user_allergens & product_allergens)),
                            meal.user_id.name
                        )
                    )


class ProductTemplateInheritAllergen(models.Model):
    _inherit = 'product.template'

    allergen_ids = fields.Many2many(
        'diet.allergen',
        'product_allergen_rel',
        'product_id',
        'allergen_id',
        string="Allergens"
    )
