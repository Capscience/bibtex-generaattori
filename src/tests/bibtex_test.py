"""Bibtex conversion related unit tests."""
from init import Reference, Type, app  # pylint: disable=unused-import


class TestReference:
    """Tests for reference class."""
    def test_all_data_valid_to_bibtex(self):
        """Test that bibtex generation works with all fields."""
        reference = Reference(
            id=1,
            author='Mikko Mallikas',
            title='Ohjelmointi',
            booktitle='Tietokoneiden salat',
            pages='10-11',
            year=2022,
            type_id=1
        )
        with app.app_context():
            assert (reference.to_bibtex() ==
                    '@InCollection{1Mallikas2022,author={Mikko Mallikas},'
                    'title={Ohjelmointi},booktitle={Tietokoneiden salat},'
                    'year={2022},pages={10-11}}')

    def test_all_nullable_values_as_null_to_bibtex(self):
        """Test that None values are output as empty string."""
        reference = Reference(type_id=1)
        with app.app_context():
            assert (reference.to_bibtex() == '@InCollection{,author={},'
                    'title={},booktitle={},year={},pages={}}')

    def test_book_type_to_bibtex(self):
        """Test that boot type is converted correctly."""
        reference = Reference(type_id=2)
        with app.app_context():
            assert (reference.to_bibtex() == '@Book{,author={},'
                    'title={},booktitle={},year={},pages={}}')
