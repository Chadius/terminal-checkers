pushd "$(dirname ${BASH_SOURCE[0]})"
python3 -m unittest tests
popd