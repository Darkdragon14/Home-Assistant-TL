import datetime
from pytz import timezone
import pytz

from .const import (
  CONFIG_STOP,
  CONFIG_BUS,
  CONFIG_WAYBACK
)

from .api_client import TlApiClient

async def get_next_bus(api_client: TlApiClient, config, now):
  current_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
  current_datetime = current_datetime.replace(' ', '%20')
  params = {
      'line': config[CONFIG_BUS],
      'stop': config[CONFIG_STOP],
      'wayback': config[CONFIG_WAYBACK],
      'count': 6
  }
  return await api_client.async_get('/departures', params, current_datetime)

async def get_buses():
  api_client = TlApiClient()
  buses = await api_client.async_get('/lines')
  buses_dict = {}
  for bus in buses:
    buses_dict[bus['id']] = f"{bus['name']} - {bus['longName']}"
  return buses_dict

async def get_directions(busId):
  api_client = TlApiClient()
  params = {
    'line': busId
  }
  directions = await api_client.async_get('/routes', params)
  directions_dict = {}
  for direction in directions:
    directions_dict[direction['id']] = direction['direction']
  return directions_dict


async def get_stops(directionId):
  api_client = TlApiClient()
  params = {
    'route': directionId
  }
  stops = await api_client.async_get('/stops', params)
  stops_dict = {}
  for stop in stops:
    stops_dict[stop['id']] = f"{stop['name']} - {stop['city']}"
  return stops_dict