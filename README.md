# Home Assistant Plugin for Amber Electric Real-Time Pricing

A custom component for Home Assistant (www.home-assistant.io) to pull the latest energy prices from the Amber Electric (https://www.amberelectric.com.au/) REST API based on Post Code.

# How to install

1. Copy custom_components/amberelectric to your hass data directory (where your configuration.yaml lives). It should go into the same directory structure (`YOUR_CONFIG_DIRECTORY/custom_components/amberelectric`)
2. Go to https://app.amber.com.au/developers and generate an API token
3. Go to the integrations page inside your home assistant install
4. Search for Amber Electric
5. Install, enter your API key, select the site you want to add.
