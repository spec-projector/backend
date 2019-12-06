# -*- coding: utf-8 -*-

from typing import Dict

from django.db.models import Model
from rest_framework.utils import model_meta


def update_from_validated_data(
    instance: Model,
    validated_data: Dict[str, object],
) -> Model:
    info = model_meta.get_field_info(instance)

    # Simply set each attribute on the instance, and then save it.
    # Note that unlike `.create()` we don't need to treat many-to-many
    # relationships as being a special case. During updates we already
    # have an instance pk for the relationships to be associated with.
    m2m_fields = []
    for attr, value in validated_data.items():
        if attr in info.relations and info.relations[attr].to_many:
            m2m_fields.append((attr, value))
        else:
            setattr(instance, attr, value)

    instance.save()

    # Note that many-to-many fields are set after updating instance.
    # Setting m2m fields triggers signals which could potentially change
    # updated instance and we do not want it to collide with .update()
    _update_m2m_fields(instance, m2m_fields)

    return instance


def _update_m2m_fields(instance: Model, m2m_fields) -> None:
    for m2m_attr, value in m2m_fields:
        field = getattr(instance, m2m_attr)
        field.set(value)
