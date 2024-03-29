import argparse
import json
import random
from tqdm import tqdm
import pandas as pd

gimmicks = [
    {
        'gimmick': 'stops',
        'gimmick_type': 'stops'
    },
    {
        'gimmick': 'stop',
        'gimmick_type': 'stops'
    },
    {
        'gimmick': 'stps',
        'gimmick_type': 'stops'
    },
    {
        'gimmick': 'stp',
        'gimmick_type': 'stops'
    },
    {
        'gimmick': 'speed changes',
        'gimmick_type': 'speeds',
    },
    {
        'gimmick': 'speeds',
        'gimmick_type': 'speeds',
    },
    {
        'gimmick': 'fakes',
        'gimmick_type': 'fakes',
    },
    {
        'gimmick': 'fks',
        'gimmick_type': 'fakes',
    },
    {
        'gimmick': 'warps',
        'gimmick_type': 'warps',
    },
    {
        'gimmick': 'wrps',
        'gimmick_type': 'warps',
    },
    {
        'gimmick': 'scrolls',
        'gimmick_type': 'scrolls',
    },
    {
        'gimmick': 'scrlls',
        'gimmick_type': 'scrolls',
    },
    {
        'gimmick': 'Sc',
        'gimmick_type': 'scrolls',
    },
    {
        'gimmick': 'delays',
        'gimmick_type': 'delays',
    },
    {
        'gimmick': 'dlys',
        'gimmick_type': 'delays',
    },
    {
        'gimmick': 'vanish',
        'gimmick_type': 'vanish',
    },
    {
        'gimmick': 'vnsh',
        'gimmick_type': 'vanish',
    },
    {
        'gimmick': 'sudden',
        'gimmick_type': 'sudden',
    },
    {
        'gimmick': 'sddn',
        'gimmick_type': 'sudden',
    },
    {
        'gimmick': 'hidden',
        'gimmick_type': 'hidden',
    },
    {
        'gimmick': 'hdn',
        'gimmick_type': 'hidden',
    }

]

steptypes_long = [
    {
        'stepstype': 'pump_single',
        'stepstype_label': 'pump_single',
    },
    {
        'stepstype': 'singles',
        'stepstype_label': 'pump_single',
    },
    {
        'stepstype': 'single',
        'stepstype_label': 'pump_single',
    },
    {
        'stepstype': 'one pad',
        'stepstype_label': 'pump_single',
    },
    {
        'stepstype': 'pump_double',
        'stepstype_label': 'pump_double',
    },
    {
        'stepstype': 'doubles',
        'stepstype_label': 'pump_double',
    },
    {
        'stepstype': 'double',
        'stepstype_label': 'pump_double',
    },
    {
        'stepstype': 'two pads',
        'stepstype_label': 'pump_double',
    },
    {
        'stepstype': 'pump_halfdouble',
        'stepstype_label': 'pump_halfdouble',
    },
    {
        'stepstype': 'halfdouble',
        'stepstype_label': 'pump_halfdouble',
    },
    {
        'stepstype': 'pump_couple',
        'stepstype_label': 'pump_couple',
    },
    {
        'stepstype': 'couple',
        'stepstype_label': 'pump_couple',
    },
    {
        'stepstype': 'pump_routine',
        'stepstype_label': 'pump_routine',
    },
    {
        'stepstype': 'routine',
        'stepstype_label': 'pump_routine',
    },
]

steptypes_short = [
    {
        'stepstype': 's',
        'stepstype_label': 'pump_single',
    },
    {
        'stepstype': 'd',
        'stepstype_label': 'pump_double',
    },
    {
        'stepstype': 'hd',
        'stepstype_label': 'pump_halfdouble',
    },
    {
        'stepstype': 'c',
        'stepstype_label': 'pump_couple',
    },
    {
        'stepstype': 'r',
        'stepstype_label': 'pump_routine',
    },
]


def parse_args():

    parser = argparse.ArgumentParser(description='Corpus creator')

    parser.add_argument('--levels', type=str, default='data/raw/levels.json',
                        help='Path to levels file')
    parser.add_argument('--mixes', type=str, default='data/raw/mixes.json',
                        help='Path to mixes file')
    parser.add_argument('--tunes', type=str, default='data/raw/tunes.json',
                        help='Path to tunes file')

    parser.add_argument('--no-samples', type=int, default=100000,
                        help='Number of samples to generate (default: 100,000)')

    parser.add_argument('--output', type=str, default='data/corpus/train.json',
                        help='Path to output file')

    return vars(parser.parse_args())


