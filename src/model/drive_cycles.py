"""
Contains utilities for working with drive cycles
"""
import copy

import pandas as pd

from model.parsers import register_parser, LineParserBase


class DriveCycle:
    """
    Encapsulates the main interface for working with drive cycles.
    Normally, drive cycles are loaded in from /data/drive_cycles via data.py
    operating the DriveCycleParser.
    Not recommended to instantiate this directly, rather copy one of the data
    examples and it will be available on program initialization.
    """

    META_FIELDS = ["v_unit"]

    def __init__(self, metadata=None):
        self.name = None
        if metadata is None:
            metadata = {}
        self.metadata = metadata
        self.segments = []

    def __iter__(self):
        yield from self.segments

    def resample(self, duration=1.0):
        for seg in self.segments:
            yield from seg.resample(duration=duration)

    def to_df(self, integration_resolution=1.0):
        """
        Converts the drive cycle into a dataframe
        :param integration_resolution: the time resolution for integrating curved
        velocity segments
        :return: a dataframe
        """
        total_t = 0.0
        data = []
        for seg in self.resample(duration=integration_resolution):
            data.append(
                (
                    total_t,
                    seg.duration,
                    seg.type,
                    seg.start_v,
                    seg.end_v,
                    seg.avg_v,
                    seg.avg_vv,
                    seg.acceleration,
                    seg.delta_alt,
                    seg.avg_alt,
                )
            )
            total_t += seg.duration
        result = pd.DataFrame(
            data,
            columns=[
                "start_time",
                "duration",
                "segment_type",
                "start_v",
                "end_v",
                "avg_v",
                "avg_vv",
                "acceleration",
                "delta_alt",
                "avg_alt",
            ],
        )

        result["delta_d"] = result["avg_v"] * result["duration"]
        return result

    def is_resolved(self):
        """
        :return: a boolean indicating if the drive cycle contains references (False)
        or if all segments have been sourced and initialized correctly
        """
        if any([isinstance(seg, IncludedCycleSegment) for seg in self.segments]):
            return False
        return True

    def resolve(self, data_structure):
        """
        given a datastructure that should contain the keys for any references,
        load and include the references to complete the drive cycle.
        """
        if not self.is_resolved():
            self.resolve_inclusions(data_structure)

    def resolve_inclusions(self, data_structure):
        """
        Actually perform reference resolution. Throws KeyError if it cannot be resolved
        """
        new_segments = []

        for seg in self.segments:
            # If a segment is a reference, attempt to resolve it, or throw
            if isinstance(seg, IncludedCycleSegment):
                if seg.ref_key in data_structure:
                    new_segments.extend(data_structure[seg.ref_key].segments)
                else:
                    raise KeyError(
                        f"{seg.ref_key} not a valid reference in " f"{self.name}"
                    )
            else:
                new_segments.append(seg)

        self.segments = new_segments

    @property
    def duration(self):
        if self.segments:
            return sum(seg.duration for seg in self.segments)
        else:
            return 0

    @property
    def total_distance(self):
        if self.segments:
            return sum([seg.avg_v * seg.duration for seg in self.segments])
        else:
            return 0


class DriveCycleSegment:
    """
    Contains a single segment.  Essentially has a segment length as well as the
    change in velocity.
    """

    def __init__(self, duration, start_v, end_v, start_alt=0, end_alt=0, metadata=None):
        self.duration = duration
        self.start_v = start_v
        self.end_v = end_v
        self.start_alt = start_alt
        self.end_alt = end_alt

        if end_v > start_v:
            self.type = "a"
        elif start_v > end_v:
            self.type = "d"
        elif start_v > 0 and start_v == end_v:
            self.type = "c"
        else:
            self.type = "i"

        self.metadata = metadata

    def resample(self, duration):
        """
        :param duration: float in seconds to resample the drive cycle
        :return: a generator yielding one sub drive cycle for each duration in the
        parent
        """
        # If the sample frequency is the same as this segment, simply yield ourself.
        if float(duration) == float(self.duration):
            yield self
        else:
            n_samples = int(self.duration / duration)
            for subsample_idx in range(n_samples):
                v_increment = (self.end_v - self.start_v) / n_samples
                a_increment = (self.end_alt - self.start_alt) / n_samples
                yield DriveCycleSegment(
                    duration,
                    self.start_v + v_increment * subsample_idx,
                    self.start_v + v_increment * (subsample_idx + 1),
                    self.start_alt + a_increment * subsample_idx,
                    self.start_alt + a_increment * (subsample_idx + 1),
                )

    @property
    def delta_v(self):
        return self.end_v - self.start_v

    @property
    def delta_alt(self):
        return self.end_alt - self.start_alt

    @property
    def avg_alt(self):
        return (self.start_alt + self.end_alt) / 2

    @property
    def avg_acceleration(self):
        return self.delta_v / self.duration

    @property
    def avg_v(self):
        return self.start_v + self.delta_v / 2

    @property
    def avg_vv(self):
        minimum = min([self.start_v, self.end_v])
        maximum = max([self.start_v, self.end_v])
        return minimum ** 2 + (maximum - minimum) ** 2 / 3

    @property
    def acceleration(self):
        return (self.end_v - self.start_v) / self.duration

    @property
    def is_linear(self):
        return True


class IncludedCycleSegment:
    def __init__(self, key):
        self.ref_key = key


class DriveCycleParser(LineParserBase):
    """
    Implements parsing of drivecycles from text files.
    """

    RESULT_CLASS = DriveCycle

    def new_object_hook(self):
        self.last_t, self.last_v, self.last_a, self.index = 0.0, 0.0, 0.0, 1

    def handle_line(self, line):
        handlers = {"v": self.add_v_line, "include": self.include_cycle}
        if line[0] in handlers:
            handlers[line[0]](line)
        else:
            print(f"unhandled line for {__class__}: {line}")

    def add_v_line(self, line):
        new_v, seg_t = float(line[1]), line[2]
        if self.result[-1].metadata["v_unit"] == "kmh":
            new_v /= 3.6
        if seg_t.startswith("+"):
            seg_t = float(seg_t[1:])
        else:
            seg_t = float(seg_t) - self.last_t
            if seg_t < 0:
                raise ValueError(
                    "Use of absolute time gives segment negative "
                    "duration: {}".format(line)
                )

        # Handle altitude if a third parameter is passed
        if len(line) > 3:
            new_a = line[3]
            if new_a.startswith("+"):
                new_a = float(new_a[1:]) + self.last_a
            else:
                new_a = float(new_a)
        else:
            new_a = self.last_a

        if seg_t == 0.0:
            self.last_v = new_v
            self.last_a = new_a
        else:
            new_segment = DriveCycleSegment(
                seg_t, self.last_v, new_v, self.last_a, new_a
            )
            self.result[-1].segments.append(new_segment)
            self.last_v = new_v
            self.last_t += seg_t
            self.last_a = new_a
            self.index += 1

    def include_cycle(self, line):
        if len(line) > 2:
            reps = int(line[2])
        else:
            reps = 1
        for i in range(0, reps):
            new_segment = IncludedCycleSegment(line[1])
            self.result[-1].segments.append(new_segment)


register_parser(".vdc", DriveCycleParser)
