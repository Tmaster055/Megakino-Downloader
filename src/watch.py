import subprocess


def watch(direct_links, titles):
    counter = 0
    for link in direct_links:
        title = titles[counter].split('(')[0].strip()
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
        counter += 1
        subprocess.run(command)
