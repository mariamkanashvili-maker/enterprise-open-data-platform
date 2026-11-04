"""
lecture 10 (დამატება): lxml-ით XML Schema ვალიდაცია — stdlib xml.etree-ს
რაც არ გააჩნია (ElementTree მხოლოდ პარსავს, სტრუქტურას არ ამოწმებს).
"""

from lxml import etree


class XMLSchemaValidationError(Exception):
    """XML-ის სქემასთან შეუსაბამობისას წარმოქმნილი შეცდომა."""


def validate_against_schema(xml_path: str, xsd_path: str) -> bool:
    """
    ამოწმებს, შეესაბამება თუ არა XML ფაილი მოცემულ XSD სქემას.
    დაბრუნებული True ნიშნავს — სტრუქტურა ვალიდურია.
    """
    schema = etree.XMLSchema(etree.parse(xsd_path))
    xml_doc = etree.parse(xml_path)
    if not schema.validate(xml_doc):
        errors = "; ".join(str(e) for e in schema.error_log)
        raise XMLSchemaValidationError(f"XML არ შეესაბამება სქემას: {errors}")
    return True
