#!/usr/bin/with-contenv bashio
# shellcheck shell=bash

set -euo pipefail

export TOWER_LED_COUNT="$(bashio::config 'led_count')"
export TOWER_LED_GPIO="$(bashio::config 'led_gpio')"
export TOWER_LED_DMA="$(bashio::config 'led_dma')"
export TOWER_LED_BRIGHTNESS="$(bashio::config 'brightness_limit')"
export TOWER_LED_STRIP_TYPE="$(bashio::config 'strip_type')"


bashio::log.info "Tower Control startet"
bashio::log.info "LED-Konfiguration: count=${TOWER_LED_COUNT}, gpio=${TOWER_LED_GPIO}, dma=${TOWER_LED_DMA}, brightness=${TOWER_LED_BRIGHTNESS}, strip_type=${TOWER_LED_STRIP_TYPE}"

TARGET="/share/tower_control"
mkdir -p "$TARGET"

cp /usr/local/bin/tower_oledctl "$TARGET/tower_oledctl"
cp /usr/local/bin/tower_ledctl "$TARGET/tower_ledctl"

chmod +x "$TARGET/tower_oledctl" "$TARGET/tower_ledctl"

bashio::log.info "Tower Control tools deployed:"
ls -l "$TARGET"
sleep infinity
