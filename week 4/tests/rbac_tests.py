import unittest
import sys
import os

# Set paths
base_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(base_dir, '..', 'src')
config_path = os.path.join(base_dir, '..', 'config')
sys.path.append(src_path)

from rbac_filter import RBACFilter

class TestRBAC(unittest.TestCase):
    def setUp(self):
        self.rbac = RBACFilter()
        self.sample_data = [
            {"id": "fin1", "metadata": {"department": "Finance"}},
            {"id": "hr1", "metadata": {"department": "HR"}},
            {"id": "gen1", "metadata": {"department": "General"}},
            {"id": "eng1", "metadata": {"department": "Engineering"}},
            {"id": "mkt1", "metadata": {"department": "Marketing"}}
        ]

    def test_finance_access(self):
        # Finance user should see Finance + General
        results = self.rbac.filter_by_role("finance", self.sample_data)
        depts = [r['metadata']['department'] for r in results]
        self.assertIn("Finance", depts)
        self.assertIn("General", depts)
        self.assertNotIn("HR", depts)
        self.assertNotIn("Marketing", depts)

    def test_hr_access(self):
        # HR user should see HR + General
        results = self.rbac.filter_by_role("hr", self.sample_data)
        depts = [r['metadata']['department'] for r in results]
        self.assertIn("HR", depts)
        self.assertNotIn("Finance", depts)

    def test_clevel_access(self):
        # C-Level sees everything
        results = self.rbac.filter_by_role("c-level", self.sample_data)
        self.assertEqual(len(results), 5)

    def test_marketing_access(self):
        # Marketing see Marketing + General
        results = self.rbac.filter_by_role("marketing", self.sample_data)
        depts = [r['metadata']['department'] for r in results]
        self.assertIn("Marketing", depts)
        self.assertNotIn("Engineering", depts)

    def test_employee_access(self):
        # Employee see General only
        results = self.rbac.filter_by_role("employees", self.sample_data)
        depts = [r['metadata']['department'] for r in results]
        self.assertIn("General", depts)
        self.assertNotIn("Finance", depts)

if __name__ == '__main__':
    # Save results to output
    import json
    # Running tests programmatically to capture results not super easy with unittest main
    # So we'll run it normally and catch exit code
    unittest.main()
