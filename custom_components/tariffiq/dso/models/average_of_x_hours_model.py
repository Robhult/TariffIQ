"""Top Peaks Average DSO model."""

from datetime import datetime
from typing import ClassVar

from homeassistant.components.recorder.statistics import StatisticsRow
from homeassistant.util import dt as dt_util

from custom_components.tariffiq.dso.models.modelbase import ModelBase


class AverageOfXHoursModel(ModelBase):
    """Top Peaks Average DSO model."""

    count_top_peaks: ClassVar[int] = 3

    @classmethod
    def peak_value(cls, statistics: list[StatisticsRow]) -> float:
        """Return the peak value for the model."""
        observed_peaks = cls.observed_peak(statistics)
        if not observed_peaks:
            return 0.0

        # Extract float values from dictionaries and sort in descending order
        peak_values = [next(iter(peak.values())) for peak in observed_peaks]
        sorted_peaks = sorted(peak_values, reverse=True)
        top_peaks = sorted_peaks[: cls.count_top_peaks]

        return sum(top_peaks) / len(top_peaks)

    @classmethod
    def observed_peak(
        cls, statistics: list[StatisticsRow]
    ) -> list[dict[datetime, float]]:
        """Return the peak values for the model."""
        filtered_stats = cls._filter_statistics(
            statistics,
            months=set(cls.tariff_schedule.month),
            weekdays=set(cls.tariff_schedule.weekday),
            hours=set(cls.tariff_schedule.hour),
        )

        peaks = []
        for stat in filtered_stats:
            change = stat.get("change", 0.0) or 0.0

            if change == 0.0:  # Skip zero change entries
                continue

            start_time = datetime.fromtimestamp(
                stat.get("start", 0.0), dt_util.DEFAULT_TIME_ZONE
            )
            peaks.append({start_time: round(change, 2)})

        selected_peaks = sorted(
            peaks,
            key=lambda peak: next(iter(peak.values())),
            reverse=True,
        )[: cls.count_top_peaks]

        return sorted(
            selected_peaks, key=lambda peak: next(iter(peak.keys())), reverse=True
        )
