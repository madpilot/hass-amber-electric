{% if installed %}

## Changes as compared to your installed version:

### Breaking Changes

### Changes

### Features

  {% if version_installed.replace("v", "").replace(".","") | int < 1  %}
- Initial deployment
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
