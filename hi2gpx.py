import json
import time


class MotionPath:
    def __init__(self):
        self.hidata = {}  # placeholder
        self.read_json()
        self.json_to_gpx()

    def read_json(self):
        with open("motion path detail data.json", "r", encoding="utf-8") as file:
            self.hidata = json.loads(file.read())

    def json_to_gpx(self):
        number_of_tracks = 0
        for i, track in enumerate(self.hidata):
            if not "attribute" in track:
                break
            # Checks track's gps data actually has any track points. If not, continues to next track
            if track.get("totalDistance") == 0:
                continue
            sport_type = track.get("sportType")
            data = (
                track.get("attribute")
                .split("\ntp=p-m")[0]
                .split("HW_EXT_TRACK_DETAIL@istp=lbs;")[1]
            )
            latitudes = [trkpt.split(";lon=")[0] for trkpt in data.split(";lat=")][1:-1]
            longtitudes = [trkpt.split(";alt=")[0] for trkpt in data.split(";lon=")][
                1:-1
            ]
            elevations = [trkpt.split(";t=")[0] for trkpt in data.split(";alt=")][
                1:-1
            ]  # Huawei didn't complete this information earlier? Alt was always 0,
            # but from 2023/2024 onwards it actually contains some nonzero values.
            epoch_times = [
                float(epoch_time_str) * 1e9
                for epoch_time_str in [
                    trkpt.split(";\ntp=")[0].split("E9")[0]
                    for trkpt in data.split(";t=")
                ][1:-1]
            ]
            time_strings = [
                time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime(epoch_time))
                for epoch_time in epoch_times
            ]
            gpx_data = [
                i for i in zip(latitudes, longtitudes, elevations, time_strings)
            ]

            # Removing faulty track points. If the watch loses connection to satellites it
            # enters lat 90.0 in those track points.
            gpx_data = [trkpt for trkpt in gpx_data if not "90.0" in trkpt[0]]

            ### Track point generation ###
            track_points = list()
            for trkpnt in gpx_data:
                tmp_str = "\n".join(
                    [
                        f"      <trkpt lat={trkpnt[0]} lon={trkpnt[1]}>",
                        f"        <ele>{trkpnt[2]}</ele>",
                        f"        <time>{trkpnt[3]}</time>",
                        "      </trkpt>",
                    ]
                )
                track_points.append(tmp_str)
            track_points = "\n".join(track_points)

            track_start_epoch = epoch_times[0]
            track_end_epoch = epoch_times[-1]
            track_start_time_str = time.strftime(
                "%Y%m%d_%H%M%S", time.localtime(track_start_epoch)
            )
            track_end_time_str = time.strftime(
                "%Y%m%d_%H%M%S", time.localtime(track_end_epoch)
            )
            creation_time_str = time.strftime("%FT%TZ", time.gmtime())
            track_name = "Huawei Watch data " + time.strftime(
                "%d.%m.%Y", time.localtime(track_start_epoch)
            )

            header = [
                '<?xml version="1.0" encoding="UTF-8" standalone="no" ?>',
                '<gpx xmlns="http://www.topografix.com/GPX/1/1" xmlns:gpxx="http://www.garmin.com/xmlschemas/GpxExtensions/v3" xmlns:gpxtpx="http://www.garmin.com/xmlschemas/TrackPointExtension/v1" creator="Huawei Watch GT" version="1.1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd http://www.garmin.com/xmlschemas/GpxExtensions/v3 http://www.garmin.com/xmlschemas/GpxExtensionsv3.xsd http://www.garmin.com/xmlschemas/TrackPointExtension/v1 http://www.garmin.com/xmlschemas/TrackPointExtensionv1.xsd">',
                "  <metadata>",
                f"    <time>{creation_time_str}</time>",
                "  </metadata>",
                "  <trk>",
                "    <name>" + track_name + "</name>",
                "    <trkseg>\n",
            ]
            header = "\n".join(header)
            footer = ["\n    </trkseg>", "  </trk>", "</gpx>"]
            footer = "\n".join(footer)
            filename = f"{track_start_time_str}-{track_end_time_str}-sport_type_{sport_type}.gpx"
            print(f"Writing file: ./{filename}")
            with open(
                filename,
                "w",
                encoding="utf-8",
            ) as file:
                file.write(header + track_points + footer)

            number_of_tracks = number_of_tracks + 1
        print(f"Done...\n\nTotal of {number_of_tracks} tracks extracted.")

    def json_to_tcx(self):
        pass


if __name__ == "__main__":
    hi = MotionPath()
