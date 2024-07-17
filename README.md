# Arthur's Adventures

A terminal-based rogue-like where you play Arthur, a young man who leaves home in search of adventure, fame and glory!

Journey through the world of Avalon to Camelot, raise through the ranks of the nobility and maybe even become king...

Well that's the dream - let's see how we get on... 🤣

## Goals

- A simple but playable game
- A world measuring 80 by 25, each element being a map also 80 x 25
  - Total world size of 6400 * 625 = 4,000,000 tiles!
  - Only certain world locations are pre-defined:
    - Home at center of the world 40, 13
    - Camelot - should consist of multiple world locations (4x4?)
    - ???
  - Each world location (map):
    - Is only generated when first visited
    - Has a terrain type - default "forest"
    - May or may not have a yaml file definition
    - Yaml file can define attributes and map elements
    - Maps smaller than the desired size are centered within the full map space
      - e.g. a map data block that defines a single 10x10 building will be located centrally on a wider 80,25 map
    - Each map should have a single path that links to the next world location
      - Other ways of reaching other locations may be possible - i.e. through the forest but having a single path
        gaureentees that a route will exist to every world location and the player shouldn't get trapped
    - Paths can either be explicitly defined in the map data file or randomly generated
      When being generated we should examine the paths at the edge of neighbouring maps and ensure the generated paths
      connect to those locations
    - Remaining map tiles are filled randomly according to terrain type
    - Doors should generate a message when entering
- Combat
  - Melee weapons only
  - Single weapon, single armour
- Items
  - Weapons
  - Armour
  - Health potions
  - Gold
  - Gems
- Merchants
  - Blacksmith - for weapons and armour
  - Herbalist - for health potions / healing
- Levelling
  - Killing enemies gives XP
  - XP gives prestige ranks - loosely follow the Imperial ranks from Elite
    - Outsider
    - Serf
    - Master
    - Squire
    - Knight
    - Lord
    - Viscount
    - Earl
    - Duke
    - King

## To Do

- [x] Core UI layout
- [x] Tileset
- [x] Core map generation
- [x] Player movement
- [x] Message log (welcome message and then message player location on each move)
- [ ] Map design
  - [ ] Home
  - [ ] Dark forrest
  - [ ] Camelot
- [ ] Movement between maps
- [ ] Refactor input handling
