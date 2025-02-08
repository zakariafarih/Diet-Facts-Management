# -*- coding: utf-8 -*-
from odoo import models, fields

class MealItemTemplate(models.Model):
    _name = 'mealitem.template'
    _description = "Meal Item"

    meal_id = fields.Many2one('meal.template', "Meal", required=True, ondelete='cascade')
    item_id = fields.Many2one('product.template', "Item", required=True)
    servings = fields.Integer("Servings", default=1)
    calories = fields.Integer(
        string="Calories per Serving",
        related="item_id.calories",
        store=True,
        readonly=True
    )
    notes = fields.Text("Meal Item Notes")
