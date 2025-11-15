# Server Files Inventory

This document lists all server-side files that need to be addressed when migrating to single-player mode.

## Summary

- **Total Files**: 430
- **AI Files**: 396 (server-side game logic per district)
- **UD Files**: 34 (global/cross-district logic)

## Categories

### Core Infrastructure (OTP)
**AI Files:**
otp/ai/BanManagerAI.py
otp/ai/TimeManagerAI.py
otp/avatar/DistributedAvatarAI.py
otp/avatar/DistributedPlayerAI.py
otp/distributed/AccountAI.py
otp/distributed/AstronAccountAI.py
otp/distributed/CentralLoggerAI.py
otp/distributed/DistributedDirectoryAI.py
otp/distributed/DistributedDistrictAI.py
otp/distributed/DistributedTestObjectAI.py
otp/distributed/ObjectServerAI.py
otp/friends/FriendManagerAI.py
otp/friends/GuildManagerAI.py
otp/level/DistributedEntityAI.py
otp/level/DistributedInteractiveEntityAI.py
otp/level/DistributedLevelAI.py
otp/level/EditMgrAI.py
otp/level/EntityCreatorAI.py
otp/level/LevelMgrAI.py
otp/level/ZoneEntityAI.py
otp/snapshot/SnapshotDispatcherAI.py
otp/snapshot/SnapshotRendererAI.py
otp/uberdog/DistributedChatManagerAI.py
otp/uberdog/OtpAvatarManagerAI.py
otp/web/SettingsMgrAI.py

**UD Files:**
otp/avatar/DistributedAvatarUD.py
otp/avatar/DistributedPlayerUD.py
otp/chat/ChatHandlerUD.py
otp/distributed/AccountUD.py
otp/distributed/AstronAccountUD.py
otp/distributed/CentralLoggerUD.py
otp/distributed/DistributedDistrictUD.py
otp/distributed/ObjectServerUD.py
otp/friends/AvatarFriendsManagerUD.py
otp/friends/GuildManagerUD.py
otp/friends/PlayerFriendsManagerUD.py
otp/login/AstronLoginManagerUD.py
otp/snapshot/SnapshotDispatcherUD.py
otp/snapshot/SnapshotRendererUD.py
otp/status/StatusDatabaseUD.py
otp/uberdog/DistributedChatManagerUD.py
otp/uberdog/OtpAvatarManagerUD.py
otp/uberdog/SpeedchatRelayUD.py
otp/web/SettingsMgrUD.py

