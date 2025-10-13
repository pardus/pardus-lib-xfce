import subprocess


# Getters
def get_available_locales():
    langs = []
    with open("/usr/share/i18n/SUPPORTED", "r") as f:
        for line in f:
            lang, encode_type = line.strip().split(" ")[0:2]
            langs.append((lang, encode_type))

    # [(tr_TR.UTF-8, UTF-8), ...]
    return langs


def get_installed_locales():
    langs = []
    with open("/etc/locale.gen", "r") as f:
        for line in f:
            if line[0] != "#" and len(line) > 3:
                lang, encode_type = line.strip().split(" ")[0:2]
                langs.append((lang, encode_type))
    # we are using en_US.UTF-8 for lc_ctype
    if ("en_US.UTF-8", "UTF-8") not in langs:
        langs.append(("en_US.UTF-8", "UTF-8"))

    # [(tr_TR.UTF-8, UTF-8), ...]
    return langs


def get_default_locale():
    p = subprocess.run(["localectl"], capture_output=True)
    lines = p.stdout.decode("utf-8").splitlines()
    if "LANG=" in lines[0]:
        return lines[0].split("LANG=")[-1].strip()


# Setters
def enable_locales(locales):
    # locale should be like this: "tr_TR.UTF-8 UTF-8"

    # disable all locales first:
    subprocess.run("sed -i 's/^ *\\([^#]\\)/# \\1/' /etc/locale.gen", shell=True)

    # remove duplications:
    subprocess.run(
        "awk '!seen[$0]++' /etc/locale.gen | sudo tee /etc/locale.gen", shell=True
    )

    # enable installed ones:
    subprocess.run(
        "sed -i 's/^# *\\(" + locales + "\\)/\\1/' /etc/locale.gen", shell=True
    )


def set_default_locale(locale):
    # locale should be like this: "tr_TR.UTF-8"
    lc = locale.split(" ")[0]
    subprocess.run(f"localectl set-locale LANG={lc}", shell=True)
    # force lc_ctype to en
    subprocess.run(f"localectl set-locale LC_CTYPE=en_US.UTF-8", shell=True)


def generate_locale():
    subprocess.run("locale-gen")


def save_locale_settings(locales, default_locale):
    enable_locales(locales)
    set_default_locale(default_locale)
    generate_locale()
