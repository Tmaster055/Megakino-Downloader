import getpass
import platform
import subprocess


def syncplay(direct_links, titles):
    counter = 0
    for link in direct_links:
        title = titles[counter].split('(')[0].strip()
        executable = "SyncplayConsole" if platform.system() == "Windows" else "syncplay"
        syncplay_username = getpass.getuser()
        syncplay_hostname = "syncplay.pl:8997"

        command = [
            executable,
            "--no-gui",
            "--no-store",
            "--host", syncplay_hostname,
            "--name", syncplay_username,
            "--room", title,
            "--player", "mpv",
            link,
            "--",
            "--profile=fast",
            "--hwdec=auto-safe",
            "--fs",
            "--video-sync=display-resample",
            f"--force-media-title={title}"
        ]
        counter += 1
        subprocess.run(command)
