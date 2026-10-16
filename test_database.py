
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import database


class ShortlistDatabaseTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "test_worthit.db"

        self.database_path_patch = patch.object(
            database, "DATABASE_PATH", self.db_path
        )
        self.database_path_patch.start()

        database.initialize_database()

    def tearDown(self):
        self.database_path_patch.stop()
        self.temp_dir.cleanup()

    def test_categories_have_separate_shortlists(self):
        database.save_shortlist(
            "Laptops", ["Demo Laptop A", "Demo Laptop B"]
        )
        database.save_shortlist(
            "Smartphones", ["Demo Phone A"]
        )

        self.assertEqual(
            database.get_shortlist("Laptops"),
            ["Demo Laptop A", "Demo Laptop B"],
        )
        self.assertEqual(
            database.get_shortlist("Smartphones"),
            ["Demo Phone A"],
        )

    def test_saving_again_replaces_only_that_category(self):
        database.save_shortlist("Laptops", ["Demo Laptop A"])
        database.save_shortlist("Smartphones", ["Demo Phone A"])

        database.save_shortlist("Laptops", ["Demo Laptop B"])

        self.assertEqual(
            database.get_shortlist("Laptops"),
            ["Demo Laptop B"],
        )
        self.assertEqual(
            database.get_shortlist("Smartphones"),
            ["Demo Phone A"],
        )

    def test_clearing_one_category_preserves_another(self):
        database.save_shortlist("Laptops", ["Demo Laptop A"])
        database.save_shortlist("Smartphones", ["Demo Phone A"])

        database.clear_shortlist("Laptops")

        self.assertEqual(database.get_shortlist("Laptops"), [])
        self.assertEqual(
            database.get_shortlist("Smartphones"),
            ["Demo Phone A"],
        )

    def test_duplicate_names_are_removed_when_saving(self):
        database.save_shortlist(
            "Earbuds",
            ["Demo Earbuds A", "Demo Earbuds A"],
        )

        self.assertEqual(
            database.get_shortlist("Earbuds"),
            ["Demo Earbuds A"],
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
