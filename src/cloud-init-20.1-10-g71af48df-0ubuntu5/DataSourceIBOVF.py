#!/usr/bin/python3
#
# Copyright(C) 2021 Infoblox Inc.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License version 3, as
#    published by the Free Software Foundation.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from cloudinit import log as logging
from cloudinit import util
from cloudinit import sources
from cloudinit.sources import DataSourceOVF
from cloudinit.util import ProcessExecutionError
from xml.dom import minidom

LOG = logging.getLogger(__name__)


class DataSourceIBOVF(DataSourceOVF.DataSourceOVF):
    def __init__(self, sys_cfg, distro, paths):
        DataSourceOVF.DataSourceOVF.__init__(self, sys_cfg, distro, paths)

    def get_data(self):
        md = {}
        ud = ""

        # Metadata defaults, not user data defaults.
        # Cloud-init needs at least an instance-id.
        defaults = {
            "instance-id": "iid-dsovf",
        }

        np = {'vmtools': transport_vmware_guestd,
              'iso': DataSourceOVF.transport_iso9660, }
        name = None
        for (name, transfunc) in np.items():
            contents = transfunc()
            if contents:
                break

        if contents:
            (md, ud, cfg) = read_ovf_environment(contents)
            md = util.mergemanydict([md, defaults])

            self.environment = contents
            self.seed = name
            self.metadata = md
            self.userdata_raw = ud
            self.cfg = cfg
            return True

        # There were no OVF transports found
        return False


def transport_vmware_guestd():
    cmd = ['vmtoolsd', '--cmd', 'info-get guestinfo.ovfEnv']
    cmd_out = None

    try:
        (cmd_out, _err) = util.subp(cmd)
    except ProcessExecutionError as _err:
        LOG.debug(('Failed command: %s\n%s') % (' '.join(cmd), _err))
    except OSError as _err:
        LOG.debug(('Failed command: %s\n%s') % (' '.join(cmd), _err.message))

    return cmd_out


# Translate the flat list of properties to a tree that
#   the rest of IB understands
def properties_to_dict(props):
    result = {}

    for (prop, val) in props.items():
        if "-" in prop:
            subnames = prop.split('-')
            if subnames[0] in result:
                result[subnames[0]][subnames[1]] = val
            else:
                result[subnames[0]] = { subnames[1] : val }
        else:
            result[prop] = val

    return result


# Create a YAML string of the given user-data structure.
def dict_to_string(userTree):
    result = "#infoblox-config\n\n"

    for upperKey, upperValue in userTree.items():
        if isinstance( upperValue, dict):
            upperKeyPrinted = False

            for lowerKey, lowerValue in upperValue.items():
                if lowerValue:
                    if not upperKeyPrinted:
                        upperKeyPrinted = True
                        result += "%s:\n" % upperKey
                    result += "  %s: %s\n" % (lowerKey, lowerValue)
            result += "\n"
        else:
            if upperValue:
                result += "%s: %s\n" % (upperKey, upperValue)

    result += "\n"

    return result


# Get the instance ID from the attribute on
#   the Environment element of the given XML
def get_instance_id(contents):
    result = ""
    dom = minidom.parseString(contents)
    if dom.documentElement.localName != "Environment":
        raise XmlError("No Environment Node")

    if "ve:vCenterId" in dom.documentElement.attributes.keys():
        result = dom.documentElement.attributes["ve:vCenterId"].value

    return result


# This will return a dict with some content
#  meta-data, user-data, some config
def read_ovf_environment(contents):
    props = DataSourceOVF.get_properties(contents)
    userTree = properties_to_dict(props)
    ud = dict_to_string( userTree)
    md = {}
    cfg = {}

    instanceId = get_instance_id(contents)
    if instanceId:
        md['instance-id'] = instanceId

    return (md, ud, cfg)


# Used to match classes to dependencies
datasources = (
  (DataSourceIBOVF, (sources.DEP_FILESYSTEM, )),
)


# Return a list of data sources that match this set of dependencies
def get_datasource_list(depends):
    return sources.list_from_depends(depends, datasources)
