# IFC coverage — every IFC 4.3 element class has an OPO

**Draft v0.1 · 24 Nov 2026** · generated from the IFC 4.3 schema (ifcopenshell `IFC4X3_ADD2`) by `tools/gen_coverage.py`; do not edit the tables by hand.

**Goal.** Every IFC element type can be created parametrically in an OPO application and shared as a file, the way a Revit family is shared. That includes elements that Revit handles as non-shareable "system families" (walls, slabs, roofs, stairs, pipes, ducts): in OPO they are ordinary objects.

**How:** two tiers (spec §4.16).
1. **Class template** — one OPO per IFC class (150 classes). Built on one of eight geometric **archetypes** (`archetypes.md`). It carries the class, every predefined type as a choice, the matching IFC property sets as parameters, ports for distribution elements, and a usable shape at three levels of detail. Templates are generated from the IFC schema, the IFC property set templates and a small hand-written per-class table, so they follow IFC releases.
2. **Library objects** — detailed objects with proper construction logic and drawing conventions, written from their sheets (`README.md`, 34 classes have at least one sheet today). A library object is a refined template: same class, same IFC data.

Anyone (a firm, a manufacturer, Curva Pro) makes their own objects by starting from a template or a library object, the way a Revit user starts from a family template.

**Counts:** 150 concrete element classes · 862 predefined types · 34 classes with a detailed sheet · 116 classes covered by their template only (for now) · class templates built: 9.

Archetypes (`any` = the user picks one, for generic classes such as `IfcBuildingElementProxy`): **point** (placed equipment or component, optionally hosted, with ports) · **linear** (profile along a path) · **area** (boundary + thickness or layer build-up) · **wall** (path + height + layers or grid) · **hosted** (sits in or on a host and cuts or adds to it) · **flight** (level to level: stairs, ramps) · **fitting** (joins the ends of segments) · **assembly** (nests other OPOs).

Not covered: abstract classes (they cannot be instantiated), spatial elements (sites, buildings, storeys, spaces: project structure, not objects), annotations, grids and alignments, and type-only entities.


## Built elements

