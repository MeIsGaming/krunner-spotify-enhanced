import shutil
import subprocess

import pytest


def _run_dbus_call(method: str, value: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [
            "dbus-send",
            "--session",
            "--print-reply",
            "--dest=org.kde.KRunnerSpotify",
            "/KRunnerSpotify",
            method,
            f"string:{value}",
        ],
        capture_output=True,
        text=True,
        check=False,
    )


@pytest.mark.integration
def test_dbus_match_returns_reply_when_service_available():
    if shutil.which("dbus-send") is None:
        pytest.skip("dbus-send not available")

    result = _run_dbus_call("org.kde.krunner1.Match", "spe login")
    if result.returncode != 0 and "ServiceUnknown" in result.stderr:
        pytest.skip("KRunner Spotify DBus service not activatable")

    assert result.returncode == 0
    assert "method return" in result.stdout


@pytest.mark.integration
def test_dbus_run_unknown_command_does_not_crash_service():
    if shutil.which("dbus-send") is None:
        pytest.skip("dbus-send not available")

    run_result = subprocess.run(
        [
            "dbus-send",
            "--session",
            "--print-reply",
            "--dest=org.kde.KRunnerSpotify",
            "/KRunnerSpotify",
            "org.kde.krunner1.Run",
            "string:spe unknowncommand",
            "string:",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if run_result.returncode != 0 and "ServiceUnknown" in run_result.stderr:
        pytest.skip("KRunner Spotify DBus service not activatable")

    assert run_result.returncode == 0

    match_result = _run_dbus_call("org.kde.krunner1.Match", "spe login")
    assert match_result.returncode == 0
