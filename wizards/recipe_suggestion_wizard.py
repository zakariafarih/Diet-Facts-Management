# -*- coding: utf-8 -*-
from odoo import models, fields, api


class RecipeSuggestionWizard(models.TransientModel):
    _name = 'recipe.suggestion.wizard'
    _description = "Recipe Suggestion Wizard"

    product_id = fields.Many2one('product.template', string="Primary Ingredient", required=True)
    suggested_meal_ids = fields.Many2many('meal.template', string="Suggested Meals", readonly=True)

    @api.model
    def generate_suggestions(self, product_id):
        if not product_id:
            return []
        product = self.env['product.template'].browse(product_id)
        if not product.exists():
            return []

        meal_items = self.env['mealitem.template'].search([('item_id', '=', product.id)])
        suggested_meals = meal_items.mapped('meal_id')

        return suggested_meals.ids

    @api.model
    def create_wizard(self, product_id):
        """Create a wizard instance with suggested meals."""
        meal_ids = self.generate_suggestions(product_id)
        wizard = self.create({
            'product_id': product_id,
            'suggested_meal_ids': [(6, 0, meal_ids)]
        })
        return wizard

    def action_open_meals(self):
        """Open meal records from the wizard"""
        self.ensure_one()

        return {
            'name': "Suggested Meals",
            'type': 'ir.actions.act_window',
            'res_model': 'meal.template',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.suggested_meal_ids.ids)],
            'target': 'current',
        }