| Class | Archetype | Types | Predefined types | Detailed sheets | Note |
|---|---|---|---|---|---|
| `IfcBuiltElement` | any | planned | 0 | — | — | generic supertype; template for elements with no specific class |
| `IfcBeam` | linear | ✅ | 12 | BEAM, CORNICE, DIAPHRAGM, EDGEBEAM, GIRDER_SEGMENT, HATSTONE, HOLLOWCORE, JOIST, LINTEL, PIERCAP, SPANDREL, T_BEAM | K-02 |  |
| `IfcBearing` | point | planned | 8 | CYLINDRICAL, DISK, ELASTOMERIC, GUIDE, POT, ROCKER, ROLLER, SPHERICAL | — |  |
| `IfcBuildingElementProxy` | any | planned | 5 | COMPLEX, ELEMENT, PARTIAL, PROVISIONFORSPACE, PROVISIONFORVOID | — |  |
| `IfcChimney` | wall | planned | 0 | — | K-08 |  |
| `IfcColumn` | linear | planned | 5 | COLUMN, PIERSTEM, PIERSTEM_SEGMENT, PILASTER, STANDCOLUMN | K-01 |  |
| `IfcCourse` | area | planned | 6 | ARMOUR, BALLASTBED, CORE, FILTER, PAVEMENT, PROTECTION | — |  |
| `IfcCovering` | area | planned | 12 | CEILING, CLADDING, COPING, FLOORING, INSULATION, MEMBRANE, MOLDING, ROOFING, SKIRTINGBOARD, SLEEVING, TOPPING, WRAPPING | K-04, K-05, K-06, K-07 |  |
| `IfcCurtainWall` | wall | planned | 0 | — | O-16, O-17, O-18 |  |
| `IfcDeepFoundation` | linear | planned | 0 | — | — | generic supertype; template for elements with no specific class |
| `IfcCaissonFoundation` | linear | planned | 2 | CAISSON, WELL | — |  |
| `IfcPile` | linear | planned | 6 | BORED, COHESION, DRIVEN, FRICTION, JETGROUTING, SUPPORT | — |  |
| `IfcDoor` | hosted | planned | 5 | BOOM_BARRIER, DOOR, GATE, TRAPDOOR, TURNSTILE | O-02, O-03, O-04, O-05, O-06, O-07, T-01 |  |
| `IfcEarthworksElement` | area | planned | 0 | — | — | generic supertype; template for elements with no specific class |
| `IfcEarthworksFill` | area | planned | 7 | BACKFILL, COUNTERWEIGHT, EMBANKMENT, SLOPEFILL, SUBGRADE, SUBGRADEBED, TRANSITIONSECTION | — |  |
| `IfcReinforcedSoil` | area | planned | 6 | DYNAMICALLYCOMPACTED, GROUTED, REPLACED, ROLLERCOMPACTED, SURCHARGEPRELOADED, VERTICALLYDRAINED | — |  |
| `IfcFooting` | point | planned | 5 | CAISSON_FOUNDATION, FOOTING_BEAM, PAD_FOOTING, PILE_CAP, STRIP_FOOTING | — |  |
| `IfcKerb` | linear | planned | 0 | — | — |  |
| `IfcMember` | linear | ✅ | 19 | ARCH_SEGMENT, BRACE, CHORD, COLLAR, MEMBER, MULLION, PLATE, POST, PURLIN, RAFTER, STAY_CABLE, STIFFENING_RIB, STRINGER, STRUCTURALCABLE, STRUT, STUD, SUSPENDER, SUSPENSION_CABLE, TIEBAR | K-03, O-18 |  |
| `IfcMooringDevice` | point | planned | 5 | BOLLARD, LINETENSIONER, MAGNETICDEVICE, MOORINGHOOKS, VACUUMDEVICE | — |  |
| `IfcNavigationElement` | point | planned | 2 | BEACON, BUOY | — |  |
| `IfcPavement` | area | planned | 2 | FLEXIBLE, RIGID | — |  |
| `IfcPlate` | area | planned | 9 | BASE_PLATE, COVER_PLATE, CURTAIN_PANEL, FLANGE_PLATE, GUSSET_PLATE, SHEET, SPLICE_PLATE, STIFFENER_PLATE, WEB_PLATE | F-05, O-18 |  |
| `IfcRail` | linear | planned | 6 | BLADE, CHECKRAIL, GUARDRAIL, RACKRAIL, RAIL, STOCKRAIL | — |  |
| `IfcRailing` | linear | planned | 4 | BALUSTRADE, FENCE, GUARDRAIL, HANDRAIL | C-07, C-08 |  |
| `IfcRamp` | flight | planned | 6 | HALF_TURN_RAMP, QUARTER_TURN_RAMP, SPIRAL_RAMP, STRAIGHT_RUN_RAMP, TWO_QUARTER_TURN_RAMP, TWO_STRAIGHT_RUN_RAMP | C-06 |  |
| `IfcRampFlight` | flight | planned | 2 | SPIRAL, STRAIGHT | C-06 |  |
| `IfcRoof` | area | planned | 13 | BARREL_ROOF, BUTTERFLY_ROOF, DOME_ROOF, FLAT_ROOF, FREEFORM, GABLE_ROOF, GAMBREL_ROOF, HIPPED_GABLE_ROOF, HIP_ROOF, MANSARD_ROOF, PAVILION_ROOF, RAINBOW_ROOF, SHED_ROOF | O-14 |  |
| `IfcShadingDevice` | hosted | planned | 3 | AWNING, JALOUSIE, SHUTTER | S-01, S-02, S-03, S-04, S-05, S-06, S-07 |  |
| `IfcSlab` | area | ✅ | 9 | APPROACH_SLAB, BASESLAB, FLOOR, LANDING, PAVING, ROOF, SIDEWALK, TRACKSLAB, WEARING | C-02, C-06, O-14 |  |
| `IfcStair` | flight | ✅ | 15 | CURVED_RUN_STAIR, DOUBLE_RETURN_STAIR, HALF_TURN_STAIR, HALF_WINDING_STAIR, LADDER, QUARTER_TURN_STAIR, QUARTER_WINDING_STAIR, SPIRAL_STAIR, STRAIGHT_RUN_STAIR, THREE_QUARTER_TURN_STAIR, THREE_QUARTER_WINDING_STAIR, TWO_CURVED_RUN_STAIR, TWO_QUARTER_TURN_STAIR, TWO_QUARTER_WINDING_STAIR, TWO_STRAIGHT_RUN_STAIR | C-01, C-02, C-03, C-04, C-05 |  |
| `IfcStairFlight` | flight | planned | 5 | CURVED, FREEFORM, SPIRAL, STRAIGHT, WINDER | C-01, C-02 |  |
| `IfcTrackElement` | linear | planned | 8 | BLOCKINGDEVICE, DERAILER, FROG, HALF_SET_OF_BLADES, SLEEPER, SPEEDREGULATOR, TRACKENDOFALIGNMENT, VEHICLESTOP | — |  |
| `IfcWall` | wall | ✅ | 11 | ELEMENTEDWALL, MOVABLE, PARAPET, PARTITIONING, PLUMBINGWALL, POLYGONAL, RETAININGWALL, SHEAR, SOLIDWALL, STANDARD, WAVEWALL | — |  |
| `IfcWallStandardCase` | wall | planned | 0 | — | — | deprecated in IFC 4.3; exported as IfcWall |
| `IfcWindow` | hosted | planned | 3 | LIGHTDOME, SKYLIGHT, WINDOW | O-06, O-08, O-09, O-10, O-11, O-12, O-14 |  |

