deviceListWeb = [
	{
		"creationTime": 1613477406000,
		"lastUpdateTime": 1613477406000,
		"label": "HOMEKIT (stack)",
		"deviceURL": "homekit://0000-0000-0000/stack",
		"shortcut": "False",
		"controllableName": "homekit:StackComponent",
		"definition": {
			"commands": [
				{
					"commandName": "deleteControllers",
					"nparams": 0
				}
			],
			"states": [],
			"dataProperties": [],
			"widgetName": "HomekitStack",
			"uiProfiles": [
				"Specific"
			],
			"uiClass": "ProtocolGateway",
			"qualifiedName": "homekit:StackComponent",
			"type": "PROTOCOL_GATEWAY"
		},
		"attributes": [
			{
				"name": "homekit:SetupCode",
				"type": 3,
				"value": "763-24-591"
			},
			{
				"name": "homekit:SetupPayload",
				"type": 3,
				"value": "X-HM://0024QDGJ3PCM9"
			}
		],
		"available": "True",
		"enabled": "True",
		"placeOID": "d33923b5-2ee0-4871-9207-594731f27983",
		"widget": "HomekitStack",
		"type": 5,
		"oid": "9cf9ef5d-32eb-4424-aea1-3706f690b080",
		"uiClass": "ProtocolGateway"
	},
	{
		"creationTime": 1552229933000,
		"lastUpdateTime": 1552229933000,
		"label": "Alarm",
		"deviceURL": "internal://0000-0000-0000/alarm/0",
		"shortcut": "False",
		"controllableName": "internal:TSKAlarmComponent",
		"definition": {
			"commands": [
				{
					"commandName": "alarmOff",
					"nparams": 0
				},
				{
					"commandName": "alarmOn",
					"nparams": 0
				},
				{
					"commandName": "arm",
					"nparams": 0
				},
				{
					"commandName": "disarm",
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
					"commandName": "on",
					"nparams": 0
				},
				{
					"commandName": "setName",
					"nparams": 1
				},
				{
					"commandName": "refreshAlarmDelay",
					"nparams": 0
				},
				{
					"commandName": "refreshCurrentAlarmMode",
					"nparams": 0
				},
				{
					"commandName": "refreshIntrusionDetected",
					"nparams": 0
				},
				{
					"commandName": "setAlarmDelay",
					"nparams": 1
				},
				{
					"commandName": "alarmPartial1",
					"nparams": 0
				},
				{
					"commandName": "alarmPartial2",
					"nparams": 0
				},
				{
					"commandName": "setIntrusionDetected",
					"nparams": 1
				},
				{
					"commandName": "setTargetAlarmMode",
					"nparams": 1
				}
			],
			"states": [
				{
					"type": "DataState",
					"qualifiedName": "core:NameState"
				},
				{
					"type": "ContinuousState",
					"qualifiedName": "internal:AlarmDelayState"
				},
				{
					"type": "DiscreteState",
					"values": [
						"off",
						"partial1",
						"partial2",
						"total"
					],
					"qualifiedName": "internal:CurrentAlarmModeState"
				},
				{
					"type": "DiscreteState",
					"values": [
						"detected",
						"notDetected",
						"pending",
						"sos"
					],
					"qualifiedName": "internal:IntrusionDetectedState"
				},
				{
					"type": "DiscreteState",
					"values": [
						"off",
						"partial1",
						"partial2",
						"sos",
						"total"
					],
					"qualifiedName": "internal:TargetAlarmModeState"
				}
			],
			"dataProperties": [],
			"widgetName": "TSKAlarmController",
			"uiProfiles": [
				"Alarm",
				"Switchable"
			],
			"uiClass": "Alarm",
			"qualifiedName": "internal:TSKAlarmComponent",
			"type": "ACTUATOR"
		},
		"states": [
			{
				"name": "internal:CurrentAlarmModeState",
				"type": 3,
				"value": "off"
			},
			{
				"name": "internal:AlarmDelayState",
				"type": 1,
				"value": 30
			},
			{
				"name": "internal:TargetAlarmModeState",
				"type": 3,
				"value": "off"
			},
			{
				"name": "internal:IntrusionDetectedState",
				"type": 3,
				"value": "notDetected"
			},
			{
				"name": "core:NameState",
				"type": 3,
				"value": "alarm name"
			}
		],
		"available": "True",
		"enabled": "True",
		"placeOID": "d33923b5-2ee0-4871-9207-594731f27983",
		"widget": "TSKAlarmController",
		"type": 1,
		"oid": "11c4cc7c-5f36-4357-8eef-0cbd26cca2aa",
		"uiClass": "Alarm"
	},
	{
		"creationTime": 1552229775000,
		"lastUpdateTime": 1552229775000,
		"label": "Button",
		"deviceURL": "internal://0000-0000-0000/pod/0",
		"shortcut": "False",
		"controllableName": "internal:PodV2Component",
		"metadata": {
			"tahoma": {
				"touchButtonFlag": "True"
			}
		},
		"definition": {
			"commands": [
				{
					"commandName": "getName",
					"nparams": 0
				},
				{
					"commandName": "update",
					"nparams": 0
				},
				{
					"commandName": "setCountryCode",
					"nparams": 1
				},
				{
					"commandName": "activateCalendar",
					"nparams": 0
				},
				{
					"commandName": "deactivateCalendar",
					"nparams": 0
				},
				{
					"commandName": "refreshBatteryStatus",
					"nparams": 0
				},
				{
					"commandName": "refreshPodMode",
					"nparams": 0
				},
				{
					"commandName": "refreshUpdateStatus",
					"nparams": 0
				},
				{
					"commandName": "setCalendar",
					"nparams": 1
				},
				{
					"commandName": "setLightingLedPodMode",
					"nparams": 1
				},
				{
					"commandName": "setPodLedOff",
					"nparams": 0
				},
				{
					"commandName": "setPodLedOn",
					"nparams": 0
				}
			],
			"states": [
				{
					"type": "DiscreteState",
					"values": [
						"offline",
						"online"
					],
					"qualifiedName": "core:ConnectivityState"
				},
				{
					"type": "DataState",
					"qualifiedName": "core:CountryCodeState"
				},
				{
					"type": "DiscreteState",
					"values": [
						"pressed",
						"stop"
					],
					"qualifiedName": "core:CyclicButtonState"
				},
				{
					"type": "DataState",
					"qualifiedName": "core:LocalIPv4AddressState"
				},
				{
					"type": "DataState",
					"qualifiedName": "core:NameState"
				},
				{
					"type": "ContinuousState",
					"qualifiedName": "internal:BatteryStatusState"
				},
				{
					"type": "ContinuousState",
					"qualifiedName": "internal:LightingLedPodModeState"
				}
			],
			"dataProperties": [],
			"widgetName": "Pod",
			"uiProfiles": [
				"UpdatableComponent"
			],
			"uiClass": "Pod",
			"qualifiedName": "internal:PodV2Component",
			"type": "ACTUATOR"
		},
		"states": [
			{
				"name": "internal:BatteryStatusState",
				"type": 3,
				"value": "no"
			},
			{
				"name": "core:CyclicButtonState",
				"type": 3,
				"value": "stop"
			},
			{
				"name": "internal:LightingLedPodModeState",
				"type": 2,
				"value": 0.05
			},
			{
				"name": "core:CountryCodeState",
				"type": 3,
				"value": "NL"
			},
			{
				"name": "core:LocalIPv4AddressState",
				"type": 3,
				"value": "192.168.60.216"
			},
			{
				"name": "core:NameState",
				"type": 3,
				"value": "Box"
			}
		],
		"available": "True",
		"enabled": "True",
		"placeOID": "d33923b5-2ee0-4871-9207-594731f27983",
		"widget": "Pod",
		"type": 1,
		"oid": "d8787f98-e571-48c5-b8a5-f1693c7a3500",
		"uiClass": "Pod"
	},
	{
		"creationTime": 1617117266000,
		"lastUpdateTime": 1617117266000,
		"label": "Shutter23",
		"deviceURL": "io://0000-0000-0000/10013480",
		"shortcut": "False",
		"controllableName": "io:RollerShutterGenericIOComponent",
		"definition": {
			"commands": [
				{
					"commandName": "advancedRefresh",
					"nparams": 2
				},
				{
					"commandName": "close",
					"nparams": 0
				},
				{
					"commandName": "delayedStopIdentify",
					"nparams": 1
				},
				{
					"commandName": "down",
					"nparams": 0
				},
				{
					"commandName": "getName",
					"nparams": 0
				},
				{
					"commandName": "identify",
					"nparams": 0
				},
				{
					"commandName": "my",
					"nparams": 0
				},
				{
					"commandName": "open",
					"nparams": 0
				},
				{
					"commandName": "refreshMemorized1Position",
					"nparams": 0
				},
				{
					"commandName": "setClosure",
					"nparams": 1
				},
				{
					"commandName": "setDeployment",
					"nparams": 1
				},
				{
					"commandName": "setMemorized1Position",
					"nparams": 1
				},
				{
					"commandName": "setName",
					"nparams": 1
				},
				{
					"commandName": "setPosition",
					"nparams": 1
				},
				{
					"commandName": "setSecuredPosition",
					"nparams": 1
				},
				{
					"commandName": "startIdentify",
					"nparams": 0
				},
				{
					"commandName": "stop",
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
					"commandName": "wink",
					"nparams": 1
				},
				{
					"commandName": "runManufacturerSettingsCommand",
					"nparams": 2
				},
				{
					"commandName": "keepOneWayControllersAndDeleteNode",
					"nparams": 0
				},
				{
					"commandName": "pairOneWayController",
					"nparams": 2
				},
				{
					"commandName": "sendIOKey",
					"nparams": 0
				},
				{
					"commandName": "setConfigState",
					"nparams": 1
				},
				{
					"commandName": "unpairAllOneWayControllersAndDeleteNode",
					"nparams": 0
				},
				{
					"commandName": "unpairAllOneWayControllers",
					"nparams": 0
				},
				{
					"commandName": "unpairOneWayController",
					"nparams": 2
				}
			],
			"states": [
				{
					"type": "DataState",
					"qualifiedName": "core:AdditionalStatusState"
				},
				{
					"type": "ContinuousState",
					"qualifiedName": "core:ClosureState"
				},
				{
					"type": "DiscreteState",
					"values": [
						"good",
						"low",
						"normal",
						"verylow"
					],
					"qualifiedName": "core:DiscreteRSSILevelState"
				},
				{
					"type": "DataState",
					"qualifiedName": "core:ManufacturerDiagnosticsState"
				},
				{
					"type": "DataState",
					"qualifiedName": "core:ManufacturerSettingsState"
				},
				{
					"type": "ContinuousState",
					"qualifiedName": "core:Memorized1PositionState"
				},
				{
					"type": "DiscreteState",
					"values": [
						"False",
						"True"
					],
					"qualifiedName": "core:MovingState"
				},
				{
					"type": "DataState",
					"qualifiedName": "core:NameState"
				},
				{
					"type": "DiscreteState",
					"values": [
						"closed",
						"open"
					],
					"qualifiedName": "core:OpenClosedState"
				},
				{
					"type": "ContinuousState",
					"qualifiedName": "core:PriorityLockTimerState"
				},
				{
					"type": "ContinuousState",
					"qualifiedName": "core:RSSILevelState"
				},
				{
					"type": "ContinuousState",
					"qualifiedName": "core:SecuredPositionState"
				},
				{
					"type": "DiscreteState",
					"values": [
						"available",
						"unavailable"
					],
					"qualifiedName": "core:StatusState"
				},
				{
					"type": "ContinuousState",
					"qualifiedName": "core:TargetClosureState"
				},
				{
					"type": "DiscreteState",
					"values": [
						"comfortLevel1",
						"comfortLevel2",
						"comfortLevel3",
						"comfortLevel4",
						"environmentProtection",
						"humanProtection",
						"userLevel1",
						"userLevel2"
					],
					"qualifiedName": "io:PriorityLockLevelState"
				},
				{
					"type": "DiscreteState",
					"values": [
						"LSC",
						"SAAC",
						"SFC",
						"UPS",
						"externalGateway",
						"localUser",
						"myself",
						"rain",
						"security",
						"temperature",
						"timer",
						"user",
						"wind"
					],
					"qualifiedName": "io:PriorityLockOriginatorState"
				}
			],
			"dataProperties": [
				{
					"value": "500",
					"qualifiedName": "core:identifyInterval"
				}
			],
			"widgetName": "PositionableRollerShutter",
			"uiProfiles": [
				"StatefulCloseableShutter",
				"StatefulCloseable",
				"Closeable",
				"StatefulOpenClose",
				"OpenClose"
			],
			"uiClass": "RollerShutter",
			"qualifiedName": "io:RollerShutterGenericIOComponent",
			"type": "ACTUATOR"
		},
		"states": [
			{
				"name": "core:NameState",
				"type": 3,
				"value": "Shutter23"
			},
			{
				"name": "core:PriorityLockTimerState",
				"type": 1,
				"value": 0
			},
			{
				"name": "core:StatusState",
				"type": 3,
				"value": "available"
			},
			{
				"name": "core:DiscreteRSSILevelState",
				"type": 3,
				"value": "low"
			},
			{
				"name": "core:RSSILevelState",
				"type": 2,
				"value": 38.0
			},
			{
				"name": "core:TargetClosureState",
				"type": 1,
				"value": 0
			},
			{
				"name": "core:ClosureState",
				"type": 1,
				"value": 0
			},
			{
				"name": "core:OpenClosedState",
				"type": 3,
				"value": "open"
			},
			{
				"name": "core:MovingState",
				"type": 6,
				"value": "False"
			},
			{
				"name": "core:Memorized1PositionState",
				"type": 1,
				"value": 85
			}
		],
		"attributes": [
			{
				"name": "core:Manufacturer",
				"type": 3,
				"value": "Somfy"
			},
			{
				"name": "core:SupportedManufacturerSettingsCommands",
				"type": 10,
				"value": [
					"dead_man_up",
					"dead_man_down",
					"dead_man_stop",
					"dead_man_impulse_up",
					"dead_man_impulse_down",
					"enter_settings_mode",
					"save_upper_end_limit",
					"save_lower_end_limit",
					"stop_after_save_limit",
					"save_settings",
					"invert_rotation",
					"save_my_position",
					"delete_my_position",
					"reset_actuator",
					"double_power_cut",
					"eject_from_setting_mode"
				]
			},
			{
				"name": "core:FirmwareRevision",
				"type": 3,
				"value": "5117737A06"
			}
		],
		"available": "True",
		"enabled": "True",
		"placeOID": "285239cf-489a-4800-b2cb-959489522f27",
		"widget": "PositionableRollerShutter",
		"type": 1,
		"oid": "fbada92a-e516-406c-81c5-9c6605d2c594",
		"uiClass": "RollerShutter"
	},
	{
		"creationTime": 1662471075000,
		"lastUpdateTime": 1662471075000,
		"label": "Lightsensor",
		"deviceURL": "io://0000-0000-0000/11521034",
		"shortcut": "False",
		"controllableName": "io:LightIOSystemSensor",
		"definition": {
			"commands": [
				{
					"commandName": "advancedRefresh",
					"nparams": 1
				}
			],
			"states": [
				{
					"type": "DiscreteState",
					"values": [
						"good",
						"low",
						"normal",
						"verylow"
					],
					"qualifiedName": "core:DiscreteRSSILevelState"
				},
				{
					"type": "ContinuousState",
					"qualifiedName": "core:LuminanceState"
				},
				{
					"type": "ContinuousState",
					"qualifiedName": "core:RSSILevelState"
				},
				{
					"type": "DiscreteState",
					"values": [
						"dead",
						"lowBattery",
						"maintenanceRequired",
						"noDefect"
					],
					"qualifiedName": "core:SensorDefectState"
				},
				{
					"type": "DiscreteState",
					"values": [
						"available",
						"unavailable"
					],
					"qualifiedName": "core:StatusState"
				}
			],
			"dataProperties": [
				{
					"value": {
						"activationDelayMap": {
							"middle": 0,
							"lower": 1200,
							"upper": 300
						},
						"referenceStates": [
							"middle",
							"lower",
							"upper"
						],
						"qualifiedName": "io:SunSensorHysteresisBehavior"
					},
					"qualifiedName": "core:timeBasedHysteresisBehavior"
				}
			],
			"widgetName": "LuminanceSensor",
			"uiProfiles": [
				"Specific"
			],
			"uiClass": "LightSensor",
			"qualifiedName": "io:LightIOSystemSensor",
			"type": "SENSOR"
		},
		"states": [
			{
				"name": "core:StatusState",
				"type": 3,
				"value": "available"
			},
			{
				"name": "core:DiscreteRSSILevelState",
				"type": 3,
				"value": "normal"
			},
			{
				"name": "core:RSSILevelState",
				"type": 2,
				"value": 52.0
			},
			{
				"name": "core:LuminanceState",
				"type": 2,
				"value": 3238.0
			}
		],
		"attributes": [
			{
				"name": "core:MinSensedValue",
				"type": 1,
				"value": 50
			},
			{
				"name": "core:FirmwareRevision",
				"type": 3,
				"value": "5126936A15"
			},
			{
				"name": "core:Manufacturer",
				"type": 3,
				"value": "Somfy"
			},
			{
				"name": "core:MaxSensedValue",
				"type": 1,
				"value": 100000
			},
			{
				"name": "core:MeasuredValueType",
				"type": 3,
				"value": "core:LuminanceInLux"
			},
			{
				"name": "core:PowerSourceType",
				"type": 3,
				"value": "battery"
			}
		],
		"available": "True",
		"enabled": "True",
		"placeOID": "1f25e4fc-8c03-462e-9ef0-a2216b3cfd47",
		"widget": "LuminanceSensor",
		"type": 2,
		"oid": "ff91dd0b-25e6-44bb-93ee-66190f36ad0e",
		"uiClass": "LightSensor"
	},
	{
		"creationTime": 1600767629000,
		"lastUpdateTime": 1600767629000,
		"label": "IO (14725444)",
		"deviceURL": "io://0000-0000-0000/14725444",
		"shortcut": "False",
		"controllableName": "io:StackComponent",
		"definition": {
			"commands": [
				{
					"commandName": "advancedSomfyDiscover",
					"nparams": 1
				},
				{
					"commandName": "discover1WayController",
					"nparams": 2
				},
				{
					"commandName": "discoverActuators",
					"nparams": 1
				},
				{
					"commandName": "discoverSensors",
					"nparams": 1
				},
				{
					"commandName": "discoverSomfyUnsetActuators",
					"nparams": 0
				},
				{
					"commandName": "joinNetwork",
					"nparams": 0
				},
				{
					"commandName": "resetNetworkSecurity",
					"nparams": 0
				},
				{
					"commandName": "shareNetwork",
					"nparams": 0
				}
			],
			"states": [],
			"dataProperties": [],
			"widgetName": "IOStack",
			"uiProfiles": [
				"Specific"
			],
			"uiClass": "ProtocolGateway",
			"qualifiedName": "io:StackComponent",
			"type": "PROTOCOL_GATEWAY"
		},
		"available": "True",
		"enabled": "True",
		"placeOID": "d33923b5-2ee0-4871-9207-594731f27983",
		"widget": "IOStack",
		"type": 5,
		"oid": "525d8667-4363-453c-b16f-e3a0b190bdee",
		"uiClass": "ProtocolGateway"
	},
	{
		"creationTime": 1596877910000,
		"lastUpdateTime": 1596877910000,
		"label": "OGP (00000BE8)",
		"deviceURL": "ogp://0000-0000-0000/00000BE8",
		"shortcut": "False",
		"controllableName": "ogp:Bridge",
		"definition": {
			"commands": [
				{
					"commandName": "sendPrivate",
					"nparams": 1
				}
			],
			"states": [
				{
					"type": "DataState",
					"qualifiedName": "core:Private10State"
				},
				{
					"type": "DataState",
					"qualifiedName": "core:Private1State"
				},
				{
					"type": "DataState",
					"qualifiedName": "core:Private2State"
				},
				{
					"type": "DataState",
					"qualifiedName": "core:Private3State"
				},
				{
					"type": "DataState",
					"qualifiedName": "core:Private4State"
				},
				{
					"type": "DataState",
					"qualifiedName": "core:Private5State"
				},
				{
					"type": "DataState",
					"qualifiedName": "core:Private6State"
				},
				{
					"type": "DataState",
					"qualifiedName": "core:Private7State"
				},
				{
					"type": "DataState",
					"qualifiedName": "core:Private8State"
				},
				{
					"type": "DataState",
					"qualifiedName": "core:Private9State"
				}
			],
			"dataProperties": [],
			"widgetName": "DynamicBridge",
			"uiProfiles": [
				"Specific"
			],
			"uiClass": "ProtocolGateway",
			"qualifiedName": "ogp:Bridge",
			"type": "ACTUATOR"
		},
		"attributes": [
			{
				"name": "ogp:Features",
				"type": 10,
				"value": [
					{
						"name": "private"
					}
				]
			}
		],
		"available": "True",
		"enabled": "True",
		"placeOID": "d33923b5-2ee0-4871-9207-594731f27983",
		"widget": "DynamicBridge",
		"type": 1,
		"oid": "7f1b7c75-c063-43a4-b982-f4372cd7b2da",
		"uiClass": "ProtocolGateway"
	},
	{
		"creationTime": 1648202676000,
		"lastUpdateTime": 1648202676000,
		"label": "OGP Sonos Bridge",
		"deviceURL": "ogp://0000-0000-0000/0003FEF3",
		"shortcut": "False",
		"controllableName": "ogp:Bridge",
		"definition": {
			"commands": [
				{
					"commandName": "discover",
					"nparams": 0
				},
				{
					"commandName": "reset",
					"nparams": 0
				}
			],
			"states": [
				{
					"type": "DiscreteState",
					"values": [
						"available",
						"unavailable"
					],
					"qualifiedName": "core:AvailabilityState"
				},
				{
					"type": "DataState",
					"qualifiedName": "core:NameState"
				},
				{
					"type": "DataState",
					"qualifiedName": "core:RemovableState"
				}
			],
			"dataProperties": [],
			"widgetName": "DynamicBridge",
			"uiProfiles": [
				"Specific"
			],
			"uiClass": "ProtocolGateway",
			"qualifiedName": "ogp:Bridge",
			"type": "ACTUATOR"
		},
		"states": [
			{
				"name": "core:NameState",
				"type": 3,
				"value": "OGP Sonos Bridge"
			}
		],
		"attributes": [
			{
				"name": "core:Manufacturer",
				"type": 3,
				"value": "Overkiz"
			},
			{
				"name": "core:Technology",
				"type": 3,
				"value": "Sonos"
			},
			{
				"name": "core:ManufacturerReference",
				"type": 3,
				"value": "OGP Sonos Bridge"
			},
			{
				"name": "ogp:Features",
				"type": 10,
				"value": [
					{
						"name": "identification",
						"commandLess": "True"
					},
					{
						"name": "discovery"
					},
					{
						"name": "reset"
					}
				]
			}
		],
		"available": "True",
		"enabled": "True",
		"placeOID": "d33923b5-2ee0-4871-9207-594731f27983",
		"widget": "DynamicBridge",
		"type": 1,
		"oid": "89f569f6-3723-4884-a61f-2e015b6f553f",
		"uiClass": "ProtocolGateway"
	},
	{
		"creationTime": 1648202675000,
		"lastUpdateTime": 1648202675000,
		"label": "OGP IBPlus Bridge",
		"deviceURL": "ogp://0000-0000-0000/00920C53",
		"shortcut": "False",
		"controllableName": "ogp:Bridge",
		"definition": {
			"commands": [
				{
					"commandName": "identify",
					"nparams": 0
				},
				{
					"commandName": "sendPrivate",
					"nparams": 1
				},
				{
					"commandName": "setName",
					"nparams": 1
				}
			],
			"states": [
				{
					"type": "DiscreteState",
					"values": [
						"available",
						"unavailable"
					],
					"qualifiedName": "core:AvailabilityState"
				},
				{
					"type": "DataState",
					"qualifiedName": "core:NameState"
				},
				{
					"type": "DataState",
					"qualifiedName": "core:Private10State"
				},
				{
					"type": "DataState",
					"qualifiedName": "core:Private1State"
				},
				{
					"type": "DataState",
					"qualifiedName": "core:Private2State"
				},
				{
					"type": "DataState",
					"qualifiedName": "core:Private3State"
				},
				{
					"type": "DataState",
					"qualifiedName": "core:Private4State"
				},
				{
					"type": "DataState",
					"qualifiedName": "core:Private5State"
				},
				{
					"type": "DataState",
					"qualifiedName": "core:Private6State"
				},
				{
					"type": "DataState",
					"qualifiedName": "core:Private7State"
				},
				{
					"type": "DataState",
					"qualifiedName": "core:Private8State"
				},
				{
					"type": "DataState",
					"qualifiedName": "core:Private9State"
				},
				{
					"type": "DataState",
					"qualifiedName": "core:RemovableState"
				}
			],
			"dataProperties": [],
			"widgetName": "DynamicBridge",
			"uiProfiles": [
				"Specific"
			],
			"uiClass": "ProtocolGateway",
			"qualifiedName": "ogp:Bridge",
			"type": "ACTUATOR"
		},
		"states": [
			{
				"name": "core:NameState",
				"type": 3,
				"value": "OGP IBPlus Bridge"
			}
		],
		"attributes": [
			{
				"name": "core:ManufacturerReference",
				"type": 3,
				"value": "OGP IBPlus Bridge"
			},
			{
				"name": "ogp:Features",
				"type": 10,
				"value": [
					{
						"name": "identification"
					},
					{
						"name": "private"
					}
				]
			},
			{
				"name": "core:Technology",
				"type": 3,
				"value": "IBPlus"
			},
			{
				"name": "core:Manufacturer",
				"type": 3,
				"value": "Overkiz"
			}
		],
		"available": "True",
		"enabled": "True",
		"placeOID": "d33923b5-2ee0-4871-9207-594731f27983",
		"widget": "DynamicBridge",
		"type": 1,
		"oid": "ed675587-0fbe-45ac-9f71-e320d0cc27c1",
		"uiClass": "ProtocolGateway"
	},
	{
		"creationTime": 1596877910000,
		"lastUpdateTime": 1596877910000,
		"label": "OGP Siegenia Bridge",
		"deviceURL": "ogp://0000-0000-0000/039575E9",
		"shortcut": "False",
		"controllableName": "ogp:Bridge",
		"definition": {
			"commands": [
				{
					"commandName": "discover",
					"nparams": 0
				},
				{
					"commandName": "identify",
					"nparams": 0
				},
				{
					"commandName": "setName",
					"nparams": 1
				}
			],
			"states": [
				{
					"type": "DiscreteState",
					"values": [
						"available",
						"unavailable"
					],
					"qualifiedName": "core:AvailabilityState"
				},
				{
					"type": "DataState",
					"qualifiedName": "core:NameState"
				},
				{
					"type": "DataState",
					"qualifiedName": "core:RemovableState"
				}
			],
			"dataProperties": [],
			"widgetName": "DynamicBridge",
			"uiProfiles": [
				"Specific"
			],
			"uiClass": "ProtocolGateway",
			"qualifiedName": "ogp:Bridge",
			"type": "ACTUATOR"
		},
		"states": [
			{
				"name": "core:NameState",
				"type": 3,
				"value": "OGP Siegenia Bridge"
			}
		],
		"attributes": [
			{
				"name": "core:Technology",
				"type": 3,
				"value": "Siegenia"
			},
			{
				"name": "core:ManufacturerReference",
				"type": 3,
				"value": "OGP Siegenia Bridge"
			},
			{
				"name": "core:Manufacturer",
				"type": 3,
				"value": "Overkiz"
			},
			{
				"name": "ogp:Features",
				"type": 10,
				"value": [
					{
						"name": "discovery"
					},
					{
						"name": "identification"
					}
				]
			}
		],
		"available": "True",
		"enabled": "True",
		"placeOID": "d33923b5-2ee0-4871-9207-594731f27983",
		"widget": "DynamicBridge",
		"type": 1,
		"oid": "54b2c7c5-7d8a-4b9e-a199-b244975f02ad",
		"uiClass": "ProtocolGateway"
	},
	{
		"creationTime": 1596877910000,
		"lastUpdateTime": 1596877910000,
		"label": "OGP Intesis Bridge",
		"deviceURL": "ogp://0000-0000-0000/09E45393",
		"shortcut": "False",
		"controllableName": "ogp:Bridge",
		"definition": {
			"commands": [
				{
					"commandName": "discover",
					"nparams": 0
				},
				{
					"commandName": "identify",
					"nparams": 0
				},
				{
					"commandName": "setName",
					"nparams": 1
				}
			],
			"states": [
				{
					"type": "DiscreteState",
					"values": [
						"available",
						"unavailable"
					],
					"qualifiedName": "core:AvailabilityState"
				},
				{
					"type": "DataState",
					"qualifiedName": "core:NameState"
				},
				{
					"type": "DataState",
					"qualifiedName": "core:RemovableState"
				}
			],
			"dataProperties": [],
			"widgetName": "DynamicBridge",
			"uiProfiles": [
				"Specific"
			],
			"uiClass": "ProtocolGateway",
			"qualifiedName": "ogp:Bridge",
			"type": "ACTUATOR"
		},
		"states": [
			{
				"name": "core:NameState",
				"type": 3,
				"value": "OGP Intesis Bridge"
			}
		],
		"attributes": [
			{
				"name": "core:ManufacturerReference",
				"type": 3,
				"value": "OGP Intesis Bridge"
			},
			{
				"name": "core:Technology",
				"type": 3,
				"value": "Intesis"
			},
			{
				"name": "core:Manufacturer",
				"type": 3,
				"value": "Overkiz"
			},
			{
				"name": "ogp:Features",
				"type": 10,
				"value": [
					{
						"name": "discovery"
					},
					{
						"name": "identification"
					}
				]
			}
		],
		"available": "True",
		"enabled": "True",
		"placeOID": "d33923b5-2ee0-4871-9207-594731f27983",
		"widget": "DynamicBridge",
		"type": 1,
		"oid": "ca77d2ea-f865-404a-bd92-aafc87427b33",
		"uiClass": "ProtocolGateway"
	}
]