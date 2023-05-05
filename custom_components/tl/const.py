import voluptuous as vol

DOMAIN = "tl"

CONFIG_NAME = "Name"
CONFIG_STOP = "Stop"
CONFIG_BUS = "Bus"
CONFIG_DIRECTION = "Direction"
CONFIG_WAYBACK = "WayBack"

DATA_SCHEMA_STOP = vol.Schema({
  vol.Required(CONFIG_NAME): str,
  vol.Required(CONFIG_BUS): str,
  vol.Required(CONFIG_DIRECTION): str,
  vol.Required(CONFIG_STOP): str,
  vol.Required(CONFIG_WAYBACK): int
})