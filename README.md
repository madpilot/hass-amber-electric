# Home Assistant Plugin for Amber Electric Real-Time Pricing

A custom component for Home Assistant (www.home-assistant.io) to pull the latest energy prices from the Amber Electric (https://www.amber.com.au/) REST API based

## Attention!

This component is now in Home Assistant core

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=amberelectric)

**it is not recommended to install this custom component**.

I have back ported the code from core here, so if you upgrade to the latest version of this custom component it will reflect the new integration in core.

I'll try to keep the two code bases in sync, though if that stops, I'll make a note here.

## Breaking changes

As part of the integration into the Home Assistant core, I had to make some breaking changes.

1. The energy sensor goes away, because it was deemed a duplicate of the price sensor.
2. Because of above: the price sensor now shows $/kWh, not c/kWh to maintain compatibility with the energy dashboard.

If you have automations based on the price, you can either divide the thresholds by 100, or you can set up a template in the `configuration.yaml`
