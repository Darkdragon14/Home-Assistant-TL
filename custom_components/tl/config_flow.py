import voluptuous as vol
import logging

from homeassistant.config_entries import (ConfigFlow, OptionsFlow)
from homeassistant.core import callback

from .const import (
  DOMAIN,
  CONFIG_NAME,
  CONFIG_STOP,
  CONFIG_BUS,
  CONFIG_DIRECTION,
  DATA_SCHEMA_STOP,
  CONFIG_WAYBACK
)

from .utils import (
  get_buses,
  get_directions,
  get_stops
)

_LOGGER = logging.getLogger(__name__)

class TlBusConfigFlow(ConfigFlow, domain=DOMAIN): 
  """Config flow."""

  VERSION = 1

  async def async_step_user(self, user_input):
    """Setup based on user config"""
    buses = await get_buses()

    if user_input is not None:
      if CONFIG_BUS in user_input:
        directions = await get_directions(user_input[CONFIG_BUS])
        if CONFIG_DIRECTION in user_input and self.context[CONFIG_BUS] == user_input[CONFIG_BUS]:
          stops = await get_stops(user_input[CONFIG_DIRECTION])
          if CONFIG_STOP in user_input and self.context[CONFIG_DIRECTION] == user_input[CONFIG_DIRECTION]:
            for id, direction in enumerate(directions):
              if direction == user_input[CONFIG_DIRECTION]:
                user_input[CONFIG_WAYBACK] = id
            return self.async_create_entry(
              title=f"Bus Stop {user_input[CONFIG_NAME]}", 
              data=user_input
            )
          self.context[CONFIG_DIRECTION] = user_input[CONFIG_DIRECTION]
          return self.async_show_form(
            step_id='user',
            data_schema=vol.Schema({
              vol.Required(CONFIG_NAME, default=user_input[CONFIG_NAME]): str,
              vol.Required(CONFIG_BUS, default=user_input[CONFIG_BUS]): vol.In(buses),
              vol.Required(CONFIG_DIRECTION, default=user_input[CONFIG_DIRECTION]): vol.In(directions),
              vol.Required(CONFIG_STOP): vol.In(stops)
            }),
            errors={}
          )
        self.context[CONFIG_BUS] = user_input[CONFIG_BUS]
        return self.async_show_form(
          step_id='user',
          data_schema=vol.Schema({
            vol.Required(CONFIG_NAME, default=user_input[CONFIG_NAME]): str,
            vol.Required(CONFIG_BUS, default=user_input[CONFIG_BUS]): vol.In(buses),
            vol.Required(CONFIG_DIRECTION): vol.In(directions)
          }),
          errors={}
        )

    return self.async_show_form(
      step_id='user',
      data_schema=vol.Schema({
        vol.Required(CONFIG_NAME): str,
        vol.Required(CONFIG_BUS): vol.In(buses)
      }),
      errors={}
    )

  @staticmethod
  @callback
  def async_get_options_flow(entry):
    return OptionsFlowHandler(entry)

class OptionsFlowHandler(OptionsFlow):
  """Handles options flow for the component."""

  def __init__(self, entry) -> None:
    self._entry = entry

  async def async_step_init(self, user_input):
    """Manage the options for the custom component."""

    config = dict(self._entry.data)
    if self._entry.options is not None:
      config.update(self._entry.options)

    return self.async_show_form(step_id="user", data_schema=DATA_SCHEMA_STOP, errors=errors)

  async def async_step_user(self, user_input):
    """Manage the options for the custom component."""

    errors = {}
    config = dict(self._entry.data)
    if self._entry.options is not None:
      config.update(self._entry.options)

    if user_input is not None:
      config.update(user_input)

    _LOGGER.debug(f"Update config {config}")

    if CONFIG_BUS in config and config[CONFIG_BUS] != None and len(config[CONFIG_BUS]) > 0:
      matches = re.search(REGEX_BUSES, config[CONFIG_BUS])
      if (matches == None):
        errors[CONFIG_BUS] = "invalid_buses"
      else:
        config[CONFIG_BUS] = config[CONFIG_BUS].split(",")
    else:
      config[CONFIG_BUS] = []

    if len(errors) < 1:
      return self.async_create_entry(title="", data=config)

    return self.async_show_form(step_id="user", data_schema=DATA_SCHEMA_STOP, errors=errors)