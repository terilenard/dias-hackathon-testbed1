
pip3 install anytree deprecation stringcase pyyaml

rm -r ../../modules/vehicle_signal_specification/spec

cp -r ../../modules/dias_kuksa/utils/in-vehicle/vss_structure_example/spec ../../modules/vehicle_signal_specification/spec/

cat vss-Makefile > ../../modules/vehicle_signal_specification/Makefile 

cd ../../modules/vehicle_signal_specification/vss-tools

git checkout b287be7

pip3 install -e .

pip3 install -r requirements.txt

cd ..

make

cp vss_rel_3.0-develop.json ../kuksa.val/