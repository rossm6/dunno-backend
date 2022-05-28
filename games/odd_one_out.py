from itertools import chain, combinations

from pandas import DataFrame

from games.utils import pick_n_random

VARS = {
    "color": ["blue", "green", "gold"],
    "shape": ["circle", "square", "star"],
    "formation": ["111111111", "000111111", "100100100"],
    "background": ["orange", "red", "pink"],
}


VAR_SETS = [
    ["background", "formation", "shape", "color"],
    ["background", "shape", "color"],
    ["background", "shape", "formation"],
    ["shape", "formation", "color"],
]


def add_prefix(prefix, value):
    return f"{prefix}:{value}"


def perm_as_object(perm):
    o = {}
    for str_val in perm:
        # str_val, e.g. colour:red
        key, value = str_val.split(":")
        o[key] = value
    return o


def get_template(n):
    if n == 3:
        return [2, 2, 3]
    elif n == 4:
        return [2, 2, 2, 3]


def all_combinations(li, n):
    """
    Get all permutations for all
    sizes up to n
    """
    perms = []
    for i in range(1, n + 1):
        perms = perms + list(combinations(li, i))
    return [list(tuple) for tuple in perms]


def list_is_subset(a, b):
    """
    Is list A a subset of list B?
    """
    for i in a:
        if i not in b:
            return False
    return True


def list_has_no_subsets(li, lists):
    for _li in lists:
        if _li != li and list_is_subset(_li, li):
            return False
    return True


def find_odd_one_out_for_game(vars, squares, group_bys):
    df = DataFrame({var: [square[var] for square in squares] for var in vars})

    odd_one_out_groups = []

    for group in group_bys:
        groups = df.groupby(by=group).groups
        single_groups = [_group for grouping, _group in groups.items() if len(_group) == 1]
        if len(single_groups) == 1:
            odd_one_out_groups.append(group)

    real_group_bys = []

    for group in odd_one_out_groups:
        if list_has_no_subsets(group, odd_one_out_groups):
            real_group_bys.append(group)

    if len(real_group_bys) == 1:
        group_by = real_group_bys[0]
        groups = df.groupby(by=group_by).groups
        odd_one_out_group = [_group for grouping, _group in groups.items() if len(_group) == 1][0]
        # odd_one_out_group is type <class 'pandas.core.indexes.numeric.Int64Index'>
        odd_one_out_index = list(odd_one_out_group.values)[0]  # is a pandas class of some kind

        return {
            "level": len(group_by),
            "squares": squares,
            "group": group_by,
            "odd_one_out_index": int(odd_one_out_index),
        }


def get_valid_games_for_vars(vars, max):
    n = len(vars.keys())

    group_bys = all_combinations(list(vars.keys()), n - 1)

    prefixed_var_values = [
        [add_prefix(var, value) for value in values] for var, values in vars.items()
    ]

    total_perms = list(combinations(list(chain(*prefixed_var_values)), n))

    total_perms = [perm_as_object(perm) for perm in total_perms]
    total_distinct_perms = [
        perm for perm in total_perms if len(perm.keys()) == n
    ]  # i.e. n distinct keys, i.e. those with all vars, e.g. color, shape, formation

    # we now have the all the possible permutations for distinct objects with N keys

    # task - get all the possible permutations for size n squared

    # e.g. n = 3, gives 12 permutations for distinct objects with 3 keys, so we want all permutations of subset length 9

    perms_as_strs = []
    for perm in total_distinct_perms:
        perm_as_str = ",".join([f"{k}:{v}" for k, v in perm.items()])
        perms_as_strs.append(perm_as_str)

    all_games = list(combinations(perms_as_strs, pow(n, 2)))
    # i.e. valid and invalid games.  invalid games are games without an odd one out

    if len(all_games) > 1000:
        all_games = pick_n_random(all_games, max)

    valid_games = []
    for game in all_games:
        square_objs = []
        for square_as_str in game:
            square_obj = {}
            for var_and_value in square_as_str.split(","):
                var, value = var_and_value.split(":")
                square_obj[var] = value
            square_objs.append(square_obj)

        if valid_game := find_odd_one_out_for_game(vars, square_objs, group_bys):
            valid_games.append(valid_game)

    return valid_games


def generate_all_games(n, max):
    var_sets = [var_set for var_set in VAR_SETS if len(var_set) == n]
    template = get_template(n)

    entire_games = []

    for var_set in var_sets:
        all_possible_vars = []
        for var in var_set:
            var_values = VARS[var]
            all_possible_vars.append([f"{var}:{v}" for v in var_values])
        all_possible_vars = list(chain(*all_possible_vars))

        all_game_vars = list(combinations(all_possible_vars, sum(template)))
        # not all are valid though because it could include 4 color variables for example
        # and we only allow 3 per the template

        valid_game_vars = []
        for vars in all_game_vars:
            game_vars = {}
            for var in vars:
                k, v = var.split(":")
                if k in game_vars:
                    game_vars[k].append(v)
                else:
                    game_vars[k] = [v]

            # does it fit the template ?
            if len(template) == len(game_vars.keys()):
                if sorted(template) == sorted([len(values) for values in game_vars.values()]):
                    valid_game_vars.append(game_vars)

        for vars in valid_game_vars:
            valid_games = get_valid_games_for_vars(vars, max)
            entire_games.append(valid_games)

    entire_games = list(chain(*entire_games))
    return entire_games
