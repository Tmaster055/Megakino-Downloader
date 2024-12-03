import getpass
import platform
import subprocess


def syncplay(direct_links):
    for link in direct_links:
        executable = "SyncplayConsole" if platform.system() == "Windows" else "syncplay"
        syncplay_username = getpass.getuser()
        syncplay_hostname = "syncplay.pl:8997"
        room_name = "MEGAKINO-8997"
        title = "File1"

        command = [
            executable,
            "--no-gui",
            "--no-store",
            "--host", syncplay_hostname,
            "--name", syncplay_username,
            "--room", room_name,
            "--player", "mpv",
            link,
            "--",
            "--profile=fast",
            "--hwdec=auto-safe",
            "--fs",
            "--video-sync=display-resample",
            f"--force-media-title={title}"
        ]
        subprocess.run(command)
