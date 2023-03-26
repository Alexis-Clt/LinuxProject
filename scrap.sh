#!/bin/bash

OUTPUT_DIR="/home/aki/LinuxProject/"
OUTPUT_FILE="$OUTPUT_DIR/data.csv"

mkdir -p "$OUTPUT_DIR"

if [ ! -f "$OUTPUT_FILE" ] || ! grep -q "timestamp,rate" "$OUTPUT_FILE"; then
    echo "timestamp,rate" > $OUTPUT_FILE
fi

URL="https://finance.yahoo.com/quote/BTC-USD/"

PRICE=$(curl -s $URL | grep '<fin-streamer class="Fw(b) Fz(36px) Mb(-4px) D(ib)" data-symbol="BTC-USD" data-test="qsp-price" data-field="regularMarketPrice" data-trend="none" data-pricehint="2" value="' | grep -o 'value=\"[^\"]\+"' | grep -o '[0-9\.]\+' | head -n 1)

timestamp=$(date +"%Y-%m-%d %H:%M:%S")
echo "$timestamp,$PRICE" >> $OUTPUT_FILE
