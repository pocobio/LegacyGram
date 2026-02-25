class View:
    VISIBLE: int = 0
    INVISIBLE: int = 4
    GONE: int = 8

    def setVisibility(self, visibility: int) -> None: ...