## Distribution: control (sensors, actuators, alarms)

| Class | Archetype | Types | Predefined types | Detailed sheets | Note |
|---|---|---|---|---|---|
| `IfcDistributionControlElement` | point | planned | 0 | — | — | generic supertype; template for elements with no specific class |
| `IfcActuator` | point | planned | 5 | ELECTRICACTUATOR, HANDOPERATEDACTUATOR, HYDRAULICACTUATOR, PNEUMATICACTUATOR, THERMOSTATICACTUATOR | — |  |
| `IfcAlarm` | point | planned | 8 | BELL, BREAKGLASSBUTTON, LIGHT, MANUALPULLBOX, RAILWAYCROCODILE, RAILWAYDETONATOR, SIREN, WHISTLE | — |  |
| `IfcController` | point | planned | 5 | FLOATING, MULTIPOSITION, PROGRAMMABLE, PROPORTIONAL, TWOPOSITION | — |  |
| `IfcFlowInstrument` | point | planned | 10 | AMMETER, COMBINED, FREQUENCYMETER, PHASEANGLEMETER, POWERFACTORMETER, PRESSUREGAUGE, THERMOMETER, VOLTMETER, VOLTMETER_PEAK, VOLTMETER_RMS | — |  |
| `IfcProtectiveDeviceTrippingUnit` | point | planned | 4 | ELECTROMAGNETIC, ELECTRONIC, RESIDUALCURRENT, THERMAL | — |  |
| `IfcSensor` | point | planned | 32 | CO2SENSOR, CONDUCTANCESENSOR, CONTACTSENSOR, COSENSOR, EARTHQUAKESENSOR, FIRESENSOR, FLOWSENSOR, FOREIGNOBJECTDETECTIONSENSOR, FROSTSENSOR, GASSENSOR, HEATSENSOR, HUMIDITYSENSOR, IDENTIFIERSENSOR, IONCONCENTRATIONSENSOR, LEVELSENSOR, LIGHTSENSOR, MOISTURESENSOR, MOVEMENTSENSOR, OBSTACLESENSOR, PHSENSOR, PRESSURESENSOR, RADIATIONSENSOR, RADIOACTIVITYSENSOR, RAINSENSOR, SMOKESENSOR, SNOWDEPTHSENSOR, SOUNDSENSOR, TEMPERATURESENSOR, TRAINSENSOR, TURNOUTCLOSURESENSOR, WHEELSENSOR, WINDSENSOR | — |  |
| `IfcUnitaryControlElement` | point | planned | 10 | ALARMPANEL, BASESTATIONCONTROLLER, COMBINED, CONTROLPANEL, GASDETECTIONPANEL, HUMIDISTAT, INDICATORPANEL, MIMICPANEL, THERMOSTAT, WEATHERSTATION | — |  |

## Distribution: energy conversion (plant)

