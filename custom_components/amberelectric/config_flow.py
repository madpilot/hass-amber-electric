"""Config flow for the Amber Electric integration."""
from __future__ import annotations

from typing import Any, List, Optional, Union

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_API_TOKEN
from homeassistant.core import HomeAssistant, callback
# from homeassistant.data_entry_flow import FlowResult
from homeassistant.util import slugify

import amberelectric
from amberelectric.api import amber_api
from amberelectric.model.site import Site

from .const import CONF_API_TOKEN, CONF_SITE_ID, CONF_SITE_NAME, CONF_SITE_NMI, DOMAIN


@callback
def amberelectric_entries(hass: HomeAssistant):
    """Return the site_ids for the domain."""
    return {
        (entry.data[CONF_API_TOKEN])
        for entry in hass.config_entries.async_entries(DOMAIN)
    }


class AmberElectricConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the config flow."""
        self._errors = {}
        self._sites: Union[List[Site], None] = None
        self._api_token: str | None = None

    def fetch_sites(self, token: str) -> Union[List[Site], None]:
        configuration = amberelectric.Configuration(
            access_token=token
        )
        api = amber_api.AmberApi.create(configuration)

        try:
            sites = api.get_sites()
            if len(sites) == 0:
                self._errors[CONF_API_TOKEN] = "no_site"
                return None
            else:
                return sites
        except amberelectric.ApiException as e:
            if e.status == 403:
                self._errors[CONF_API_TOKEN] = "invalid_api_token"
            else:
                self._errors[CONF_API_TOKEN] = "unknown_error"
            return None

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ):
        """Step when user initializes a integration."""
        self._errors = {}
        self._sites = None
        self._api_token = None

        if user_input is not None:
            token = user_input[CONF_API_TOKEN]
            self._sites = await self.hass.async_add_executor_job(
                self.fetch_sites, token
            )

            if self._sites is not None:
                self._api_token = token
                return await self.async_step_site()

        else:
            user_input = {CONF_API_TOKEN: ""}

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_API_TOKEN, default=user_input[CONF_API_TOKEN]): str,
                }
            ),
            errors=self._errors,
        )

    async def async_step_site(self, user_input: dict[str, Any] = None):
        self._errors = {}

        api_token = self._api_token
        if user_input is not None:
            site_id = user_input[CONF_SITE_ID]
            sites = list(filter(lambda site: site.id == site_id, self._sites))

            if len(sites) != 0:
                site: Site = sites[0]
                name = user_input.get(CONF_SITE_NAME, site_id)
                return self.async_create_entry(title=name, data={CONF_SITE_ID: site_id, CONF_API_TOKEN: api_token, CONF_SITE_NMI: site.nmi})
        else:
            user_input = {CONF_API_TOKEN: api_token,
                          CONF_SITE_ID: "", CONF_SITE_NAME: ""}

        return self.async_show_form(
            step_id="site",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_SITE_ID, default=user_input[CONF_SITE_ID]): vol.In(list(map(lambda site: site.id, self._sites))),
                    vol.Optional(CONF_SITE_NAME, default=user_input[CONF_SITE_NAME]): str
                }
            ),
            errors=self._errors,
        )
