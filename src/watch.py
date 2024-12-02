import subprocess


def watch(direct_links):
    for link in direct_links:
        title = "File1"
        command = [
                "mpv",
                link,
                "--fs",
                "--quiet",
                "--really-quiet",
                "--profile=fast",
                "--hwdec=auto-safe",
                "--video-sync=display-resample",
                f"--force-media-title={title}"
            ]
        subprocess.run(command)