| Class | Archetype | Types | Predefined types | Detailed sheets | Note |
|---|---|---|---|---|---|
| `IfcEnergyConversionDevice` | point | planned | 0 | — | — | generic supertype; template for elements with no specific class |
| `IfcAirToAirHeatRecovery` | point | planned | 9 | FIXEDPLATECOUNTERFLOWEXCHANGER, FIXEDPLATECROSSFLOWEXCHANGER, FIXEDPLATEPARALLELFLOWEXCHANGER, HEATPIPE, ROTARYWHEEL, RUNAROUNDCOILLOOP, THERMOSIPHONCOILTYPEHEATEXCHANGERS, THERMOSIPHONSEALEDTUBEHEATEXCHANGERS, TWINTOWERENTHALPYRECOVERYLOOPS | — |  |
| `IfcBoiler` | point | ✅ | 2 | STEAM, WATER | — |  |
| `IfcBurner` | point | planned | 0 | — | — |  |
| `IfcChiller` | point | planned | 3 | AIRCOOLED, HEATRECOVERY, WATERCOOLED | — |  |
| `IfcCoil` | point | planned | 7 | DXCOOLINGCOIL, ELECTRICHEATINGCOIL, GASHEATINGCOIL, HYDRONICCOIL, STEAMHEATINGCOIL, WATERCOOLINGCOIL, WATERHEATINGCOIL | — |  |
| `IfcCondenser` | point | planned | 7 | AIRCOOLED, EVAPORATIVECOOLED, WATERCOOLED, WATERCOOLEDBRAZEDPLATE, WATERCOOLEDSHELLCOIL, WATERCOOLEDSHELLTUBE, WATERCOOLEDTUBEINTUBE | — |  |
| `IfcCooledBeam` | point | planned | 2 | ACTIVE, PASSIVE | — |  |
| `IfcCoolingTower` | point | planned | 3 | MECHANICALFORCEDDRAFT, MECHANICALINDUCEDDRAFT, NATURALDRAFT | — |  |
| `IfcElectricGenerator` | point | planned | 3 | CHP, ENGINEGENERATOR, STANDALONE | — |  |
| `IfcElectricMotor` | point | planned | 5 | DC, INDUCTION, POLYPHASE, RELUCTANCESYNCHRONOUS, SYNCHRONOUS | — |  |
| `IfcEngine` | point | planned | 2 | EXTERNALCOMBUSTION, INTERNALCOMBUSTION | — |  |
| `IfcEvaporativeCooler` | point | planned | 9 | DIRECTEVAPORATIVEAIRWASHER, DIRECTEVAPORATIVEPACKAGEDROTARYAIRCOOLER, DIRECTEVAPORATIVERANDOMMEDIAAIRCOOLER, DIRECTEVAPORATIVERIGIDMEDIAAIRCOOLER, DIRECTEVAPORATIVESLINGERSPACKAGEDAIRCOOLER, INDIRECTDIRECTCOMBINATION, INDIRECTEVAPORATIVECOOLINGTOWERORCOILCOOLER, INDIRECTEVAPORATIVEPACKAGEAIRCOOLER, INDIRECTEVAPORATIVEWETCOIL | — |  |
| `IfcEvaporator` | point | planned | 6 | DIRECTEXPANSION, DIRECTEXPANSIONBRAZEDPLATE, DIRECTEXPANSIONSHELLANDTUBE, DIRECTEXPANSIONTUBEINTUBE, FLOODEDSHELLANDTUBE, SHELLANDCOIL | — |  |
| `IfcHeatExchanger` | point | planned | 3 | PLATE, SHELLANDTUBE, TURNOUTHEATING | — |  |
| `IfcHumidifier` | point | planned | 13 | ADIABATICAIRWASHER, ADIABATICATOMIZING, ADIABATICCOMPRESSEDAIRNOZZLE, ADIABATICPAN, ADIABATICRIGIDMEDIA, ADIABATICULTRASONIC, ADIABATICWETTEDELEMENT, ASSISTEDBUTANE, ASSISTEDELECTRIC, ASSISTEDNATURALGAS, ASSISTEDPROPANE, ASSISTEDSTEAM, STEAMINJECTION | — |  |
| `IfcMotorConnection` | point | planned | 3 | BELTDRIVE, COUPLING, DIRECTDRIVE | — |  |
| `IfcSolarDevice` | point | planned | 2 | SOLARCOLLECTOR, SOLARPANEL | — |  |
| `IfcTransformer` | point | planned | 7 | CHOPPER, COMBINED, CURRENT, FREQUENCY, INVERTER, RECTIFIER, VOLTAGE | — |  |
| `IfcTubeBundle` | point | planned | 1 | FINNED | — |  |
| `IfcUnitaryEquipment` | point | planned | 5 | AIRCONDITIONINGUNIT, AIRHANDLER, DEHUMIDIFIER, ROOFTOPUNIT, SPLITSYSTEM | — |  |

## Distribution: flow controllers

| Class | Archetype | Types | Predefined types | Detailed sheets | Note |
|---|---|---|---|---|---|
| `IfcFlowController` | point | planned | 0 | — | — | generic supertype; template for elements with no specific class |
| `IfcAirTerminalBox` | point | planned | 3 | CONSTANTFLOW, VARIABLEFLOWPRESSUREDEPENDANT, VARIABLEFLOWPRESSUREINDEPENDANT | — |  |
| `IfcDamper` | point | planned | 11 | BACKDRAFTDAMPER, BALANCINGDAMPER, BLASTDAMPER, CONTROLDAMPER, FIREDAMPER, FIRESMOKEDAMPER, FUMEHOODEXHAUST, GRAVITYDAMPER, GRAVITYRELIEFDAMPER, RELIEFDAMPER, SMOKEDAMPER | — |  |
| `IfcDistributionBoard` | point | planned | 6 | CONSUMERUNIT, DISPATCHINGBOARD, DISTRIBUTIONBOARD, DISTRIBUTIONFRAME, MOTORCONTROLCENTRE, SWITCHBOARD | — |  |
| `IfcElectricDistributionBoard` | point | planned | 4 | CONSUMERUNIT, DISTRIBUTIONBOARD, MOTORCONTROLCENTRE, SWITCHBOARD | — |  |
| `IfcElectricTimeControl` | point | planned | 3 | RELAY, TIMECLOCK, TIMEDELAY | — |  |
| `IfcFlowMeter` | point | planned | 4 | ENERGYMETER, GASMETER, OILMETER, WATERMETER | — |  |
| `IfcProtectiveDevice` | point | planned | 10 | ANTI_ARCING_DEVICE, CIRCUITBREAKER, EARTHINGSWITCH, EARTHLEAKAGECIRCUITBREAKER, FUSEDISCONNECTOR, RESIDUALCURRENTCIRCUITBREAKER, RESIDUALCURRENTSWITCH, SPARKGAP, VARISTOR, VOLTAGELIMITER | — |  |
| `IfcSwitchingDevice` | point | planned | 11 | CONTACTOR, DIMMERSWITCH, EMERGENCYSTOP, KEYPAD, MOMENTARYSWITCH, RELAY, SELECTORSWITCH, STARTER, START_AND_STOP_EQUIPMENT, SWITCHDISCONNECTOR, TOGGLESWITCH | M-04 |  |
| `IfcValve` | point | planned | 21 | AIRRELEASE, ANTIVACUUM, CHANGEOVER, CHECK, COMMISSIONING, DIVERTING, DOUBLECHECK, DOUBLEREGULATING, DRAWOFFCOCK, FAUCET, FLUSHING, GASCOCK, GASTAP, ISOLATING, MIXING, PRESSUREREDUCING, PRESSURERELIEF, REGULATING, SAFETYCUTOFF, STEAMTRAP, STOPCOCK | — |  |

