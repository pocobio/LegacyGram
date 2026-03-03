from hook_utils import find_class

from LegacyGram.data.constants import Keys
from LegacyGram.utils.xposed_utils import BaseHook

"""
EXPLANATION
MessageCell.GetAuthorStatus() # WORKS ONLY IN CHATS!
    -> if user not null -> call UserObject.GetEmojiStatusDocumentId & exteraBadge
        -> if EmojiStatusDocumentId not null -> return it
        -> if exteraBadge not null -> return badge
        -> if user.premium -> return msg_premium_liststar
    else logic for chat / channels (or idk)
    not checked for exteraBadge

UserObject.GetEmojiStatusDocumentIdHook() # Only 5 calls
    called in ChatMessageCell, DrawerUserCell, DrawerProfileCell
    so it's removes emoji status from (you will see msg_premium_liststar):
        messages in chats, drawer menu, chat list, title in chat list (search is not effected)

DialogObject.GetEmojiStatusDocumentIdHook() has over then 52 calls
"""

"""
class ChatMessageCellGetAuthorStatusHook(BaseHook):
    def before_hooked_method(self, param):
        # Return null - no status badge shown
        param.setResult(None)


class UserObjectGetEmojiStatusDocumentIdHook(BaseHook):
    def before_hooked_method(self, param):
        # Return null - no emoji status document ID
        param.setResult(None)


class DialogObjectGetEmojiStatusDocumentIdHook(BaseHook):
    def before_hooked_method(self, param):
        # Return 0 - no emoji status document ID
        param.setResult(0)

"""


class ProfileActivitySetCollectibleGiftStatusHook(BaseHook):
    def before_hooked_method(self, param):
        if not self.is_enabled():
            return
        param.setResult(None)


def register_premium_badge(plugin) -> None:
    ProfileActivity = find_class("org.telegram.ui.ProfileActivity")
    if ProfileActivity:
        plugin.hook_all_methods(ProfileActivity, "setCollectibleGiftStatus", ProfileActivitySetCollectibleGiftStatusHook(plugin, Keys.hide_gift_hint))

    """
    UserObject = find_class("org.telegram.messenger.UserObject")
    if UserObject:
        plugin.hook_all_methods(UserObject, "getEmojiStatusDocumentId", UserObjectGetEmojiStatusDocumentIdHook(plugin))
    DialogObject = find_class("org.telegram.messenger.DialogObject")
    if DialogObject:
        plugin.hook_all_methods(DialogObject, "getEmojiStatusDocumentId", DialogObjectGetEmojiStatusDocumentIdHook(plugin))
    ChatMessageCell = find_class("org.telegram.ui.Cells.ChatMessageCell")
    if ChatMessageCell:
        plugin.hook_all_methods(ChatMessageCell, "getAuthorStatus", ChatMessageCellGetAuthorStatusHook(plugin))
    """
