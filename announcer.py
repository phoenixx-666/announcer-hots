# -*- coding: utf-8 -*-
from collections import OrderedDict
import re
import sys


if not (3 <= len(sys.argv) <= 4):
  print u'Usage: python {} <conversation_strings_file> <search_string> [output_file]'.format(sys.argv[0])

  
input_filename = sys.argv[1]
search_string = sys.argv[2]
output_file = sys.argv[3] if len(sys.argv) == 4 else '{}.txt'.format(search_string)


WORDS = {
  # Player
  'start': u"'''Start of a Match'''",
    'spawn': u'Players spawning',
    'spawnsame': u'Players spawning (playing as the same hero)',
    'countdown': u'Countdown',
    'gamestart': u'Battle begins',
  'talents': u"'''Talents Unlocked'''",
  'abandon': u"'''Player Abandons'''",
  'rejoin': u"'''Player Rejoins'''",
  'kill': u"'''Player Kills'''",
    '2kill': 'Double kill',
    '3kill': 'Triple kill',
    '4kill': 'Quadruple kill',
    'megakill': 'Mega kill',
    '6kill': 'Sextuple kill',
    '7kill': 'Seven kill',
    '8kill': 'Eight kill',
    '9kill': 'Nine kill',
    '10kill': 'Ten kill',
    'firstblood': 'First blood',
  'death': u"'''Player Deaths'''",
    'deathkillspree': 'Death on a killing spree',
    'deathkillspreeally': 'Ally death on a killing spree',
  'teamwipe': u"'''Enemy Team Wiped'''",
  'spree': u"'''Killing Spree'''",
    'spree5': u'Tier 1<br/>(5 takedowns)',
    'spree10': u'Tier 2<br/>(10 takedowns)',
    'spree15': u'Tier 3<br/>(15 takedowns)',
    'spree20': u'Tier 4<br/>(20 takedowns)',
  'fortdestroy': u"'''Enemy [[Fort]] destroyed'''",
  'keepdestroy': u"'''Enemy [[Keep]] destroyed'''",
  'fortlost': u"'''Own [[Fort]] lost'''",
  'keeplost': u"'''Own [[Keep]] lost'''",
  'core': u"'''[[Core]] is under attack'''",
  'victory': u"'''Victory'''",
  'defeat': u"'''Defeat'''",
  'mvpscreen': u"'''MVP Screen'''",
    'mvp': u'Announcing the MVP',
    'epic': u'A player gets 3 commendations',
    'legendary': u'A player gets 7 commendations',

  # Draft Intro Map
  'draftmap': u"'''Draft Map'''",

  # Observer
  'gamestartobs': u"'''Start of a Match'''",
  'killobs': u"'''Player Kills'''",
  'firstbloodobs': u"'''First blood'''",
    'firstblood_blue': u'Blue team',
    'firstblood_red': u'Red team',
  'teamwipeobs': u"'''Team Wiped'''",
    'teamwipe_blue': u'Blue team',
    'teamwipe_red': u'Red team',
  'fortdestroyobs': u"'''[[Fort]] destroyed'''",
    'fortdestroy_blue': u'Blue team',
    'fortdestroy_red': u'Red team',
  'keepdestroyobs': u"'''[[Keep]] destroyed'''",
    'keepdestroy_blue': u'Blue team',
    'keepdestroy_red': u'Red team',
  'coreobs': u"'''[[Core]] is under attack'''",
    'core_blue': u'Blue team',
    'core_red': u'Red team',
  'victoryobs': u"'''Victory'''",
    'victory_blue': u'Blue team',
    'victory_red': u'Red team',

  # Brawl
  'chooseherobrawl': u"'''Hero Selection'''",
  'crazymode': u'Only One Hero Available',
  'timerunningout': u"'''Time Running Out'''",
  'fountaindestroyed': u"'''[[Healing Fountain]] Destroyed'''",
  'fountainlost': u"'''Healing Fountain Lost'''",
  'round1win': u"'''Round One: Victory'''",
  'round1loss': u"'''Round One: Defeat'''",
  'round2roundloss': u"'''Round Two: Round Defeat'''",
  'round2matchloss': u"'''Round Two: Match Defeat'''",
  'round2roundwin': u"'''Round Two: Round Victory'''",
  'round2matchwin': u"'''Round Two: Match Victory'''",
  'round3win': u"'''Round Three: Victory'''",
  'round3loss': u"'''Round Three: Defeat'''",

  # Brawl Observer
  'fountaindestroyedobs': u"'''[[Healing Fountain]] Destroyed'''",
    'fountaindestroyed_blue': u'Blue team',
    'fountaindestroyed_red': u'Red team',
  'round1winobs': u"'''Round One Victory'''",
    'round1win_blue': u'Blue team',
    'round1win_red': u'Red team',
  'round2roundwinobs': u"'''Round Two: Round Victory'''",
    'round2roundwin_blue': u'Blue team',
    'round2roundwin_red': u'Red team',
  'round2matchwinobs': u"'''Round Two: Match Victory'''",
    'round2matchwin_blue': u'Blue team',
    'round2matchwin_red': u'Red team',
  'round3winobs': u"'''Round Three Victory'''",
    'round3win_blue': u'Blue team',
    'round3win_red': u'Red team',

  # Unrecognized Entries
  'unknown': u"'''Unknown'''\n\n<small>(Possible a map objective, a newly introduced feature, an unused or an irregularly named phrase)</small>",
}