## Distribution: fittings

| Class | Archetype | Types | Predefined types | Detailed sheets | Note |
|---|---|---|---|---|---|
| `IfcFlowFitting` | fitting | planned | 0 | — | — | generic supertype; template for elements with no specific class |
| `IfcCableCarrierFitting` | fitting | planned | 7 | BEND, CONNECTOR, CROSS, JUNCTION, REDUCER, TEE, TRANSITION | — |  |
| `IfcCableFitting` | fitting | planned | 6 | CONNECTOR, ENTRY, EXIT, FANOUT, JUNCTION, TRANSITION | — |  |
| `IfcDuctFitting` | fitting | planned | 7 | BEND, CONNECTOR, ENTRY, EXIT, JUNCTION, OBSTRUCTION, TRANSITION | — |  |
| `IfcJunctionBox` | point | planned | 2 | DATA, POWER | — |  |
| `IfcPipeFitting` | fitting | ✅ | 7 | BEND, CONNECTOR, ENTRY, EXIT, JUNCTION, OBSTRUCTION, TRANSITION | — |  |

## Distribution: pumps, fans, compressors

| Class | Archetype | Types | Predefined types | Detailed sheets | Note |
|---|---|---|---|---|---|
| `IfcFlowMovingDevice` | point | planned | 0 | — | — | generic supertype; template for elements with no specific class |
| `IfcCompressor` | point | planned | 15 | BOOSTER, DYNAMIC, HERMETIC, OPENTYPE, RECIPROCATING, ROLLINGPISTON, ROTARY, ROTARYVANE, SCROLL, SEMIHERMETIC, SINGLESCREW, SINGLESTAGE, TROCHOIDAL, TWINSCREW, WELDEDSHELLHERMETIC | — |  |
| `IfcFan` | point | planned | 7 | CENTRIFUGALAIRFOIL, CENTRIFUGALBACKWARDINCLINEDCURVED, CENTRIFUGALFORWARDCURVED, CENTRIFUGALRADIAL, PROPELLORAXIAL, TUBEAXIAL, VANEAXIAL | — |  |
| `IfcPump` | point | planned | 7 | CIRCULATOR, ENDSUCTION, SPLITCASE, SUBMERSIBLEPUMP, SUMPPUMP, VERTICALINLINE, VERTICALTURBINE | — |  |

## Distribution: segments (pipes, ducts, cables)

| Class | Archetype | Types | Predefined types | Detailed sheets | Note |
|---|---|---|---|---|---|
| `IfcFlowSegment` | linear | planned | 0 | — | — | generic supertype; template for elements with no specific class |
| `IfcCableCarrierSegment` | linear | planned | 7 | CABLEBRACKET, CABLELADDERSEGMENT, CABLETRAYSEGMENT, CABLETRUNKINGSEGMENT, CATENARYWIRE, CONDUITSEGMENT, DROPPER | — |  |
| `IfcCableSegment` | linear | planned | 10 | BUSBARSEGMENT, CABLESEGMENT, CONDUCTORSEGMENT, CONTACTWIRESEGMENT, CORESEGMENT, FIBERSEGMENT, FIBERTUBE, OPTICALCABLESEGMENT, STITCHWIRE, WIREPAIRSEGMENT | — |  |
| `IfcConveyorSegment` | linear | planned | 4 | BELTCONVEYOR, BUCKETCONVEYOR, CHUTECONVEYOR, SCREWCONVEYOR | — |  |
| `IfcDuctSegment` | linear | planned | 2 | FLEXIBLESEGMENT, RIGIDSEGMENT | — |  |
| `IfcPipeSegment` | linear | planned | 5 | CULVERT, FLEXIBLESEGMENT, GUTTER, RIGIDSEGMENT, SPOOL | — |  |

