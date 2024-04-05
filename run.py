import argparse
import json
import sys


def main():
    """
    Main function.
    """
    args = parse_args()
    config = parse_file(args.filename)
    keyboard = detect_keyboard(config)

    if keyboard is None:
        log("Failed to detect which keyboard this config file is for.")
        sys.exit(1)

    announce_plan(keyboard)
    new_config = map_config(config, keyboard)
    print_as_json(new_config)
    log("Done.")


def log(string):
    """
    Print string to stderr.
    """
    print(string, file=sys.stderr)


def parse_args():
    """
    Parse the arguments to the program.
    """
    parser = argparse.ArgumentParser(
        prog="VIA Mapper",
        description="This script maps between VIA configuration files for Keychron Q1 Pro and GMMK Pro.",
    )
    parser.add_argument("filename")
    return parser.parse_args()


def parse_file(filename):
    """
    Parse a VIA json config file.
    """
    data = None
    with open(filename, encoding="UTF-8") as f:
        data = json.load(f)
    return data


def detect_keyboard(config):
    """
    Detect whether the config is for the Keychron or GMMK.
    """
    key = "vendorProductId"
    if config[key] == KEYCHRON_INFO[key]:
        return "KEYCHRON"
    if config[key] == GMMK_INFO[key]:
        return "GMMK"
    return None


def announce_plan(keyboard):
    """
    Print which keyboard config was detected and which config will be
    generated.
    """
    if keyboard == "KEYCHRON":
        log("Detected Keychron Q1 Pro config.")
        log("Mapping to a GMMK Pro config...")
    elif keyboard == "GMMK":
        log("Detected GMMK Pro config.")
        log("Mapping to a Keychron Q1 Pro config...")


def map_config(config, keyboard):
    """
    Maps a config for a keyboard to the other keyboard's config.
    """
    is_keychron = keyboard == "KEYCHRON"
    keyboard_info = GMMK_INFO if is_keychron else KEYCHRON_INFO
    layer_size = len(GMMK_LAYER) if is_keychron else len(KEYCHRON_LAYER)
    fixes = KEYCHRON_FIXES if is_keychron else GMMK_FIXES
    from_layer = KEYCHRON_LAYER if is_keychron else GMMK_LAYER
    to_layer = GMMK_LAYER if is_keychron else KEYCHRON_LAYER
    mapping = get_mapping(from_layer, to_layer)
    return _map_config(config, keyboard_info, layer_size, mapping, fixes)


def _map_config(config, keyboard_info, layer_size, mapping, fixes):
    new_config = config.copy()
    new_config.update(keyboard_info)
    new_layers = [
        map_layer(layer, layer_size, mapping, fixes) for layer in config["layers"]
    ]
    new_config.update({"layers": new_layers})
    return new_config


def map_layer(layer, layer_size, mapping, fixes):
    new_layer = ["KC_NO" for i in range(0, layer_size)]
    for idx, new_idx in mapping.items():
        if layer[idx] == "KC_NO":
            continue
        key = layer[idx]
        new_layer[new_idx] = fixes[key] if key in fixes else key
    return new_layer


def print_as_json(config):
    """
    Prints the given config as json.
    """
    json_config = json.dumps(config, indent=2)
    print(json_config)


def argsort(seq):
    """
    Sort list but output indices instead of sorted list.
    """
    # https://stackoverflow.com/a/3382369/2445841
    return sorted(range(len(seq)), key=seq.__getitem__)


def get_mapping(old, new):
    mapping = dict()
    for i, key in enumerate(old):
        if key == "KC_NO":
            continue
        try:
            j = new.index(key)
            mapping[i] = j
        except ValueError:
            continue
    return mapping


