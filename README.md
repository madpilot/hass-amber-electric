# Home Assistant Plugin for Amber Electric Real-Time Pricing

A custom component for Home Assistant (www.home-assistant.io) to pull the latest energy prices from the Amber Electric (https://www.amberelectric.com.au/) REST API based on Post Code.

# How to install

1. Install [HACS](https://hacs.xyz/docs/installation/installation/)
2. Within HA go to HACS > Integrations > ... (in top right corner) > Custom Repositories
3. Add URL: `https://github.com/madpilot/hass-amber-electric`, Category: `Integration`
4. Scroll down to the Amber integration and upgrade/install the latest version
5. Go to https://app.amber.com.au/developers and generate an API token
6. Go to the integrations page inside your home assistant install
7. Search for Amber Electric
8. Install, enter your API key, select the site you want to add.
