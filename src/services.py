"""Module for database actions"""
import sys
import urllib.request
from urllib.error import HTTPError
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
        pages: str
    ): # pylint: disable=too-many-arguments
        """Save form data book type to database."""
        new = Reference(
            author=author,
            title=title,
            booktitle=booktitle,
            year=year,
            pages=pages,
            type_id=2
        )
        self.database.session.add(new)  # pylint: disable=no-member
        self.database.session.commit()  # pylint: disable=no-member

    def get_all_references(self):
        """Get references from database"""
        return Reference.query.all()

    def create_bibtex_file(self) -> None:
        """Create bibtex file for upload."""
        references = Reference.query.all()
        text = ''
        for i, reference in enumerate(references):
            text += reference.to_bibtex()
            if i != len(references) - 1:
                text += '\n\n'

        with open('references.bib','w', encoding='utf-8') as file:
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
        self.database.session.delete(reference) # pylint: disable=no-member
        self.database.session.commit() # pylint: disable=no-member

    def get_bibtex_from_doi(self, doi):
        """Module from https://scipython.com/blog/doi-to-bibtex/"""
        base_url = 'http://dx.doi.org/'

        url = base_url + doi
        req = urllib.request.Request(url)
        req.add_header('Accept', 'application/x-bibtex')
        try:
            with urllib.request.urlopen(req) as reader:
                bibtex = reader.read().decode()
            return bibtex
        except HTTPError as error:
            if error.code == 404:
                print('DOI not found.')
            else:
                print('Service unavailable.')
            sys.exit(1)
    def get_reference_by_id(self, ref_id: int):
        """Get specific reference from database"""
        return Reference.query.filter_by(id=ref_id).one()

    def edit_reference(self, ref_id: int, author: str, title: str, year: str):
        """Edit inCollection type reference"""
        reference_to_edit = Reference.query.filter_by(id=ref_id).one()
        reference_to_edit.author = author
        reference_to_edit.title = title
        reference_to_edit.year = year
        self.database.session.commit()# pylint: disable=no-member

    def edit_reference_book(self, ref_id: int, author: str, title: str,
        year: str, booktitle: str, pages: str
    ): # pylint: disable=too-many-arguments
        """Edit book type reference"""
        reference_to_edit = Reference.query.filter_by(id=ref_id).one()
        reference_to_edit.author = author
        reference_to_edit.title = title
        reference_to_edit.year = year
        reference_to_edit.booktitle = booktitle
        reference_to_edit.pages = pages
        self.database.session.commit()# pylint: disable=no-member
