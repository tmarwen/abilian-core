# coding=utf-8
"""
"""
from __future__ import absolute_import, division, print_function

import os
import sys

import pip
import pkg_resources
from flask import render_template, current_app
from pathlib import Path
from pip.vcs import vcs

from ..panel import AdminPanel


class SysinfoPanel(AdminPanel):
    id = 'sysinfo'
    label = 'System information'
    icon = 'hdd'

    def get(self):
        uname = os.popen("uname -a").read()
        python_version = sys.version.strip()

        packages = []

        for dist in pkg_resources.working_set:
            package = dict(name=dist.project_name,
                           key=dist.key,
                           version=dist.version if dist.has_version(
                           ) else u'Unknown version',
                           vcs=None, )

            location = unicode(Path(dist.location).absolute())
            vcs_name = vcs.get_backend_name(location)

            if vcs_name:
                vc = vcs.get_backend(vcs_name)()
                try:
                    url = vc.get_url(location)
                except pip.exceptions.InstallationError:
                    url = 'None'
                try:
                    revision = vc.get_revision(location)
                except pip.exceptions.InstallationError:
                    revision = 'None'
                package['vcs'] = dict(name=vcs_name, url=url, revision=revision)

            packages.append(package)
            packages.sort(key=lambda d: d.get('key'))

        config_values = [(k, repr(v))
                        for k, v in sorted(current_app.config.items())
                        ]

        return render_template("admin/sysinfo.html",
                               python_version=python_version,
                               packages=packages,
                               uname=uname,
                               config_values=config_values)
