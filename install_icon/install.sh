#!/bin/bash

if [ -f "../dist/potato" ]; then
	cp ../dist/potato ~/.local/bin/
fi

xdg-icon-resource install --size 64 --context apps --mode user k6gte-potato.png k6gte-potato

xdg-desktop-icon install k6gte-potato.desktop

xdg-desktop-menu install k6gte-potato.desktop

