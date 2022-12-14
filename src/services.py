"""Module for database actions"""
import urllib.request
from urllib.error import HTTPError
import bibtexparser
from init import Reference


class Service:
    """Class for database actions"""
    def __init__(self, database) -> None:
        self.database = database

    def save_reference(self, author: str, title: str, year: str):
        """Save form data for inCollection type to database."""
        new = Reference(
            author=author,
            title=title,
            year=year,
            type_id=1
        )
        self.database.session.add(new)  # pylint: disable=no-member
        self.database.session.commit()  # pylint: disable=no-member

    def save_reference_book(
        self, author: str, title: str, year: str, booktitle: str,
        pagenumber: str
    ):  # pylint: disable=too-many-arguments
        """Save form data book type to database."""
        new = Reference(
            author=author,
            title=title,
            booktitle=booktitle,
            year=year,
            pages=pagenumber,
            type_id=2
        )
        self.database.session.add(new)  # pylint: disable=no-member
        self.database.session.commit()  # pylint: disable=no-member

    def from_bibtex(self, bibtex: str) -> None:
        """Save bibtex reference to database."""
        fields = ['author', 'title', 'booktitle', 'pages', 'year']
        accepted_types = {'incollection': 1, 'book': 2}
        bibtex_db = bibtexparser.loads(bibtex)
        bibtex_dict = bibtex_db.entries_dict
        for reference in bibtex_dict.values():
            if reference['ENTRYTYPE'] not in accepted_types:
                return
            # Fill missing fields to avoid an error later
            for field in fields:
                if field not in reference:
                    reference[field] = ''

            new_type_id = accepted_types[reference['ENTRYTYPE']]
            new = Reference(
                type_id=new_type_id,
                author=reference['author'],
                title=reference['title'],
                booktitle=reference['booktitle'],
                pages=reference['pages'],
                year=reference['year']
            )
            self.database.session.add(new)
            self.database.session.commit()

    @staticmethod
    def get_all_references():
        """Get references from database"""
        return Reference.query.all()

    @staticmethod
    def create_bibtex_file() -> None:
        """Create bibtex file for upload."""
        references = Reference.query.all()
        text = ''
        for i, reference in enumerate(references):
            text += reference.to_bibtex()
            if i != len(references) - 1:
                text += '\n\n'

        with open('references.bib', 'w', encoding='utf-8') as file:
            file.write(text)

    def create_bibtex_str_from_selected(self, selected: set) -> str:
        """Create bibtex string from selected reference ids."""
        references = Reference.query.filter(Reference.id.in_(selected)).all() # pylint: disable=no-member
        result = ''
        for i, reference in enumerate(references):
            result += reference.to_bibtex()
            if i != len(references) - 1:
                result += '\n\n'

        return result

    def delete_reference(self, ref_id: int):
        """Remove reference from database"""
        reference = Reference.query.filter_by(id=ref_id).one()
        self.database.session.delete(reference)  # pylint: disable=no-member
        self.database.session.commit()  # pylint: disable=no-member

    def get_bibtex_from_doi(self, doi):
        """Module adapted from https://scipython.com/blog/doi-to-bibtex/"""
        base_url = 'http://dx.doi.org/'
        # Allow user to input doi url or doi id
        if not doi.startswith(base_url):
            url = base_url + doi
        else:
            url = doi

        req = urllib.request.Request(url)
        req.add_header('Accept', 'application/x-bibtex')
        try:
            with urllib.request.urlopen(req) as reader:
                bibtex = reader.read().decode()
            self.from_bibtex(bibtex)
        except HTTPError as error:
            if error.code == 404:
                print('DOI not found.')
            else:
                print('Service unavailable.')
