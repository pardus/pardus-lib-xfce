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
def _enable_locales(locales):
    # locale should be like this: "tr_TR.UTF-8 UTF-8"
    # e.g. locales: "tr_TR.UTF-8 UTF-8|en_US.UTF-8 UTF-8" two locales here

    locales_list = locales.split("|")

    new_locale_gen_content = ""

    with open("/etc/locale.gen", "r") as f:
        lines = f.readlines()

        for line in lines:
            # Example line:
            # Disabled: '# tr_TR.UTF-8 UTF-8'
            # Enabled:  'tr_TR.UTF-8 UTF-8'

            if line.startswith("#"):
                locale = line.split("#")[1].strip()

                if locale in locales_list:
                    new_line = locale + "\n"
                else:
                    new_line = line

            else:
                if line.strip() in locales_list:
                    new_line = line
                else:
                    new_line = "# " + line

            new_locale_gen_content += new_line

    if new_locale_gen_content:
        with open("/etc/locale.gen", "w") as f:
            f.write(new_locale_gen_content)


def _set_default_locale(locale):
    # locale should be like this: "tr_TR.UTF-8"
    lc = locale.split(" ")[0]
    subprocess.run(f"localectl set-locale LANG={lc}", shell=True)
    # force lc_ctype to en
    subprocess.run(f"localectl set-locale LC_CTYPE=en_US.UTF-8", shell=True)


def _generate_locale():
    subprocess.run("locale-gen")


def save_locale_settings(locales, default_locale):
    _enable_locales(locales)
    _set_default_locale(default_locale)
    _generate_locale()