### Toontown Game Logic
**AI Files:**
toontown/ai/DistributedBlackCatMgrAI.py
toontown/ai/DistributedGreenToonEffectMgrAI.py
toontown/ai/DistributedHydrantZeroMgrAI.py
toontown/ai/DistributedMailboxZeroMgrAI.py
toontown/ai/DistributedPhaseEventMgrAI.py
toontown/ai/DistributedPolarPlaceEffectMgrAI.py
toontown/ai/DistributedResistanceEmoteMgrAI.py
toontown/ai/DistributedScavengerHuntTargetAI.py
toontown/ai/DistributedSillyMeterMgrAI.py
toontown/ai/DistributedTrashcanZeroMgrAI.py
toontown/ai/DistributedTrickOrTreatTargetAI.py
toontown/ai/DistributedWinterCarolingTargetAI.py
toontown/ai/HolidayBaseAI.py
toontown/ai/HolidayManagerAI.py
toontown/ai/NewsManagerAI.py
toontown/ai/WelcomeValleyManagerAI.py
toontown/battle/BattleCalculatorAI.py
toontown/battle/BattleExperienceAI.py
toontown/battle/BattleManagerAI.py
toontown/battle/DistributedBattleAI.py
toontown/battle/DistributedBattleBaseAI.py
toontown/battle/DistributedBattleBldgAI.py
toontown/battle/DistributedBattleDinersAI.py
toontown/battle/DistributedBattleFinalAI.py
toontown/battle/DistributedBattleWaitersAI.py
toontown/fishing/DistributedFishingPondAI.py
toontown/fishing/DistributedFishingTargetAI.py
toontown/fishing/DistributedPondBingoManagerAI.py
toontown/golf/DistributedGolfCourseAI.py
toontown/golf/DistributedGolfHoleAI.py
toontown/golf/DistributedPhysicsWorldAI.py
toontown/golf/GolfManagerAI.py
toontown/safezone/BRTreasurePlannerAI.py
toontown/safezone/DistributedMMTreasureAI.py
toontown/safezone/DistributedTTTreasureAI.py
toontown/safezone/RegenTreasurePlannerAI.py
toontown/toon/DistributedNPCBlockerAI.py
toontown/toon/DistributedNPCClerkAI.py
toontown/toon/DistributedNPCFishermanAI.py
toontown/toon/DistributedNPCFlippyInToonHallAI.py
toontown/toon/DistributedNPCKartClerkAI.py
toontown/toon/DistributedNPCPartyPersonAI.py
toontown/toon/DistributedNPCPetclerkAI.py
toontown/toon/DistributedNPCScientistAI.py
toontown/toon/DistributedNPCSpecialQuestGiverAI.py
toontown/toon/DistributedNPCTailorAI.py
toontown/toon/DistributedNPCToonAI.py
toontown/toon/DistributedNPCToonBaseAI.py
toontown/toon/DistributedToonAI.py
toontown/toonbase/ToontownAccessAI.py
... and 321 more files

**UD Files:**
toontown/coderedemption/TTCodeRedemptionMgrUD.py
toontown/distributed/NonRepeatableRandomSourceUD.py
toontown/friends/TTPlayerFriendsManagerUD.py
toontown/rpc/AwardManagerUD.py
toontown/rpc/RATManagerUD.py
toontown/toon/DistributedToonUD.py
toontown/uberdog/DistributedCpuInfoMgrUD.py
toontown/uberdog/DistributedDataStoreManagerUD.py
toontown/uberdog/DistributedDeliveryManagerUD.py
toontown/uberdog/DistributedInGameNewsMgrUD.py
toontown/uberdog/DistributedMailManagerUD.py
toontown/uberdog/DistributedPartyManagerUD.py
toontown/uberdog/DistributedSecurityMgrUD.py
toontown/uberdog/DistributedWhitelistMgrUD.py
toontown/uberdog/TTSpeedchatRelayUD.py

## Key Systems to Migrate

### High Priority (Core Game)
- Avatar/Toon management (DistributedToonAI.py, DistributedToonUD.py)
- Zone/District management (ToontownDistrictAI.py)
- Battle system (coghq/Distributed*BattleAI.py)
- Quest system (QuestManagerAI.py)
- Suit/Cog AI (suit/Distributed*AI.py)

### Medium Priority (Activities)
- Minigames (minigame/Distributed*AI.py)
- Fishing (fishing/Distributed*AI.py)
- Golf (golf/Distributed*AI.py)
- Racing (racing/Distributed*AI.py)
- Parties (parties/Distributed*AI.py)

### Lower Priority (Social/Optional)
- Friends system (friends/*UD.py)
- Mail system (uberdog/DistributedMailManager*.py)
- Party management (uberdog/DistributedPartyManager*.py)
- News (uberdog/DistributedInGameNewsMgr*.py)

### Estate System
- Houses and furniture (estate/Distributed*AI.py)
- Gardens and pets (estate/Distributed*Garden*AI.py)
- Pet management (pets/*AI.py)

## Migration Strategy

Each file will need to be:
1. Analyzed for critical functionality
2. Either migrated to client-side or removed
3. Tested to ensure functionality is preserved
4. Documented for future reference

See SINGLEPLAYER_MIGRATION.md for the full migration plan.
