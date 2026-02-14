from hook_utils import find_class, get_private_field, set_private_field
from java import jint

from LegacyGram.data.constants import Keys
from LegacyGram.utils.xposed_utils import BaseHook

"""
EXPLANATION
code from updateTabs, but it's looks same in SharedMediaLayout constructor
boolean hasGifts = giftsContainer != null && (userInfo != null && userInfo.stargifts_count > 0 || info != null && info.stargifts_count > 0);
hasGifts = giftsContainer NOT null AND (userInfo NOT null AND userInfo.stargifts_count > 0 OR info not null AND info.stargifts_count > 0)
hasGifts = true AND (true AND false OR false) -> true AND (false) -> false -> tab won't be appeared
"""

TL_profileTabGifts = find_class("org.telegram.tgnet.TLRPC$TL_profileTabGifts")
# TL_profileTabPosts = find_class("org.telegram.tgnet.TLRPC$TL_profileTabPosts")


# currently using hide_gifts instead __init__, cuz I will add hide_stories here later
class SharedMediaLayoutHook(BaseHook):
    def before_hooked_method(self, param) -> None:
        hide_gifts = self.plugin.get_setting(Keys.Gifts.hide_gifts_tab, False)

        chat_info = param.args[5]  # TLRPC.ChatFull chatInfo
        user_info = param.args[6]  # TLRPC.UserFull userInfo

        if user_info:
            main_tab = get_private_field(user_info, "main_tab")
            if hide_gifts:
                set_private_field(user_info, "stargifts_count", jint(0))
                if isinstance(main_tab, TL_profileTabGifts):
                    set_private_field(user_info, "main_tab", None)

        if chat_info:
            main_tab = get_private_field(chat_info, "main_tab")
            if hide_gifts:
                set_private_field(chat_info, "stargifts_count", jint(0))
                if isinstance(main_tab, TL_profileTabGifts):
                    set_private_field(chat_info, "main_tab", None)


# same thing, will add hide_stories later
class UpdateTabsHook(BaseHook):
    def before_hooked_method(self, param) -> None:
        hide_gifts = self.plugin.get_setting(Keys.Gifts.hide_gifts_tab, False)
        if not hide_gifts:
            return

        layout = param.thisObject
        user_info = get_private_field(layout, "userInfo")  # org.telegram.tgnet.TLRPC$TL_userFull
        chat_info = get_private_field(layout, "info")  # not a user (channel, chats..)

        if user_info:
            if hide_gifts:
                set_private_field(user_info, "stargifts_count", jint(0))
        if chat_info:
            if hide_gifts:
                set_private_field(chat_info, "stargifts_count", jint(0))


def register_media_layout(plugin) -> None:
    SharedMediaLayout = find_class("org.telegram.ui.Components.SharedMediaLayout")
    if SharedMediaLayout:
        plugin.hook_all_constructors(SharedMediaLayout, SharedMediaLayoutHook(plugin))
        plugin.hook_all_methods(SharedMediaLayout, "updateTabs", UpdateTabsHook(plugin))
