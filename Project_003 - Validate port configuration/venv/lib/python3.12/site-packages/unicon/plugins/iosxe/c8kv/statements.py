import re
import time
import logging

from unicon.eal.dialogs import Statement
from unicon.plugins.generic.statements import (
    boot_timeout_stmt,
)

from unicon.plugins.iosxe.patterns import IosXEReloadPatterns, IosXEPatterns

log = logging.getLogger(__name__)
reload_patterns = IosXEReloadPatterns()
patterns = IosXEPatterns()

def boot_image(spawn, context, session):
    if not context.get('boot_prompt_count'):
        context['boot_prompt_count'] = 1
    if context.get('boot_prompt_count') < \
            spawn.settings.MAX_BOOT_ATTEMPTS:
        if "boot_cmd" in context:
            cmd = context.get('boot_cmd')
        elif "image_to_boot" in context:
            cmd = "boot {}".format(context['image_to_boot']).strip()
        elif spawn.settings.FIND_BOOT_IMAGE:
            filesystem = spawn.settings.BOOT_FILESYSTEM if \
                hasattr(spawn.settings, 'BOOT_FILESYSTEM') else 'flash:'
            spawn.buffer = ''
            spawn.sendline('dir {}'.format(filesystem))
            dir_listing = spawn.expect(patterns.rommon_prompt).match_output
            boot_file_regex = spawn.settings.BOOT_FILE_REGEX if \
                hasattr(spawn.settings, 'BOOT_FILE_REGEX') else r'(\S+\.bin)'
            m = re.search(boot_file_regex, dir_listing)
            if m:
                boot_image = m.group(1)
                cmd = "boot {}{}".format(filesystem, boot_image)
            else:
                cmd = "boot"
        else:
            cmd = "boot"
        spawn.sendline(cmd)
        context['boot_prompt_count'] += 1
    else:
        raise Exception("Too many failed boot attempts have been detected.")


boot_from_rommon_stmt = Statement(
    pattern=patterns.rommon_prompt,
    action=boot_image,
    args=None,
    loop_continue=True,
    continue_timer=False)

# This list is extended later, see below
boot_from_rommon_statement_list = [
    boot_timeout_stmt,
    boot_from_rommon_stmt
]