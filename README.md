# Home Assistant Plugin for Amber Electric Real-Time Pricing

A custom component for Home Assistant (www.home-assistant.io) to pull the latest energy prices from the Amber Electric (https://www.amberelectric.com.au/) REST API based on Post Code.

## Attention!

This component has now been accepted into the Home Assistant core, and will be available from October 13, 2021. After this date, it is **not recommended to install this custom component**.

I have back ported the code from core here, so if you upgrade to the latest version of this custom component it will reflect the new integration in core.

I'll try to keep the two code bases in sync, though if that stops, I'll make a note here.

The custom integration will be removed from HACS once the version of Home Assistant that contains the official integration hits gold.

## Breaking changes

As part of the integration into the Home Assistant core, I had to make some breaking changes.

1. The energy sensor goes away, because it was deemed a duplicate of the price sensor.
2. Because of above: the price sensor now shows $/kWh, not c/kWh to maintain compatibility with the energy dashboard.

If you have automations based on the price, you can either divide the thresholds by 100, or you can set up a template in the `configuration.yaml`

# How to install

1. Copy custom_components/amberelectric to your hass data directory (where your configuration.yaml lives). It should go into the same directory structure (`YOUR_CONFIG_DIRECTORY/custom_components/amberelectric`)
2. Go to https://app.amber.com.au/developers and generate an API token
3. Go to the integrations page inside your home assistant install
4. Search for Amber Electric
5. Install, enter your API key, select the site you want to add.
