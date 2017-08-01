"""
This module contains device class Shopper and run method for it.
"""

# Imports
from tango import DevState, AttrWriteType, DispLevel
from facadedevice import Facade, proxy_attribute, proxy_command, state_attribute


class Shopper(Facade):
    """
    This class implements Tango device server for control of shutter device (integrated shutter and stopper).
    Each Tango device represents one shutter, which can be open or closed.

    The Tango device works on a set of four PLC attributes of type bool, which must be
    exposed by PLC device server.

    OpenS PLC attribute should be True when shutter is open and False when it is closed
    ClosedS PLC attribute should be True when shutter is closed and False when it is opened

    OpenC PLC attribute should cause shutter to open if it is closed
    CloseC PLC attribute should cause shutter to close if it is open
    """

    def safe_init_device(self):
        """
        This is a method to safely initialize the Shopper device,
        overrode from Facade base class
        """
        super(Shopper, self).safe_init_device()
        self.set_state(DevState.ON)
        self.set_status("Device is running.")

    # proxy attributes

    ShopperOpen = proxy_attribute(
        dtype=bool,
        access=AttrWriteType.READ,
        property_name="PLCAttrName_OpenS",
        display_level=DispLevel.OPERATOR,
        description="Attribute that represents PLC signal for shutter open "
                    "state.")

    ShopperClosed = proxy_attribute(
        dtype=bool,
        access=AttrWriteType.READ,
        property_name="PLCAttrName_ClosedS",
        display_level=DispLevel.OPERATOR,
        description="Attribute that represents PLC signal for shutter closed "
                    "state.")

    ShopperInterlock = proxy_attribute(
        dtype=bool,
        access=AttrWriteType.READ,
        property_name="PLCAttrName_InterlockA",
        display_level=DispLevel.OPERATOR,
        description="Attribute that represents PLC signal for shutter in "
                    "interlock alarm.")

    # state attributes

    @state_attribute(
        bind=['ShopperInterlock'])
    def interlock_alarm(self, alarm):
        """
        This method changes state of device, accordingly to ShopperInterlock
        attribute. When it's on, the state is ALARM, otherwise the state is ON.
        :param alarm: ShopperInterlock
        :return: ALARM state when ShopperInterlock is on, ON state otherwise
        :rtype: DevState
        """
        if alarm:
            return DevState.ALARM, "Shutter is interlocked"
        return DevState.ON, "Device is running"

    # proxy commands

    @proxy_command(
        dtype_out=bool,
        write_attribute=True,
        property_name="PLCAttrName_OpenC",
        doc_out="True to PLCAttrName_OpenC")
    def Open(self, subcommand):
        """
         :rtype: bool
        """
        subcommand(True)
        return True

    @proxy_command(
        dtype_out=bool,
        write_attribute=True,
        property_name="PLCAttrName_CloseC",
        doc_out="True to PLCAttrName_CloseC")
    def Close(self, subcommand):
        """
        :rtype: bool
        """
        subcommand(True)
        return True

# run server

run = Shopper.run_server()

if __name__ == '__main__':
    run()
