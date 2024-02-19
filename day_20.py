from copy import deepcopy
from itertools import chain
import pytest

from read_data_function import read_data

# ----- PART ONE -----


class Broadcaster():

    def __init__(self, destinations: list[str]) -> None:
        self.destinations = deepcopy(destinations)

    def parse_pulse(self, source: str, pulse: int):
        return pulse




class FlipFlop():

    def __init__(self, destinations: str) -> None:
        self.state = -1
        self.destinations = deepcopy(destinations)

    def parse_pulse(self, source: str, pulse: int):
        self.state *= pulse
        if pulse == -1:
            return self.state
        

class Conjunction():

    def __init__(self, destinations: str) -> None:
        self.state = {}
        self.destinations = deepcopy(destinations)

    def add_connection(self, source: str):
        self.state[source] = -1

    def parse_pulse(self, source: str, pulse: int):
        self.state[source] = pulse
        if sum(self.state.values()) == len(self.state):
            return -1
        return 1


def create_modules(str_input: str) -> dict:
    modules = {}
    all_destinations = []
    lines = str_input.split('\n')
    for line in lines:
        destinations = line.split(' -> ')[1].split(', ')
        type = line[0]
        name = line.split(' -> ')[0][1:]
        all_destinations.append([name, deepcopy(destinations)])
        match type:
            case 'b':
                modules['broadcaster'] = Broadcaster(destinations)
            case '%':
                modules[name] = FlipFlop(destinations)
            case '&':
                modules[name] = Conjunction(destinations)

    for source, sinks in all_destinations:
        for sink in sinks:
            if (sink in modules) and modules[sink].__class__.__name__ == 'Conjunction':
                modules[sink].add_connection(source)

    return modules


def push_button(modules: dict[object]):
    pulses = [[None, 'broadcaster', -1]]
    count = 0
    for pulse in pulses:
        if pulse[1] in modules:
            new_pulse = modules[pulse[1]].parse_pulse(pulse[0], pulse[2])
            if new_pulse is not None:
                pulses += [[pulse[1], destination, new_pulse] for destination in modules[pulse[1]].destinations]

    return [pulse[2] for pulse in pulses]


def part_one(str_input: str, times_button_pushed: int):
    modules = create_modules(str_input)
    pulses = list(chain.from_iterable([push_button(modules) for i in range(times_button_pushed)]))
    return sum([1 for pulse in pulses if pulse == 1])*sum([1 for pulse in pulses if pulse == -1])


def test_part_one():
    assert part_one("""broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a""", 1) == 32
    assert part_one("""broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a""", 1000) == 32000000


# ----- PART TWO -----


def push_button_v2(modules: dict[object]):
    pulses = [[None, 'broadcaster', -1]]
    count = 0
    for pulse in pulses:
        if pulse[1] == 'rx' and pulse[2] == -1:
            return True
        elif pulse[1] in modules:
            new_pulse = modules[pulse[1]].parse_pulse(pulse[0], pulse[2])
            if new_pulse is not None:
                pulses += [[pulse[1], destination, new_pulse] for destination in modules[pulse[1]].destinations]

    return False


def part_two(str_input: str):
    modules = create_modules(str_input)
    press_count = 0
    while not push_button_v2(modules):
        print(press_count)
        press_count += 1
    return press_count


def test_part_two():
    assert part_two("""""") == None


# --------------------


if __name__ == "__main__":
    print(part_one(read_data("day_20.txt"), 1000))
    print(part_two(read_data("day_20.txt")))