SUBCAT = u"<small>''{}''</small>"


def translate(key):
  res = WORDS.get(key)
  return res if res else key

  
STRUCT = OrderedDict([
  ('start', OrderedDict([
      ('spawn', 'HeroSelect'),
      ('spawnsame', 'HeroSelectPlayer'),
      ('countdown', OrderedDict([
          ('ctdremain', 'CountdownRemain'),
          ('ctd10', 'Countdown10sec'),
          ('ctd5', 'Countdown5sec'),
          ('ctd4', 'Countdown4sec'),
          ('ctd3', 'Countdown3sec'),
          ('ctd2', 'Countdown2sec'),
          ('ctd1', 'Countdown1sec'),
        ])),
      ('gamestart', 'GameStart'),
    ])),
  ('talents', 'TalentUnlock'),
  ('abandon', 'PlayerAbandon'),
  ('rejoin', 'PlayerRejoin'),
  ('kill', OrderedDict([
      ('_kill', 'HeroKill'),
      ('2kill', 'DoubleKill'),
      ('3kill', 'TripleKill'),
      ('4kill', 'FourKill'),
      ('megakill', 'MegaKill'),
      ('6kill', 'SixKill'),
      ('7kill', 'SevenKill'),
      ('8kill', 'EightKill'),
      ('9kill', 'NineKill'),
      ('10kill', 'TenKill'),
      ('firstblood', 'FirstBloodAlly'),
    ])),
  ('death', OrderedDict([
      ('_death', 'HeroSlain'),
      ('deathkillspree', 'SpreeEnd'),
      ('deathkillspreeally', 'SpreeEnd_Ally'),
    ])),
  ('teamwipe', 'TeamKill'),
  ('spree', OrderedDict([
      ('spree5', 'SpreeStart'),
      ('spree10', 'SpreeFirstUpgrade'),
      ('spree15', 'SpreeThirdUpgrade'),
      ('spree20', 'SpreeMax'),
    ])),
  ('fortdestroy', 'OutpostDestroy'),
  ('keepdestroy', 'KeepDestroy'),
  ('fortlost', 'OutpostLost'),
  ('keeplost', 'KeepLost'),
  ('core', 'CastleAttackAlly'),
  ('victory', 'EndingWin'),
  ('defeat', 'EndingLose'),  
  ('mvpscreen', OrderedDict([
      ('mvp', 'MVP'),
      ('epic', 'Epic'),
      ('legendary', 'Legendary'),
    ])),

  # Draft Intro Map
  ('draftmap', 'Draft_Map'),

  # Observer
  ('gamestartobs', 'HeroSelect_Observer'),
  ('killobs', 'Kill_Observer'),
  ('firstbloodobs', OrderedDict([      
      ('firstblood_blue', 'FirstBlood_Blue'),
      ('firstblood_red', 'FirstBlood_Red'),
    ])),
  ('teamwipeobs', OrderedDict([
      ('teamwipe_blue', 'TeamKill_Blue'),
      ('teamwipe_red', 'TeamKill_Red'),
    ])),
  ('fortdestroyobs', OrderedDict([
      ('fortdestroy_blue', 'OutpostDestroy_Blue'),
      ('fortdestroy_red', 'OutpostDestroy_Red'),
    ])),
  ('keepdestroyobs', OrderedDict([
      ('keepdestroy_blue', 'KeepDestroy_Blue'),
      ('keepdestroy_red', 'KeepDestroy_Red'),
    ])),
  ('coreobs', OrderedDict([
    ('core_blue', 'CastleAttack_Blue'),
    ('core_red', 'CastleAttack_Red'),
    ])),
  ('victoryobs', OrderedDict([
    ('victory_blue', 'Ending_Blue'),
    ('victory_red', 'Ending_Red'),
    ])),

  # Brawl
  ('chooseherobrawl', OrderedDict([
    ('_chooseherobrawl', 'ChooseHero'),
    ('crazymode', 'CrazyMode'),
    ])),
  ('timerunningout', 'TimeRunningOut'),
  ('fountaindestroyed', 'FountainDestroyed_Enemy'),
  ('fountainlost', 'FountainDestroyed_Ally'),
  ('round1win', 'RoundOne_Victory'),
  ('round1loss', 'RoundOne_Loss'),
  ('round2roundloss', 'RoundTwo_LossFirst'),
  ('round2matchloss', 'RoundTwo_LossSweep'),
  ('round2roundwin', 'RoundTwo_VictoryFirst'),
  ('round2matchwin', 'RoundTwo_VictorySweep'),
  ('round3win', 'RoundThree_Victory'),
  ('round3loss', 'RoundThree_Loss'),

  # Brawl Observer
  ('fountaindestroyedobs', OrderedDict([
    ('fountaindestroyed_blue', 'FountainDestroyed_Blue'),
    ('fountaindestroyed_red', 'FountainDestroyed_Red'),
  ])),
  ('round1winobs', OrderedDict([
    ('round1win_blue', 'RoundOne_Victory_Blue'),
    ('round1win_red', 'RoundOne_Victory_Red'),
  ])),
  ('round2roundwinobs', OrderedDict([
    ('round2roundwin_blue', 'RoundTwo_VictoryFirst_Blue'),
    ('round2roundwin_red', 'RoundTwo_VictoryFirst_Red'),
  ])),
  ('round2matchwinobs', OrderedDict([
    ('round2matchwin_blue', 'RoundTwo_VictorySweep_Blue'),
    ('round2matchwin_red', 'RoundTwo_VictorySweep_Red'),
  ])),
  ('round3winobs', OrderedDict([
    ('round3win_blue', 'RoundThree_Victory_Blue'),
    ('round3win_red', 'RoundThree_Victory_Red'),
  ])),

  # Unrecognized Entries
  ('unknown', None),
])


