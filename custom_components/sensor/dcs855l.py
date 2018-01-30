from homeassistant.const import TEMP_CELSIUS
from homeassistant.helpers.entity import Entity
from homeassistant.components.sensor import PLATFORM_SCHEMA
import homeassistant.helpers.config_validation as cv
from homeassistant.const import CONF_NAME
from requests.auth import HTTPBasicAuth
import logging
import re
import requests
import voluptuous as vol

CONF_HOST = 'host'
CONF_USERNAME = 'username'
CONF_PASSWORD = 'password'
DEFAULT_NAME = 'DCS855 Temp Sensor'
DEFAULT_HOST = 'http://127.0.0.1'
DEFAULT_USERNAME = ''
DEFAULT_PASSWORD = ''
_RESOURCE = '{}/users/notify.cgi'
_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Optional(CONF_HOST, default=DEFAULT_HOST): cv.string,
    vol.Optional(CONF_USERNAME, default=DEFAULT_USERNAME): cv.string,
    vol.Optional(CONF_PASSWORD, default=DEFAULT_PASSWORD): cv.string
})

def setup_platform(hass, config, add_devices, discovery_info=None):
    name = config.get(CONF_NAME)
    host = config.get(CONF_HOST)
    username = config.get(CONF_USERNAME)
    password = config.get(CONF_PASSWORD)
    add_devices([DCS855LSensor(name, host, username, password)])



class DCS855LSensor(Entity):

    def __init__(self, name, host, username, password):
        self._name = name
        self._state = None
        self._host = host
        self._username = username
        self._password = password

    @property
    def name(self):
        return self._name

    @property
    def host(self):
        return self._host

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password

    @property
    def state(self):
        return self._state

    @property
    def url(self):
        return _RESOURCE.format(self._host)

    @property
    def unit_of_measurement(self):
        return TEMP_CELSIUS

    def update(self):
        try:
            result = requests.get(self.url, auth=(self.username, self.password), timeout=10).text
            _LOGGER.info("DCS855L  results were %s", result)
            m = re.search('tpC=(.*)', result)
            if m:
                found = m.group(1)
            self._state = found
        except ValueError as err:
            _LOGGER.error("Error check DCS855L temp component %s", err.args)
            self._state = 00
            raise



