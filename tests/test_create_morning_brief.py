"""Timezone tests for the Zoom transcript summarizer."""

from datetime import datetime, timezone
import importlib.util
import os
from pathlib import Path
import time
import unittest

ZOOM_SCRIPT = Path(__file__).parents[1] / "dot_local/bin/executable_summarize-zoom-transcripts.py"
ZOOM_SPEC = importlib.util.spec_from_file_location("summarize_zoom_transcripts", ZOOM_SCRIPT)
assert ZOOM_SPEC and ZOOM_SPEC.loader
ZOOM = importlib.util.module_from_spec(ZOOM_SPEC)
ZOOM_SPEC.loader.exec_module(ZOOM)


class ZoomTimezoneTest(unittest.TestCase):
    def test_zoom_fallback_date_uses_denver_time_not_process_timezone(self) -> None:
        source = Path(self._testMethodName + ".vtt")
        source.write_text("WEBVTT\n", encoding="utf-8")
        timestamp = datetime(2026, 9, 8, 5, 30, tzinfo=timezone.utc).timestamp()
        os.utime(source, (timestamp, timestamp))
        previous_tz = os.environ.get("TZ")
        try:
            os.environ["TZ"] = "UTC"
            time.tzset()
            self.assertEqual(ZOOM.meeting_metadata(source)[0], "2026-09-07")
        finally:
            if previous_tz is None:
                os.environ.pop("TZ", None)
            else:
                os.environ["TZ"] = previous_tz
            time.tzset()
            source.unlink()

    def test_zoom_timestamp_in_filename_is_converted_to_denver_date(self) -> None:
        source = Path("Late call 2026-09-08 00:30(GMT-4:00).vtt")
        source.write_text("WEBVTT\n", encoding="utf-8")
        try:
            self.assertEqual(ZOOM.meeting_metadata(source)[0], "2026-09-07")
        finally:
            source.unlink()

if __name__ == "__main__":
    unittest.main()
