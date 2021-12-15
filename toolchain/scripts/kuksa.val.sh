
echo "Installing dependencies"

sudo apt install -y cmake python3-pip

sudo apt install -y libblkid-dev e2fslibs-dev libboost-all-dev libaudit-dev libssl-dev mosquitto libmosquitto-dev libglib2.0-dev build-essential

cd ../../modules/kuksa.val/

mkdir build

cd build

cmake ..

make