def uniq(levels: str, mixes: str, tunes: str, **kwargs):
    levels_df = pd.read_json(levels)
    mixes_df = pd.read_json(mixes)
    tunes_df = pd.read_json(tunes)

    # get list of column "name" from mixes_df
    mix_names = mixes_df['name'].tolist()

    # get list of column "name" from tunes_df
    tune_names = tunes_df['name'].tolist()

    tune_artists = tunes_df['artist'].tolist()

    level_stepstypes = levels_df['stepstype'].tolist()
    level_credits = levels_df['credit'].tolist()

    # make all lists unique
    mix_names = list(set(mix_names))
    tune_names = list(set(tune_names))
    tune_artists = list(set(tune_artists))
    level_stepstypes = list(set(level_stepstypes))
    level_credits = list(set(level_credits))

    # remove none values
    mix_names = [x for x in mix_names if x is not None]
    tune_names = [x for x in tune_names if x is not None]
    tune_artists = [x for x in tune_artists if x is not None]
    level_stepstypes = [x for x in level_stepstypes if x is not None]
    level_credits = [x for x in level_credits if x is not None]

    # remove any string starting with "Lv." in level_credits
    level_credits = [x for x in level_credits if not x.startswith('Lv.')]

    level_stepstypes.extend(['singles', 'doubles'])

    return mix_names, tune_names, tune_artists, level_stepstypes, level_credits


def gen_slot(slot_name: str, slot_value: str, prompt_prior: str, prompt_after: str = '', sep_prior: str = " ", sep_after: str = ""):
    try:
        slot_value_len = len(slot_value)
    except:
        print(slot_value)
        raise Exception('slot_value is not a string')
    prompt_prior_len = len(prompt_prior)
    prompt_after_len = len(prompt_after)
    sep_prior_len = len(sep_prior)
    sep_after_len = len(sep_after)
    return {
        'slot': {
            slot_name: f'{slot_value}',
        },
        'gen_text': {
            slot_name: f'{prompt_prior}{sep_prior}{slot_value}{sep_after}{prompt_after}'
        },
        'text': f'{prompt_prior}{sep_prior}{slot_value}{sep_after}{prompt_after}',
        'positions':
        {
            slot_name: {
                'begin': prompt_prior_len + sep_prior_len,
                'end': prompt_prior_len + sep_prior_len + slot_value_len,
            }
        }
    }


def glue_slots(slot1, slot2, text_slot_sep: str):
    text = f'{slot1["text"]}{text_slot_sep}{slot2["text"]}'
    gen_text = f'{slot1["gen_text"]}{text_slot_sep}{slot2["gen_text"]}'
    new_slot = {
        'slot': {
            **slot1['slot'],
            **slot2['slot']
        },
        'gen_text': gen_text,
        'text': text,
    }

    # update positions of slot2, so that each begin and end is shifted by the length of the text of slot1
    for slot2_key in slot2['positions'].keys():
        slot2['positions'][slot2_key]['begin'] += len(
            slot1['text']) + len(text_slot_sep)
        slot2['positions'][slot2_key]['end'] += len(
            slot1['text']) + len(text_slot_sep)

    new_slot['positions'] = {
        **slot2['positions'],
        **slot1['positions']
    }

    return new_slot


def prompt_tune_name(tune_name: str):

    prompt_choices = [
        'tune',
        'song',
        'title',
        '',
        'chart',
        'Play a tune',
        'Choose a song',
        'Find the title',
        'Select the chart',
        'Pick the melody',
        'Search for the track',
        'Listen to the tune',
        'Look up the song',
        'Retrieve the melody',
        'Get the chart'
    ]
    prompt = random.choice(prompt_choices)

    slot = gen_slot('tune', tune_name, prompt)
    # get a random choice from the list
    return slot


def prompt_mix_name(mix_name: str):
    prompt_choices = [
        'mix',
        'album',
        'release',
        'folder',
        '',
        'Play the mix',
        'Choose the album',
        'Find the release',
        'Select the folder',
        'Pick the playlist',
        'Search for the mix',
        'Listen to the album',
        'Look up the release',
        'Retrieve the playlist',
        'Get the folder'
    ]
    prompt = random.choice(prompt_choices)

    slot = gen_slot('mix', mix_name, prompt)
    # get a random choice from the list
    return slot


def prompt_artist_name(artist_name: str):
    prompt_choices = [
        'artist',
        'by',
        '',
        'from',
    ]
    prompt = random.choice(prompt_choices)

    slot = gen_slot('artist', artist_name, prompt)
    # get a random choice from the list
    return slot


def prompt_credit_name(credit_name: str):
    prompt_choices = [
        'credit',
        'credits',
        'steps by',
        'steps creator',
        'stepmaker',
        '',
    ]

    prompt = random.choice(prompt_choices)
    slot = gen_slot('credit', credit_name, prompt)
    # get a random choice from the list
    return slot


def prompt_stepstype_name(stepstype_name: str, stepstype_label: str):

    prompt_choices = [
        'steps type',
        'steps',
        'stepstype',
        'style',
        '',
    ]

    prompt = random.choice(prompt_choices)
    slot = gen_slot(stepstype_label, stepstype_name, prompt)
    # get a random choice from the list
    return slot


