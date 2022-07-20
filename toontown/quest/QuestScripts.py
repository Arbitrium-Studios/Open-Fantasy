script = '''
ID quest_assign_101
CLEAR_CHAT npc
LOAD squirt1 "user/default/resources/default/phase_3.5/models/gui/tutorial_gui" "squirt1"
LOAD squirt2 "user/default/resources/default/phase_3.5/models/gui/tutorial_gui" "squirt2"
LOAD toonBuilding "user/default/resources/default/phase_3.5/models/gui/tutorial_gui" "toon_buildings"
LOAD cogBuilding "user/default/resources/default/phase_3.5/models/gui/tutorial_gui" "suit_buildings"
LOAD cogs "user/default/resources/default/phase_3.5/models/gui/tutorial_gui" "suits"
POSHPRSCALE cogs -1.05 7 0 0 0 0 1 1 1
POSHPRSCALE toonBuilding -1.05 7 0 0 0 0 1.875 1.875 1.875
POSHPRSCALE cogBuilding -1.05 7 0 0 0 0 1.875 1.875 1.875
POSHPRSCALE squirt1 -1.05 7 0 0 0 0 1.875 1.875 1.875
POSHPRSCALE squirt2 -1.05 7 0 0 0 0 1.875 1.875 1.875
WRTREPARENTTO camera npc
LERP_POSHPRSCALE camera 2.8 0.0 3.5 35 5 0 1 1 1 1.5
WRTREPARENTTO camera localToon
LOCAL_CHAT_CONFIRM npc QuestScript100_0 "CFReversed"
LOCAL_CHAT_CONFIRM npc QuestScript100_1 "CFReversed"
LOCAL_CHAT_CONFIRM npc QuestScript100_2 "CFReversed"
LOCAL_CHAT_CONFIRM npc QuestScript100_3 "CFReversed"
LOCAL_CHAT_CONFIRM npc QuestScript100_4 "CFReversed"
PLAY_ANIM npc "right-hand-start" 1
WAIT 1
REPARENTTO cogs camera
LERP_SCALE cogs 1.875 1.875 1.875 0.5
WAIT 1.0833
LOOP_ANIM npc "right-hand" 1
FUNCTION npc "angryEyes"
FUNCTION npc "blinkEyes"
LOCAL_CHAT_CONFIRM npc QuestScript100_5 "CFReversed"
LOCAL_CHAT_CONFIRM npc QuestScript100_6 "CFReversed"
REPARENTTO cogs hidden
REPARENTTO toonBuilding camera
LOCAL_CHAT_CONFIRM npc QuestScript100_7 "CFReversed"
REPARENTTO toonBuilding hidden
REPARENTTO cogBuilding camera
FUNCTION npc "sadEyes"
FUNCTION npc "blinkEyes"
LOCAL_CHAT_CONFIRM npc QuestScript100_8 "CFReversed"
REPARENTTO cogBuilding hidden
LOCAL_CHAT_CONFIRM npc QuestScript100_9 "CFReversed"
LOCAL_CHAT_CONFIRM npc QuestScript100_10 "CFReversed"
LOCAL_CHAT_CONFIRM npc QuestScript100_11 "CFReversed"
LOCAL_CHAT_CONFIRM npc QuestScript100_12 "CFReversed"
LOCAL_CHAT_CONFIRM npc QuestScript100_13 "CFReversed"
REPARENTTO squirt1 camera
FUNCTION npc "normalEyes"
FUNCTION npc "blinkEyes"
LOCAL_CHAT_CONFIRM npc QuestScript100_14 "CFReversed"
REPARENTTO squirt1 hidden
REPARENTTO squirt2 camera
LOCAL_CHAT_CONFIRM npc QuestScript100_15 "CFReversed"
LERP_SCALE squirt2 1 1 0.01 0.5
WAIT 0.5
REPARENTTO squirt2 hidden
LOCAL_CHAT_CONFIRM npc QuestScript100_16 "CFReversed"
LOCAL_CHAT_CONFIRM npc QuestScript100_17 "CFReversed"
OBSCURE_LAFFMETER 0
SHOW laffMeter
POS laffMeter 0.153 0.0 0.13
SCALE laffMeter 0.0 0.0 0.0
WRTREPARENTTO laffMeter aspect2d
LERP_POS laffMeter -0.25 0 -0.15 1
LERP_SCALE laffMeter 0.2 0.2 0.2 0.6
WAIT 1.0833
LOOP_ANIM npc "right-hand"
LOCAL_CHAT_CONFIRM npc QuestScript100_18 "CFReversed"
LOCAL_CHAT_CONFIRM npc QuestScript100_19 "CFReversed"
FUNCTION npc "sadEyes"
FUNCTION npc "blinkEyes"
LAFFMETER 15 15
WAIT 0.1
LAFFMETER 14 15
WAIT 0.1
LAFFMETER 13 15
WAIT 0.1
LAFFMETER 12 15
WAIT 0.1
LAFFMETER 11 15
WAIT 0.1
LAFFMETER 10 15
WAIT 0.1
LAFFMETER 9 15
WAIT 0.1
LAFFMETER 8 15
WAIT 0.1
LAFFMETER 7 15
WAIT 0.1
LAFFMETER 6 15
WAIT 0.1
LAFFMETER 5 15
WAIT 0.1
LAFFMETER 4 15
WAIT 0.1
LAFFMETER 3 15
WAIT 0.1
LAFFMETER 2 15
WAIT 0.1
LAFFMETER 1 15
WAIT 0.1
LAFFMETER 0 15
LOCAL_CHAT_CONFIRM npc QuestScript100_20 "CFReversed"
FUNCTION npc "normalEyes"
FUNCTION npc "blinkEyes"
LAFFMETER 15 15
WRTREPARENTTO laffMeter bottomLeft
WAIT 0.5
LERP_POS laffMeter 0.153 0.0 0.13 0.6
LERP_SCALE laffMeter 0.075 0.075 0.075 0.6
LOCAL_CHAT_CONFIRM npc QuestScript100_21 "CFReversed"
LOCAL_CHAT_CONFIRM npc QuestScript100_22 "CFReversed"
LOCAL_CHAT_CONFIRM npc QuestScript100_23 "CFReversed"
LOCAL_CHAT_CONFIRM npc QuestScript100_24 "CFReversed"
LOCAL_CHAT_CONFIRM npc QuestScript100_25 "CFReversed"
LOCAL_CHAT_CONFIRM npc QuestScript100_26 "CFReversed"
LOCAL_CHAT_CONFIRM npc QuestScript100_27 "CFReversed"
LOCAL_CHAT_CONFIRM npc QuestScript100_28 "CFReversed"
LOCAL_CHAT_CONFIRM npc QuestScript100_29 "CFReversed"
PLAY_ANIM npc "right-hand-start" -2
WAIT 1.0625
LOOP_ANIM npc "neutral"
WAIT 0.5
LERP_HPR npc -50 0 0 0.5
FUNCTION npc "surpriseEyes"
FUNCTION npc "showSurpriseMuzzle"
PLAY_ANIM npc "right-point-start" 1.5
WAIT 0.6944
LOOP_ANIM npc "right-point"
LOCAL_CHAT_CONFIRM npc QuestScript100_30 "CFReversed"
PLAY_ANIM npc "right-point-start" -1
LERP_HPR npc -0.068 0 0 0.75
WAIT 1.0417
FUNCTION npc "angryEyes"
FUNCTION npc "blinkEyes"
FUNCTION npc "hideSurpriseMuzzle"
LOOP_ANIM npc "neutral"
FUNCTION localToon "questPage.showQuestsOnscreenTutorial"
LOCAL_CHAT_CONFIRM npc QuestScript100_31 "CFReversed"
FUNCTION localToon "questPage.hideQuestsOnscreenTutorial"
FUNCTION npc "normalEyes"
FUNCTION npc "blinkEyes"
UPON_TIMEOUT FUNCTION cogs "removeNode"
UPON_TIMEOUT FUNCTION toonBuilding "removeNode"
UPON_TIMEOUT FUNCTION cogBuilding "removeNode"
UPON_TIMEOUT FUNCTION squirt1 "removeNode"
UPON_TIMEOUT FUNCTION squirt2 "removeNode"
UPON_TIMEOUT LOOP_ANIM npc "neutral"
UPON_TIMEOUT SHOW laffMeter
UPON_TIMEOUT REPARENTTO laffMeter bottomLeft
UPON_TIMEOUT POS laffMeter 0.15 0 0.13
UPON_TIMEOUT SCALE laffMeter 0.075 0.075 0.075
POS localToon 0.776 14.6 0
HPR localToon 47.5 0 0
FINISH_QUEST_MOVIE


ID quest_incomplete_110
LOCAL_CHAT_CONFIRM npc QuestScript110_1
LOCAL_CHAT_CONFIRM npc QuestScript110_2
LOCAL_CHAT_CONFIRM npc QuestScript110_3
LOCAL_CHAT_CONFIRM npc QuestScript110_4
LOCAL_CHAT_CONFIRM npc QuestScript110_5
LOCAL_CHAT_CONFIRM npc QuestScript110_6
LOCAL_CHAT_CONFIRM npc QuestScript110_7
LOCAL_CHAT_CONFIRM npc QuestScript110_8
LOCAL_CHAT_CONFIRM npc QuestScript110_9
FINISH_QUEST_MOVIE

ID tutorial_blocker
HIDE localToon
REPARENTTO camera npc
FUNCTION npc "stopLookAround"
POS camera 0.0 6.0 4.0
HPR camera 180.0 0.0 0.0
LOCAL_CHAT_CONFIRM npc QuestScriptTutorialBlocker_1
WAIT 0.8 
LOCAL_CHAT_CONFIRM npc QuestScriptTutorialBlocker_2
WAIT 0.8 
POS camera -5.0 -9.0 6.0
HPR camera -25.0 -10.0 0.0
POS localToon 203.8 18.64 -0.475
HPR localToon -90.0 0.0 0.0
SHOW localToon
LOCAL_CHAT_CONFIRM npc QuestScriptTutorialBlocker_3
OBSCURE_CHAT 1 0 1
REPARENTTO chatScButton aspect2d
SHOW chatScButton
POS chatScButton -0.3 0 -0.1
SCALE chatScButton 2.0 2.0 2.0
LERP_COLOR_SCALE chatScButton 1 1 1 0 1 1 1 1 0.5
WRTREPARENTTO chatScButton topLeft
WAIT 0.5
LERP_POS chatScButton 0.204 0 -0.072 0.6
LERP_SCALE chatScButton 1.179 1.179 1.179 0.6
WAIT 0.6 
REPARENTTO arrows topLeft
ARROWS_ON 0.41 -0.09 180 0.21 -0.26 -90
LOCAL_CHAT_PERSIST npc QuestScriptTutorialBlocker_4
WAIT_EVENT "enterSpeedChat"
ARROWS_OFF
BLACK_CAT_LISTEN 1
WAIT_EVENT "SCChatEvent"
BLACK_CAT_LISTEN 0
WAIT 0.5
CLEAR_CHAT localToon
REPARENTTO camera localToon
LOCAL_CHAT_CONFIRM npc QuestScriptTutorialBlocker_5 "CFReversed"
LOCAL_CHAT_CONFIRM npc QuestScriptTutorialBlocker_6 "CFReversed"
OBSCURE_CHAT 0 0 0
REPARENTTO chatNormalButton aspect2d
SHOW chatNormalButton
POS chatNormalButton -0.3 0 -0.1
SCALE chatNormalButton 2.0 2.0 2.0
LERP_COLOR_SCALE chatNormalButton 1 1 1 0 1 1 1 1 0.5
WAIT 0.5
WRTREPARENTTO chatNormalButton topLeft
LERP_POS chatNormalButton 0.068 0 -0.072 0.6
LERP_SCALE chatNormalButton 1.179 1.179 1.179 0.6
WAIT 0.6
TUTORIAL_ACK_DONE
LOCAL_CHAT_CONFIRM npc QuestScriptTutorialBlocker_7 "CFReversed"
LOCAL_CHAT_CONFIRM npc QuestScriptTutorialBlocker_8 1 "CFReversed"
LOOP_ANIM npc "walk"
LERP_HPR npc 270 0 0 0.5
WAIT 0.5
LOOP_ANIM npc "run"
LERP_POS npc 217.4 18.81 -0.475 0.75 
LERP_HPR npc 240 0 0 0.75 
WAIT 0.75
LERP_POS npc 222.4 15.0 -0.475 0.35
LERP_HPR npc 180 0 0 0.35
WAIT 0.35
LERP_POS npc 222.4 5.0 -0.475 0.75
WAIT 0.75
REPARENTTO npc hidden
FREE_LOCALTOON
UPON_TIMEOUT ARROWS_OFF
UPON_TIMEOUT REPARENTTO arrows aspect2d
UPON_TIMEOUT POS chatScButton 0.204 0 -0.072
UPON_TIMEOUT SCALE chatScButton 1.179 1.179 1.179 
UPON_TIMEOUT POS chatNormalButton 0.068 0 -0.072
UPON_TIMEOUT SCALE chatNormalButton 1.179 1.179 1.179 
UPON_TIMEOUT OBSCURE_CHAT 0 0 0
UPON_TIMEOUT REPARENTTO camera localToon
FINISH_QUEST_MOVIE

ID gag_intro
SEND_EVENT "disableGagPanel"
SEND_EVENT "disableBackToPlayground"
HIDE inventory
TOON_HEAD npc 0 0 1
WAIT 0.1
LOCAL_CHAT_CONFIRM npc QuestScriptGagShop_1
LERP_POS npcToonHead -0.64 0 -0.74 0.7
LERP_SCALE npcToonHead 0.82 0.82 0.82 0.7
LERP_COLOR_SCALE purchaseBg 1 1 1 1 0.6 0.6 0.6 1 0.7
WAIT 0.7
SHOW inventory
LOCAL_CHAT_CONFIRM npc QuestScriptGagShop_1a
ARROWS_ON -0.19 0.04 180 -0.4 0.26 90
LOCAL_CHAT_PERSIST npc QuestScriptGagShop_3
SEND_EVENT "enableGagPanel"
WAIT_EVENT "inventory-selection"
ARROWS_OFF
CLEAR_CHAT npc
WAIT 0.5
LOCAL_CHAT_CONFIRM npc QuestScriptGagShop_4
LOCAL_CHAT_PERSIST npc QuestScriptGagShop_5
WAIT 0.5
SHOW_PREVIEW
CLEAR_CHAT npc
WAIT 0.5
SET_BIN backToPlaygroundButton "gui-popup"
LERP_POS backToPlaygroundButton -0.12 0 0.18 0.5
LERP_SCALE backToPlaygroundButton 2 2 2 0.5
LERP_COLOR_SCALE backToPlaygroundButton 1 1 1 1  2.78 2.78 2.78 1 0.5
LERP_COLOR_SCALE inventory 1 1 1 1  0.6 0.6 0.6 1 0.5
WAIT 0.5
START_THROB backToPlaygroundButton 2.78 2.78 2.78 1  2.78 2.78 2.78 0.7  2
LOCAL_CHAT_CONFIRM npc QuestScriptGagShop_6
STOP_THROB
LERP_POS backToPlaygroundButton 0.72 0 -0.045 0.5
LERP_SCALE backToPlaygroundButton 1.04 1.04 1.04 0.5
LERP_COLOR_SCALE backToPlaygroundButton 2.78 2.78 2.78 1  1 1 1 1 0.5
WAIT 0.5
CLEAR_BIN backToPlaygroundButton
SET_BIN playAgainButton "gui-popup"
LERP_POS playAgainButton -0.12 0 0.18 0.5
LERP_SCALE playAgainButton 2 2 2 0.5
LERP_COLOR_SCALE playAgainButton 1 1 1 1  2.78 2.78 2.78 1 0.5
WAIT 0.5
START_THROB playAgainButton 2.78 2.78 2.78 1  2.78 2.78 2.78 0.7  2
LOCAL_CHAT_CONFIRM npc QuestScriptGagShop_7
STOP_THROB
LERP_POS playAgainButton 0.72 0 -0.24 0.5
LERP_SCALE playAgainButton 1.04 1.04 1.04 0.5
LERP_COLOR_SCALE playAgainButton 2.78 2.78 2.78 1  1 1 1 1 0.5
WAIT 0.5
CLEAR_BIN playAgainButton
LOCAL_CHAT_CONFIRM npc QuestScriptGagShop_8 1
TOON_HEAD npc 0 0 0
LERP_COLOR_SCALE inventory 0.6 0.6 0.6 1  1 1 1 1 0.5
LERP_COLOR_SCALE purchaseBg 0.6 0.6 0.6 1  1 1 1 1 0.5
WAIT 0.5
SEND_EVENT "enableBackToPlayground"
UPON_TIMEOUT TOON_HEAD npc 0 0 0
UPON_TIMEOUT ARROWS_OFF
UPON_TIMEOUT SHOW inventory
UPON_TIMEOUT SEND_EVENT "enableGagPanel"
UPON_TIMEOUT SEND_EVENT "enableBackToPlayground"

ID quest_incomplete_145
CHAT_CONFIRM npc QuestScript145_1 1
LOAD frame "user/default/resources/default/phase_4/models/gui/tfa_images" "FrameBlankA"
LOAD tunnel "user/default/resources/default/phase_4/models/gui/tfa_images" "tunnelSignA"
POSHPRSCALE tunnel 0 0 0 0 0 0 0.8 0.8 0.8
REPARENTTO tunnel frame
POSHPRSCALE frame 0 0 0 0 0 0 0.1 0.1 0.1
REPARENTTO frame aspect2d
LERP_SCALE frame 1.0 1.0 1.0 1.0
WAIT 3.0
LERP_SCALE frame 0.1 0.1 0.1 0.5
WAIT 0.5
REPARENTTO frame hidden
CHAT_CONFIRM npc QuestScript145_2 1
UPON_TIMEOUT FUNCTION frame "removeNode"
FINISH_QUEST_MOVIE

ID quest_incomplete_150
CHAT_CONFIRM npc QuestScript150_1
ARROWS_ON  1.05 0.51 -120 1.05 0.51 -120
SHOW_FRIENDS_LIST
CHAT_CONFIRM npc QuestScript150_2
ARROWS_OFF
HIDE_FRIENDS_LIST
CHAT_CONFIRM npc QuestScript150_3
HIDE bFriendsList
CHAT_CONFIRM npc QuestScript150_4 1
UPON_TIMEOUT HIDE_FRIENDS_LIST
UPON_TIMEOUT ARROWS_OFF
FINISH_QUEST_MOVIE
'''