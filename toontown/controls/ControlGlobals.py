Separater = '-'
Shift = 'shift'
Control = 'control'
Release = 'up'
HotkeyMovement = 'movement'
HotkeyInteraction = 'interaction'
HotkeyDebug = 'debug'
HotkeyMisc = 'misc'
Hotkeys = (HotkeyMovement, HotkeyInteraction, HotkeyDebug, HotkeyMisc)
HotkeyUp = 0
HotkeyDown = 1
HotkeyLeft = 2
HotkeyRight = 3
HotkeyJump = 4
HotkeyThrow = 5
HotkeyMovementDefaults = {
    HotkeyUp: 'arrow_up',
    HotkeyDown: 'arrow_down',
    HotkeyLeft: 'arrow_left',
    HotkeyRight: 'arrow_right',
    HotkeyJump: 'control',
    HotkeyThrow: 'delete'
}
HotkeyBook = 0
HotkeyBookSecondary = 1
HotkeyTasks = 2
HotkeyTasksClose = 3
HotkeyInventory = 4
HotkeyInventoryClose = 5
HotkeyFriends = 6
HotkeyMap = 7
HotkeyMapClose = 8
HotkeyTeleport = 9
HotkeyPropGenerator = 10
HotkeyMountKart = 11
HotkeyScreenshot = 12
HotkeyChat = 13
HotkeyChatlog = 14
HotkeyGlobalChat = 15
HotkeyInteractionDefaults = {
    HotkeyBook: 'escape',
    HotkeyBookSecondary: 'f8',
    HotkeyTasks: 'end',
    HotkeyTasksClose: 'end' + Separater + Release,
    HotkeyInventory: 'home',
    HotkeyInventoryClose: 'home' + Separater + Release,
    HotkeyFriends: 'f7',
    HotkeyMap: 'alt',
    HotkeyMapClose: 'alt' + Separater + Release,
    HotkeyTeleport: 'f10',
    HotkeyPropGenerator: 'f11',
    HotkeyMountKart: 'insert',
    HotkeyScreenshot: 'f9',
    HotkeyChat: 'f5',
    HotkeyChatlog: 'enter',
    HotkeyGlobalChat: 'f6'
}
HotkeyDebugInfo = 0
HotkeyFacilityDebug = 1
HotkeyCameraDebug = 2
HotkeyGarbage = 3
HotkeySync = 4
HotkeyMarker = 5
HotkeyDebugDefaults = {
    HotkeyDebugInfo: Shift + Separater + 'f1',
    HotkeyFacilityDebug: Shift + Separater + 'f2',
    HotkeyCameraDebug: Shift + Separater + 'f12',
    HotkeyGarbage: Shift + Separater + 'f11',
    HotkeySync: Shift + Separater + 'f6',
    HotkeyMarker: Shift + Separater + 'f3'
}
HotkeyCameraForward = 0
HotkeyCameraBackward = 1
HotkeyCameraFirstPerson = 2
HotkeyPageUp = 3
HotkeyPageDown = 4
HotkeyNametags = 5
HotkeyMargins = 6
HotkeyOobe = 7
HotkeyMiscDefaults = {
    HotkeyCameraForward: 'tab',
    HotkeyCameraBackward: Shift + Separater + 'tab',
    HotkeyCameraFirstPerson: Shift + Separater + Control,
    HotkeyPageUp: 'page_up',
    HotkeyPageDown: 'page_down',
    HotkeyNametags: 'f2',
    HotkeyMargins: 'f3',
    HotkeyOobe: 'f4'
}
AllHotkeys = (HotkeyMovementDefaults, HotkeyInteractionDefaults, HotkeyDebugDefaults, HotkeyMiscDefaults)
SpecialKeys = {
    'page_up': 'Page Up',
    'page_down': 'Page Down',
    'escape': 'Esc',
    'delete': 'Del',
    'control': 'Ctrl',
    'insert': 'Ins',
    'arrow_up': 'Up Arrow',
    'arrow_down': 'Down Arrow',
    'arrow_left': 'Left Arrow',
    'arrow_right': 'Right Arrow',
    'num_lock': 'Number Lock',
    'print_screen': 'Print Screen',
    'caps_lock': 'Caps Lock'
}
