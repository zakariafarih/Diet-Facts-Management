# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class MealSchedule(models.Model):
    _name = 'meal.schedule'
    _description = "Weekly Meal Schedule"

    name = fields.Char("Schedule Name", required=True, default="Weekly Plan")
    user_id = fields.Many2one('res.users', string="User", required=True)
    meal_ids = fields.One2many('meal.template', 'meal_schedule_id', string="Meals in this Schedule")
    start_date = fields.Date("Start Date")
    end_date = fields.Date("End Date")

    @api.constrains('start_date', 'end_date')
    def _check_date_range(self):
        for schedule in self:
            if schedule.start_date and schedule.end_date and schedule.end_date < schedule.start_date:
                raise ValidationError("The end date cannot be before the start date.")

class MealTemplate(models.Model):
    _inherit = 'meal.template'
    meal_schedule_id = fields.Many2one('meal.schedule', string="Meal Schedule")
