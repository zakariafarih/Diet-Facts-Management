# -*- coding: utf-8 -*-
import requests
from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    calories = fields.Integer(string="Calories (per 100g)")
    servingsize = fields.Float(string="Serving Size (g)", help="Default serving size in grams.")
    nutrition_ids = fields.One2many('nutritionfact.template', 'product_id', string="Nutrition Facts")

    nutritionscore = fields.Float(string="Nutrition Score",
                                  compute='_compute_nutrition_score',
                                  store=True)
    is_nutrition_incomplete = fields.Boolean(string="Nutrition Incomplete",
                                             compute="_compute_is_incomplete",
                                             store=True)
    nutri_score_letter = fields.Char(string="Nutri-Score Letter",
                                     compute="_compute_nutri_letter",
                                     store=True)

    @api.model_create_multi
    def create(self, vals_list):
        products = super().create(vals_list)
        all_nutrients = self.env['nutrient.template'].search([])
        for product in products:
            for nutr in all_nutrients:
                existing_fact = self.env['nutritionfact.template'].search([
                    ('product_id', '=', product.id),
                    ('nutrient_id', '=', nutr.id)
                ], limit=1)
                if not existing_fact:
                    self.env['nutritionfact.template'].create({
                        'nutrient_id': nutr.id,
                        'product_id': product.id,
                        'value': 0.0,
                        'dailypercent': 0.0,
                    })
        return products

    def open_recipe_suggestion(self):
        """Open the recipe suggestion wizard for the current product."""
        self.ensure_one()  # Ensure we're working with a single product

        # Ensure the wizard exists correctly
        wizard = self.env['recipe.suggestion.wizard'].sudo().create_wizard(self.id)

        return {
            'name': 'Recipe Suggestions',
            'type': 'ir.actions.act_window',
            'res_model': 'recipe.suggestion.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('diet_facts_management.view_recipe_suggestion_wizard').id,
            'res_id': wizard,
            'target': 'new',
        }

    @api.depends('nutrition_ids', 'nutrition_ids.value')
    def _compute_nutrition_score(self):
        for product in self:
            score = 0.0
            for fact in product.nutrition_ids:
                if not fact.nutrient_id:
                    continue
                name_lower = fact.nutrient_id.name.lower()
                val = fact.value
                if 'protein' in name_lower:
                    score += val * 2
                elif 'fiber' in name_lower:
                    score += val
                elif 'carbohydrates' in name_lower:
                    score += val * 0.1
                elif 'sugar' in name_lower:
                    score -= val
                elif 'fat' in name_lower and 'saturated' not in name_lower:
                    score += val * 0.1
                elif 'saturated fat' in name_lower:
                    score -= val * 1.5
                elif 'cholesterol' in name_lower:
                    score -= val * 10
                elif 'sodium' in name_lower or 'salt' in name_lower:
                    score -= val * 2
            product.nutritionscore = score

    @api.depends('nutrition_ids', 'nutrition_ids.value')
    def _compute_is_incomplete(self):
        for product in self:
            product.is_nutrition_incomplete = any(fact.value == 0.0 for fact in product.nutrition_ids)

    @api.depends('nutritionscore')
    def _compute_nutri_letter(self):
        for product in self:
            score = product.nutritionscore
            if score >= 20:
                letter = 'A'
            elif score >= 10:
                letter = 'B'
            elif score >= 0:
                letter = 'C'
            elif score >= -10:
                letter = 'D'
            else:
                letter = 'E'
            product.nutri_score_letter = letter

    def get_calories_for_serving(self):
        self.ensure_one()
        if self.servingsize and self.calories:
            return self.calories * (self.servingsize / 100.0)
        return 0.0

class ProductTemplateInheritBarcode(models.Model):
    _inherit = 'product.template'

    barcode = fields.Char(string="Barcode")
    available_in_kitchen = fields.Boolean("Available at Home", default=False)

    def action_fetch_from_barcode(self):
        self.ensure_one()
        if not self.barcode:
            raise UserError("No barcode set on this product.")

        url = f"https://world.openfoodfacts.org/api/v0/product/{self.barcode}.json"
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            raise UserError(f"Error calling OpenFoodFacts: {str(e)}")

        status = data.get('status', 0)
        product_data = data.get('product', {})
        if status == 1 and product_data:
            nutriments = product_data.get('nutriments', {})
            calories_val = nutriments.get('energy-kcal_100g') or nutriments.get('energy-kcal_value', 0)
            self.calories = calories_val or 0
        else:
            raise UserError("Barcode not found in Open Food Facts database.")
