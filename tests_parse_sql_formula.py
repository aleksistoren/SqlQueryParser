import pytest

from main import extract_fields_from_formula


# Test cases
@pytest.mark.parametrize("formula,expected_fields", [
    ("toDecimal(col44, 20) / nullif(toDecimal(col10, 20), 0)", {"col44", "col10"}),
    ("col1 + col2", {"col1", "col2"}),
    ("CASE WHEN col3 > 100 THEN col3 ELSE col4 END", {"col3", "col4"}),
    ("col5 * (col6 - col7)", {"col5", "col6", "col7"}),
    ("concat(col8, '_suffix')", {"col8"}),
    ("", set()),  # No fields in an empty formula
])

def test_extract_fields_from_formula(formula, expected_fields):
    """
    Tests the extract_fields_from_formula function with various formulas to ensure it correctly extracts field names.
    """
    assert extract_fields_from_formula(formula) == expected_fields, f"Failed to extract correct fields from formula: {formula}"
