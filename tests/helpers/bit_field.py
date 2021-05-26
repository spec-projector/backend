from jnt_django_toolbox.models.fields.bit.types import BitHandler


def assert_bitfield(actual, expected):
    """Assert bitfield value."""
    expected_bits = BitHandler(
        expected,
        actual.keys(),
    ).items()
    assert int(actual) == int(expected), "value is {0}, should be {1}".format(
        [bit_value for bit_value, is_set in actual.items() if is_set],
        [bit_value for bit_value, is_set in expected_bits if is_set],
    )
