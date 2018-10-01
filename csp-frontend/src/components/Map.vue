<template>
    <v-card>
        <template slot="top">
            <l-map ref="map" :zoom="map.zoom" :center="map.center"
                   @click="set_marker" v-if="map.marker.lat !== '-'">
                <l-geo-json ref="geo" :geojson="map.geojson" :options="map.options" :visible="!map.visible"></l-geo-json>
                <l-tile-layer :url="map.url" :attribution="map.attribution" :visible="map.showTiles"></l-tile-layer>
                <l-marker :lat-lng="map.marker" :visible="map.visible"></l-marker>
            </l-map>
            <v-overlay :content="'Getting your current location...'" v-else></v-overlay>
        </template>
        <template slot="header">
            <span ><i class="fas fa-map-marker-alt"></i> {{map.marker.lat | length}}, {{map.marker.lng | length}}</span>
        </template>
        <template slot="body">
            <div class="row">
                <div class="col-md-12 text-center">
                    <button :disabled="map.geojson.length === 0" @click="map.showTiles = !map.showTiles" @mouseenter="info(0)" @mouseleave="info(-1)" type="button" class="btn btn-primary btn-circle mr-2"><i class="fas fa-globe"></i></button>
                    <button :disabled="map.geojson.length === 0" @click="removeGeoLayer" @mouseenter="info(2)" @mouseleave="info(-1)" type="button" class="btn btn-danger btn-circle mr-2"><i class="fas fa-trash"></i></button>
                    <button @click="centerMap" @mouseenter="info(1)" @mouseleave="info(-1)" type="button" class="btn btn-default btn-circle mr-2"><i class="fas fa-map-marked-alt"></i></button>
                    <button :disabled="!map.visible || !map.showTiles" @click="solve" @mouseenter="info(3)" @mouseleave="info(-1)" type="button" class="btn btn-success btn-circle"><i class="fas fa-long-arrow-alt-right"></i></button>
                </div>
            </div>
            <v-overlay :show="overlay.show" :content="overlay.msg" :after="overlay.hide_after"></v-overlay>
        </template>
        <template slot="footer">
            {{buttonInfo}}
        </template>
    </v-card>
</template>

<script>
import { LMap, LTileLayer, LMarker, LGeoJson } from "vue2-leaflet";
import Overlay from "./Overlay.vue";
import Card from "./BaseCard.vue";
import { getColor } from "../utils";
import store from "../store";
import api from "../api";

export default {
  name: "example",
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LGeoJson,
    "v-card": Card,
    "v-overlay": Overlay
  },
  filters: {
    length: function(value) {
      return !isNaN(value) ? value.toFixed(5) : value;
    }
  },
  created: function() {
    this.$options.sockets.mapErr = err => {
      let self = this;
      setTimeout(function() {
        self.showOverlay(err, 2000);
      }, 100);
    };
    this.$options.sockets.mapSol = sol => {
      var self = this;
      setTimeout(function() {
        self.getGeoData(sol);
      }, 500);
    };
  },
  mounted: function() {
    let cur_location = store.state.location;
    if (cur_location === null) {
      api.map
        .location()
        .then(response => {
          this.goTo(response.lat, response.lon);
          store.commit("UPDATE_LOCATION", {
            lat: response.lat,
            lng: response.lon
          });
        })
        .catch(() => {
          this.map.marker = this.$L.latLng(40.41931, -3.69599);
        });
    } else {
      this.goTo(cur_location.lat, cur_location.lng);
    }
    console.log("LOCATION", store.state.location);
  },
  data() {
    return {
      buttonInfo: "-",
      overlay: {
        show: false,
        msg: "Loading",
        hide_after: 0
      },
      map: {
        visible: true,
        showTiles: true,
        marker: { lat: "-", lng: "-" },
        //        marker: this.$L.latLng(40.41931, -3.69599),
        attribution:
          '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
        center: this.$L.latLng(40.41931, -3.69599),
        url: "http://{s}.tile.osm.org/{z}/{x}/{y}.png",
        zoom: 13,
        geojson: [],
        options: {
          style: function(feature) {
            return {
              weight: 2,
              color: "#ECEFF1",
              opacity: 1,
              fillColor: getColor(feature.properties.color),
              fillOpacity: 1
            };
          },
          onEachFeature: function(feature, layer) {
            // does this feature have a property named province?
            if (feature.properties && feature.properties.province) {
              layer.bindPopup(feature.properties.province);
            }
          }
        }
      }
    };
  },
  computed: {
    state: function() {
      return store.state.me;
    }
  },
  methods: {
    showOverlay: function(msg, hide_after) {
      this.overlay.msg = msg;
      this.overlay.hide_after = hide_after;
      this.overlay.show = hide_after > 0 ? !this.overlay.show : true;
    },
    hideOverlay: function() {
      this.overlay.show = false;
    },
    showMarker: function() {
      this.map.visible = true;
    },
    hideMarker: function() {
      this.map.visible = false;
    },
    set_marker: function(a) {
      if (this.map.visible) {
        this.map.marker = a.latlng;
        this.centerMap(true);
      }
    },
    removeGeoLayer: function() {
      this.map.geojson = [];
      this.map.showTiles = this.map.showTiles
        ? this.map.showTiles
        : !this.map.showTiles;
      this.showMarker();
    },
    getGeoData: function(task_id) {
      if (store.state.runMap) {
        api.map
          .getData(task_id)
          .then(response => {
            this.map.geojson = response;
            let self = this;
            setTimeout(function() {
              self.hideMarker();
              self.centerMap();
            }, 1);
          })
          .catch(error => {
            if (error === null) {
              this.showOverlay("No solution or error found! :(", 2000);
            } else {
              this.showOverlay("Ouch! Houston, we have a problem....", 500);
            }
          })
          .finally(() => {
            this.hideOverlay();
          });
        store.commit("UPDATE_MAP", false);
      }
    },
    solve: function() {
      let data = {
        lat: this.map.marker.lat,
        long: this.map.marker.lng,
        colors: 6,
        id: this.state
      };

      api.map
        .solve(data)
        .then(() => {
          this.showOverlay("Loading!", 0);
        })
        .catch(error => {
          this.showOverlay("Ouch! Houston, we have a problem....", 500);
          console.log(error);
        });
      console.log("SOLVE ", data, this.map.marker.lng);
    },
    goTo: function(lat, lng) {
      this.map.center = this.$L.latLng(lat, lng);
      this.map.marker = this.$L.latLng(lat, lng);
    },
    centerMap: function(default_zoom) {
      let zoom = this.map.visible
        ? default_zoom
          ? Math.max(this.map.zoom, this.$refs.map.mapObject._zoom)
          : this.map.zoom
        : 6;

      if (!this.map.visible) {
        this.$refs.map.mapObject.fitBounds(this.$refs.geo.getBounds());
      } else {
        this.$refs.map.mapObject.setView(this.map.marker, zoom);
      }
    },
    info: function(message_type) {
      switch (message_type) {
        case 0:
          this.buttonInfo = "Show/Hide TileLayer";
          break;
        case 1:
          this.buttonInfo = "Center map on lat/lng coordinates";
          break;
        case 2:
          this.buttonInfo = "Restart the map (removing GeoJSON data)";
          break;
        case 3:
          this.buttonInfo = "Send data to the server";
          break;
        default:
          this.buttonInfo = "-";
          break;
      }
    }
  }
};
</script>
<style scoped>
.btn-circle {
  width: 40px;
  height: 40px;
  text-align: center;
  padding: 6px 0;
  font-size: 15px;
  line-height: 1.42857;
  border-radius: 20px;
}
</style>