KEYCHRON_LAYER = [
    "KC_ESC",
    "KC_F1",
    "KC_F2",
    "KC_F3",
    "KC_F4",
    "KC_F5",
    "KC_F6",
    "KC_F7",
    "KC_F8",
    "KC_F9",
    "KC_F10",
    "KC_F11",
    "KC_F12",
    "KC_PSCR",  # Default is KC_DEL. Changed to match.
    "KC_NO",
    "KC_MUTE",
    "KC_GRV",
    "KC_1",
    "KC_2",
    "KC_3",
    "KC_4",
    "KC_5",
    "KC_6",
    "KC_7",
    "KC_8",
    "KC_9",
    "KC_0",
    "KC_MINS",
    "KC_EQL",
    "KC_BSPC",
    "KC_NO",
    "KC_PGUP",
    "KC_TAB",
    "KC_Q",
    "KC_W",
    "KC_E",
    "KC_R",
    "KC_T",
    "KC_Y",
    "KC_U",
    "KC_I",
    "KC_O",
    "KC_P",
    "KC_LBRC",
    "KC_RBRC",
    "KC_BSLS",
    "KC_NO",
    "KC_PGDN",
    "KC_CAPS",
    "KC_A",
    "KC_S",
    "KC_D",
    "KC_F",
    "KC_G",
    "KC_H",
    "KC_J",
    "KC_K",
    "KC_L",
    "KC_SCLN",
    "KC_QUOT",
    "KC_NO",
    "KC_ENT",
    "KC_NO",
    "KC_HOME",
    "KC_LSFT",
    "KC_NO",
    "KC_Z",
    "KC_X",
    "KC_C",
    "KC_V",
    "KC_B",
    "KC_N",
    "KC_M",
    "KC_COMM",
    "KC_DOT",
    "KC_SLSH",
    "KC_NO",
    "KC_RSFT",
    "KC_UP",
    "KC_NO",
    "KC_LCTL",
    "KC_LGUI",
    "KC_LALT",
    "KC_NO",
    "KC_NO",
    "KC_NO",
    "KC_SPC",
    "KC_NO",
    "KC_NO",
    "KC_NO",
    "KC_RALT",
    "KC_FN",  # Default is MO(3). Changed to match.
    "KC_RCTL",
    "KC_LEFT",
    "KC_DOWN",
    "KC_RGHT",
]

GMMK_LAYER = [
    "KC_LSFT",
    "KC_MUTE",
    "KC_NO",
    "KC_LEFT",
    "KC_RCTL",
    "KC_RGHT",
    "KC_LCTL",
    "KC_F5",
    "KC_Q",
    "KC_TAB",
    "KC_A",
    "KC_ESC",
    "KC_Z",
    "KC_PGUP",
    "KC_GRV",
    "KC_1",
    "KC_W",
    "KC_CAPS",
    "KC_S",
    "KC_NO",
    "KC_X",
    "KC_PGDN",
    "KC_F1",
    "KC_2",
    "KC_E",
    "KC_F3",
    "KC_D",
    "KC_F4",
    "KC_C",
    "KC_UP",
    "KC_F2",
    "KC_3",
    "KC_R",
    "KC_T",
    "KC_F",
    "KC_G",
    "KC_V",
    "KC_B",
    "KC_5",
    "KC_4",
    "KC_U",
    "KC_Y",
    "KC_J",
    "KC_H",
    "KC_M",
    "KC_N",
    "KC_6",
    "KC_7",
    "KC_I",
    "KC_RBRC",
    "KC_K",
    "KC_F6",
    "KC_COMM",
    "KC_DEL",  # This is an extra key compared to the Keychron Q1 Pro.
    "KC_EQL",
    "KC_8",
    "KC_O",
    "KC_F7",
    "KC_L",
    "KC_DOWN",
    "KC_DOT",
    "KC_HOME",  # Default is KC_END. Changed to match.
    "KC_F8",
    "KC_9",
    "KC_P",
    "KC_LBRC",
    "KC_SCLN",
    "KC_QUOT",
    "KC_NO",
    "KC_SLSH",
    "KC_MINS",
    "KC_0",
    "KC_LGUI",
    "KC_RSFT",
    "KC_FN",  # Default is MO(1). Changed to match.
    "KC_LALT",
    "KC_SPC",
    "KC_RALT",
    "KC_NO",
    "KC_PSCR",
    "KC_NO",
    "KC_BSPC",
    "KC_BSLS",
    "KC_F11",
    "KC_ENT",
    "KC_F12",
    "KC_F9",
    "KC_F10",
]

KEYCHRON_FIXES = {
    "CUSTOM(0)": "KC_LALT",
    "CUSTOM(1)": "KC_RALT",
    "CUSTOM(3)": "KC_RGUI",
}

GMMK_FIXES = {}

KEYCHRON_INFO = {
    "name": "Keyboard 81 Pro/Q1 Pro ANSI RGB Knob",
    "vendorProductId": 875824656,
}

GMMK_INFO = {"name": "GMMK Pro", "vendorProductId": 839864388}

if __name__ == "__main__":
    main()
