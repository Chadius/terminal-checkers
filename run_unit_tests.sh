pushd "$(dirname ${BASH_SOURCE[0]})"
python3 -m unittest tests #tests.JumpingPieceTests.test_white_jump_1
popd