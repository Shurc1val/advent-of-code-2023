from copy import deepcopy
import pytest
from itertools import chain
from functools import reduce

from read_data_function import read_data

# ----- PART ONE -----


def parse_workflows(str_input: str) -> list[dict]:
    operations = {
        '<': lambda a,b: a < b,
        '>': lambda a,b: a < b
    }
    workflows = {}
    for line in str_input.split('\n'):
        workflows[line.split('{')[0]] = []
        rules = line.split('{')[1].rstrip('}').split(',')
        for i, rule in enumerate(rules):
            if rule.count(':') > 0:
                workflows[line.split('{')[0]].append({
                    'condition': {
                        'key': rule[0],
                        'operator': rule[1],
                        'number': int(rule.split(':')[0][2:])
                    },
                    'destination': rule.split(':')[1]
                })
            else:
                workflows[line.split('{')[0]].append({
                    'destination': rule
                })

    return workflows


def parse_parts(str_input: str) -> list[dict]:
    parts = []
    for line in str_input.split('\n'):
        parts.append({})
        for attribute in line.lstrip('{').rstrip('}').split(','):
            parts[-1][attribute[0]] = int(attribute.split('=')[1])

    return parts
        

def is_part_accepted(workflows: list[dict], part: dict) -> bool:
    operations = {
        '<': lambda a,b: a < b,
        '>': lambda a,b: a > b
    }
    current_workflow_key = 'in'
    while current_workflow_key not in ['A','R']:
        workflow = workflows[current_workflow_key]
        for rule in workflow:
            condition = rule.get('condition')
            if not condition:
                current_workflow_key = rule['destination']
                break
            if operations[condition['operator']](part[condition['key']], condition['number']):
                current_workflow_key = rule['destination']
                break
    
    if current_workflow_key == 'A':
        return True
    return False


def part_one(str_input: str):
    workflows = parse_workflows(str_input.split('\n\n')[0])
    parts = parse_parts(str_input.split('\n\n')[1])

    return(sum([sum(part.values()) for part in parts if is_part_accepted(workflows, part)]))


def test_part_one():
    workflows = parse_workflows("""px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}""")
    part_1 = parse_parts("{x=787,m=2655,a=1222,s=2876}")[0]
    assert is_part_accepted(workflows, part_1) == True
    assert part_one("""px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}""") == 19114


# ----- PART TWO -----

def trace_ranges(workflows: list[dict]):

    to_check = [['in',
                 {}]]
    for key in list('xmas'):
        to_check[0][-1][key] = {
            'min': 1,
            'max': 4000
        }
    
    valid_ranges = []
    for pair in to_check:
        for key in pair[1].keys():
            if pair[1][key]['min'] > pair[1][key]['max']:
                pair = None
                break

        for rule in workflows[pair[0]]:
            part_1 = deepcopy(pair[1])
            condition = rule.get('condition')
            if not condition:
                if rule['destination'] == 'A':
                    valid_ranges.append(pair[1])
                elif rule['destination'] != 'R':
                    to_check.append([rule['destination'], pair[1]])
                break

            operator = condition['operator']
            if operator == '<':
                if part_1[condition['key']]['min'] < condition['number']:
                    part_1[condition['key']]['max'] = min(condition['number'] - 1, part_1[condition['key']]['max'])
                    if rule['destination'] == 'A':
                        valid_ranges.append(part_1)
                    elif rule['destination'] != 'R':
                        to_check.append([rule['destination'], part_1])

                pair[1][condition['key']]['min'] = max(condition['number'], pair[1][condition['key']]['min'])
            elif operator == '>':
                if part_1[condition['key']]['max'] > condition['number']:
                    part_1[condition['key']]['min'] = min(condition['number'] + 1, part_1[condition['key']]['min'])
                    if rule['destination'] == 'A':
                        valid_ranges.append(part_1)
                    elif rule['destination'] != 'R':
                        to_check.append([rule['destination'], part_1])

                pair[1][condition['key']]['max'] = min(condition['number'], pair[1][condition['key']]['max'])             

    return valid_ranges


def range_difference(range_1: dict, range_2: dict) -> list[dict]:
    if (range_2['min'] > range_1['max']) or (range_2['max'] < range_1['min']):
        return [range_1]
    
    if (range_2['min'] <= range_1['min']) and (range_2['max'] < range_1['max']):
        return [
            {
                'min': range_2['max'] + 1,
                'max': range_1['max']
            }
        ]
    
    if (range_2['min'] > range_1['min']) and (range_2['max'] < range_1['max']):
        return [
            {
                'min': range_1['min'],
                'max': range_2['min'] - 1
            },
            {
                'min': range_2['max'] + 1,
                'max': range_1['max']
            }
        ]
    
    if (range_2['min'] <= range_1['min']) and (range_2['max'] >= range_1['max']):
        return []
    
    if (range_2['min'] <= range_1['max']) and (range_2['max'] >= range_1['max']):
        return [
            {
                'min': range_1['min'],
                'max': range_2['min'] - 1
            }
        ]


def get_range_width(range: dict) -> int:
    return range['max'] - range['min'] + 1


def multi_range_difference(ranges: list[dict]) -> int:
    for range_1 in ranges:
        print(range_1)
    total_possible_combinations = 0
    for i, range_1 in enumerate(ranges):
        range_lengths = []
        refined_lengths = []
        for key in list('xmas'):
            distinct_ranges = [range_1[key]]
            for range_2 in ranges[i+1:]:
                distinct_ranges = list(chain.from_iterable([range_difference(range_3, range_2[key]) for range_3 in distinct_ranges]))
            numbers = [get_range_width(range_2) for range_2 in distinct_ranges]
            range_lengths.append(get_range_width(range_1[key]))
            refined_lengths.append(sum(numbers))


        possible_combinations = reduce(lambda x,y: x*y, [(range_lengths[j] - refined_lengths[j]) for j in range(len(refined_lengths))])
        
        possible_combinations -= reduce(lambda x,y: x*y, refined_lengths)


        total_possible_combinations += possible_combinations
    return total_possible_combinations


def part_two(str_input: str):
    workflows = parse_workflows(str_input.split('\n\n')[0])
    ranges = trace_ranges(workflows)
    return multi_range_difference(ranges)


def test_part_two():
    assert part_two("""px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}""") == 167409079868000


# --------------------


if __name__ == "__main__":
    print(part_one(read_data("day_19.txt")))
    print(part_two(read_data("day_.txt")))