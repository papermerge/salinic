from salinic.field import KeywordField, TextField, UUIDField


def test_field_instantiation_with_various_flag():
    """No exception/Error should be raised"""
    assert TextField(multi_value=True)
    assert TextField(general_search=True, multi_lang=True)
    assert UUIDField(index=False)
    assert KeywordField()
    assert KeywordField(multi_value=True)
