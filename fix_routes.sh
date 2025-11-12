python3 $SUMO_HOME/tools/randomTrips.py \
    -n src/scenarios/4x4_grid/osm.net.xml.gz \
    -o src/scenarios/4x4_grid/medium_traffic.rou.xml \
    -e 3600 \
    -p 3.6 \
    --seed 42 \
    --fringe-factor 5 \
    --validate