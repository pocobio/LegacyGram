from android_utils import log
from hook_utils import find_class
from ui.bulletin import BulletinHelper

from LegacyGram.data.constants import Keys
from LegacyGram.utils.utils import get_client_version, parse_version


# thx jadx
def open_extera_setting(alias: str, plugin_id: str | None = None):
    SettingsRegistry = find_class("com.exteragram.messenger.preferences.utils.SettingsRegistry")

    if SettingsRegistry:
        try:
            alias = resolve_extera_function(alias)
            log(alias)
            registry_instance = SettingsRegistry.getInstance()
            registry_instance.handleLink(alias, plugin_id)

        except Exception as e:
            BulletinHelper.show_error(f"Failed to invoke extera handleLink: {e}")


def resolve_extera_function(function_name: str) -> str:
    if not function_name:
        return function_name

    client_version = parse_version(get_client_version())

    if client_version == (12, 1, 1):
        if function_name == Keys.General.drawer_options:
            return "myProfileItem"

    return function_name
