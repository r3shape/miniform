class MiniAppFlag:
    APP_RUNNING:    int =       (1 << 0)

    APP_DRAW_INTERFACE: int =   (1 << 1)

    APP_DEBUG_LIGHTS: int =     (1 << 2)
    APP_DEBUG_OBJECTS: int =    (1 << 3)
    APP_DEBUG_TILE_MAP: int =   (1 << 4)
    APP_DEBUG_PARTITION: int =  (1 << 5)

class MiniObjectFlag:
    OBJECT_DIRTY:   int =       (1 << 0)
    OBJECT_STATIC: int =        (1 << 1)
    OBJECT_DYNAMIC: int =       (1 << 2)
    OBJECT_COLLISIONS: int =    (1 << 3)

class MiniElementFlag:
    # Visibility flags
    VISIBLE: int                 = (1 << 0)
    SHOW_TEXT: int               = (1 << 2)
    SHOW_BORDER: int             = (1 << 3)
    SHOW_SURFACE: int            = (1 << 4)
    SHOW_ELEMENTS: int           = (1 << 5)

    # Anchor flags
    ANCHOR_CENTER: int           = (1 << 6)
    ANCHOR_TOP_LEFT: int         = (1 << 7)
    ANCHOR_TOP_RIGHT: int        = (1 << 8)
    ANCHOR_TOP_CENTER: int       = (1 << 9)
    ANCHOR_BOTTOM_LEFT: int      = (1 << 10)
    ANCHOR_BOTTOM_RIGHT: int     = (1 << 11)
    ANCHOR_BOTTOM_CENTER: int    = (1 << 12)

    # Interaction flags
    HOVERED: int                 = (1 << 13)
    CLICKED: int                 = (1 << 14)
    
    # Visual Flags
    ANTI_ALIAS: int              = (1 << 15)

    # Layout Flags
    DISPLAY_ROW: int             = (1 << 16)
    DISPLAY_LIST: int            = (1 << 17)
    DISPLAY_ABSOLUTE: int        = (1 << 18)
    
    # Alignment flags
    ALIGN_LEFT: int              = (1 << 19)
    ALIGN_RIGHT: int             = (1 << 20)
    ALIGN_CENTER: int            = (1 << 21)

class MiniCameraFlag:
    CAMERA_DIRTY:   int =       (1 << 0)

class MiniTileFlag:
    TILE_DYNAMIC:   int =       (1 << 0)
    TILE_ANIMATED:  int =       (1 << 1)
