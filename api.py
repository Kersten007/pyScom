#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##########################################################################################################################################
#                                                        Python-File Information                                                         #
##########################################################################################################################################
#
#   File:   Xcom_API.py
#   Author: Tobias Müller
#   Date:   2017.08.09
#
##########################################################################################################################################
#                                                             Requirements                                                               #
##########################################################################################################################################

import struct

##########################################################################################################################################
#                                                     Class Definition & Description                                                     #
##########################################################################################################################################

#   This class is used to generate byte-frames, which are needed to communicate with Xtender-Moduls over the RS232-BUS with the Xcom-232i.
#   After generating  the byte-frame, you can use "pyserial" to communicate with the Serial-BUS and to put the byte-frame into the write-
#   method of "pyserial". You can decode also read-frames of the Serial-BUS with this class. 
#
#   This class contains methods to generate read- or write-frames, and methods to decode frames. There are pre-defined types, properties 
#   and formats for the most important parameter- and information-numbers. This reduces the effort for generating byte-frames, but there 
#   are extended methods to generate byte-frames with other parameter- and information-numbers.

class Xcom_API():

    """
    This class is used to generate byte-frames, which are needed to communicate with Xtender-Moduls over the RS232-BUS with the Xcom-232i.
    After generating  the byte-frame, you can use "pyserial" to communicate with the Serial-BUS and to put the byte-frame into the write-
    method of "pyserial". You can decode also read-frames of the Serial-BUS with this class. 

    This class contains methods to generate read- or write-frames, and methods to decode frames. There are pre-defined types, properties 
    and formats for the most important parameter- and information-numbers. This reduces the effort for generating byte-frames, but there 
    are extended methods to generate byte-frames with other parameter- and information-numbers.

    """

    ##################################################################################################################################
    #                                                     Program Information                                                        #
    ##################################################################################################################################

    __PROG_NAME                           = 'Xcom_API'
    __PROG_Version                        = 'v1.0'   

    ##################################################################################################################################
    #                                                Private-Object-Instance-Counter                                                 #
    ##################################################################################################################################

    __object_counter                      = 0

    ##################################################################################################################################
    #                                                  Private-Attributes-Service_ID                                                 #
    ##################################################################################################################################

    __service_read                         = 1
    __service_write                        = 2

    ##################################################################################################################################
    #                                                Protected-Attributes-Object_Type                                                #
    ##################################################################################################################################

    _object_type_info                     = 1
    _object_type_parameter                = 2
    _object_type_message                  = 3
    _object_type_datalog_field            = 5
    _object_type_datalog_transfer         = 257

    ##################################################################################################################################
    #                                              Protected-Attributes-Info-Object_ID                                               #
    ##################################################################################################################################


    INFO_BATTERY_VOLTAGE                 = 3000
    INFO_BATTERY_TEMPERATURE             = 3001
    INFO_BATTERY_CHARGE_CURRENT          = 3005
    INFO_BATTERY_VOLTAGE_RIPPLE          = 3006
    INFO_STATE_OF_CHARGE                 = 3007
    INFO_NUMBER_OF_BATTERY_ELEMENTS      = 3050
    INFO_INPUT_VOLTAGE                   = 3011
    INFO_INPUT_CURRENT                   = 3012
    INFO_INPUT_FREQUENCY                 = 3084
    INFO_INPUT_POWER                     = 3138
    INFO_OUTPUT_VOLTAGE                  = 3021
    INFO_OUTPUT_CURRENT                  = 3022
    INFO_OUTPUT_FREQUENCY                = 3085
    INFO_OUTPUT_POWER                    = 3139
    INFO_OPERATING_STATE                 = 3028
    INFO_BOOST_ACTIVE                    = 3019
    INFO_STATE_OF_INVERTER               = 3049
    INFO_STATE_OF_TRANSFER_RELAY         = 3020
    INFO_STATE_OF_OUTPUT_RELAY           = 3030
    INFO_STATE_OF_AUX_RELAY_1            = 3031
    INFO_STATE_OF_AUX_RELAY_2            = 3032
    INFO_STATE_OF_GROUND_RELAY           = 3074
    INFO_STATE_OF_NEUTRAL_TRANSFER_RELAY = 3075
    INFO_STATE_OF_REMOTE_ENTRY           = 3086

    Obj = {"INFO_BATTERY_VOLTAGE" : 3000}

    ##################################################################################################################################
    #                                           Protected-Attributes-Parameter-Object_ID                                             #
    ##################################################################################################################################

    PARA_MAXIMUM_CURRENT_OF_AC_SOURCE    = 1107
    PARA_BATTERY_CHARGE_CURRENT          = 1138
    PARA_SMART_BOOST_ALLOWED             = 1126
    PARA_INVERTER_ALLOWED                = 1124
    PARA_TYPE_OF_DETECTION_OF_GRID_LOSS  = 1552
    PARA_CHARGER_ALLOWED                 = 1125
    PARA_CHARGER_USES_ONLY_POWER_FROM_AC = 1646
    PARA_AC_OUTPUT_VOLTAGE               = 1286
    PARA_INVERTER_FREQUENCY              = 1112
    PARA_TRANSFER_RELAY_ALLOWED          = 1128
    PARA_LIMITATION_OF_THE_POWER_BOOST   = 1607
    PARA_REMOTE_ENTRY_ACTIVE             = 1545

    ##################################################################################################################################
    #                                               Protected-Attributes-Property_ID                                                 #
    ##################################################################################################################################

    _property_id_value                    = 1
    _property_id_string                   = 1
    _property_id_value_qsp                = 5
    _property_id_min_qsp                  = 6
    _property_id_max_qsp                  = 7
    _property_id_level_qsp                = 8
    _property_id_unsaved_value_qsp        = 13
    _property_id_invalid_Action           = 0
    _property_id_sd_start                 = 21
    _property_id_sd_datablock             = 22
    _property_id_sd_ack_continue          = 23
    _property_id_sd_nack_retry            = 24
    _property_id_sd_abort                 = 25
    _property_id_sd_finish                = 26

    ##################################################################################################################################
    #                                                  Protected-Attributes-Format                                                   #
    ##################################################################################################################################

    _format_bool                          = [1,1]
    _format_format                        = [2,2]
    _format_short_int                     = [3,2]
    _format_enum                          = [4,2]
    _format_short_enum                    = [5,2]
    _format_long_enum                     = [6,4]
    _format_error                         = [7,2]
    _format_int32                         = [8,4]
    _format_float                         = [9,4]
    _format_byte                          = [10,1]

    ##################################################################################################################################
    #                                                        Private-Level-QSP                                                       #
    ##################################################################################################################################
    
    __level_qsp_view_only                 = 0x0000
    __level_qsp_basic                     = 0x0010
    __level_qsp_expert                    = 0x0020
    __level_qsp_installer                 = 0x0030
    __level_qsp_qsp                       = 0x0040

    ##################################################################################################################################
    #                                                       Private-Attributes                                                       #
    ##################################################################################################################################
                             
    __start_byte                          = 0xAA
    __frame_flags                         = 0x00
    __data_flags                          = 0x00
    __data_frame                          = 0x0A

    #   Dictionary of Error-Codes-Descriptions

    __error_code_dict   =  {0x0001  :   'INVALID_FRAME',
                            0x0002  :   'DEVICE_NOT_FOUND',
                            0x0003  :   'RESPONSE_TIMEOUT',
                            0x0011  :   'SERVICE_NOT_SUPPORTED',
                            0x0012  :   'INVALID_SERVICE_ARGUMENT',
                            0x0013  :   'SCOM_ERROR_GATEWAY_BUSY',
                            0x0021  :   'TYPE_NOT_SUPPORTED',
                            0x0022  :   'OBJECT_ID_NOT_FOUND',
                            0x0023  :   'PROPERTY_NOT_SUPPORTED',
                            0x0024  :   'INVALID_DATA_LENGTH',
                            0x0025  :   'PROPERTY_IS_READ_ONLY',
                            0x0026  :   'INVALID_DATA',
                            0x0027  :   'DATA_TOO_SMALL',
                            0x0028  :   'DATA_TO_BIG',
                            0x0029  :   'WRITE_PROPERTY_FAILED',
                            0x002A  :   'READ_PROPERTY_FAILED',
                            0X002B  :   'ACCESS_DENIED',
                            0x002C  :   'SCOM_ERROR_OBJECT_NOT_SUPPORTED',
                            0x002D  :   'SCOM_ERROR_MULTICAST_READ_NOT_SUPPORTED',
                            0x002E  :   'OBJECT_PROPERTY_INVALID',
                            0x002F  :   'FILE_OR_DIR_NOT_PRESENT',
                            0x0030  :   'FILE_CORRUPTED',
                            0x0081  :   'INVALID_SHELL_ARG'}

    #   Dictionary of Parameter-Info-Numbers with type, property and format

    __para_info_dict    =  {INFO_BATTERY_VOLTAGE    :   [_object_type_info,_property_id_value,_format_float],
                            INFO_BATTERY_TEMPERATURE    :   [_object_type_info,_property_id_value,_format_float],
                            3005    :   [_object_type_info,_property_id_value,_format_float],
                            3006    :   [_object_type_info,_property_id_value,_format_float],
                            3007    :   [_object_type_info,_property_id_value,_format_float],
                            3050    :   [_object_type_info,_property_id_value,_format_float],
                            3011    :   [_object_type_info,_property_id_value,_format_float],
                            3012    :   [_object_type_info,_property_id_value,_format_float],
                            3084    :   [_object_type_info,_property_id_value,_format_float],
                            3138    :   [_object_type_info,_property_id_value,_format_float],
                            3020    :   [_object_type_info,_property_id_value,_format_short_enum],
                            3021    :   [_object_type_info,_property_id_value,_format_float],
                            3022    :   [_object_type_info,_property_id_value,_format_float],
                            3085    :   [_object_type_info,_property_id_value,_format_float],
                            3139    :   [_object_type_info,_property_id_value,_format_float],
                            3028    :   [_object_type_info,_property_id_value,_format_short_enum],
                            3019    :   [_object_type_info,_property_id_value,_format_short_enum],
                            3049    :   [_object_type_info,_property_id_value,_format_short_enum],
                            3030    :   [_object_type_info,_property_id_value,_format_short_enum],
                            3031    :   [_object_type_info,_property_id_value,_format_short_enum],
                            3032    :   [_object_type_info,_property_id_value,_format_short_enum],
                            3074    :   [_object_type_info,_property_id_value,_format_short_enum],
                            3075    :   [_object_type_info,_property_id_value,_format_short_enum],
                            3086    :   [_object_type_info,_property_id_value,_format_short_enum],
                            1107    :   [_object_type_parameter,_property_id_value_qsp,_format_float],
                            1138    :   [_object_type_parameter,_property_id_value_qsp,_format_float],
                            1126    :   [_object_type_parameter,_property_id_value_qsp,_format_bool],
                            1124    :   [_object_type_parameter,_property_id_value_qsp,_format_bool],
                            1552    :   [_object_type_parameter,_property_id_value_qsp,_format_long_enum],
                            1125    :   [_object_type_parameter,_property_id_value_qsp,_format_bool],
                            1646    :   [_object_type_parameter,_property_id_value_qsp,_format_bool],
                            1286    :   [_object_type_parameter,_property_id_value_qsp,_format_float],
                            1112    :   [_object_type_parameter,_property_id_value_qsp,_format_float],
                            1128    :   [_object_type_parameter,_property_id_value_qsp,_format_bool],
                            1607    :   [_object_type_parameter,_property_id_value_qsp,_format_float],
                            1545    :   [_object_type_parameter,_property_id_value_qsp,_format_long_enum]}


    ##################################################################################################################################
    #                                                       Constructor-Method                                                       #
    ##################################################################################################################################

    #   This Method is used with generating an object of the Xcom_API-Class. There are pre-defined arguments (CRC-Check, source-address, 
    #   destination-address) for this object, when you generate an objects without relevant arguments.

    def __init__(self, crc = True, source = 1, destination = 101):

        """
        ### Description:
        This Method is used with generating an object of the Xcom_API-Class. There are predefined arguments (CRC-Check, source-address,
        destination-address) for this object, when you generate an objects without relevant arguments.

        ### Arguments:
        There are predefined arguments, which you can change:

        +-+-+
        | | |
        +=+=+
        | **crc** | = True |
        +-+-+
        | **source** | = 1 |
        +-+-+
        | **destination** | = 101 |
        +-+-+

        ### Return-Value:
        This Method return an object of the Xcom_API-Class. 

        ### Example-Code:

        ```>>> Object = Xcom_API()

        **Or if you want to change predefined arguments:**
        ```>>> Object = Xcom_API(crc = False)
        """
        
        # Check the type of the argument "crc". It raises a "ValueError" with a false type.
        if not isinstance(crc, bool):
            raise ValueError('CRC is not type \"bool\"!')

        # Check the type of the argument "source". It raises a "ValueError" with a false type.
        elif not isinstance(source, int) or isinstance(source, bool):
            raise ValueError('Source-Address is not type \"int\"!')

        # Check the range of the argument "source" It raises a "ValueError", if the argument is out of range.
        elif not 0<source<100:
            raise ValueError('Source-Address is out of range!')

        # Check the type of the argument "destination" It raises a "ValueError" with a false type.
        elif not isinstance(destination, int) or isinstance(destination, bool):
            raise ValueError('Destination-Address is not type \"int\"!')

        # Check the range of the argument "destination" It raises a "ValueError", if the argument is out of range.
        elif not (destination==0 or destination==401 or destination==501 or destination==601 or 100<=destination<=109 or 
                191<=destination<=193 or 300<=destination<=315 or 700<=destination<=715):
            raise ValueError('Destination-Address is out of range!')

        # If there is no error, the arguments will be stored in variables of the object. The object-counter will be increased.
        else:
            self.__dest                = destination
            self.__source              = source
            self.__crc                 = crc
            self.__frame_check_done    = False
            Xcom_API.__object_counter += 1

    ##################################################################################################################################
    #                                                     Deconstructor-Method                                                       #
    ##################################################################################################################################

    #   This Method delete an object of this class with the stored variables and decrease the object-counter.

    def __del__(self):

        """
        ### Description:
        This Method delete an object of this class with the stored variables and decrease the object-counter.

        ### Example-Code:

        ```>>> Object = Xcom_API()
        >>> del Object
        """

        if hasattr(self,'__crc'):
            del self.__crc
        if hasattr(self,'__source'):
            del self.__source
        if hasattr(self,'__dest'):
            del self.__dest
        if hasattr(self,'__frame_check_done'):
            del self.__frame_check_done
        Xcom_API.__object_counter -= 1

    ##################################################################################################################################
    #                                                     Information-Methods                                                        #
    ##################################################################################################################################

    #   This method returns an integer-value of the source-address of an object.

    def get_source_address(self):

        """
        ### Description:
        This method returns an integer-value of the source-address of an object.

        ### Return-Value:
        This Method return an **int**.

        ### Example-Code:

        ```>>> Object = Xcom_API()
        >>> Src_Addr = Object.get_source_address()
        >>> Src_Addr
            1
        """

        return self.__source

    #   This method returns an integer-value of the destination-address of an object.
     
    def get_destination_address(self):

        """
        ### Description:
        This method returns an integer-value of the destination-address of an object.

        ### Return-Value:
        This Method return an **int**.

        ### Example-Code:

        ```>>> Object = Xcom_API()
        >>> Dest_Addr = Object.get_destination_address()
        >>> Dest_Addr
            101
        """

        return self.__dest

    #   This method returns a boolean-value of the active-state of the CRC-Check of an object.

    def is_crc_check_active(self):

        """
        ### Description:
        This method returns a boolean-value of the active-state of the CRC-Check of an object.

        ### Return-Value:
        This Method return a **boolean**.

        ### Example-Code:

        ```>>> Object = Xcom_API()
        >>> CRC_Active = Object.is_crc_check_active()
        >>> CRC_Active
            True
        """

        return self.__crc

    #   This method returns a integer-value of the counter of active-objects of this class.

    @staticmethod
    def get_object_counter():

        """
        ### Description:
        This method returns a integer-value of the counter of active-objects of this class.

        ### Return-Value:
        This Method return an **int**.

        ### Example-Code:

        ```>>> Obj_Count = Xcom_API.get_object_counter()
        >>> Obj_Count
            0

        **Or if you have generate an Object:**

        ```>>> Object = Xcom_API()
        >>> Obj_Count = Object.get_object_counter()
        >>> Obj_Count
            1
        """

        return  Xcom_API.__object_counter
    
    #   This method returns a string of the of the program-name of this class.

    @staticmethod
    def get_prog_name():

        """
        ### Description:
        This method returns a string of the of the program-name of this class.

        ### Return-Value:
        This Method return a **string**.

        ### Example-Code:

        ```>>> Prog_Name = Xcom_API.get_prog_name()
        >>> Prog_Name
            'Xcom_API'

        **Or if you have generate an Object:**

        ```>>> Object = Xcom_API()
        >>> Prog_Name = Object.get_prog_name()
        >>> Prog_Name
            'Xcom_API'
        """

        return Xcom_API.__PROG_NAME

    #   This method returns a string of the of the program-version of this class.

    @staticmethod
    def get_prog_version():

        """
        ### Description:
        This method returns a string of the of the program-version of this class.

        ### Return-Value:
        This Method return a **string**.

        ### Example-Code:

        ```>>> Prog_Version = Xcom_API.get_prog_version
        >>> Prog_Version
            'v1.0'

        **Or if you have generate an Object:**

        ```>>> Object = Xcom_API()
        >>> Prog_Version = Object.get_prog_version
        >>> Prog_Version
            'v1.0'
        """

        return Xcom_API.__PROG_Version

    ##################################################################################################################################
    #                                                       Private-Methods                                                          #
    ##################################################################################################################################

    #   This Method calculate the CRC-Values of a Frame. It returns the CRC-Values in a list or bytearray.

    def __calculate_checksum(byte_frame):

        """
        ### Description:
        This Method calculate the CRC-Values of a Frame. It returns the CRC-Values in a **list**.

        ### Arguments:
        The **<byte_frame>** argument must be a type of **list** or **bytearray**.

        ### Return-Value:
        This Method return a **list** of length two with the CRC-Values.

        ### Example-Code:

        ```>>> Byte_Frame = [0x0, 0x1, 0x0, 0x0, 0x0, 0x65, 0x0, 0x0, 0x0, 0xA, 0x0]
        >>> CRC_Value = Xcom_API.__calculate_checksum(Byte_Frame)
        >>> CRC_Value 
            [0x6F, 0x71]

        **Or if you are not using this function inside the API:**

        ```>>> Byte_Frame = [0x0, 0x1, 0x0, 0x0, 0x0, 0x65, 0x0, 0x0, 0x0, 0xA, 0x0]
        >>> CRC_Value  = Xcom_API._Xcom_API__calculate_checksum(Byte_Frame)
        >>> CRC_Value 
            [0x6F, 0x71]
        """

        # Define two Buffers for the CRC-Values.
        Buffer1 = 0xFF
        Buffer2 = 0

        # Calculate the CRC-Values of a Frame.
        for i in range(0,len(byte_frame)):
            Buffer1 = (Buffer1 + byte_frame[i]) % 256
            Buffer2 = (Buffer1 + Buffer2) % 256
            
        # Return the CRC-Values in a list.
        return [Buffer1, Buffer2]
    
    #   This Method generate a Byte-Frame of a Value depending of the format. It returns a list of Bytes, which are ordered in LSB to
    #   MSB.

    def __value_to_byte_frame(property_data, data_format):

        """
        ### Description:
        This Method generate a Byte-Frame of a Value depending of the format. It returns a list of Bytes, which are ordered in LSB to MSB.

        ### Arguments:
        The **<property_data>** argument must be a type of **int** or **float** depending of the type of **<data_format>**.

        For the **<data_format>** argument use one of the following formats:

        +-+-+
        | | |
        +=+=+
        | _format_bool | = [1, 1] |
        +-+-+
        | _format_format | = [2, 2] |
        +-+-+
        | _format_short_int | = [3, 2] |
        +-+-+
        | _format_enum | = [4, 2] |
        +-+-+
        | _format_short_enum | = [5, 2] |
        +-+-+
        | _format_long_enum | = [6, 4] |
        +-+-+
        | _format_error | = [7, 2] |
        +-+-+
        | _format_int32 | = [8, 4] |
        +-+-+
        | _format_float | = [9, 4] |
        +-+-+
        | _format_byte | = [10, 1] |
        +-+-+

        ### Return-Value:
        This Method return a **list** with values, which represents the **Byte_Frame**. The length of the **list** depends of the **<data_format>** argument.

        ### Example-Code:

        ```>>> Value = 12.0
        >>> Byte_Frame = Xcom_API.__value_to_byte_frame(Value, Xcom_API._format_float)
        >>> Byte_Frame
            [0x0, 0x0, 0x40, 0x41]

        **Or if you are not using this function inside the API:**

        ```>>> Value = 12.0
        >>> Byte_Frame = Xcom_API._Xcom_API__value_to_byte_frame(Value, Xcom_API._format_float)
        >>> Byte_Frame
            [0x0, 0x0, 0x40, 0x41]
        """

        # It checks the argument "data_format" for type "Bool" and check the range/type of "property_data", depending of the 
        # data_format. It raises an ValueError if the checks failed, otherwise it returns the list of the Byte-Frame.
        if   data_format==Xcom_API._format_bool:
            if not 0<=property_data<=1 or not (isinstance(property_data, int) or isinstance(property_data, bool)):
                raise ValueError('Invalid \"property_data\" for the data_format of type \"bool\"!')
            else:
                # Return a list of the Byte-Frame.
                if property_data == 0 or property_data == False:
                    return [0]
                else:
                    return [1]

        # It checks the argument "data_format" for type "Byte" and check the range/type of "property_data", depending of the 
        # data_format. It raises an ValueError if the checks failed, otherwise it returns the list of the Byte-Frame.
        elif data_format==Xcom_API._format_byte:
            if not 0<=property_data<256 or not isinstance(property_data, int):
                raise ValueError('Invalid \"property_data\" for the data_format of type \"Byte\"!')
            else:
                # Return a list of the Byte-Frame.
                return [property_data]
        
        # It checks the argument "data_format" for type "Error" and check the range/type of "property_data", depending of the 
        # data_format. It raises an ValueError if the checks failed, otherwise it calculate and returns the list of the Byte-Frame.
        elif data_format==Xcom_API._format_error:
            if not 0<=property_data<=0x65535 or not isinstance(property_data, int):
                raise ValueError('Invalid \"property_data\" for the data_format of type \"Error\"!')
            else:
                # Define a Buffer for calculating.
                Buffer = hex(property_data)

                # Calculate the Byte-Frame.
                for i in range(0,data_format[1]*2-(len(Buffer)-2)):
                    Buffer = Buffer[0:2]+str(0)+Buffer[2:]

                # Return a list of the Byte-Frame.
                return [int(Buffer[4:6],16),int(Buffer[2:4],16)]

        # It checks the argument "data_format" for type "Format" or "Short Integer" and check the range/type of "property_data", 
        # depending of the data_format. It raises an ValueError if the checks failed, otherwise it calculate and returns the list of 
        # the Byte-Frame.
        elif data_format==Xcom_API._format_format or data_format==Xcom_API._format_short_int:
            if not -32768<=property_data<=32767 or not isinstance(property_data, int):
                raise ValueError('Invalid \"property_data\" for the data_format of type \"Format\" or \"Short Integer\"!')
            else:
                # Calculate the Byte-Frame.
                if property_data<0:
                    # Define a Buffer for calculating.
                    Buffer = hex(2**16 + property_data)

                else:
                    # Define a Buffer for calculating.
                    Buffer = hex(property_data)

                    for i in range(0,data_format[1]*2-(len(Buffer)-2)):
                        Buffer = Buffer[0:2]+str(0)+Buffer[2:]

                # Return a list of the Byte-Frame.
                return [int(Buffer[4:6],16),int(Buffer[2:4],16)]

        # It checks the argument "data_format" for type "Enum" or "Short Enum" and check the range/type of "property_data", depending 
        # of the data_format. It raises an ValueError if the checks failed, otherwise it calculate and returns the list of the Byte-Frame. 
        # Only one Bit can be set in data_format of type "Enum".
        elif data_format==Xcom_API._format_enum or data_format==Xcom_API._format_short_enum:
            if not 0<=property_data<=32767 or not isinstance(property_data, int):
                raise ValueError('Invalid \"property_data\" for the data_format of type \"Enum\" or \"Short Enum\"!')
            else:
                check = False
                for i in range(0,16):
                    if (2**i==2**i&property_data) and check:
                        raise ValueError('Invalid \"property_data\" for the data_format of type \"Enum\" or \"Short Enum\"!')
                    elif 2**i==2**i&property_data:
                        check = True

                # Define a Buffer for calculating.
                Buffer = hex(property_data)

                # Calculate the Byte-Frame.
                for i in range(0,data_format[1]*2-(len(Buffer)-2)):
                    Buffer = Buffer[0:2]+str(0)+Buffer[2:]

                # Return a list of the Byte-Frame.
                return [int(Buffer[4:6],16),int(Buffer[2:4],16)]

        # It checks the argument "data_format" for type "Long Enum" and check the range/type of "property_data", depending of the 
        # data_format. It raises an ValueError if the checks failed, otherwise it calculate and returns the list of the Byte-Frame. 
        # Only one Bit can be set in data_format of type "Enum".
        elif data_format==Xcom_API._format_long_enum:
            if not 0<=property_data<=2147483647 or not isinstance(property_data, int):
                raise ValueError('Invalid \"property_data\" for the data_format of type \"Long Enum\"!')
            else:
                check = False
                for i in range(0,32):
                    if (2**i==2**i&property_data) and check:
                        raise ValueError('Invalid \"property_data\" for the data_format of type \"Long Enum\"!')
                    elif 2**i==2**i&property_data:
                        check = True

                # Define a Buffer for calculating.
                Buffer = hex(property_data)

                # Calculate the Byte-Frame.
                for i in range(0,data_format[1]*2-(len(Buffer)-2)):
                    Buffer = Buffer[0:2]+str(0)+Buffer[2:]

                # Return a list of the Byte-Frame.
                return [int(Buffer[8:10],16),int(Buffer[6:8],16),int(Buffer[4:6],16),int(Buffer[2:4],16)]

        # It checks the argument "data_format" for type "INT32" and check the range/type of "property_data", depending of the 
        # data_format. It raises an ValueError if the checks failed, otherwise it calculate and returns the list of the Byte-Frame.
        elif data_format==Xcom_API._format_int32:
            if not -2147483648<=property_data<=2147483647 or not isinstance(property_data, int):
                raise ValueError('Invalid \"property_data\" for the data_format of type \"INT32\"!')
            else:
                # Calculate the Byte-Frame.
                if property_data<0:
                    # Define a Buffer for calculating.
                    Buffer = hex(2**32 + property_data)

                else:
                    # Define a Buffer for calculating.
                    Buffer = hex(property_data)
                    
                    for i in range(0,data_format[1]*2-(len(Buffer)-2)):
                        Buffer = Buffer[0:2]+str(0)+Buffer[2:]
                        
                # Return a list of the Byte-Frame.
                return [int(Buffer[8:10],16),int(Buffer[6:8],16),int(Buffer[4:6],16),int(Buffer[2:4],16)]

        # It checks the argument "data_format" for type "Float" and check the range/type of "property_data", depending of the 
        # data_format. It raises an ValueError if the checks failed, otherwise it calculate and returns the list of the Byte-Frame.
        elif data_format==Xcom_API._format_float:
            if not -2147483648<=property_data<=2147483647 or not isinstance(property_data, float):
                raise ValueError('Invalid \"property_data\" for the data_format of type \"Float\"!')
            else:
                # Calculate the Byte-Frame.
                Buffer = struct.pack("!f",property_data)

                # Return a list of the Byte-Frame.
                return [Buffer[3],Buffer[2],Buffer[1],Buffer[0]]

        # It raises an Error, if the argument "data_format" doesn't fit.
        else:
            raise ValueError('data_format is unknown!')

    #   This Method generate a Value of a Byte-Frame depending of the format. It returns the value as a integer/float.
    
    def __byte_frame_to_value(byte_frame, data_format):

        """
        ### Description:
        This Method generate a Value of a Byte-Frame depending of the format. It returns the value as a integer/float.

        ### Arguments:
        The **<byte_frame>** argument must be a type of **list** or **bytearray**. The lenght depends of the type of **<data_format>**.

        For the **<data_format>** argument use one of the following formats:

        +-+-+
        | | |
        +=+=+
        | _format_bool | = [1, 1] |
        +-+-+
        | _format_format | = [2, 2] |
        +-+-+
        | _format_short_int | = [3, 2] |
        +-+-+
        | _format_enum | = [4, 2] |
        +-+-+
        | _format_short_enum | = [5, 2] |
        +-+-+
        | _format_long_enum | = [6, 4] |
        +-+-+
        | _format_error | = [7, 2] |
        +-+-+
        | _format_int32 | = [8, 4] |
        +-+-+
        | _format_float | = [9, 4] |
        +-+-+
        | _format_byte | = [10, 1] |
        +-+-+

        ### Return-Value:
        This Method return a value of type **int** or **float** depending of the **<data_format>** argument.

        ### Example-Code:

        ```>>> Byte_Frame = [0x0, 0x0, 0x40, 0x41]
        >>> Value = Xcom_API.__byte_frame_to_value(Byte_Frame, Xcom_API._format_float)
        >>> Value
            12.0

        **Or if you are not using this function inside the API:**

        ```>>> Byte_Frame = [0x0, 0x0, 0x40, 0x41]
        >>> Value = Xcom_API._Xcom_API__byte_frame_to_value(Byte_Frame, Xcom_API._format_float)
        >>> Value
            12.0
        """

        # It checks the argument "data_format" for type "Bool" and check the length/type of "byte_frame", depending of the 
        # data_format. It raises an ValueError if the checks failed, otherwise it returns the value of the Byte-Frame.
        if   data_format==Xcom_API._format_bool:
            if not len(byte_frame)==data_format[1] or not isinstance(byte_frame[0], int) or not 0<=byte_frame[0]<=1:
                raise ValueError('Invalid \"byte_frame\" for the data_format of type \"bool\"!')
            else:
                # Return the value of the Byte-Frame.
                return byte_frame[0]
            
        # It checks the argument "data_format" for type "Byte" and check the length/type of "byte_frame", depending of the 
        # data_format. It raises an ValueError if the checks failed, otherwise it returns the value of the Byte-Frame.
        elif data_format==Xcom_API._format_byte:
            if not len(byte_frame)==data_format[1] or not isinstance(byte_frame[0], int):
                raise ValueError('Invalid \"byte_frame\" for the data_format of type \"Byte\"!')
            else:
                # Return the value of the Byte-Frame.
                return byte_frame[0]
        
        # It checks the argument "data_format" for type "Error" and check the length/type of "byte_frame", depending of the 
        # data_format. It raises an ValueError if the checks failed, otherwise it calculate and returns the value of the Byte-Frame.
        elif data_format==Xcom_API._format_error:
            if not len(byte_frame)==data_format[1] or not isinstance(byte_frame[0], int) or not isinstance(byte_frame[1], int):
                raise ValueError('Invalid \"byte_frame\" for the data_format of type \"Error\"!')
            else:
                # Define a Buffer.
                Buffer = '0x'

                # Calculate the value.
                for i in range(0,data_format[1]):
                    if len(hex(byte_frame[data_format[1]-1-i]))==4:
                        Buffer = Buffer + hex(byte_frame[data_format[1]-1-i])[2:]
                    else:
                        Buffer = Buffer + '0' + hex(byte_frame[data_format[1]-1-i])[2:]

                # Return the value of the Byte-Frame.
                return int(Buffer,16)

        # It checks the argument "data_format" for type "Format" or "Short Integer" and check the length/type of "byte_frame", depending 
        # of the data_format. It raises an ValueError if the checks failed, otherwise it calculate and returns the value of the Byte-Frame.
        elif data_format==Xcom_API._format_format or data_format==Xcom_API._format_short_int:
            if not len(byte_frame)==data_format[1] or not isinstance(byte_frame[0], int) or not isinstance(byte_frame[1], int):
                raise ValueError('Invalid \"byte_frame\" for the data_format of type \"Format\" or \"Short Integer\"!')
            else:
                # Define a Buffer.
                Buffer = '0x'

                # Calculate the value.
                for i in range(0,data_format[1]):
                    if len(hex(byte_frame[data_format[1]-1-i]))==4:
                        Buffer = Buffer + hex(byte_frame[data_format[1]-1-i])[2:]
                    else:
                        Buffer = Buffer + '0' + hex(byte_frame[data_format[1]-1-i])[2:]

                # Return the value of the Byte-Frame.
                if int(Buffer,16)<32768:
                    return int(Buffer,16)
                else:
                    return (-65536 + int(Buffer,16))

        # It checks the argument "data_format" for type "Enum" or "Short Enum" and check the length/type of "byte_frame", depending of the 
        # data_format. It raises an ValueError if the checks failed, otherwise it calculate and returns the value of the Byte-Frame.
        elif data_format==Xcom_API._format_enum or data_format==Xcom_API._format_short_enum:
            if not len(byte_frame)==data_format[1] or not isinstance(byte_frame[0], int) or not isinstance(byte_frame[1], int):
                raise ValueError('Invalid \"byte_frame\" for the data_format of type \"Enum\" or \"Short Enum\"!')
            else:
                # Define a Buffer.
                Buffer = '0x'

                # Calculate the value.
                for i in range(0,data_format[1]):
                    if len(hex(byte_frame[data_format[1]-1-i]))==4:
                        Buffer = Buffer + hex(byte_frame[data_format[1]-1-i])[2:]
                    else:
                        Buffer = Buffer + '0' + hex(byte_frame[data_format[1]-1-i])[2:]

                # Return the value of the Byte-Frame.
                if int(Buffer,16)<32768:
                    return int(Buffer,16)
                else:
                    raise ValueError('Invalid \"byte_frame\" for the data_format of type \"Enum\" or \"Short Enum\"!')
                
        # It checks the argument "data_format" for type "Long Enum" and check the length/type of "byte_frame", depending of the data_format.
        # It raises an ValueError if the checks failed, otherwise it calculate and returns the value of the Byte-Frame. 
        elif data_format==Xcom_API._format_long_enum:
            if (not len(byte_frame)==data_format[1] or not isinstance(byte_frame[0], int) or not isinstance(byte_frame[1], int)  
                or not isinstance(byte_frame[2], int) or not isinstance(byte_frame[3], int)):
                raise ValueError('Invalid \"byte_frame" for the data_format of type \"Long Enum\"!')
            else:
                # Define a Buffer.
                Buffer = '0x'

                # Calculate the value.
                for i in range(0,data_format[1]):
                    if len(hex(byte_frame[data_format[1]-1-i]))==4:
                        Buffer = Buffer + hex(byte_frame[data_format[1]-1-i])[2:]
                    else:
                        Buffer = Buffer + '0' + hex(byte_frame[data_format[1]-1-i])[2:]

                # Return the value of the Byte-Frame.
                if int(Buffer,16)<2147483648:
                    return int(Buffer,16)
                else:
                    raise ValueError('Invalid \"byte_frame" for the data_format of type \"Long Enum\"!')

        # It checks the argument "data_format" for type "INT32" and check the length/type of "byte_frame", depending of the data_format.
        # It raises an ValueError if the checks failed, otherwise it calculate and returns the value of the Byte-Frame.
        elif data_format==Xcom_API._format_int32:
            if (not len(byte_frame)==data_format[1] or not isinstance(byte_frame[0], int) or not isinstance(byte_frame[1], int)  
                or not isinstance(byte_frame[2], int) or not isinstance(byte_frame[3], int)):
                raise ValueError('Invalid \"byte_frame\" for the data_format of type \"INT32\"!')
            else:
                # Define a Buffer.
                Buffer = '0x'

                # Calculate the value.
                for i in range(0,data_format[1]):
                    if len(hex(byte_frame[data_format[1]-1-i]))==4:
                        Buffer = Buffer + hex(byte_frame[data_format[1]-1-i])[2:]
                    else:
                        Buffer = Buffer + '0' + hex(byte_frame[data_format[1]-1-i])[2:]

                # Return the value of the Byte-Frame.
                if int(Buffer,16)<2147483648:
                    return int(Buffer,16)
                else:
                    return (-4294967296 + int(Buffer,16))

        # It checks the argument "data_format" for type "Float" and check the length/type of "byte_frame", depending of the data_format.
        # It raises an ValueError if the checks failed, otherwise it calculate and returns the value of the Byte-Frame.
        elif data_format==Xcom_API._format_float:
            if (not len(byte_frame)==data_format[1] or not isinstance(byte_frame[0], int) or not isinstance(byte_frame[1], int)  
                or not isinstance(byte_frame[2], int) or not isinstance(byte_frame[3], int)):
                raise ValueError('Invalid \"byte_frame\" for the data_format of type \"Float\"!')
            else:
                # Define a Buffer.
                Buffer = bytearray([byte_frame[3],byte_frame[2],byte_frame[1],byte_frame[0]])

                # Calculate and return the value of the Byte-Frame.
                return struct.unpack("!f",Buffer)[0]     

        # It raises an Error, if the argument "format" doesn't fit.
        else:
            raise ValueError('data_format is unknown!')

    
    #   This Method does a Frame-Check. It checks the startbyte, Frame-Length, the checksum and the response-flags. It returns a 
    #   boolean-value of the result.

    def __frame_check(self,bytearray_of_frame):

        """
        ### Description:
        This Method does a Frame-Check. It checks the startbyte, Frame-Length, the checksum and the response-flags. It returns a 
        boolean-value of the result.

        ### Arguments:
        The **<self>** argument must be an object. The **<bytearray_of_frame>** argument is a complete Byte_frame.

        ### Return-Value:
        This Method return a **boolean**.

        ### Example-Code:

        ```>>> Object = Xcom_API()
        >>> Byte_Frame = [0xAA, 0x37, 0x65, 0x0, 0x0, 0x0, 0x1, 0x0, 0x0, 0x0, 0xA, 0x0, 0xA6, 0x5E, 0x2, 0x2, 0x2, 0x0, 0x53, 0x4, 0x0, 0x0, 0x5, 0x0, 0x61, 0x3C]
        >>> Check = Xcom_API.__frame_check(Object,Byte_Frame)
        >>> Check
            True

        **Or if you are not using this function inside the API:**

        ```>>> Object = Xcom_API()
        >>> Byte_Frame = [0xAA, 0x37, 0x65, 0x0, 0x0, 0x0, 0x1, 0x0, 0x0, 0x0, 0xA, 0x0, 0xA6, 0x5E, 0x2, 0x2, 0x2, 0x0, 0x53, 0x4, 0x0, 0x0, 0x5, 0x0, 0x61, 0x3C]
        >>> Check = Xcom_API._Xcom_API__frame_check(Object,Byte_Frame)
        >>> Check
            True
        """
        
        # Define Buffer for Frame_check.
        Buffer = list(bytearray_of_frame)
        
        try:
            # Check Start-Byte available  
            if not Buffer[0]==0xAA:
                raise ValueError('Can\'t find Start-Frame (0xAA)')

            # Check checksum if activated and check Frame-Length
            if self.__crc and len(Buffer)>=14:
                # check Header-Checksum
                if not Xcom_API.__calculate_checksum(Buffer[1:12])==Buffer[12:14]:
                    raise ValueError('Header-Checksum wrong!')

                # check Frame-Length
                if not len(Buffer)==(Xcom_API.__byte_frame_to_value(Buffer[10:12],Xcom_API._format_short_int) + 16):
                    raise ValueError('Frame is not complete!')

                # check Data-Checksum 
                if not Xcom_API.__calculate_checksum(Buffer[14:(len(Buffer)-2)])==Buffer[(len(Buffer)-2):len(Buffer)]:
                    raise ValueError('Data-Checksum wrong!')

            elif not self.__crc and len(Buffer)>=14:
                # check Frame-Length
                if not len(Buffer)==(Xcom_API.__byte_frame_to_value(Buffer[10:12],Xcom_API._format_short_int) + 16):
                    raise ValueError('Frame is not complete!')                

            else:
                raise ValueError('Frame is not complete!')
            
            # Check Response-Flags
            if not Buffer[14]>0:                      
                raise ValueError('Frame is not a Response-Frame!')

            return True
               
        except IndexError:
            raise ValueError('Frame is not complete!') 
        
    ##################################################################################################################################
    #                                                     Public-Methods                                                             #
    ##################################################################################################################################

    #   This method is used to generate a Byte-Frame for a 'read'-instruction. It Returns a bytearray.  
    
    def get_read_frame_ext(self, object_type, object_id, property_id):

        """
        ### Description:
        This method is used to generate a Byte-Frame for a 'read'-instruction. It Returns a bytearray.  

        ### Arguments:
        The **<self>** argument is pointing to the object, which calls the method.

        The **<object_type>** argument indicates the type of the **<object_id>**. The following shows the possibilities:

        +-+-+
        | | |
        +=+=+
        | _object_type_info                     | = 1 |
        +-+-+
        | _object_type_parameter                | = 2 |
        +-+-+
        | _object_type_message                  | = 3 |
        +-+-+
        | _object_type_datalog_field            | = 5 |
        +-+-+
        | _object_type_datalog_transfer         | = 257 |
        +-+-+

        The **<object_id>** argument indicates, which id should be read. You can find a list of all id's in the communication protocoll
        at http://www.studer-innotec.com/de/downloads/.


        The **<property_id>** argument indicates, which type the property_data has, which you want to read. The following shows the possibilities:

        +-+-+
        | | |
        +=+=+
        | _property_id_value                    | = 1 | 
        +-+-+
        | _property_id_string                   | = 1 | 
        +-+-+
        | _property_id_value_qsp                | = 5 | 
        +-+-+
        | _property_id_min_qsp                  | = 6 | 
        +-+-+
        | _property_id_max_qsp                  | = 7 | 
        +-+-+
        | _property_id_level_qsp                | = 8 | 
        +-+-+
        | _property_id_unsaved_value_qsp        | = 13 | 
        +-+-+
        | _property_id_invalid_Action           | = 0 | 
        +-+-+
        | _property_id_sd_start                 | = 21 | 
        +-+-+
        | _property_id_sd_datablock             | = 22 | 
        +-+-+
        | _property_id_sd_ack_continue          | = 23 | 
        +-+-+
        | _property_id_sd_nack_retry            | = 24 | 
        +-+-+
        | _property_id_sd_abort                 | = 25 | 
        +-+-+
        | _property_id_sd_finish                | = 26 | 
        +-+-+

        ### Return-Value:
        This Method return a **bytearray** of the frame.

        ### Example-Code:

        ```>>> Object = Xcom_API()
        >>> input_current = 3116
        >>> Byte_frame = Object.get_read_frame_ext(Xcom_API._object_type_info, input_current, Xcom_API._property_id_value)
        >>> Byte_frame
            bytearray(b'\\xAA\\x00\\x01\\x00\\x00\\x00\\x65\\x00\\x00\\x00\\x0A\\x00\\x6F\\x71\\x00\\x01\\x01\\x00\\x2C\\x0C\\x00\\x00\\x01\\x00\\x3A\\x4D')
        """
        
        # Create Buffer
        Buffer = []
        
        # Append Buffer with Start-Byte.
        Buffer.append(Xcom_API.__start_byte)
        
        # Append Buffer with Frame-Flags.
        Buffer.append(Xcom_API.__frame_flags)
        
        # Extend Buffer with Source-Address.
        Buffer.extend(Xcom_API.__value_to_byte_frame(self.__source,Xcom_API._format_int32))
        
        # Extend Buffer with Destination-Address.
        Buffer.extend(Xcom_API.__value_to_byte_frame(self.__dest,Xcom_API._format_int32))
        
        # Extend Buffer with Data-Length.
        Buffer.extend(Xcom_API.__value_to_byte_frame(Xcom_API.__data_frame,Xcom_API._format_short_int))
        
        # Extend Buffer with Header-Checksum.
        Buffer.extend(Xcom_API.__calculate_checksum(Buffer[1:len(Buffer)]))
        
        # Append Buffer with Data-Flags.
        Buffer.append(Xcom_API.__data_flags)
        
        # Append Buffer with Service_ID.
        Buffer.append(Xcom_API.__service_read)
        
        # Extend Buffer with Opject_Type.
        Buffer.extend(Xcom_API.__value_to_byte_frame(object_type,Xcom_API._format_short_int))
        
        # Extend Buffer with Object_ID.
        Buffer.extend(Xcom_API.__value_to_byte_frame(object_id,Xcom_API._format_int32))
        
        # Extend Buffer with Property_ID.
        Buffer.extend(Xcom_API.__value_to_byte_frame(property_id,Xcom_API._format_short_int))
        
        # Extend Buffer with Data-Checksum.
        Buffer.extend(Xcom_API.__calculate_checksum(Buffer[14:len(Buffer)]))
        
        # Return Byte-Frame.
        return bytearray(Buffer)
        
    #   This method is used to generate a Byte-Frame for a 'write'-instruction. It Returns a List of Bytes.
    
    def get_write_frame_ext(self, object_type, object_id, property_id, property_data, data_format):

        """
        ### Description:
        This method is used to generate a Byte-Frame for a 'write'-instruction. It Returns a bytearray. 

        ### Arguments:
        The **<self>** argument is pointing to the object, which calls the method.

        The **<object_type>** argument indicates the type of the **<object_id>**. The following shows the possibilities:

        +-+-+
        | | |
        +=+=+
        | _object_type_info                     | = 1 |
        +-+-+
        | _object_type_parameter                | = 2 |
        +-+-+
        | _object_type_message                  | = 3 |
        +-+-+
        | _object_type_datalog_field            | = 5 |
        +-+-+
        | _object_type_datalog_transfer         | = 257 |
        +-+-+

        The **<object_id>** argument indicates, which id should be written. You can find a list of all id's in the communication protocoll
        at http://www.studer-innotec.com/de/downloads/.


        The **<property_id>** argument indicates, which type the property_data has, which you want to read. The following shows the possibilities:

        +-+-+
        | | |
        +=+=+
        | _property_id_value                    | = 1 | 
        +-+-+
        | _property_id_string                   | = 1 | 
        +-+-+
        | _property_id_value_qsp                | = 5 | 
        +-+-+
        | _property_id_min_qsp                  | = 6 | 
        +-+-+
        | _property_id_max_qsp                  | = 7 | 
        +-+-+
        | _property_id_level_qsp                | = 8 | 
        +-+-+
        | _property_id_unsaved_value_qsp        | = 13 | 
        +-+-+
        | _property_id_invalid_Action           | = 0 | 
        +-+-+
        | _property_id_sd_start                 | = 21 | 
        +-+-+
        | _property_id_sd_datablock             | = 22 | 
        +-+-+
        | _property_id_sd_ack_continue          | = 23 | 
        +-+-+
        | _property_id_sd_nack_retry            | = 24 | 
        +-+-+
        | _property_id_sd_abort                 | = 25 | 
        +-+-+
        | _property_id_sd_finish                | = 26 | 
        +-+-+

        The **<property_data>** argument is the value you want to send. The format depends of the **<data_format>** argument.

        For the **<data_format>** argument use one of the following formats:

        +-+-+
        | | |
        +=+=+
        | _format_bool | = [1, 1] |
        +-+-+
        | _format_format | = [2, 2] |
        +-+-+
        | _format_short_int | = [3, 2] |
        +-+-+
        | _format_enum | = [4, 2] |
        +-+-+
        | _format_short_enum | = [5, 2] |
        +-+-+
        | _format_long_enum | = [6, 4] |
        +-+-+
        | _format_error | = [7, 2] |
        +-+-+
        | _format_int32 | = [8, 4] |
        +-+-+
        | _format_float | = [9, 4] |
        +-+-+
        | _format_byte | = [10, 1] |
        +-+-+

        
        ### Return-Value:
        This Method return a **bytearray** of the frame.

        ### Example-Code:

        ```>>> Object = Xcom_API()
        >>> Equalization_current = 1290
        >>> Data_in_Ampere = 120.0
        >>> Byte_frame = Object.get_write_frame_ext(Xcom_API._object_type_parameter, Equalization_current, Xcom_API._property_id_value, Data_in_Ampere, Xcom_API._format_float)
        >>> Byte_frame
            bytearray(b'\\xAA\\x00\\x01\\x00\\x00\\x00\\x65\\x00\\x00\\x00\\x0E\\x00\\x73\\x79\\x00\\x02\\x02\\x00\\x0A\\x05\\x00\\x00\\x01\\x00\\x00\\x00\\xF0\\x42\\x45\\xDD')
        """
        
        # Create Buffer
        Buffer = []
    
        # Append Buffer with Start-Byte.
        Buffer.append(Xcom_API.__start_byte)
    
        # Append Buffer with Frame-Flags.
        Buffer.append(Xcom_API.__frame_flags)
    
        # Extend Buffer with Source-Address.
        Buffer.extend(Xcom_API.__value_to_byte_frame(self.__source,Xcom_API._format_int32))
    
        # Extend Buffer with Destination-Address.
        Buffer.extend(Xcom_API.__value_to_byte_frame(self.__dest,Xcom_API._format_int32))
    
        # Extend Buffer with Data-Length.
        Buffer.extend(Xcom_API.__value_to_byte_frame(Xcom_API.__data_frame + data_format[1],Xcom_API._format_short_int))
    
        # Extend Buffer with Header-Checksum.
        Buffer.extend(Xcom_API.__calculate_checksum(Buffer[1:len(Buffer)]))
    
        # Append Buffer with Data-Flags.
        Buffer.append(Xcom_API.__data_flags)
    
        # Append Buffer with Service_ID.
        Buffer.append(Xcom_API.__service_write)
    
        # Extend Buffer with Opject_Type.
        Buffer.extend(Xcom_API.__value_to_byte_frame(object_type,Xcom_API._format_short_int))
    
        # Extend Buffer with Object_ID.
        Buffer.extend(Xcom_API.__value_to_byte_frame(object_id,Xcom_API._format_int32))
    
        # Extend Buffer with Property_ID.
        Buffer.extend(Xcom_API.__value_to_byte_frame(property_id,Xcom_API._format_short_int))
        
        # Extend Buffer with Property_Data.
        Buffer.extend(Xcom_API.__value_to_byte_frame(property_data,data_format))
        
        # Extend Buffer with Data-Checksum.
        Buffer.extend(Xcom_API.__calculate_checksum(Buffer[14:len(Buffer)]))
    
        # Return Byte-Frame.
        return bytearray(Buffer)

    #   This method is used to decode Data from the received Byte-Frame, what you get from the xtender-system.
    #   It returns a List with the result of the returned Data and the Data itself.

    def get_data_from_frame_ext(self, bytearray_of_frame, data_format):

        """
        ### Description:
        This method is used to decode Data from the received Byte-Frame, what you get from the xtender-system. 
        If CRC-Check is active, it will check the byte-frame and raises a Value_Error, if a CRC-Error was detected. 
        It returns a List with the result of the returned Data and the Data itself.

        ### Arguments:
        The **<self>** argument is pointing to the object, which calls the method.

        The **<bytearray_of_frame>** argument is the frame what you get, when you receive data from the serial port.

        The **<data_format>** argument is needed to decode the value. For the **<data_format>** argument use one of the following formats:

        +-+-+
        | | |
        +=+=+
        | _format_bool | = [1, 1] |
        +-+-+
        | _format_format | = [2, 2] |
        +-+-+
        | _format_short_int | = [3, 2] |
        +-+-+
        | _format_enum | = [4, 2] |
        +-+-+
        | _format_short_enum | = [5, 2] |
        +-+-+
        | _format_long_enum | = [6, 4] |
        +-+-+
        | _format_error | = [7, 2] |
        +-+-+
        | _format_int32 | = [8, 4] |
        +-+-+
        | _format_float | = [9, 4] |
        +-+-+
        | _format_byte | = [10, 1] |
        +-+-+

        ### Return-Value:
        This Method return a **list** with two elements. The First is a **boolean** value, which is **True**, if the xtender-system detects an error and the second 
        element of the **list** then contains the error-id. If no error occures, then the first element is **False** und the second element contains the answer of your request.
        The returned value of the second element is a **string**, **int** or **float**, depending of the service (read/write) of the request frame and of the 
        **<data_format>** argument.

        ### Example-Code:

        ```>>> Object = Xcom_API()
        >>> Frame =  bytearray(b'\\xAA\\x37\\x65\\x00\\x00\\x00\\x01\\x00\\x00\\x00\\x0E\\x00\\xAA\\x66\\x02\\x01\\x02\\x00\\x53\\x04\\x00\\x00\\x05\\x00\\x00\\xD0\\x14\\x42\\x86\\x8D')
        >>> Answer = Object.get_data_from_frame_ext(Frame, Xcom_API._format_float)
        >>> Answer
            [False, 37.203125]
        """
        
        # Do a Frame-Check. If it fails, it returns a ValueError.
        if not self.__frame_check_done:
            if not Xcom_API.__frame_check(self, bytearray_of_frame):
                raise ValueError('Frame-Check failed!')
        self.__frame_check_done = False
        
        # Check Frame for an Error and return the value.
        if bytearray_of_frame[14] == 2:
            # Check if property_data available
            if len(bytearray_of_frame) == 26:
                return [False,'value_set']
            else:
                return [False, Xcom_API.__byte_frame_to_value(bytearray_of_frame[24:(24+data_format[1])],data_format)]
        else:
            return [True, Xcom_API.__byte_frame_to_value(bytearray_of_frame[24:(24+Xcom_API._format_error[1])],Xcom_API._format_error)]

    #   This method is used to generate a Byte-Frame for a 'read'-instruction. It can only be used with a known Object_ID, otherwise it 
    #   will raise a Value_Error. It Returns a bytearray.
    
    def get_read_frame(self, object_id):

        """
        ### Description:
        This method is used to generate a Byte-Frame for a 'read'-instruction. It can only be used with a known Object_ID, otherwise it
        will raise a Value_Error. It Returns a bytearray.

        ### Arguments:
        The **<self>** argument is pointing to the object, which calls the method.

        The **<object_id>** argument indicates, which id should be read. The following shows the possibilities:

        +-+-+
        | Information-Numbers | |
        +=+=+
        | _info_battery_voltage                 | = 3000 | 
        +-+-+
        | _info_battery_temperature             | = 3001 | 
        +-+-+
        | _info_battery_charge_current          | = 3005 | 
        +-+-+
        | _info_battery_voltage_ripple          | = 3006 | 
        +-+-+
        | _info_state_of_charge                 | = 3007 | 
        +-+-+
        | _info_number_of_battery_elements      | = 3050 | 
        +-+-+
        | _info_input_voltage                   | = 3011 | 
        +-+-+
        | _info_input_current                   | = 3012 | 
        +-+-+
        | _info_input_frequency                 | = 3084 | 
        +-+-+
        | _info_input_power                     | = 3138 | 
        +-+-+
        | _info_output_voltage                  | = 3021 | 
        +-+-+
        | _info_output_current                  | = 3022 | 
        +-+-+
        | _info_output_frequency                | = 3085 | 
        +-+-+
        | _info_output_power                    | = 3139 | 
        +-+-+
        | _info_operating_state                 | = 3028 | 
        +-+-+
        | _info_boost_active                    | = 3019 | 
        +-+-+
        | _info_state_of_inverter               | = 3049 | 
        +-+-+
        | _info_state_of_transfer_relay         | = 3020 | 
        +-+-+
        | _info_state_of_output_relay           | = 3030 | 
        +-+-+
        | _info_state_of_aux_relay_1            | = 3031 | 
        +-+-+
        | _info_state_of_aux_relay_2            | = 3032 | 
        +-+-+
        | _info_state_of_ground_relay           | = 3074 | 
        +-+-+
        | _info_state_of_neutral_transfer_relay | = 3075 | 
        +-+-+
        | _info_state_of_remote_entry           | = 3086 | 
        +-+-+
        
        +-+-+
        | Parameter-Numbers | |
        +=+=+
        | _para_maximum_current_of_ac_source    | = 1107 | 
        +-+-+
        | _para_battery_charge_current          | = 1138 | 
        +-+-+
        | _para_smart_boost_allowed             | = 1126 | 
        +-+-+
        | _para_inverter_allowed                | = 1124 | 
        +-+-+
        | _para_type_of_detection_of_grid_loss  | = 1552 | 
        +-+-+
        | _para_charger_allowed                 | = 1125 | 
        +-+-+
        | _para_charger_uses_only_power_from_ac | = 1646 | 
        +-+-+
        | _para_ac_output_voltage               | = 1286 | 
        +-+-+
        | _para_inverter_frequency              | = 1112 | 
        +-+-+
        | _para_transfer_relay_allowed          | = 1128 | 
        +-+-+
        | _para_limitation_of_the_power_boost   | = 1607 | 
        +-+-+
        | _para_remote_entry_active             | = 1545 | 
        +-+-+

        ### Return-Value:
        This Method return a **bytearray** of the frame.

        ### Example-Code:

        ```>>> Object = Xcom_API()
        >>> Byte_frame = Object.get_read_frame(Xcom_API._info_battery_voltage)
        >>> Byte_frame
            bytearray(b'\\xAA\\x00\\x01\\x00\\x00\\x00\\x65\\x00\\x00\\x00\\x0A\\x00\\x6F\\x71\\x00\\x01\\x01\\x00\\xB8\\x0B\\x00\\x00\\x01\\x00\\xC5\\x90')
        """
        
        try:
            # Read Object-ID infomations from Dictionary and store it into a Buffer.
            Buffer = Xcom_API.__para_info_dict[object_id]
            
            # Return a Byte-Frame from the Read-Extenion method.
            return self.get_read_frame_ext(Buffer[0],object_id,Buffer[1])
        
        except KeyError:
            # If the Object_ID is unknown, the method raise a ValueError.
            raise ValueError('Object_ID unknown!')

    #   This method is used to generate a Byte-Frame for a 'write'-instruction. It can only be used with a known Object_ID, otherwise it 
    #   will raise a Value_Error. It Returns a bytearray.
        
    def get_write_frame(self, object_id, property_data):

        """
        ### Description:
        This method is used to generate a Byte-Frame for a 'write'-instruction. It can only be used with a known Object_ID, otherwise it 
        will raise a Value_Error. It Returns a bytearray.

        ### Arguments:
        The **<self>** argument is pointing to the object, which calls the method.

        The **<object_id>** argument indicates, which id should be written. The following shows the possibilities:
        
        +-+-+
        | | |
        +=+=+
        | _para_maximum_current_of_ac_source    | = 1107 | 
        +-+-+
        | _para_battery_charge_current          | = 1138 | 
        +-+-+
        | _para_smart_boost_allowed             | = 1126 | 
        +-+-+
        | _para_inverter_allowed                | = 1124 | 
        +-+-+
        | _para_type_of_detection_of_grid_loss  | = 1552 | 
        +-+-+
        | _para_charger_allowed                 | = 1125 | 
        +-+-+
        | _para_charger_uses_only_power_from_ac | = 1646 | 
        +-+-+
        | _para_ac_output_voltage               | = 1286 | 
        +-+-+
        | _para_inverter_frequency              | = 1112 | 
        +-+-+
        | _para_transfer_relay_allowed          | = 1128 | 
        +-+-+
        | _para_limitation_of_the_power_boost   | = 1607 | 
        +-+-+
        | _para_remote_entry_active             | = 1545 | 
        +-+-+

        The **<property_data>** argument is the value you want to send.

        ### Return-Value:
        This Method return a **bytearray** of the frame.

        ### Example-Code:

        ```>>> Object = Xcom_API()
        >>> Data_in_Ampere = 32.0
        >>> Byte_frame = Object.get_write_frame(Xcom_API._para_maximum_current_of_ac_source, Data_in_Ampere)
        >>> Byte_frame
            bytearray(b'\\xAA\\x00\\x01\\x00\\x00\\x00\\x65\\x00\\x00\\x00\\x0E\\x00\\x73\\x79\\x00\\x02\\x02\\x00\\x53\\x04\\x00\\x00\\x05\\x00\\x00\\x00\\x00\\x42\\xA1\\xE6')
        """
        
        try:
            # Read Object-ID infomations from Dictionary and store it into a Buffer.
            Buffer = Xcom_API.__para_info_dict[object_id]

            # Cheack for parameter
            if not Buffer[0] == Xcom_API._object_type_parameter:
                raise KeyError

            # Return a Byte-Frame from the Read-Extenion method.
            return self.get_write_frame_ext(Buffer[0],object_id,Buffer[1],property_data,Buffer[2])
        
        except KeyError:
            # If the Object_ID is unknown, the method raise a ValueError.
            raise ValueError('Object_ID unknown!')

    #   This method is used to decode Data from the received Byte-Frame, what you get from the xtender-system. It can only be used with a known Object_ID, 
    #   otherwise it will raise a Value_Error. It returns a List with the result of the returned Data and the Data itself.

    def get_data_from_frame(self, bytearray_of_frame):

        """
        ### Description:
        This method is used to decode Data from the received Byte-Frame, what you get from the xtender-system. 
        If CRC-Check is active, it will check the byte-frame and raises a Value_Error, if a CRC-Error was detected.
        It can only be used with a known Object_ID, otherwise it will raise a Value_Error. It returns a List with the result of the returned Data and the Data itself.

        ### Arguments:
        The **<self>** argument is pointing to the object, which calls the method.

        The **<bytearray_of_frame>** argument is the frame what you get, when you receive data from the serial port.

        ### Return-Value:
        This Method return a **list** with two elements. The First is a **boolean** value, which is **True**, if the xtender-system detects an error and the second 
        element of the **list** then contains the error-id. If no error occures, then the first element is **False** und the second element contains the answer of your request.
        The returned value of the second element is a **string**, **int** or **float**, depending of the service (read/write) of the request frame and of the 
        **<data_format>** argument.

        ### Example-Code:

        ```>>> Object = Xcom_API()
        >>> Frame =  bytearray(b'\\xAA\\x37\\x65\\x00\\x00\\x00\\x01\\x00\\x00\\x00\\x0E\\x00\\xAA\\x66\\x02\\x01\\x01\\x00\\xB8\\x0B\\x00\\x00\\x01\\x00\\x00\\x40\\x42\\x42\\x8B\\x46')
        >>> Answer = Object.get_data_from_frame(Frame)
        >>> Answer
            [False, 48.5625]
        """

        try:
            # Do a Frame-Check. If it fails, it returns a ValueError.
            if Xcom_API.__frame_check(self, bytearray_of_frame):
                self.__frame_check_done = True
            else:
                raise ValueError('Frame-Check failed!')

            # Read Object-ID infomations from Dictionary and store it into a Buffer.
            Buffer = Xcom_API.__para_info_dict[Xcom_API.__byte_frame_to_value(bytearray_of_frame[18:22],Xcom_API._format_int32)]
            
            # Return a Byte-Frame from the Read-Extension method.
            return self.get_data_from_frame_ext(bytearray_of_frame,Buffer[2])

        except KeyError:
            # If the Object_ID is unknown, the method raise a ValueError.
            self.__frame_check_done = False
            raise ValueError('Object_ID unknown!')

    #   This method is used to return the frame-flags as a binary.

    def get_bin_from_frame_flags(self, bytearray_of_frame):

        """
        ### Description:
        This method is used to return the frame-flags as a binary.

        ### Arguments:
        The **<self>** argument is pointing to the object, which calls the method.

        The **<bytearray_of_frame>** argument is the frame what you get, when you receive data from the serial port.

        ### Return-Value:
        The returned value is type **binary**.

        ### Example-Code:

        ```>>> Object = Xcom_API()
        >>> Frame =  bytearray(b'\\xAA\\x37\\x65\\x00\\x00\\x00\\x01\\x00\\x00\\x00\\x0E\\x00\\xAA\\x66\\x02\\x01\\x01\\x00\\xB8\\x0B\\x00\\x00\\x01\\x00\\x00\\x40\\x42\\x42\\x8B\\x46')
        >>> Answer = Object.get_bin_from_frame_flags(Frame)
        >>> Answer
            0b00110111
        """

        # Do a Frame-Check. If it fails, it returns a ValueError.
        if not Xcom_API.__frame_check(self, bytearray_of_frame):
            raise ValueError('Frame-Check failed!')

        # Create a Buffer with binary Information.
        Buffer = bin(bytearray_of_frame[1])

        # Extend Buffer to 8-bit
        for i in range(0,10-len(Buffer)):
            Buffer = Buffer[0:2] + '0' + Buffer[2:]
        
        # Return Buffer.
        return Buffer

    #   This method is used to return the frame-flags as a list with explanation (string) for each bit, starting from LSB to MSB.

    def get_text_from_frame_flags(self, bytearray_of_frame):

        """
        ### Description:
        This method is used to return the frame-flags as a **list** with explanation (**string**) for each bit, starting with lsb.

        ### Arguments:
        The **<self>** argument is pointing to the object, which calls the method.

        The **<bytearray_of_frame>** argument is the frame what you get, when you receive data from the serial port.

        ### Return-Value:
        The method returns a **list** with **strings** of explanation for each bit of the frame-flags, starting from LSB to MSB.

        ### Example-Code:

        ```>>> Object = Xcom_API()
        >>> Frame =  bytearray(b'\\xAA\\x37\\x65\\x00\\x00\\x00\\x01\\x00\\x00\\x00\\x0E\\x00\\xAA\\x66\\x02\\x01\\x01\\x00\\xB8\\x0B\\x00\\x00\\x01\\x00\\x00\\x40\\x42\\x42\\x8B\\x46')
        >>> Answer = Object.get_text_from_frame_flags(Frame)
        >>> Answer
            ['Messages are pending.','A reset or restart was carried out.','The SD-Card is present.','The SD-Card is not full.','New datalog file on the SD-Card.','Datalogger is supported.']
        """

        # Create Buffer and get binary from byte-frame.
        Buffer = self.get_bin_from_frame_flags(bytearray_of_frame)
        
        # Create Out-Buffer.
        BufferOut = []

        # Check bit 0.
        if int(Buffer[9]) == 1:
            BufferOut.append('Messages are pending.')
        else:
            BufferOut.append('No messages are pending.')

        # Check bit 1.
        if int(Buffer[8]) == 1:
            BufferOut.append('A reset or restart was carried out.')
        else:
            BufferOut.append('No reset or restart was carried out.')

        # Check bit 2.
        if int(Buffer[7]) == 1:
            BufferOut.append('The SD-Card is present.')
        else:
            BufferOut.append('No SD-Card is present')

        # Check bit 3.
        if int(Buffer[6]) == 1:
            BufferOut.append('The SD-Card is full.')
        else:
            BufferOut.append('The SD-Card is not full.')

        # Check bit 4.
        if int(Buffer[5]) == 1:
            BufferOut.append('New datalog file on the SD-Card.')
        else:
            BufferOut.append('No new datalog file on the SD-Card.')

        # Check bit 5.
        if int(Buffer[4]) == 1:
            BufferOut.append('Datalogger is supported.')
        else:
            BufferOut.append('Datalogger is not supported.')

        # Return list with Frame-flag informations.
        return BufferOut

    #   This method is used to get the error message from the error-id.

    def get_text_from_error_id(self, error_id):

        """
        ### Description:
        This method is used to get the error message from the error-id.

        ### Arguments:
        The **<self>** argument is pointing to the object, which calls the method.

        The **<error_id>** argument is an **int** from the xtender-system.

        ### Return-Value:
        The method returns a **strings** with the explanation of the error-id.

        ### Example-Code:

        ```>>> Object = Xcom_API()
        >>> Error_ID =  0x0022
        >>> Answer = Object.get_text_from_error_id(Error_ID)
        >>> Answer
            'OBJECT_ID_NOT_FOUND'
        """
        
        try:
            # Check ID and store error-message in Buffer
            Buffer = Xcom_API.__error_code_dict[error_id]

            # return error-message
            return Buffer

        except KeyError:
            # If Error ID is unknown
            return 'Error-ID is unknown.'