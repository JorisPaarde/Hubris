"""
Model for creating the wiki form
"""
from django import forms

SEARCH_SKILL_STYLES = (
    ('AL', 'All'),
    ('LN', 'Lightning'),
    ('FR', 'Fire'),
    ('GL', 'Golem'),
    ('DR', 'Drain'),
    ('IC', 'Ice'),
    ('HL', 'Heal'),
    ('MN', 'Mana'),
)

SEARCH_ALLOWED_PHASES = (
    ('ANY', 'Any'),
    ('1', 'I'),
    ('2', 'II'),
    ('3', 'III'),
    ('4', 'IV'),
    ('5', 'V'),
    ('ALL', 'I-V'),
    ('NONE', 'None'),
)


class WikiForm(forms.Form):
    """
    Model for creating the wiki form
    Allows searching in full or free version.
    And filtering by skill-style and/or allowed-phase
    """
    search_full_version = forms.BooleanField(required=False)
    skill_style = forms.MultipleChoiceField(
        choices=SEARCH_SKILL_STYLES,
        widget=forms.SelectMultiple,
        required=False
        )
    alowed_phase = forms.MultipleChoiceField(
        choices=SEARCH_ALLOWED_PHASES,
        widget=forms.SelectMultiple,
        required=False
        )
