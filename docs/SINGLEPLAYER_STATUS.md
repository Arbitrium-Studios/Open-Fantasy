# Single-Player Migration Status

## Current Status: Phase 1 (Planning) Complete

This document tracks the progress of removing online functionality to make Open-Fantasy exclusively single-player.

## Completed Tasks ✓

1. **Architecture Analysis**
   - Documented current client-server architecture
   - Identified Astron, AI servers, and UberDog servers as components to remove
   - Analyzed distributed object communication patterns

2. **Scope Assessment**
   - Inventoried all server files: **430 files total**
     - 396 AI files (per-district game logic)
     - 34 UD files (global/cross-district logic)
   - Identified affected systems: battles, quests, NPCs, cogs, minigames, estates, pets, etc.

3. **Planning Documentation**
   - Created `SINGLEPLAYER_MIGRATION.md` with 7-phase migration plan
   - Created `SERVER_FILES_INVENTORY.md` with complete file listing
   - Added `want-single-player` configuration flag to `etc/Configrc.prc`

## Next Steps (Not Yet Started)

### Phase 2: Infrastructure
- Create local save/load system to replace database
- Implement local distributed object registry
- Add offline mode detection

### Phase 3: Core Systems
- Migrate avatar/toon management to client
- Migrate zone/district management to client
- Migrate quest and battle systems to client

### Phases 4-7
- See `SINGLEPLAYER_MIGRATION.md` for details

## Estimated Effort

- **Total Estimated Time**: 8-13 weeks of full-time development
- **Files to Modify/Remove**: ~430 server files + client modifications
- **Risk Level**: High (affects all game systems)

## Alternatives to Consider

1. **Keep Current Architecture**: Run servers locally but simplify deployment
2. **Replace Astron**: Use OtpGo or another lightweight alternative (mentioned in issue comments)
3. **Hybrid Approach**: Keep some server components but make them embedded/invisible to users
4. **Incremental Migration**: Focus on specific features first (news, certain NPCs, etc.)

## Recommendations

Given the scope and complexity:

1. **Re-evaluate Goals**: Confirm if full removal is necessary or if simplification would suffice
2. **Incremental Approach**: If proceeding, tackle one system at a time
3. **Consider Alternatives**: Evaluate OtpGo or embedded server approach
4. **Community Input**: Involve community in decision about approach

## References

- **Main Issue**: Remove Online Functionality
- **Planning Docs**: 
  - `SINGLEPLAYER_MIGRATION.md` - Full migration plan
  - `SERVER_FILES_INVENTORY.md` - Complete file inventory
- **Config Flag**: `want-single-player` in `etc/Configrc.prc` (currently disabled)

## Decision Points

Before proceeding to Phase 2, the following questions should be answered:

1. **Scope**: Full removal or simplified local server approach?
2. **Timeline**: Is 8-13 weeks of development time acceptable?
3. **Features**: Which features are essential vs. optional?
4. **Alternative**: Should we explore OtpGo or other alternatives first?

---

**Last Updated**: Initial planning phase completed
**Status**: Awaiting decision on approach before proceeding to Phase 2
