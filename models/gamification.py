# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging
from datetime import datetime, timedelta

_logger = logging.getLogger(__name__)

class UserBadge(models.Model):
    _name = 'user.badge'
    _description = "Achievement Badge"

    name = fields.Char("Badge Name", required=True)
    user_id = fields.Many2one('res.users', "User", required=True)
    earned_date = fields.Date("Earned On", default=fields.Date.today())
    description = fields.Text("Description")

class GamificationTools(models.Model):
    _name = 'gamification.tools'
    _description = "Gamification Tools (Helper)"

    def cron_award_badges(self):
        _logger.info("Running Gamification Cron to award badges...")
        users = self.env['res.users'].search([])
        for user in users:
            # Check if the user has set dietary goals
            goal = self.env['dietary.goal'].search([('user_id', '=', user.id)], limit=1)
            if not goal:
                continue

            # 1) Award badge for 7 consecutive days of meal logging
            consecutive_days = self._check_consecutive_meals(user)
            if consecutive_days >= 7:
                existing_badge = self.env['user.badge'].search([
                    ('user_id', '=', user.id),
                    ('name', '=', '7-Day Streak')
                ], limit=1)
                if not existing_badge:
                    self.env['user.badge'].create({
                        'name': '7-Day Streak',
                        'user_id': user.id,
                        'description': 'Logged meals for 7 consecutive days!'
                    })

            # 2) Award hydration badge if water intake ≥ 2000 ml today
            water_intake_today = self.env['water.intake'].search([
                ('user_id', '=', user.id),
                ('date', '=', fields.Date.today())
            ])
            if sum(w.intake_ml for w in water_intake_today) >= 2000:
                existing_badge = self.env['user.badge'].search([
                    ('user_id', '=', user.id),
                    ('name', '=', 'Hydration Hero')
                ], limit=1)
                if not existing_badge:
                    self.env['user.badge'].create({
                        'name': 'Hydration Hero',
                        'user_id': user.id,
                        'description': 'Drank 2L of water today!'
                    })

    def _check_consecutive_meals(self, user):
        """Returns the number of consecutive days the user has logged at least one meal."""
        Meal = self.env['meal.template']
        day_count = 0
        today_str = fields.Date.today()
        # Convert the Odoo date (string or date) to a datetime.date object
        if isinstance(today_str, str):
            day_cursor = datetime.strptime(today_str, "%Y-%m-%d").date()
        else:
            day_cursor = today_str
        while True:
            meals_count = Meal.search_count([
                ('user_id', '=', user.id),
                ('meal_date', '=', day_cursor.strftime("%Y-%m-%d"))
            ])
            if meals_count > 0:
                day_count += 1
                day_cursor -= timedelta(days=1)
            else:
                break
        return day_count
