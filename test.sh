#!/bin/bash

# Define the URL for the Nvidia stock page on Yahoo Finance
URL="https://finance.yahoo.com/quote/BTC-USD/"

# Use curl to retrieve the HTML of the page, then grep to extract the stock price
PRICE=$(curl -s $URL | grep '<fin-streamer class="Fw(b) Fz(36px) Mb(-4px) D(ib)" data-symbol="BTC-USD" data-test="qsp-price" data-field="regularMarketPrice" data-trend="none" data-pricehint="2" value="' | grep -o 'value=\"[^\"]\+"' | grep -o '[0-9\.]\+' | head -n 1)
# Print the current Nvidia stock price to the console
echo "$PRICE"
