"""Component to manage a shoppling list."""
import asyncio
import json
import logging
import os
import uuid

import voluptuous as vol

from homeassistant.const import HTTP_NOT_FOUND, HTTP_BAD_REQUEST
from homeassistant.core import callback
from homeassistant.components import light
from homeassistant.helpers import intent
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'intent_handler'
DEPENDENCIES = ['group', 'light']
EVENT = 'custom_intent_handled'

@asyncio.coroutine
def async_setup(hass, config):
    """Initialize the shopping list."""

    intent.async_register(hass, ChangeLightState())

    return True


class ChangeLightState(intent.IntentHandler):
    """Handle AddItem intents."""

    intent_type = 'ChangeLightState'

    slot_schema = {
        'area': cv.string,
        'action': cv.string,
        'value': cv.string
    }

    @asyncio.coroutine
    def async_handle(self, intent_obj):
        """Handle the intent."""
        slots = self.async_validate_slots(intent_obj.slots)

        area = slots['area']['value']
        action = slots['action']['value']
        value = slots['value']['value']

        response = intent_obj.create_response()
        response.async_set_speech(
            "{} {} {}".format(area, action, value))

        intent_obj.hass.bus.async_fire(EVENT)

        intent_obj.hass.bus.async_fire('light.turn_on', {"entity_id": "group.kitchen_lights", "brightness_pct": "10"})

        kwargs = {'entity_id': area, action: value}
        light.turn_on(intent_obj.hass, **kwargs)

        return response
