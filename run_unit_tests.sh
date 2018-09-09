pushd "$(dirname ${BASH_SOURCE[0]})"
python3 -m unittest tests.JumpingPieceTests.test_white_can_jump_multiple_times
popd
