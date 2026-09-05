"""Smoke tests for a running Finova API.

Run after starting the API with: python -m unittest discover -s tests
"""
import json
import unittest
import urllib.request


class ApiSmokeTests(unittest.TestCase):
    def get_json(self, path):
        with urllib.request.urlopen(f'http://127.0.0.1:8000{path}') as response:
            self.assertEqual(response.status, 200)
            return json.load(response)

    def test_health(self):
        self.assertEqual(self.get_json('/api/health')['status'], 'healthy')

    def test_evaluation(self):
        result = self.get_json('/api/evaluation')
        self.assertGreater(result['total_records'], 0)
        self.assertIn('precision', result)
        self.assertIn('f1', result)

    def test_dashboard_matches_exception_queue(self):
        dashboard = self.get_json('/api/dashboard')
        exceptions = self.get_json('/api/exceptions')
        self.assertEqual(dashboard['unmatched'], len(exceptions))
