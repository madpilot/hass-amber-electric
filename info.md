{% if installed %}

## Changes as compared to your installed version:

### Breaking Changes

  {% if version_installed.replace("v", "").replace(".","") | int < 2  %}
- Energy integration removed.
- Price sensor now in $/kWh not c/kWh
  {% endif %}

### Changes

### Features

  {% if version_installed.replace("v", "").replace(".","") | int < 1  %}
- Initial deployment
  {% endif %}
  {% if version_installed.replace("v", "").replace(".","") | int < 2  %}
- Backport official core integration.
  {% endif %}

### Bugfixes

  {% if version_installed.replace("v", "").replace(".","") | int < 1  %}
- Working version
  {% endif %}

---

{% else %}

## Connect to the Amber Electric API

Retrieve real time pricing and demand information.
{% endif %}
