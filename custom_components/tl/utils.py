import datetime
from pytz import timezone
import pytz

from .const import (
  CONFIG_STOP,
  CONFIG_BUS,
  CONFIG_DIRECTION
)

from .api_client import TlApiClient

async def get_next_bus(api_client: TlApiClient, config, now):
  current_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
  current_datetime = current_datetime.replace(' ', '%20')
  params = {
      'line': config[CONFIG_BUS],
      'stop': config[CONFIG_STOP],
      'wayback': config[CONFIG_DIRECTION],
      'count': 6
  }
  return await api_client.async_get('/departures', params, current_datetime)

async def get_buses():
  api_client = TlApiClient()
  buses = await api_client.async_get('/lines')
  busesOption = []
  for bus in buses:
    busesOption.append({'id': bus['id'], 'name': f"{bus['name']} - {bus['longName']}"})
  return busesOption