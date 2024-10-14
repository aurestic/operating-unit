# Copyright 2024 Aures TIC - Almudena de La Puente <almudena@aurestic.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Operating Unit in Partners",
    "summary": "Adds the concept of operating unit (OU) in partners",
    "version": "16.0.1.0.1",
    "author": "Aures TIC, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/operating-unit",
    "category": "Partner Management",
    "depends": ["base", "operating_unit"],
    "license": "LGPL-3",
    "data": [
        "security/res_partner_security.xml",
        "views/res_partner_view.xml",
    ],
}
