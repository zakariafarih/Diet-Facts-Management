# -*- coding: utf-8 -*-
from odoo import models, fields, api

class WaterIntake(models.Model):
    _name = 'water.intake'
    _description = "Daily Water Intake"

    user_id = fields.Many2one('res.users', string="User", required=True)
    date = fields.Date("Date", default=fields.Date.today(), required=True)
    intake_ml = fields.Integer("Water Intake (ml)")

    # computed field for total daily intake
    total_intake_ml = fields.Integer(
        string="Total Daily Intake (ml)",
        compute='_compute_total_intake_ml',
        store=False
    )

    @api.depends('user_id', 'date', 'intake_ml')
    def _compute_total_intake_ml(self):
        """
        For the same user & date, sum up all records.
        """
        for rec in self:
            same_day_intakes = self.search([
                ('user_id', '=', rec.user_id.id),
                ('date', '=', rec.date)
            ])
            rec.total_intake_ml = sum(r.intake_ml for r in same_day_intakes)
