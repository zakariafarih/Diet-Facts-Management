# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class MealTemplate(models.Model):
    _name = 'meal.template'
    _description = "Meal"

    name = fields.Char("Meal Name", required=True)
    user_id = fields.Many2one('res.users', "Meal User", required=True)
    item_ids = fields.One2many('mealitem.template', 'meal_id', string="Meal Items")
    notes = fields.Text("Meal Notes")

    meal_type = fields.Selection([
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
    ], string="Meal Type", default='breakfast', required=True)

    meal_date = fields.Date("Meal Date", required=True)

    totalcalories = fields.Integer(
        string="Total Calories",
        compute="_compute_total_calories",
        store=True
    )
    largemeal = fields.Boolean("Large Meal", readonly=True)

    @api.depends('item_ids', 'item_ids.servings', 'item_ids.calories')
    def _compute_total_calories(self):
        for meal in self:
            total = sum(mi.servings * mi.calories for mi in meal.item_ids)
            meal.totalcalories = total
            meal.largemeal = total > 500

    @api.constrains('meal_date')
    def _check_meal_date_not_in_past(self):
        for record in self:
            if record.meal_date and record.meal_date < fields.Date.today():
                raise ValidationError("The meal date cannot be in the past!")
