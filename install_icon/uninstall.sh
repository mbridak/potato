#!/bin/bash

if [ -f "~/.local/bin/potato" ]; then
	rm ~/.local/bin/potato
fi

xdg-icon-resource uninstall --size 64 k6gte-potato

xdg-desktop-icon uninstall k6gte-potato.desktop

xdg-desktop-menu uninstall k6gte-potato.desktop

