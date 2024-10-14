# Copyright 2024 Aures TIC - Almudena de La Puente <almudena@aurestic.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def _default_operating_unit_ids(self):
        default_ou = self.env["res.users"].operating_unit_default_get(self.env.uid)
        if default_ou:
            return [
                (
                    6,
                    0,
                    default_ou.ids,
                )
            ]

    operating_unit_ids = fields.Many2many(
        "operating.unit",
        "partner_operating_unit_rel",
        string="Operating Units",
        default=_default_operating_unit_ids,
    )