## Distribution: storage

| Class | Archetype | Types | Predefined types | Detailed sheets | Note |
|---|---|---|---|---|---|
| `IfcFlowStorageDevice` | point | planned | 0 | — | — | generic supertype; template for elements with no specific class |
| `IfcElectricFlowStorageDevice` | point | planned | 9 | BATTERY, CAPACITOR, CAPACITORBANK, COMPENSATOR, HARMONICFILTER, INDUCTOR, INDUCTORBANK, RECHARGER, UPS | — |  |
| `IfcTank` | point | planned | 8 | BASIN, BREAKPRESSURE, EXPANSION, FEEDANDEXPANSION, OILRETENTIONTRAY, PRESSUREVESSEL, STORAGE, VESSEL | — |  |

## Distribution: terminals

| Class | Archetype | Types | Predefined types | Detailed sheets | Note |
|---|---|---|---|---|---|
| `IfcFlowTerminal` | point | planned | 0 | — | — | generic supertype; template for elements with no specific class |
| `IfcAirTerminal` | point | planned | 4 | DIFFUSER, GRILLE, LOUVRE, REGISTER | M-02 |  |
| `IfcAudioVisualAppliance` | point | planned | 13 | AMPLIFIER, CAMERA, COMMUNICATIONTERMINAL, DISPLAY, MICROPHONE, PLAYER, PROJECTOR, RECEIVER, RECORDINGEQUIPMENT, SPEAKER, SWITCHER, TELEPHONE, TUNER | — |  |
| `IfcCommunicationsAppliance` | point | planned | 24 | ANTENNA, AUTOMATON, COMPUTER, FAX, GATEWAY, INTELLIGENTPERIPHERAL, IPNETWORKEQUIPMENT, LINESIDEELECTRONICUNIT, MODEM, NETWORKAPPLIANCE, NETWORKBRIDGE, NETWORKHUB, OPTICALLINETERMINAL, OPTICALNETWORKUNIT, PRINTER, RADIOBLOCKCENTER, REPEATER, ROUTER, SCANNER, TELECOMMAND, TELEPHONYEXCHANGE, TRANSITIONCOMPONENT, TRANSPONDER, TRANSPORTEQUIPMENT | — |  |
| `IfcElectricAppliance` | point | planned | 16 | DISHWASHER, ELECTRICCOOKER, FREESTANDINGELECTRICHEATER, FREESTANDINGFAN, FREESTANDINGWATERCOOLER, FREESTANDINGWATERHEATER, FREEZER, FRIDGE_FREEZER, HANDDRYER, KITCHENMACHINE, MICROWAVE, PHOTOCOPIER, REFRIGERATOR, TUMBLEDRYER, VENDINGMACHINE, WASHINGMACHINE | F-13 |  |
| `IfcFireSuppressionTerminal` | point | planned | 6 | BREECHINGINLET, FIREHYDRANT, FIREMONITOR, HOSEREEL, SPRINKLER, SPRINKLERDEFLECTOR | M-05, M-06 |  |
| `IfcLamp` | point | planned | 9 | COMPACTFLUORESCENT, FLUORESCENT, HALOGEN, HIGHPRESSUREMERCURY, HIGHPRESSURESODIUM, LED, METALHALIDE, OLED, TUNGSTENFILAMENT | — |  |
| `IfcLightFixture` | point | planned | 3 | DIRECTIONSOURCE, POINTSOURCE, SECURITYLIGHTING | E-08 |  |
| `IfcLiquidTerminal` | point | planned | 2 | HOSEREEL, LOADINGARM | — |  |
| `IfcMedicalDevice` | point | planned | 5 | AIRSTATION, FEEDAIRUNIT, OXYGENGENERATOR, OXYGENPLANT, VACUUMSTATION | — |  |
| `IfcMobileTelecommunicationsAppliance` | point | planned | 13 | ACCESSPOINT, BASEBANDUNIT, BASETRANSCEIVERSTATION, E_UTRAN_NODE_B, GATEWAY_GPRS_SUPPORT_NODE, MASTERUNIT, MOBILESWITCHINGCENTER, MSCSERVER, PACKETCONTROLUNIT, REMOTERADIOUNIT, REMOTEUNIT, SERVICE_GPRS_SUPPORT_NODE, SUBSCRIBERSERVER | — |  |
| `IfcOutlet` | point | planned | 5 | AUDIOVISUALOUTLET, COMMUNICATIONSOUTLET, DATAOUTLET, POWEROUTLET, TELEPHONEOUTLET | M-03 |  |
| `IfcSanitaryTerminal` | point | planned | 10 | BATH, BIDET, CISTERN, SANITARYFOUNTAIN, SHOWER, SINK, TOILETPAN, URINAL, WASHHANDBASIN, WCSEAT | F-01, F-02, F-03, F-04, F-05, F-06, F-07 |  |
| `IfcSignal` | point | planned | 3 | AUDIO, MIXED, VISUAL | — |  |
| `IfcSpaceHeater` | point | planned | 2 | CONVECTOR, RADIATOR | M-01 |  |
| `IfcStackTerminal` | point | planned | 3 | BIRDCAGE, COWL, RAINWATERHOPPER | — |  |
| `IfcWasteTerminal` | point | planned | 7 | FLOORTRAP, FLOORWASTE, GULLYSUMP, GULLYTRAP, ROOFDRAIN, WASTEDISPOSALUNIT, WASTETRAP | — |  |

