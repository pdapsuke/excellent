#!/bin/bash
FRONT_DIR=/opt/app/front
if [ -d "$FRONT_DIR" ]; then
  cd $FRONT_DIR
  npm run build
  npm run start
fi