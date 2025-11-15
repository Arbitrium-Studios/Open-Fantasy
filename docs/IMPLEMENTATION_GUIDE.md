# Removing Online Functionality - Implementation Guide

This guide provides an overview of the work done and next steps for removing online functionality from Open-Fantasy.

## What Has Been Done (Phase 1)

This PR completes the initial planning phase:

### Documentation Created
1. **SINGLEPLAYER_MIGRATION.md** - Comprehensive 7-phase migration plan
2. **SERVER_FILES_INVENTORY.md** - Complete inventory of 430 server files to address
3. **docs/SINGLEPLAYER_STATUS.md** - Current status and decision points
4. **docs/IMPLEMENTATION_GUIDE.md** - This file

### Infrastructure Added
- `want-single-player` configuration flag in `etc/Configrc.prc` (currently set to 0/disabled)

### Analysis Completed
- Documented current client-server architecture
- Identified all server components (Astron, AI servers, UberDog servers)
- Inventoried 430 server files (396 AI + 34 UD)
- Estimated effort: 8-13 weeks full-time development
- Identified 7 phases for migration

## Key Findings

### Architecture Overview
```
Current:
┌──────────┐     ┌─────────┐     ┌────────────┐     ┌─────────────┐
│  Client  │ <-> │ Astron  │ <-> │ AI Servers │ <-> │  Database   │
└──────────┘     └─────────┘     └────────────┘     └─────────────┘
                      ↕
                 ┌─────────┐
                 │ UberDog │
                 └─────────┘

Target (Single-Player):
┌──────────┐
│  Client  │ (with embedded game logic and local saves)
└──────────┘
```

### File Impact
- **396 AI Files**: Per-district game logic (battles, NPCs, quests, etc.)
- **34 UD Files**: Global/cross-district logic (friends, parties, mail, etc.)
- **~20+ Repository Files**: Connection and communication logic
- **Multiple Config Files**: Astron configuration, DC files, etc.

### System Impact
Every major game system is affected:
- ✓ Avatar/Toon management
- ✓ Battle system
- ✓ Quest system  
- ✓ NPC AI
- ✓ Cog/Suit AI
- ✓ Minigames
- ✓ Fishing, Golf, Racing
- ✓ Estates and Housing
- ✓ Pet system
- ✓ Friends system
- ✓ Parties
- ✓ Mail
- ✓ And more...

## How to Proceed

### Option 1: Full Migration (Original Goal)
Follow the 7-phase plan in `SINGLEPLAYER_MIGRATION.md`:
1. **Phase 1** ✓ Complete - Planning and documentation
2. **Phase 2** - Infrastructure (local saves, mock distributed objects)
3. **Phase 3** - Core systems (avatar, zones, quests, battles)
4. **Phase 4** - NPC and AI systems
5. **Phase 5** - Social systems (remove or mock)
6. **Phase 6** - Activities and minigames
7. **Phase 7** - Cleanup (remove Astron, servers)

**Timeline**: 8-13 weeks of dedicated development
**Risk**: High - affects all game systems
**Benefit**: True single-player game with no server requirements

### Option 2: Simplified Approach
Keep servers running locally but simplify:
- Bundle Astron with the game
- Auto-start servers in background
- Hide server management from users
- Keep architecture but improve UX

**Timeline**: 1-2 weeks
**Risk**: Low - minimal code changes
**Benefit**: Easier for users without architectural overhaul

### Option 3: Alternative Server (OtpGo)
Replace Astron with a lightweight alternative:
- Evaluate OtpGo (mentioned in issue comments)
- Port game logic to new server
- Potentially simpler than full removal

**Timeline**: Unknown - depends on OtpGo compatibility
**Risk**: Medium - requires learning new system
**Benefit**: Modern, potentially better maintained server

### Option 4: Incremental Hybrid
Start with specific features and gradually migrate:
- Make news system local first
- Add offline mode for specific activities
- Gradually move non-critical features to client
- Keep critical features on local servers

**Timeline**: Ongoing, delivered incrementally
**Risk**: Low per increment
**Benefit**: Steady progress without big bang migration

## Decision Framework

Before proceeding, answer these questions:

1. **What's the actual problem?**
   - Is it server complexity for users?
   - Is it deployment/maintenance burden?
   - Is it desire for offline play?
   - Is it architectural preference?

2. **What's the acceptable timeline?**
   - Can we wait 8-13 weeks?
   - Do we need something sooner?
   - Can we deliver incrementally?

3. **What features are essential?**
   - Do we need all multiplayer features (parties, friends)?
   - Can we simplify or remove some systems?
   - What's the minimum viable single-player experience?

4. **What resources are available?**
   - How many developers?
   - What's their expertise level?
   - How much time can they dedicate?

## Recommended Next Steps

Based on maintainer comments suggesting this might be "reaching," I recommend:

1. **Evaluate Option 2 first** (simplified local servers)
   - Quick win, low risk
   - Improves user experience immediately
   - Doesn't prevent future migration

2. **Research Option 3** (OtpGo or alternatives)
   - Might be better long-term solution
   - Community has mentioned it
   - Could simplify maintenance

3. **If proceeding with Option 1** (full migration)
   - Start with Phase 2 (infrastructure)
   - Build local save system first
   - Create proof-of-concept with one simple system
   - Evaluate before committing to full migration

4. **Get community input**
   - What do users actually need?
   - What problems are we solving?
   - What features can we drop?

## Using This Work

The planning documents created can be used regardless of which option is chosen:

- **SERVER_FILES_INVENTORY.md** - Useful for any server refactoring
- **SINGLEPLAYER_MIGRATION.md** - Roadmap if doing full migration
- **docs/SINGLEPLAYER_STATUS.md** - Track progress for any approach
- **want-single-player flag** - Can be used to toggle features

## Contact and Questions

For questions about this work or to discuss the approach:
- See issue comments for community discussion
- Review the planning documents for details
- Check `docs/SINGLEPLAYER_STATUS.md` for current status

---

**Remember**: This is a massive undertaking. Take time to evaluate options before committing to the full migration. The planning work done here will be valuable regardless of which approach is ultimately chosen.
