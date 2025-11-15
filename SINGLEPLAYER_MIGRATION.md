# Single-Player Migration Plan

This document outlines the plan for migrating Open-Fantasy from a client-server architecture to a single-player game.

## Current Architecture

Open-Fantasy currently uses a distributed architecture:
- **Astron**: Distributed object server that routes messages between components
- **AI Servers**: Handle per-district game logic (NPCs, buildings, cogs, pets, quests, etc.)
- **UberDog Servers**: Handle cross-district logic (friends, parties, mail, news, etc.)
- **Client**: Connects to servers via network protocols

## Migration Strategy

Given the complexity of this change, we recommend an incremental approach:

### Phase 1: Preparation (Current)
- [x] Document current architecture
- [x] Add configuration flag for single-player mode (want-single-player)
- [x] Identify all server-side functionality that needs to be migrated
- [x] Create inventory of all AI and UD files (430 total files identified)

### Phase 2: Infrastructure
- [ ] Create local save/load system to replace database
- [ ] Implement local distributed object registry (replace Astron functionality)
- [ ] Add offline mode detection and handling

### Phase 3: Core Systems Migration
- [ ] Migrate avatar management from UD to client
- [ ] Migrate zone/district management from AI to client
- [ ] Migrate quest system from AI to client
- [ ] Migrate battle system from AI to client

### Phase 4: NPC and AI Systems
- [ ] Migrate NPC AI from server to client
- [ ] Migrate Cog AI from server to client
- [ ] Migrate Pet AI from server to client
- [ ] Migrate building/suit building from server to client

### Phase 5: Social Systems (Remove or Mock)
- [ ] Remove or mock friends system
- [ ] Remove or mock parties system
- [ ] Remove or mock mail system
- [ ] Remove news system or make it local

### Phase 6: Activities and Minigames
- [ ] Update fishing to work locally
- [ ] Update golf to work locally
- [ ] Update racing to work locally
- [ ] Add AI opponents or remove multiplayer requirements

### Phase 7: Cleanup
- [ ] Remove Astron binaries and configuration
- [ ] Remove all server startup scripts
- [ ] Update launcher to not require servers
- [ ] Remove network communication code
- [ ] Clean up unused imports and files

## Files to Migrate or Remove

### AI Files (Server-side game logic)
**Total: 396 files** that need to be merged into client or removed:
- `otp/ai/*.py` (25 files)
- `otp/*AI.py` across modules (25 files)  
- `toontown/ai/*.py` (16 files)
- `toontown/*/Distributed*AI.py` (321 files across all game modules)
- See SERVER_FILES_INVENTORY.md for complete list

### UberDog Files (Global server logic)
**Total: 34 files** that need to be merged into client or removed:
- `otp/*UD.py` across modules (20 files)
- `toontown/uberdog/*.py` (9 files)
- `toontown/*/Distributed*UD.py` (5 files)
- See SERVER_FILES_INVENTORY.md for complete list

### Repository Files (Connection logic)
These files need significant modification:
- `toontown/distributed/ToontownClientRepository.py`
- `toontown/distributed/ToontownInternalRepository.py`
- `toontown/ai/ToontownAIRepository.py`
- `toontown/uberdog/ToontownUDRepository.py`

### Server Scripts and Configuration
These can be removed in final phase:
- `scripts/run_astron.py`
- `scripts/start_astron_server.bat`
- `scripts/start_uberdog_server.bat`
- `scripts/start_*_ai_server.bat`
- `astron/` directory

## Configuration Changes

Add to `etc/Configrc.prc`:
```
# Single-player mode (removes server requirements)
want-single-player 1
```

## Testing Strategy

For each phase:
1. Implement changes in a feature branch
2. Test that existing functionality still works
3. Test that new local functionality works
4. Merge to development branch
5. Proceed to next phase

## Estimated Effort

- **Phase 1**: 1-2 days
- **Phase 2**: 1-2 weeks
- **Phase 3**: 2-3 weeks
- **Phase 4**: 2-3 weeks
- **Phase 5**: 1 week
- **Phase 6**: 1-2 weeks
- **Phase 7**: 1 week

**Total**: 8-13 weeks of dedicated development time

## Risks

1. **Feature Loss**: Many social features may need to be removed
2. **Complexity**: The distributed object system is deeply integrated
3. **Testing**: Difficult to test all code paths and interactions
4. **Maintenance**: Significant ongoing maintenance as features are migrated

## Alternatives Considered

1. **Keep Current Architecture**: Maintain client-server setup for local play
2. **Replace Astron**: Use OtpGo or another lightweight alternative
3. **Hybrid Approach**: Keep servers running locally but simplify architecture

## Recommendations

Given the scope and complexity, we recommend:
1. Start with Phase 1 to prepare infrastructure
2. Evaluate feasibility after Phase 2
3. Consider hybrid approach or Astron alternatives
4. Focus on making local server setup easier rather than removing it entirely