REGEX_TEMPLATE = ur'{}\d+'
REGEX = re.compile(ur'^VoiceOver/([A-Za-z\d]+)/([A-Za-z\d_]+)=(.*)$')
ALL_REGEX = {}
ROWSPAN_TEMPLATE = 'rowspan="{}" '
CATEGORY_TEMPLATE = u'| {rowspan}align="center" | {cat_name}\n'
SIMPLE_ROW_TEMPLATE = u"""| colspan="2" |{quote}
|[[File:{file_name}]]
|
|-
"""
SUBCATEGORY_TEMPLATE = u"""| align="right" width="50px" {rowspan}|<small>''{subcat_name}''</small>
"""
SUBCATEGORY_ROW_TEMPLATE = u"""|{quote}
|[[File:{file_name}]]
|
|-
"""

def create_regex(struct):
  for key, val in struct.items():
    if isinstance(val, OrderedDict):
      create_regex(val)
    elif isinstance(val, basestring):
      regex = struct[key] = re.compile(REGEX_TEMPLATE.format(val))
      if regex:
        ALL_REGEX[key] = regex
    

create_regex(STRUCT)

with open(input_filename, 'r') as f:
  lines = map(lambda s: s.rstrip('\n').rstrip('\r'), f.readlines())

ALL_QUOTES = {}