## Distribution: treatment

| Class | Archetype | Types | Predefined types | Detailed sheets | Note |
|---|---|---|---|---|---|
| `IfcFlowTreatmentDevice` | point | planned | 0 | — | — | generic supertype; template for elements with no specific class |
| `IfcDuctSilencer` | point | planned | 3 | FLATOVAL, RECTANGULAR, ROUND | — |  |
| `IfcElectricFlowTreatmentDevice` | point | planned | 1 | ELECTRONICFILTER | — |  |
| `IfcFilter` | point | planned | 6 | AIRPARTICLEFILTER, COMPRESSEDAIRFILTER, ODORFILTER, OILFILTER, STRAINER, WATERFILTER | — |  |
| `IfcInterceptor` | point | planned | 4 | CYCLONIC, GREASE, OIL, PETROL | — |  |

## Distribution: chambers

| Class | Archetype | Types | Predefined types | Detailed sheets | Note |
|---|---|---|---|---|---|
| `IfcDistributionChamberElement` | point | planned | 8 | FORMEDDUCT, INSPECTIONCHAMBER, INSPECTIONPIT, MANHOLE, METERCHAMBER, SUMP, TRENCH, VALVECHAMBER | — |  |

## Components

| Class | Archetype | Types | Predefined types | Detailed sheets | Note |
|---|---|---|---|---|---|
| `IfcBuildingElementPart` | point | planned | 5 | APRON, ARMOURUNIT, INSULATION, PRECASTPANEL, SAFETYCAGE | — |  |
| `IfcDiscreteAccessory` | point | planned | 21 | ANCHORPLATE, BIRDPROTECTION, BRACKET, CABLEARRANGER, ELASTIC_CUSHION, EXPANSION_JOINT_DEVICE, FILLER, FLASHING, INSULATOR, LOCK, PANEL_STRENGTHENING, POINTMACHINEMOUNTINGDEVICE, POINT_MACHINE_LOCKING_DEVICE, RAILBRACE, RAILPAD, RAIL_LUBRICATION, RAIL_MECHANICAL_EQUIPMENT, SHOE, SLIDINGCHAIR, SOUNDABSORPTION, TENSIONINGEQUIPMENT | O-18 |  |
| `IfcFastener` | point | planned | 3 | GLUE, MORTAR, WELD | — |  |
| `IfcImpactProtectionDevice` | point | planned | 4 | BUMPER, CRASHCUSHION, DAMPINGSYSTEM, FENDER | — |  |
| `IfcMechanicalFastener` | point | planned | 15 | ANCHORBOLT, BOLT, CHAIN, COUPLER, DOWEL, NAIL, NAILPLATE, RAILFASTENING, RAILJOINT, RIVET, ROPE, SCREW, SHEARCONNECTOR, STAPLE, STUDSHEARCONNECTOR | O-18 |  |
| `IfcReinforcingBar` | linear | planned | 9 | ANCHORING, EDGE, LIGATURE, MAIN, PUNCHING, RING, SHEAR, SPACEBAR, STUD | — |  |
| `IfcReinforcingMesh` | area | planned | 0 | — | — |  |
| `IfcTendon` | linear | planned | 4 | BAR, COATED, STRAND, WIRE | — |  |
| `IfcTendonAnchor` | point | planned | 3 | COUPLER, FIXED_END, TENSIONING_END | — |  |
| `IfcTendonConduit` | linear | planned | 5 | COUPLER, DIABOLO, DUCT, GROUTING_DUCT, TRUMPET | — |  |
| `IfcSign` | point | planned | 3 | MARKER, MIRROR, PICTORAL | G-03 |  |
| `IfcVibrationDamper` | point | planned | 6 | AXIAL_YIELD, BENDING_YIELD, FRICTION, RUBBER, SHEAR_YIELD, VISCOUS | — |  |
| `IfcVibrationIsolator` | point | planned | 3 | BASE, COMPRESSION, SPRING | — |  |

