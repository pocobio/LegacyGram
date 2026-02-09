from hook_utils import find_class
from base_plugin import MethodHook

class ActionBarMenuItemHook(MethodHook):
    def __init__(self, plugin):
        self.plugin = plugin

    def before_hooked_method(self, param):
        if not self.plugin.get_setting("send_gift_action_bar_in_profile", False):
            return

        # private final static int gift_premium = 38; in ProfileActivity, which call this method
        if len(param.args) > 0 and param.args[0] == 38:
            param.setResult(None)


def register_remove_gift_button(plugin) -> None:
    ActionBarMenuItem = find_class("org.telegram.ui.ActionBar.ActionBarMenuItem")
    if ActionBarMenuItem:
        plugin.hook_all_methods(ActionBarMenuItem, "addSubItem", ActionBarMenuItemHook(plugin))
