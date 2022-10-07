deviceList = [
	{
		"deviceURL": "internal://0000-0000-0000/pod/0",
		"available": "True",
		"synced": "True",
		"type": 1,
		"states": [
			{
				"type": 3,
				"name": "core:CountryCodeState",
				"value": "NL"
			},
			{
				"type": 2,
				"name": "internal:LightingLedPodModeState",
				"value": 0.05
			},
			{
				"type": 3,
				"name": "core:NameState",
				"value": "Box"
			},
			{
				"type": 3,
				"name": "internal:BatteryStatusState",
				"value": "no"
			},
			{
				"type": 3,
				"name": "core:LocalIPv4AddressState",
				"value": "192.168.1.1"
			},
			{
				"type": 3,
				"name": "core:ConnectivityState",
				"value": "online"
			}
		],
		"label": "Button",
		"subsystemId": 0,
		"attributes": [],
		"enabled": "True",
		"controllableName": "internal:PodV2Component",
		"definition": {
			"states": [
				{
					"name": "core:ConnectivityState"
				},
				{
					"name": "core:LocalIPv4AddressState"
				},
				{
					"name": "core:CountryCodeState"
				},
				{
					"name": "internal:LightingLedPodModeState"
				},
				{
					"name": "core:CyclicButtonState"
				},
				{
					"name": "core:NameState"
				},
				{
					"name": "internal:BatteryStatusState"
				}
			],
			"widgetName": "Pod",
			"attributes": [],
			"uiClass": "Pod",
			"commands": [
				{
					"commandName": "deactivateCalendar",
					"nparams": 0
				},
				{
					"commandName": "refreshPodMode",
					"nparams": 0
				},
				{
					"commandName": "getName",
					"nparams": 0
				},
				{
					"commandName": "setPodLedOff",
					"nparams": 0
				},
				{
					"nparams": 1,
					"commandName": "setCalendar",
					"paramsSig": "p1"
				},
				{
					"commandName": "update",
					"nparams": 0
				},
				{
					"commandName": "setPodLedOn",
					"nparams": 0
				},
				{
					"commandName": "refreshBatteryStatus",
					"nparams": 0
				},
				{
					"nparams": 1,
					"commandName": "setLightingLedPodMode",
					"paramsSig": "p1"
				},
				{
					"commandName": "activateCalendar",
					"nparams": 0
				},
				{
					"commandName": "refreshUpdateStatus",
					"nparams": 0
				},
				{
					"nparams": 1,
					"commandName": "setCountryCode",
					"paramsSig": "p1"
				}
			],
			"type": "ACTUATOR"
		}
	},
	{
		"deviceURL": "io://0000-0000-0000/1541661",
		"available": "True",
		"synced": "True",
		"type": 1,
		"states": [
			{
				"type": 3,
				"name": "core:StatusState",
				"value": "available"
			},
			{
				"type": 3,
				"name": "core:DiscreteRSSILevelState",
				"value": "good"
			},
			{
				"type": 1,
				"name": "core:RSSILevelState",
				"value": 100
			},
			{
				"type": 11,
				"name": "core:ManufacturerSettingsState",
				"value": {
					"current_position": 0
				}
			},
			{
				"type": 1,
				"name": "core:ClosureState",
				"value": 0
			},
			{
				"type": 3,
				"name": "core:OpenClosedState",
				"value": "open"
			},
			{
				"type": 1,
				"name": "core:TargetClosureState",
				"value": 0
			},
			{
				"type": 6,
				"name": "core:MovingState",
				"value": "False"
			},
			{
				"type": 3,
				"name": "core:NameState",
				"value": "Shutter01"
			},
			{
				"type": 1,
				"name": "core:Memorized1PositionState",
				"value": 86
			}
		],
		"label": "Shutter01",
		"subsystemId": 0,
		"attributes": [
			{
				"type": 3,
				"name": "core:Manufacturer",
				"value": "Somfy"
			},
			{
				"type": 3,
				"name": "core:FirmwareRevision",
				"value": "5100394X23"
			}
		],
		"enabled": "True",
		"controllableName": "io:RollerShutterGenericIOComponent",
		"definition": {
			"states": [
				{
					"name": "core:StatusState"
				},
				{
					"name": "core:NameState"
				},
				{
					"name": "core:AdditionalStatusState"
				},
				{
					"name": "core:TargetClosureState"
				},
				{
					"name": "core:SecuredPositionState"
				},
				{
					"name": "core:ManufacturerSettingsState"
				},
				{
					"name": "core:ClosureState"
				},
				{
					"name": "core:OpenClosedState"
				},
				{
					"name": "core:MovingState"
				},
				{
					"name": "core:ManufacturerDiagnosticsState"
				},
				{
					"name": "core:DiscreteRSSILevelState"
				},
				{
					"name": "core:RSSILevelState"
				},
				{
					"name": "core:Memorized1PositionState"
				}
			],
			"widgetName": "PositionableRollerShutter",
			"attributes": [
				{
					"name": "core:SupportedManufacturerSettingsCommands"
				},
				{
					"name": "core:Manufacturer"
				},
				{
					"name": "core:FirmwareRevision"
				}
			],
			"uiClass": "RollerShutter",
			"commands": [
				{
					"commandName": "stop",
					"nparams": 0
				},
				{
					"nparams": 1,
					"commandName": "setDeployment",
					"paramsSig": "p1"
				},
				{
					"nparams": 1,
					"commandName": "delayedStopIdentify",
					"paramsSig": "p1"
				},
				{
					"nparams": 2,
					"commandName": "runManufacturerSettingsCommand",
					"paramsSig": "p1,p2"
				},
				{
					"commandName": "down",
					"nparams": 0
				},
				{
					"nparams": 1,
					"commandName": "setClosure",
					"paramsSig": "p1"
				},
				{
					"commandName": "unpairAllOneWayControllers",
					"nparams": 0
				},
				{
					"nparams": 1,
					"commandName": "setConfigState",
					"paramsSig": "p1"
				},
				{
					"nparams": 1,
					"commandName": "pairOneWayController",
					"paramsSig": "p1,*p2"
				},
				{
					"commandName": "unpairAllOneWayControllersAndDeleteNode",
					"nparams": 0
				},
				{
					"nparams": 1,
					"commandName": "advancedRefresh",
					"paramsSig": "p1,*p2"
				},
				{
					"commandName": "refreshMemorized1Position",
					"nparams": 0
				},
				{
					"commandName": "startIdentify",
					"nparams": 0
				},
				{
					"commandName": "stopIdentify",
					"nparams": 0
				},
				{
					"commandName": "up",
					"nparams": 0
				},
				{
					"commandName": "open",
					"nparams": 0
				},
				{
					"commandName": "keepOneWayControllersAndDeleteNode",
					"nparams": 0
				},
				{
					"commandName": "sendIOKey",
					"nparams": 0
				},
				{
					"nparams": 1,
					"commandName": "setMemorized1Position",
					"paramsSig": "p1"
				},
				{
					"nparams": 1,
					"commandName": "wink",
					"paramsSig": "p1"
				},
				{
					"commandName": "close",
					"nparams": 0
				},
				{
					"nparams": 1,
					"commandName": "setName",
					"paramsSig": "p1"
				},
				{
					"commandName": "identify",
					"nparams": 0
				},
				{
					"nparams": 1,
					"commandName": "setPosition",
					"paramsSig": "p1"
				},
				{
					"nparams": 1,
					"commandName": "unpairOneWayController",
					"paramsSig": "p1,*p2"
				},
				{
					"nparams": 1,
					"commandName": "setSecuredPosition",
					"paramsSig": "p1"
				},
				{
					"commandName": "my",
					"nparams": 0
				},
				{
					"commandName": "getName",
					"nparams": 0
				}
			],
			"type": "ACTUATOR"
		}
	},
	{
		"deviceURL": "io://0000-0000-0000/2711689",
		"available": "True",
		"synced": "True",
		"type": 2,
		"states": [
			{
				"type": 3,
				"name": "core:StatusState",
				"value": "available"
			},
			{
				"type": 3,
				"name": "core:DiscreteRSSILevelState",
				"value": "normal"
			},
			{
				"type": 1,
				"name": "core:RSSILevelState",
				"value": 42
			},
			{
				"type": 1,
				"name": "core:LuminanceState",
				"value": 4498
			}
		],
		"label": "Sensor1",
		"subsystemId": 0,
		"attributes": [
			{
				"type": 3,
				"name": "core:PowerSourceType",
				"value": "battery"
			},
			{
				"type": 3,
				"name": "core:Manufacturer",
				"value": "Somfy"
			}
		],
		"enabled": "True",
		"controllableName": "io:LightIOSystemSensor",
		"definition": {
			"states": [
				{
					"name": "core:StatusState"
				},
				{
					"name": "core:DiscreteRSSILevelState"
				},
				{
					"name": "core:RSSILevelState"
				},
				{
					"name": "core:LuminanceState"
				},
				{
					"name": "core:SensorDefectState"
				}
			],
			"widgetName": "LuminanceSensor",
			"attributes": [
				{
					"name": "core:MaxSensedValue"
				},
				{
					"name": "core:PowerSourceType"
				},
				{
					"name": "core:MinSensedValue"
				},
				{
					"name": "core:MeasuredValueType"
				},
				{
					"name": "core:FirmwareRevision"
				},
				{
					"name": "core:Manufacturer"
				}
			],
			"uiClass": "LightSensor",
			"commands": [
				{
					"nparams": 1,
					"commandName": "advancedRefresh",
					"paramsSig": "p1"
				}
			],
			"type": "SENSOR"
		}
	},
	{
		"deviceURL": "internal://0000-0000-0000/alarm/0",
		"available": "True",
		"synced": "True",
		"type": 1,
		"states": [
			{
				"type": 3,
				"name": "internal:IntrusionDetectedState",
				"value": "notDetected"
			},
			{
				"type": 3,
				"name": "core:NameState",
				"value": "alarm name"
			},
			{
				"type": 3,
				"name": "internal:CurrentAlarmModeState",
				"value": "off"
			},
			{
				"type": 3,
				"name": "internal:TargetAlarmModeState",
				"value": "off"
			},
			{
				"type": 1,
				"name": "internal:AlarmDelayState",
				"value": 30
			}
		],
		"label": "Alarm1",
		"subsystemId": 0,
		"attributes": [],
		"enabled": "True",
		"controllableName": "internal:TSKAlarmComponent",
		"definition": {
			"states": [
				{
					"name": "internal:TargetAlarmModeState"
				},
				{
					"name": "internal:AlarmDelayState"
				},
				{
					"name": "core:NameState"
				},
				{
					"name": "internal:IntrusionDetectedState"
				},
				{
					"name": "internal:CurrentAlarmModeState"
				}
			],
			"widgetName": "TSKAlarmController",
			"attributes": [],
			"uiClass": "Alarm",
			"commands": [
				{
					"commandName": "arm",
					"nparams": 0
				},
				{
					"commandName": "alarmOn",
					"nparams": 0
				},
				{
					"commandName": "disarm",
					"nparams": 0
				},
				{
					"nparams": 1,
					"commandName": "setTargetAlarmMode",
					"paramsSig": "p1"
				},
				{
					"commandName": "on",
					"nparams": 0
				},
				{
					"commandName": "refreshAlarmDelay",
					"nparams": 0
				},
				{
					"commandName": "getName",
					"nparams": 0
				},
				{
					"commandName": "off",
					"nparams": 0
				},
				{
					"commandName": "alarmPartial2",
					"nparams": 0
				},
				{
					"nparams": 1,
					"commandName": "setName",
					"paramsSig": "p1"
				},
				{
					"commandName": "alarmOff",
					"nparams": 0
				},
				{
					"commandName": "alarmPartial1",
					"nparams": 0
				},
				{
					"nparams": 1,
					"commandName": "setIntrusionDetected",
					"paramsSig": "p1"
				},
				{
					"nparams": 1,
					"commandName": "setAlarmDelay",
					"paramsSig": "p1"
				},
				{
					"commandName": "refreshCurrentAlarmMode",
					"nparams": 0
				},
				{
					"commandName": "refreshIntrusionDetected",
					"nparams": 0
				}
			],
			"type": "ACTUATOR"
		}
	},
	{
		"deviceURL": "io://0000-0000-0000/14725444",
		"available": "True",
		"synced": "True",
		"type": 5,
		"states": [],
		"label": "IO (14725444)",
		"subsystemId": 0,
		"attributes": [],
		"enabled": "True",
		"controllableName": "io:StackComponent",
		"definition": {
			"states": [],
			"widgetName": "IOStack",
			"attributes": [],
			"uiClass": "ProtocolGateway",
			"commands": [
				{
					"nparams": 1,
					"commandName": "discoverActuators",
					"paramsSig": "p1"
				},
				{
					"commandName": "joinNetwork",
					"nparams": 0
				},
				{
					"nparams": 1,
					"commandName": "advancedSomfyDiscover",
					"paramsSig": "p1"
				},
				{
					"commandName": "resetNetworkSecurity",
					"nparams": 0
				},
				{
					"commandName": "shareNetwork",
					"nparams": 0
				},
				{
					"nparams": 0,
					"commandName": "discover1WayController",
					"paramsSig": "*p1,*p2"
				},
				{
					"nparams": 1,
					"commandName": "discoverSensors",
					"paramsSig": "p1"
				},
				{
					"commandName": "discoverSomfyUnsetActuators",
					"nparams": 0
				}
			],
			"type": "PROTOCOL_GATEWAY"
		}
	}
]