## Features (voids, projections, surface treatments)

| Class | Archetype | Types | Predefined types | Detailed sheets | Note |
|---|---|---|---|---|---|
| `IfcProjectionElement` | hosted | planned | 2 | BLISTER, DEVIATOR | — |  |
| `IfcEarthworksCut` | hosted | planned | 9 | BASE_EXCAVATION, CUT, DREDGING, EXCAVATION, OVEREXCAVATION, PAVEMENTMILLING, STEPEXCAVATION, TOPSOILREMOVAL, TRENCH | — |  |
| `IfcOpeningElement` | hosted | ✅ | 2 | OPENING, RECESS | O-15 |  |
| `IfcVoidingFeature` | hosted | planned | 6 | CHAMFER, CUTOUT, EDGE, HOLE, MITER, NOTCH | — |  |
| `IfcSurfaceFeature` | hosted | planned | 11 | DEFECT, HATCHMARKING, LINEMARKING, MARK, NONSKIDSURFACING, PAVEMENTSURFACEMARKING, RUMBLESTRIP, SYMBOLMARKING, TAG, TRANSVERSERUMBLESTRIP, TREATMENT | — |  |

## Furnishing

| Class | Archetype | Types | Predefined types | Detailed sheets | Note |
|---|---|---|---|---|---|
| `IfcFurnishingElement` | point | planned | 0 | — | — | generic supertype; template for elements with no specific class |
| `IfcFurniture` | point | planned | 8 | BED, CHAIR, DESK, FILECABINET, SHELF, SOFA, TABLE, TECHNICALCABINET | E-01, E-02, E-03, E-04, E-05, E-06, E-07, F-08, F-09, F-10, F-12, F-14, G-02 |  |
| `IfcSystemFurnitureElement` | point | planned | 3 | PANEL, SUBRACK, WORKSURFACE | F-11 |  |

## Geographic

| Class | Archetype | Types | Predefined types | Detailed sheets | Note |
|---|---|---|---|---|---|
| `IfcGeographicElement` | point | planned | 3 | SOIL_BORING_POINT, TERRAIN, VEGETATION | G-01 |  |

## Geotechnical

| Class | Archetype | Types | Predefined types | Detailed sheets | Note |
|---|---|---|---|---|---|
| `IfcBorehole` | point | planned | 0 | — | — |  |
| `IfcGeomodel` | area | planned | 0 | — | — |  |
| `IfcGeoslice` | area | planned | 0 | — | — |  |
| `IfcGeotechnicalStratum` | area | planned | 3 | SOLID, VOID, WATER | — |  |

## Transportation devices

| Class | Archetype | Types | Predefined types | Detailed sheets | Note |
|---|---|---|---|---|---|
| `IfcTransportElement` | point | planned | 6 | CRANEWAY, ELEVATOR, ESCALATOR, HAULINGGEAR, LIFTINGGEAR, MOVINGWALKWAY | T-01, T-02, T-03 |  |
| `IfcVehicle` | point | planned | 7 | CARGO, ROLLINGSTOCK, VEHICLE, VEHICLEAIR, VEHICLEMARINE, VEHICLETRACKED, VEHICLEWHEELED | — |  |

## Other

| Class | Archetype | Types | Predefined types | Detailed sheets | Note |
|---|---|---|---|---|---|
| `IfcCivilElement` | any | planned | 0 | — | — | generic supertype; template for elements with no specific class |
| `IfcDistributionElement` | point | planned | 0 | — | — | generic supertype; template for elements with no specific class |
| `IfcDistributionFlowElement` | point | planned | 0 | — | — | generic supertype; template for elements with no specific class |
| `IfcElementAssembly` | assembly | ✅ | 28 | ABUTMENT, ACCESSORY_ASSEMBLY, ARCH, BEAM_GRID, BRACED_FRAME, CROSS_BRACING, DECK, DILATATIONPANEL, ENTRANCEWORKS, GIRDER, GRID, MAST, PIER, PYLON, RAIL_MECHANICAL_EQUIPMENT_ASSEMBLY, REINFORCEMENT_UNIT, RIGID_FRAME, SHELTER, SIGNALASSEMBLY, SLAB_FIELD, SUMPBUSTER, SUPPORTINGASSEMBLY, SUSPENSIONASSEMBLY, TRACKPANEL, TRACTION_SWITCHING_ASSEMBLY, TRAFFIC_CALMING_DEVICE, TRUSS, TURNOUTPANEL | O-17 |  |
| `IfcVirtualElement` | area | planned | 3 | BOUNDARY, CLEARANCE, PROVISIONFORVOID | — |  |
