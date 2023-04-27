from datetime import (
  timedelta, 
  datetime
)
from pytz import timezone
import pytz
import logging

from homeassistant.components.sensor import (
    SensorEntity,
)
from .const import (
  CONFIG_NAME,
  CONFIG_STOP,
)

from .api_client import TlApiClient
from .utils import (
  get_next_bus
)

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=1)

async def async_setup_entry(hass, entry, async_add_entities):
  """Setup sensors based on our entry"""

  entities = [TlBusNextBus(entry.data)]

  async_add_entities(entities, True)

class TlBusNextBus(SensorEntity):
  """Sensor for the next bus."""

  def __init__(self, data):
    """Init sensor."""
    self._client = TlApiClient()
    self._data = data
    self._attributes = {}
    self._state = None
    self._minsSinceLastUpdate = 0

  @property
  def unique_id(self):
    """The id of the sensor."""
    return f"tl_{self._data[CONFIG_STOP]}_next_bus"
    
  @property
  def name(self):
    """Name of the sensor."""
    return self._data[CONFIG_NAME]

  @property
  def icon(self):
    """Icon of the sensor."""
    return "mdi:bus"

  @property
  def extra_state_attributes(self):
    """Attributes of the sensor."""
    return self._attributes

  @property
  def native_unit_of_measurement(self):
    return "minutes"

  @property
  def state(self):
    """The state of the sensor."""
    return self._state

  async def async_update(self):
    """Retrieve the next bus"""
    self._minsSinceLastUpdate = self._minsSinceLastUpdate - 1

    # We only want to update every 5 minutes so we don't hammer the service
    if self._minsSinceLastUpdate <= 0:
      self._minsSinceLastUpdate = 1
    timezone = pytz.timezone("Europe/Zurich")
    now = datetime.now(timezone)
    departures = await get_next_bus(self._client, self._data, now)
    self._state = int((departures[0]['realDepartureTime']/1000 - datetime.timestamp(now)) / 60)
    self._attributes['destination'] = f"{departures[0]['destination']['name']} - {departures[0]['destination']['city']}"
    self._attributes['messages'] = departures[0]['messages']
    del departures[0]
    self._attributes['otherDepartures'] = []
    for departure in departures:
      self._attributes['otherDepartures'].append(int((departure['realDepartureTime']/1000 - datetime.timestamp(now)) / 60))