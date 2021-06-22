# import amberelectric
from typing import Any, List, Mapping, Union
from amberelectric.model.channel import ChannelType

from amberelectric.model.interval import SpikeStatus
import amberelectric
from amberelectric.api import amber_api
from amberelectric.model.current_interval import CurrentInterval
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .coordinator import AmberDataService

from .const import CONF_API_TOKEN, CONF_SITE_ID
from homeassistant.const import ATTR_ATTRIBUTION

ATTRIBUTION = "Data provided by the Amber Electric pricing API"


def friendly_channel_type(channel_type: str) -> str:
    if channel_type == ChannelType.GENERAL:
        return "General"
    if channel_type == ChannelType.CONTROLLED_LOAD:
        return "Controlled Load"
    if channel_type == ChannelType.FEED_IN:
        return "Feed In"
    return channel_type


class AmberPriceSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, platform_name: str, channel_type: str, data_service: AmberDataService) -> None:
        super().__init__(data_service.coordinator)
        self._channel_type = channel_type
        self._platform_name = platform_name
        self._data_service = data_service

    @property
    def name(self) -> Union[str, None]:
        return self._platform_name + " - " + friendly_channel_type(self._channel_type) + " " + " Price"

    @property
    def icon(self):
        """Return the icon of the sensor."""
        if self._channel_type == ChannelType.FEED_IN:
            return "mdi:solar-power"
        if self._channel_type == ChannelType.CONTROLLED_LOAD:
            return "mdi:clock-outline"
        return "mdi:transmission-tower"

    @property
    def unit_of_measurement(self):
        return "¢/kWh"

    @property
    def state(self) -> Union[str, None]:
        channel = self._data_service.current_prices.get(self._channel_type)
        if channel:
            if self._channel_type == ChannelType.FEED_IN:
                return round(channel.per_kwh, 0) * -1
            return round(channel.per_kwh, 0)

    @property
    def device_state_attributes(self) -> Union[Mapping[str, Any], None]:
        meta = self._data_service.current_prices.get(self._channel_type)
        data = {}
        if meta is not None:
            data['duration'] = meta.duration
            data['date'] = meta.date.isoformat()
            data['nem_date'] = meta.nem_time.isoformat()
            data['spot_per_kwh'] = round(meta.spot_per_kwh)
            data['start_time'] = meta.start_time.isoformat()
            data['end_time'] = meta.end_time.isoformat()
            data['renewables'] = round(meta.renewables)
            data['estimate'] = meta.estimate
            data['spike_status'] = meta.spike_status.value
            data['channel_type'] = meta.channel_type.value

            if meta.range is not None:
                data['range_min'] = meta.range.min
                data['range_max'] = meta.range.max

        data[ATTR_ATTRIBUTION] = ATTRIBUTION
        return data


class AmberRenewablesSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, platform_name: str, data_service: AmberDataService) -> None:
        super().__init__(data_service.coordinator)
        self._platform_name = platform_name
        self._data_service = data_service

    @property
    def name(self) -> Union[str, None]:
        return self._platform_name + " - Renewables"

    @property
    def icon(self):
        return "mdi:solar-power"

    @property
    def unit_of_measurement(self):
        return "%"

    @property
    def state(self) -> Union[str, None]:
        channel = self._data_service.current_prices.get(ChannelType.GENERAL)
        if channel:
            return round(channel.renewables, 0)

    @property
    def device_state_attributes(self) -> Union[Mapping[str, Any], None]:
        data = {}
        data[ATTR_ATTRIBUTION] = ATTRIBUTION
        return data


class AmberForecastSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, platform_name: str, channel_type: str, data_service: AmberDataService) -> None:
        super().__init__(data_service.coordinator)
        self._channel_type = channel_type
        self._platform_name = platform_name
        self._data_service = data_service

    @property
    def name(self) -> Union[str, None]:
        return self._platform_name + " - " + friendly_channel_type(self._channel_type) + " " + " Forecast"

    @property
    def icon(self):
        if self._channel_type == ChannelType.FEED_IN:
            return "mdi:solar-power"
        if self._channel_type == ChannelType.CONTROLLED_LOAD:
            return "mdi:clock-outline"
        return "mdi:transmission-tower"

    @property
    def unit_of_measurement(self):
        return "¢/kWh"

    @property
    def state(self) -> Union[str, None]:
        forecasts = self._data_service.forecasts.get(self._channel_type)
        if forecasts and len(forecasts) > 0:
            if self._channel_type == ChannelType.FEED_IN:
                return round(forecasts[0].per_kwh, 0) * -1
            return round(forecasts[0].per_kwh, 0)

    @property
    def device_state_attributes(self) -> Union[Mapping[str, Any], None]:
        forecasts = self._data_service.forecasts.get(self._channel_type)
        data = {}
        data['forecasts'] = []
        data['channel_type'] = self._channel_type.value

        if forecasts is not None:
            for meta in forecasts:
                datum = {}
                datum['duration'] = meta.duration
                data['date'] = meta.date.isoformat()
                datum['nem_date'] = meta.nem_time.isoformat()
                datum['spot_per_kwh'] = round(meta.spot_per_kwh)
                datum['start_time'] = meta.start_time.isoformat()
                datum['end_time'] = meta.end_time.isoformat()
                datum['renewables'] = round(meta.renewables)
                datum['spike_status'] = meta.spike_status.value

                if meta.range is not None:
                    datum['range_min'] = meta.range.min
                    datum['range_max'] = meta.range.max

                data['forecasts'].append(datum)

        data[ATTR_ATTRIBUTION] = ATTRIBUTION
        return data


class AmberPriceSpikeSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, platform_name: str, data_service: AmberDataService) -> None:
        super().__init__(data_service.coordinator)
        self._platform_name = platform_name
        self._data_service = data_service

    @property
    def name(self) -> Union[str, None]:
        return self._platform_name + " - Price Spike"

    @property
    def state(self) -> Union[str, None]:
        channel = self._data_service.current_prices.get(ChannelType.GENERAL)
        if channel is not None:
            return channel.spike_status == SpikeStatus.SPIKE
        return False

    @property
    def icon(self):
        channel = self._data_service.current_prices.get(ChannelType.GENERAL)
        if channel is not None:
            if channel.spike_status == SpikeStatus.SPIKE:
                return "mdi:power-plug-off"
            if channel.spike_status == SpikeStatus.POTENTIAL:
                return "mdi:power-plug-outline"
        return "mdi:power-plug"

    @property
    def device_state_attributes(self) -> Union[Mapping[str, Any], None]:
        data = {}
        channel = self._data_service.current_prices.get(ChannelType.GENERAL)
        if channel is not None:
            data['spike_status'] = channel.spike_status.value
        data[ATTR_ATTRIBUTION] = ATTRIBUTION
        return data


class AmberFactory():
    def __init__(self, hass: HomeAssistant, platform_name: str, site_id: str, api: amber_api.AmberApi):
        self._platform_name = platform_name
        self.data_service = AmberDataService(hass, api, site_id)

    def build_sensors(self) -> List[SensorEntity]:
        sensors = []
        if self.data_service.site is not None:
            sensors.append(AmberPriceSensor(
                self._platform_name, ChannelType.GENERAL, self.data_service))

            sensors.append(AmberForecastSensor(
                self._platform_name, ChannelType.GENERAL, self.data_service))

            if len(list(filter(lambda channel: channel.type == ChannelType.FEED_IN, self.data_service.site.channels))) > 0:
                sensors.append(AmberPriceSensor(
                    self._platform_name, ChannelType.FEED_IN, self.data_service))

                sensors.append(AmberForecastSensor(
                    self._platform_name, ChannelType.FEED_IN, self.data_service))

            if len(list(filter(lambda channel: channel.type == ChannelType.CONTROLLED_LOAD, self.data_service.site.channels))) > 0:
                sensors.append(AmberPriceSensor(
                    self._platform_name, ChannelType.CONTROLLED_LOAD, self.data_service))

                sensors.append(AmberForecastSensor(
                    self._platform_name, ChannelType.CONTROLLED_LOAD, self.data_service))

            sensors.append(AmberRenewablesSensor(
                self._platform_name, self.data_service))

            sensors.append(AmberPriceSpikeSensor(
                self._platform_name, self.data_service))
        return sensors


def setup_platform(hass: HomeAssistant, config, add_entities, discovery_info=None):
    return True


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    configuration = amberelectric.Configuration(
        access_token=entry.data.get(CONF_API_TOKEN)
    )

    api_instance = amber_api.AmberApi.create(configuration)
    # Do a sites enquiry, and get all the channels...
    factory = AmberFactory(
        hass, entry.title, entry.data.get(CONF_SITE_ID), api_instance)
    factory.data_service.async_setup()
    await factory.data_service.coordinator.async_refresh()
    async_add_entities(factory.build_sensors())
