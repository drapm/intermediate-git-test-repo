"""
Copyright 2025 National Oceanography Centre
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
 http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import geopandas as gpd
from matplotlib.offsetbox import AnchoredText
import matplotlib.pyplot as plt
import pandas as pd


def plot_buoy_data():

    north_atlantic = gpd.read_file("data/north_atlantic.geojson")

    buoys = pd.read_csv("data/buoy_data.csv", keep_default_na=False, na_values=[""])

    locations = buoys[["Name", "latitude", "longitude"]]

    buoys_geo = gpd.GeoDataFrame(
        locations,
        geometry=gpd.points_from_xy(locations.longitude, locations.latitude),
        crs="EPSG:4326",
    )

    bounds = buoys_geo.total_bounds

    fig, ax = plt.subplots()
    ax.set_ylim([bounds[1] - 0.5, bounds[3] + 0.5])
    ax.set_xlim([bounds[0] - 0.5, bounds[2] + 0.5])
    north_atlantic.plot(ax=ax)

    buoys_geo.plot(ax=ax, color="red")

    axis_labels = []

    for buoy in buoys_geo.iterfeatures():
        ax.annotate(
            int(buoy["id"]) + 1,
            xy=(buoy["properties"]["longitude"], buoy["properties"]["latitude"]),
        )
        axis_labels.append(f"{int(buoy['id'])+1}: {buoy['properties']['Name']}")

    labels = AnchoredText(
        "\n".join(axis_labels),
        loc="lower left",
        prop=dict(size=8),
        frameon=True,
        bbox_to_anchor=(1.0, 0),
        bbox_transform=ax.transAxes,
    )
    labels.patch.set_boxstyle("round,pad=0.,rounding_size=0.2")
    ax.add_artist(labels)
    fig.tight_layout()
    fig.savefig("buoys_plot.png")


if __name__ == "__main__":
    plot_buoy_data()