for line in lines:
  m = REGEX.match(line)
  if not m:
    continue
    
  subj = m.group(1)
  if search_string != subj:
    continue
    
  quote_key, quote = m.group(2), m.group(3)
  for key, regex in ALL_REGEX.items():
    if regex.match(quote_key):
      quote_list = ALL_QUOTES.setdefault(key, [])
      quote_list.append((quote, '{}_{}.ogg'.format(subj, quote_key)))
      break
  else:
    quote_list = ALL_QUOTES.setdefault('unknown', [])
    quote_list.append((quote, '{}_{}.ogg'.format(subj, quote_key)))

wiki = u"""{| class="wikitable" width="1300px"
! width="200px" | Event
! width="500px" colspan="2" | Quote
! width="300px" | Audio
! width="300px" | Background
|-
"""

for key, val in STRUCT.items():
  if isinstance(val, OrderedDict):
    rowspan = 0
    wiki_ = u''
    for key_, val_ in val.items():
      if isinstance(val_, OrderedDict):
        rowspan_ = 0
        wiki__ = u''
        for key__, val__ in val_.items():
          quotes = ALL_QUOTES.get(key__)
          if not quotes:
            continue
          for quote, quote_file in quotes:
            wiki__ += SUBCATEGORY_ROW_TEMPLATE.format(quote=quote, file_name=quote_file)
            rowspan_ += 1
            rowspan += 1
        if rowspan_:
          rowspan_ = ROWSPAN_TEMPLATE.format(rowspan_) if rowspan_ > 1 else ''
          wiki_ += SUBCATEGORY_TEMPLATE.format(rowspan=rowspan_, subcat_name=translate(key_)) + wiki__
      else:
        quotes = ALL_QUOTES.get(key_)
        if not quotes:
          continue
        if key_[0] == '_':
          for quote, quote_file in quotes:
            wiki_ += SIMPLE_ROW_TEMPLATE.format(quote=quote, file_name=quote_file)
            rowspan += 1
        else:
          rowspan_ = ROWSPAN_TEMPLATE.format(len(quotes)) if len(quotes) > 1 else ''
          wiki_ += SUBCATEGORY_TEMPLATE.format(rowspan=rowspan_, subcat_name=translate(key_))
          for quote, quote_file in quotes:
            wiki_ += SUBCATEGORY_ROW_TEMPLATE.format(quote=quote, file_name=quote_file)
            rowspan += 1
    
    if rowspan:
      rowspan = ROWSPAN_TEMPLATE.format(rowspan) if rowspan > 1 else ''
      wiki += CATEGORY_TEMPLATE.format(rowspan=rowspan, cat_name=translate(key)) + wiki_
  else:
    quotes = ALL_QUOTES.get(key)
    if not quotes:
      continue
    rowspan = ROWSPAN_TEMPLATE.format(len(quotes)) if len(quotes) > 1 else ''
    wiki += CATEGORY_TEMPLATE.format(rowspan=rowspan, cat_name=translate(key))
    for quote, quote_file in quotes:
      wiki += SIMPLE_ROW_TEMPLATE.format(quote=quote, file_name=quote_file)

wiki += u'|}'

file = open(output_file, 'w')
file.write(wiki)
file.close()