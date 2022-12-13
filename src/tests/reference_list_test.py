"""Tests for reference list functionality."""
from os import remove, path
from init import app, db, Reference
from services import Service


class TestReferenceList:
    """Tests for reference list functionality."""
    def setup_method(self):
        """Pytest setup method"""
        self.services = Service(db) # pylint: disable=attribute-defined-outside-init

    def test_db_write_and_read(self):
        """Test adding a reference to the database and reading references."""
        with app.app_context():
            self.services.save_reference("Very Real", "Test Data", "2022")
            assert self.services.get_all_references() == [
                Reference(
                    id=1,
                    author='Very Real',
                    title='Test Data',
                    year=2022,
                    type_id=1
                )
            ]

    def test_db_remove_entry(self):
        """Test removing a reference from the database."""
        with app.app_context():
            assert len(self.services.get_all_references()) == 1
            self.services.delete_reference(1)
            references = self.services.get_all_references()
            assert references == []

    def test_create_file(self):
        """Test bibtex-file is created and is correct"""
        with app.app_context():
            self.services.save_reference("Test Author", "Test Title", "2022")
            self.services.create_bibtex_file()
            assert path.isfile('references.bib')

            with open('references.bib', 'r', encoding='utf-8') as file:
                bibtex_file = file.read()
                should_be = (
                    '@InCollection{1Author2022,author={Test Author},'
                    'title={Test Title},'
                    'booktitle={},year={2022},pages={}}'
                )

                assert bibtex_file == should_be

    def test_create_bibtex_string_from_selected(self):
        """Test correct bibtex string is created from selected references"""
        with app.app_context():
            self.services.save_reference('Test Author1', 'Test Title1', '2022')
            self.services.save_reference('Test Author2', 'Test Title2', '2022')
            self.services.save_reference('Test Author3', 'Test Title3', '2022')

            test_ref_1 = Reference.query.filter(
                Reference.title == 'Test Title1'
            ).first()
            test_ref_2 = Reference.query.filter(
                Reference.title == 'Test Title2'
            ).first()

            selected = set([test_ref_1.id, test_ref_2.id])

            bibtex_str = self.services.create_bibtex_str_from_selected(selected)

            should_be = (
                '@InCollection{2Author12022,author={Test Author1},title={Test Title1},booktitle={},year={2022},pages={}}' #pylint: disable=line-too-long
                '\n\n'
                '@InCollection{3Author22022,author={Test Author2},title={Test Title2},booktitle={},year={2022},pages={}}' #pylint: disable=line-too-long
            )

            assert bibtex_str == should_be

def teardown_module():
    """Pytest test suite teardown."""
    remove('src/instance/test.db')