def prompt_meter(meter: str):
    prompt_choices = [
        'meter',
        'lvl',
        'level',
    ]

    prompt = random.choice(prompt_choices)
    slot = gen_slot('meter', meter, prompt)
    return slot


def prompt_meter_less_than(meter: str):
    prompt_choices_before = [
        'meter <',
        'lvl <',
        'level <',
        '<',
        'level less than',
        'meter less than',
        'level lower than',
        'meter lower than',
        'lvl less than',
    ]

    prompt_choices_after = [
        '-'
    ]
    list_choices = prompt_choices_before + prompt_choices_after
    prompt = random.choice(list_choices)
    if prompt in prompt_choices_after:
        slot = gen_slot('meter_lower_than', meter, '', prompt, '', '')
    else:
        slot = gen_slot('meter_lower_than', meter, prompt)
    return slot


def prompt_meter_greater_than(meter: str):
    prompt_choices_before = [
        'meter >',
        'lvl >',
        'level >',
        '>',
        'level greater than',
        'meter greater than',
        'level higher than',
        'meter higher than',
        'lvl greater than',
    ]

    prompt_choices_after = [
        '+'
    ]
    list_choices = prompt_choices_before + prompt_choices_after
    prompt = random.choice(list_choices)
    if prompt in prompt_choices_after:
        slot = gen_slot('meter_greater_than', meter, '', prompt, '', '')
    else:
        slot = gen_slot('meter_greater_than', meter, prompt)
    return slot


def prompt_meter_stepstype_name(meter: str, stepstype_name: str, stepstype_label: str, slot_name: str = 'meter'):
    slot_meter = gen_slot(slot_name, meter, '', '', '', '')
    slot_stepstype = gen_slot(stepstype_label, stepstype_name, '', '', '', '')
    sep_choices = [
        ' ',
        ' lvl. ',
        ' lvl ',
    ]
    slot = glue_slots(
        slot_stepstype,
        slot_meter,
        random.choice(sep_choices)
    )

    return slot


def prompt_meter_greater_than_stepstype(meter: str, stepstype_name: str, stepstype_label: str):
    slot_meter = gen_slot('meter_greater_than', meter, '', '+', '', '')
    slot_stepstype = gen_slot(stepstype_label, stepstype_name, '', '', '', '')
    sep_choices = [
        ' ',
        ' lvl. ',
        ' lvl ',
    ]
    slot = glue_slots(
        slot_stepstype,
        slot_meter,
        random.choice(sep_choices)
    )

    return slot


def prompt_meter_lower_than_stepstype(meter: str, stepstype_name: str, stepstype_label: str):
    slot_meter = gen_slot('meter_lower_than', meter, '', '-', '', '')
    slot_stepstype = gen_slot(stepstype_label, stepstype_name, '', '', '', '')
    sep_choices = [
        ' ',
        ' lvl. ',
        ' lvl ',
    ]
    slot = glue_slots(
        slot_stepstype,
        slot_meter,
        random.choice(sep_choices)
    )

    return slot


def prompt_meter_stepstype_range(meter_low: str, meter_high: str, stepstype_name: str, stepstype_label: str):
    low = prompt_meter_stepstype_name(
        meter_low, stepstype_name, stepstype_label, 'meter_greater_than')
    slot_high = gen_slot('meter_lower_than', meter_high, '', '', '', '')

    sep_choices = [
        ' to ',
        ' - ',
        '-',
    ]

    slot = glue_slots(
        low,
        slot_high,
        random.choice(sep_choices)
    )

    return slot


def prompt_bpm(bpm: str, slot_name: str = 'bpm'):

    prompt_choices = [
        'bpm',
        'bpms',
    ]

    prompt = random.choice(prompt_choices)
    slot = gen_slot(slot_name, bpm, prompt)
    return slot


def prompt_bpm_less_than(bpm: str):

    prompt_choices = [
        'bpm <',
        'bpm less than',
        'bpm <',
    ]

    prompt = random.choice(prompt_choices)
    slot = gen_slot('bpm_lower_than', bpm, prompt)
    return slot


def prompt_bpm_greater_than(bpm: str):

    prompt_choices = [
        'bpm >',
        'bpm greater than',
        'bpm >',
    ]

    prompt = random.choice(prompt_choices)
    slot = gen_slot('bpm_greater_than', bpm, prompt)
    return slot


def prompt_bpm_range(bpm_low: str, bpm_high: str):
    low = prompt_bpm(bpm_low, 'bpm_greater_than')
    slot_high = gen_slot('bpm_lower_than', bpm_high, '', '', '', '')

    sep_choices = [
        ' to ',
        ' - ',
        '-',
    ]

    slot = glue_slots(
        low,
        slot_high,
        random.choice(sep_choices)
    )

    return slot


