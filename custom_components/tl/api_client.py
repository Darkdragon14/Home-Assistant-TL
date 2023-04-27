from urllib.parse import urlencode
import aiohttp

class TlApiClient:

  def __init__(self):
    self._base_url = 'https://tl-apps.t-l.ch/ni-web/api'

  async def async_get(self, path, params = '', date = ''):
    """Get element we want from tl"""
    async with aiohttp.ClientSession() as client:
      url = f'{self._base_url}{path}'
      if params:
        parameters = urlencode(params)
        url += f'?{parameters}'
      if date:
        url += '&date=' + date
      async with client.get(url) as response:
        if response.status:
          # Disable content type check as sometimes it can report text/html
          data = await response.json(content_type=None)
          return data
        else:
          return []