# Copyright 2024 Aures TIC - Almudena de La Puente <almudena@aurestic.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.tests import common


class TestPartnerOperatingUnit(common.TransactionCase):
    def setUp(self):
        super().setUp()
        self.ResUsers = self.env["res.users"]
        self.ResPartner = self.env["res.partner"]
        # company
        self.company = self.env.ref("base.main_company")
        # group
        self.group_user = self.env.ref("base.group_user")
        # Main Operating Unit
        self.ou1 = self.env.ref("operating_unit.main_operating_unit")
        # B2B Operating Unit
        self.b2b = self.env.ref("operating_unit.b2b_operating_unit")
        # Partners
        self.partner1 = self.ResPartner.create({"name": "Partner 1 test"})
        self.partner2 = self.ResPartner.create({"name": "Partner 2 test"})
        self.partner3 = self.ResPartner.create({"name": "Partner 3 test"})
        # Create users
        self.user1_id = self._create_user(
            "user_1", [self.group_user], self.company, [self.ou1, self.b2b]
        )
        self.user2_id = self._create_user(
            "user_2", [self.group_user], self.company, [self.b2b]
        )
        self.partner1.operating_unit_ids = [(6, 0, [self.ou1.id])]
        self.partner2.operating_unit_ids = [(6, 0, [self.b2b.id])]
        self.partner3.operating_unit_ids = [(6, 0, [self.ou1.id, self.b2b.id])]

    def _create_user(self, login, groups, company, operating_units):
        """Create a user."""
        group_ids = [group.id for group in groups]
        user = self.ResUsers.with_context(no_reset_password=True).create(
            {
                "name": "Test User",
                "login": login,
                "password": "test",
                "email": "testuser@yourcompany.com",
                "company_id": company.id,
                "company_ids": [(4, company.id)],
                "operating_unit_ids": [(4, ou.id) for ou in operating_units],
                "groups_id": [(6, 0, group_ids)],
            }
        )
        return user.id

    def test_partner_ou_security(self):
        """Test Security of Partner Operating Unit"""

        # User 1 is only assigned to Operating Unit 1, and can see all
        # partners having Operating Unit 1.
        ou_domain = [("operating_unit_ids", "in", self.ou1.id)]
        partners = self.ResPartner.with_user(self.user1_id).search(ou_domain)
        self.assertIn(self.partner1, partners)
        self.assertIn(self.partner3, partners)
        self.assertNotIn(self.partner2, partners)

        # User 2 is only assigned to Operating Unit 2, so can see partners
        # having Operating Unit b2b
        partners = self.ResPartner.with_user(self.user2_id).search(ou_domain)
        self.assertIn(self.partner3, partners)

        b2b_domain = [("operating_unit_ids", "in", self.b2b.id)]
        partners = self.ResPartner.with_user(self.user2_id).search(b2b_domain)
        self.assertIn(self.partner2, partners)
        self.assertNotIn(self.partner1, partners)
