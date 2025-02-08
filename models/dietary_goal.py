# -*- coding: utf-8 -*-
from odoo import models, fields, api

class DietaryGoal(models.Model):
    _name = 'dietary.goal'
    _description = "Daily Nutrient Goals"
    _rec_name = 'user_id'

    user_id = fields.Many2one('res.users', string="User", required=True)
    calorie_target = fields.Integer(string="Daily Calorie Target", default=2000)
    protein_target = fields.Float(string="Protein (g/day)")
    fat_target = fields.Float(string="Fat (g/day)")
    carbs_target = fields.Float(string="Carbohydrates (g/day)")

    def get_remaining_calories(self):
        """
        Return how many calories remain for the user today.
        We'll sum up today's meals from diet_facts_management.
        """
        self.ensure_one()
        Meal = self.env['meal.template']
        # All meals for this user today
        meals_today = Meal.search([
            ('user_id', '=', self.user_id.id),
            ('meal_date', '=', fields.Date.today())
        ])
        total_consumed = sum(meal.totalcalories for meal in meals_today)
        return self.calorie_target - total_consumed
