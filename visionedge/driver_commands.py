#!/usr/bin/python
# -*- coding: utf-8 -*-

from cloudshell.layer_one.core.driver_commands_interface import DriverCommandsInterface
from cloudshell.layer_one.core.response.response_info import GetStateIdResponseInfo

from ixia_nto import *


class DriverCommands(DriverCommandsInterface):
    """
    Driver commands implementation
    """

    def __init__(self, logger, runtime_config):
        """
        :type logger: logging.Logger
        :type runtime_config: cloudshell.layer_one.core.helper.runtime_configuration.RuntimeConfiguration
        """
        self._logger = logger
        self._logger.warn('started driver ')
        self._runtime_config = runtime_config

    def login(self, address, username, password):
        """
        Perform login operation on the device
        :param address: resource address, "192.168.42.240"
        :param username: username to login on the device
        :param password: password
        :return: None
        :raises Exception: if command failed
        Example:
            # Define session attributes
            self._cli_handler.define_session_attributes(
                address, username, password)

            # Obtain cli session
            with self._cli_handler.default_mode_service() as session:
                # Executing simple command
                device_info = session.send_command('show version')
                self._logger.info(device_info)

        raise NotImplementedError
        """

        self._logger.warn('received request ')

        port = 8000
        self.nto_session = NtoApiClient(host=address, username=username,
            password=password, port=port)
        self._logger.info('completed log in')

    def get_state_id(self):
        """
        Check if CS synchronized with the device.
        :return: Synchronization ID, GetStateIdResponseInfo(-1) if not used
        :rtype: cloudshell.layer_one.core.response.response_info.GetStateIdResponseInfo
        :raises Exception: if command failed

        Example:
            # Obtain cli session
            with self._cli_handler.default_mode_service() as session:
                # Execute command
                chassis_name = session.send_command('show chassis name')
                return chassis_name
        """
        return GetStateIdResponseInfo(-1)

    def set_state_id(self, state_id):
        """
        Set synchronization state id to the device, called after Autoload or SyncFomDevice commands
        :param state_id: synchronization ID
        :type state_id: str
        :return: None
        :raises Exception: if command failed

        Example:
            # Obtain cli session
            with self._cli_handler.config_mode_service() as session:
                # Execute command
                session.send_command('set chassis name {}'.format(state_id))
        """
        pass

    def map_bidi(self, src_port, dst_port):
        """
        Create a bidirectional connection between source and destination ports
        :param src_port: src port address, '192.168.42.240/1/21'
        :type src_port: str
        :param dst_port: dst port address, '192.168.42.240/1/22'
        :type dst_port: str
        :return: None
        :raises Exception: if command failed

        Example:
            with self._cli_handler.config_mode_service() as session:
                session.send_command('map bidir {0} {1}'.format(
                    convert_port(src_port), convert_port(dst_port)))

        """

        nto = self.nto_session
        src_port_name= src_port.split("/")[2]
        dst_port_name = dst_port.split("/")[2]

        #id1 = nto.getPortProperty(srcPortName, 'id')
        #id2 = nto.getPortProperty(dstPortName, 'id')
        src_port_id = nto.getCtePort(src_port_name)['uuid']
        dst_port_id = nto.getCtePort(dst_port_name)['uuid']

        #nto.modifyPort(str(id1), {'mode': 'BIDIRECTIONAL', 'enabled': True})
        #nto.modifyPort(str(id2), {'mode': 'BIDIRECTIONAL', 'enabled': True})
        nto.modifyCtePort(str(src_port_id), {'mode': 'BIDIRECTIONAL', 'enabled': True})
        nto.modifyCtePort(str(dst_port_id), {'mode': 'BIDIRECTIONAL', 'enabled': True})


        self._logger.warn('getting  port ids')
        #result1 = nto.createFilter({'source_port_list': [id1], 'dest_port_list': [id2], 'mode': 'PASS_ALL'})
        #result2 = nto.createFilter({'source_port_list': [id2], 'dest_port_list': [id1], 'mode': 'PASS_ALL'})
        nto.createCteFilter({'source_port_uuid_list': [src_port_id], 'dest_port_uuid_list': [dst_port_id], 'mode': 'PASS_ALL'})
        nto.createCteFilter({'source_port_uuid_list': [dst_port_id], 'dest_port_uuid_list': [src_port_id], 'mode': 'PASS_ALL'})
        #self._logger.warn('results = ' + result1 + ' ' + result2)
        pass

    def map_uni(self, src_port, dst_ports):
        """
        Unidirectional mapping of two ports
        :param src_port: src port address, '192.168.42.240/1/21'
        :type src_port: str
        :param dst_ports: list of dst ports addresses, ['192.168.42.240/1/22', '192.168.42.240/1/23']
        :type dst_ports: list
        :return: None
        :raises Exception: if command failed

        Example:
            with self._cli_handler.config_mode_service() as session:
                for dst_port in dst_ports:
                    session.send_command(
                        'map {0} also-to {1}'.format(convert_port(src_port), convert_port(dst_port)))
        """
        raise NotImplementedError

    def get_resource_description(self, address):
        """
        Auto-load function to retrieve all information from the device
        :param address: resource address, '192.168.42.240'
        :type address: str
        :return: resource description
        :rtype: cloudshell.layer_one.core.response.response_info.ResourceDescriptionResponseInfo
        :raises cloudshell.layer_one.core.layer_one_driver_exception.LayerOneDriverException: Layer one exception.

        Example:

            from cloudshell.layer_one.core.response.resource_info.entities.chassis import Chassis
            from cloudshell.layer_one.core.response.resource_info.entities.blade import Blade
            from cloudshell.layer_one.core.response.resource_info.entities.port import Port
            from cloudshell.layer_one.core.response.resource_info. import Res

            chassis_resource_id = chassis_info.get_id()
            chassis_address = chassis_info.get_address()
            chassis_model_name = "Visionedge Chassis"
            chassis_serial_number = chassis_info.get_serial_number()
            chassis = Chassis(resource_id, address, model_name, serial_number)

            blade_resource_id = blade_info.get_id()
            blade_model_name = 'Generic L1 Module'
            blade_serial_number = blade_info.get_serial_number()
            blade.set_parent_resource(chassis)

            port_id = port_info.get_id()
            port_serial_number = port_info.get_serial_number()
            port = Port(port_id, 'Generic L1 Port', port_serial_number)
            port.set_parent_resource(blade)

            return ResourceDescriptionResponseInfo([chassis])
        """
        #self._logger.warn('getting resources 1 ')

        from cloudshell.layer_one.core.response.resource_info.entities.chassis import Chassis
        from cloudshell.layer_one.core.response.resource_info.entities.blade import Blade
        from cloudshell.layer_one.core.response.resource_info.entities.port import Port
        from cloudshell.layer_one.core.response.response_info import ResourceDescriptionResponseInfo

        # chassis_resource_id = chassis_info.get_id()
        # chassis_address = chassis_info.get_address()
        chassis_model_name = "Visionedge Chassis"
        # chassis_serial_number = chassis_info.get_serial_number()
        chassis = Chassis("ChassisID", address, chassis_model_name, "C1")

        #self._logger.warn('getting resources 2 ')
        # blade_resource_id = blade_info.get_id()
        blade_model_name = 'Generic L1 Module'
        # blade_serial_number = blade_info.get_serial_number()
        blade = Blade("Bladeid", blade_model_name, "S1")
        blade.set_parent_resource(chassis)

        nto = self.nto_session

        # port_id = port_info.get_id()
        ports = nto.getAllCtePorts()
        for port_id in ports:
            # port_id = "P1-01"
            # port_serial_number = port_info.get_serial_number()
            self._logger.warn('getting resources port' + port_id['name'])
            port = Port(port_id['name'], 'Generic L1 Port', "P"+str(port_id['uuid']))
            port.set_parent_resource(blade)

        self._logger.warn('getting resources 3')

        return ResourceDescriptionResponseInfo([chassis])

    def map_clear(self, ports):
        """
        Remove simplex/multi-cast/duplex connection ending on the destination port
        :param ports: ports, ['192.168.42.240/1/21', '192.168.42.240/1/22']
        :type ports: list
        :return: None
        :raises Exception: if command failed

        Example:
            exceptions = []
            with self._cli_handler.config_mode_service() as session:
                for port in ports:
                    try:
                        session.send_command('map clear {}'.format(convert_port(port)))
                    except Exception as e:
                        exceptions.append(str(e))
                if exceptions:
                    raise Exception('self.__class__.__name__', ','.join(exceptions))
        """
        raise NotImplementedError

    def map_clear_to(self, src_port, dst_ports):
        """
        Remove simplex/multi-cast/duplex connection ending on the destination port
        :param src_port: src port address, '192.168.42.240/1/21'
        :type src_port: str
        :param dst_ports: list of dst ports addresses, ['192.168.42.240/1/21', '192.168.42.240/1/22']
        :type dst_ports: list
        :return: None
        :raises Exception: if command failed

        Example:
            with self._cli_handler.config_mode_service() as session:
                _src_port = convert_port(src_port)
                for port in dst_ports:
                    _dst_port = convert_port(port)
                    session.send_command('map clear-to {0} {1}'.format(_src_port, _dst_port))
        """
        nto = self.nto_session
        src_port_name = src_port.split("/")[2]
        dst_port_name = dst_ports[0].split("/")[2]

        #id1 = nto.getPortProperty(srcPortName, 'id')
        #id2 = nto.getPortProperty(dstPortName, 'id')
        src_port_id = nto.getCtePort(src_port_name)['uuid']
        #dst_port_id = nto.getCtePort(dst_port_name)['uuid']

        #filter1 = nto.getPort(str(id1))['dest_filter_list']
        #filter2 = nto.getPort(str(id2))['dest_filter_list']
        src_port_filter = nto.getCtePort(str(src_port_id))['dest_filter_uuid_list']
        #dst_port_filter = nto.getCtePort(str(dst_port_id))['dest_filter_uuid_list']


        #nto.deleteFilter(str(filter1[0]))
        #nto.deleteFilter(str(filter2[0]))
        nto.deleteCteFilter(str(src_port_filter[0]))
        #nto.deleteCteFilter(str(dst_port_filter[0]))

        #nto.modifyPort(str(id1), {'mode': 'NETWORK', 'enabled': False})
        #nto.modifyPort(str(id2), {'mode': 'NETWORK', 'enabled': False})
        nto.modifyCtePort(str(src_port_id), {'mode': 'NETWORK', 'enabled': False})
        #nto.modifyCtePort(str(dst_port_id), {'mode': 'NETWORK', 'enabled': False})

        pass

    def get_attribute_value(self, cs_address, attribute_name):
        """
        Retrieve attribute value from the device
        :param cs_address: address, '192.168.42.240/1/21'
        :type cs_address: str
        :param attribute_name: attribute name, "Port Speed"
        :type attribute_name: str
        :return: attribute value
        :rtype: cloudshell.layer_one.core.response.response_info.AttributeValueResponseInfo
        :raises Exception: if command failed

        Example:
            with self._cli_handler.config_mode_service() as session:
                command = AttributeCommandFactory.get_attribute_command(cs_address, attribute_name)
                value = session.send_command(command)
                return AttributeValueResponseInfo(value)
        """
        raise NotImplementedError

    def set_attribute_value(self, cs_address, attribute_name, attribute_value):
        """
        Set attribute value to the device
        :param cs_address: address, '192.168.42.240/1/21'
        :type cs_address: str
        :param attribute_name: attribute name, "Port Speed"
        :type attribute_name: str
        :param attribute_value: value, "10000"
        :type attribute_value: str
        :return: attribute value
        :rtype: cloudshell.layer_one.core.response.response_info.AttributeValueResponseInfo
        :raises Exception: if command failed

        Example:
            with self._cli_handler.config_mode_service() as session:
                command = AttributeCommandFactory.set_attribute_command(cs_address, attribute_name, attribute_value)
                session.send_command(command)
                return AttributeValueResponseInfo(attribute_value)
        """
        raise NotImplementedError

    def map_tap(self, src_port, dst_ports):
        """
        Add TAP connection
        :param src_port: port to monitor '192.168.42.240/1/21'
        :type src_port: str
        :param dst_ports: ['192.168.42.240/1/22', '192.168.42.240/1/23']
        :type dst_ports: list
        :return: None
        :raises Exception: if command failed

        Example:
            return self.map_uni(src_port, dst_ports)
        """
        raise NotImplementedError

    def set_speed_manual(self, src_port, dst_port, speed, duplex):
        """
        Set connection speed. It is not used with new standard
        :param src_port:
        :param dst_port:
        :param speed:
        :param duplex:
        :return:
        """
        raise NotImplementedError