def prompt_gimmick(gimmick: str, gimmick_type: str):
    return gen_slot(gimmick_type, gimmick, '', '', '', '')


class ListIterator:

    def __init__(self, list):
        self.list = list
        self.it = 0

    def next(self):
        item = self.list[self.it]
        self.it = (self.it + 1) % len(self.list)
        return item


def strip_string(string: str, min_number_chars: int = 3):
    # strip string so that its number of chars ranges between 3 and a random number between 3 and the length of the string.
    # if the legnth of the string is 3 or less, don't strip it
    if len(string) > min_number_chars:
        a = string[:random.randint(
            min_number_chars, len(string)-1)]

        # remove trailing spaces
        a = a.rstrip()
        # remove specials unicode chars
        a = a.encode('ascii', 'ignore').decode('ascii')
        return a
    return string


def create_prompts(no_samples: int, mix_names, tune_names, tune_artists, level_stepstypes, level_credits, **kwargs):

    mixes = ListIterator(mix_names)
    tunes = ListIterator(tune_names)
    artists = ListIterator(tune_artists)
    stepstypes_long_it = ListIterator(steptypes_long)
    stepstypes_short_it = ListIterator(steptypes_short)
    credits = ListIterator(level_credits)
    # create a random int generator between 0 and 99 for levels. it won't be a list iterator
    def levels(): return str(random.randint(0, 99))
    def bpms(): return str(random.randint(50, 280))
    gmmcks = ListIterator(gimmicks)

    samples = []

    for i in tqdm(range(no_samples)):
        # get a random choice from the list
        mix_name = mixes.next()
        tune_name = tunes.next()
        artist_name = artists.next()
        credit_name = credits.next()

        min_number_chars = 3
        mix_name = strip_string(mix_name, min_number_chars)
        tune_name = strip_string(tune_name, min_number_chars)
        artist_name = strip_string(artist_name, min_number_chars)
        credit_name = strip_string(credit_name, min_number_chars)

        stepstype_name_long = stepstypes_long_it.next()
        stepstype_name_short = stepstypes_short_it.next()

        lvls = [levels(), levels()]
        lvls.sort()
        level1, level2 = lvls

        bps = [bpms(), bpms()]
        bps.sort()
        bpm1, bpm2 = bps
        gimmick = gmmcks.next()

        prompt_list = [
            random.choice([
                prompt_mix_name(mix_name),
                prompt_tune_name(tune_name),
                prompt_artist_name(artist_name),
                prompt_credit_name(credit_name),
            ]),
            random.choice([
                prompt_stepstype_name(
                    stepstype_name_long['stepstype'], stepstype_name_long['stepstype_label']),
                prompt_meter(level1),
                prompt_meter_less_than(level1),
                prompt_meter_greater_than(level1),
                prompt_meter_stepstype_name(
                    level1, stepstype_name_long['stepstype'], stepstype_name_long['stepstype_label']),
                prompt_meter_stepstype_range(
                    level1, level2, stepstype_name_short['stepstype'], stepstype_name_short['stepstype_label']),
                prompt_meter_greater_than_stepstype(
                    level1, stepstype_name_short['stepstype'], stepstype_name_short['stepstype_label']),
                prompt_meter_lower_than_stepstype(
                    level1, stepstype_name_short['stepstype'], stepstype_name_short['stepstype_label']),

            ]),
            random.choice([
                prompt_bpm(bpm1),
                prompt_bpm_less_than(bpm1),
                prompt_bpm_greater_than(bpm1),
                prompt_bpm_range(bpm1, bpm2),
            ]),
            prompt_gimmick(gimmick['gimmick'], gimmick['gimmick_type']),
        ]

        # generate a list with up to 7 random numbers between 0 and 6 without repetition
        # this will be the order of the prompts
        # then sort it
        prompt_order = random.sample(range(4), random.randint(1, 4))

        # glue all prompts together using glue_slots
        prompt = prompt_list[prompt_order[0]]
        for i in range(1, len(prompt_order)):
            prompt = glue_slots(
                prompt,
                prompt_list[prompt_order[i]],
                ' '
            )

        samples.append(prompt)

    return samples


def main(no_samples: int, output: str, **kwargs):

    mix_names, tune_names, tune_artists, level_stepstypes, level_credits = uniq(
        **kwargs)

    samples = create_prompts(no_samples, mix_names, tune_names,
                             tune_artists, level_stepstypes, level_credits, **kwargs)

    # save samples list to json
    with open(output, 'w') as f:
        json.dump(samples, f, indent=4)
        print(f'Saved {len(samples)} samples to {output}')

    return


if __name__ == '__main__':
    args = parse_args()
    main(**args)
