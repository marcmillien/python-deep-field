#!/usr/bin/env python

import unittest

from deep_field import DeepField


class TestLibsDeepField(unittest.TestCase):
    def test_struture_standard(self):
        self.assertEqual(
            DeepField(".metadata.labels.app").field_structure,
            {"metadata": {"labels": "app"}},
        )

    def test_struture_with_array(self):
        self.assertEqual(
            DeepField(".spec.containers.[0].image").field_structure,
            {"spec": {"containers": {0: "image"}}},
        )

    def test_struture_with_array_trailing(self):
        self.assertEqual(
            DeepField(".spec.containers.[0]").field_structure,
            {"spec": {"containers": 0}},
        )

    def test_struture_with_dot(self):
        self.assertEqual(
            DeepField(".metadata.labels.{app.kubernetes.io/name}.bla").field_structure,
            {"metadata": {"labels": {"app.kubernetes.io/name": "bla"}}},
        )

    def test_struture_with_dot_trailing(self):
        self.assertEqual(
            DeepField(".metadata.labels.{app.kubernetes.io/name}").field_structure,
            {"metadata": {"labels": "app.kubernetes.io/name"}},
        )

    def test_extract_with_array(self):
        self.assertEqual(
            DeepField(".spec.containers.[0].image").extract(
                {
                    "metadata": {
                        "labels": {
                            "app.kubernetes.io/name": "awesome",
                            "app": "crazy",
                        }
                    },
                    "spec": {
                        "containers": [
                            {
                                "image": "bla",
                                "other": "blabla",
                            }
                        ]
                    },
                },
            ),
            {"spec": {"containers": [{"image": "bla"}]}},
        )

    def test_extract_with_dot(self):
        self.assertEqual(
            DeepField(".metadata.labels.{app.kubernetes.io/name}").extract(
                {
                    "metadata": {
                        "labels": {
                            "app.kubernetes.io/name": "awesome",
                            "app": "crazy",
                        }
                    },
                    "spec": {
                        "containers": [
                            {
                                "image": "bla",
                                "other": "blabla",
                            }
                        ]
                    },
                },
            ),
            {"metadata": {"labels": {"app.kubernetes.io/name": "awesome"}}},
        )
