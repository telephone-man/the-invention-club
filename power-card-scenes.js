(function () {
  const partLibrary = {
    wheel: {
      label: "Wheel",
      connectors: { center: { x: 70, y: 70, type: "axle" } },
      connectsTo: { center: ["axle.center", "motor.shaft", "servo.horn"] }
    },
    axle: {
      label: "Axle",
      connectors: {
        left: { x: 0, y: 12, type: "axle" },
        center: { x: 90, y: 12, type: "axle" },
        right: { x: 180, y: 12, type: "axle" }
      },
      connectsTo: { center: ["wheel.center", "motor.shaft"] }
    },
    motor: {
      label: "Motor",
      connectors: {
        shaft: { x: 62, y: 72, type: "axle" },
        powerPositive: { x: 230, y: 56, type: "power" },
        powerNegative: { x: 230, y: 92, type: "ground" },
        mount: { x: 122, y: 145, type: "mount" }
      },
      connectsTo: {
        shaft: ["wheel.center", "axle.center"],
        powerPositive: ["batteryPack.positive", "switch.output", "fuse.output"],
        powerNegative: ["batteryPack.negative", "board.ground"]
      }
    },
    servo: {
      label: "Servo",
      connectors: {
        horn: { x: 88, y: 55, type: "pivot" },
        power: { x: 0, y: 100, type: "power" },
        signal: { x: 160, y: 100, type: "signal" },
        mount: { x: 84, y: 130, type: "mount" }
      },
      connectsTo: {
        horn: ["arm.pivotA", "linkage.pivotA"],
        power: ["batteryPack.positive", "board.output"],
        signal: ["board.signal"]
      }
    },
    arm: {
      label: "Arm",
      connectors: {
        pivotA: { x: 10, y: 25, type: "pivot" },
        pivotB: { x: 200, y: 25, type: "pivot" }
      },
      connectsTo: { pivotA: ["servo.horn", "hinge.pivot"], pivotB: ["linkage.pivotB"] }
    },
    linkage: {
      label: "Linkage",
      connectors: {
        pivotA: { x: 0, y: 40, type: "pivot" },
        pivotB: { x: 200, y: 40, type: "pivot" }
      },
      connectsTo: { pivotA: ["servo.horn", "arm.pivotA"], pivotB: ["arm.pivotB"] }
    },
    batteryPack: {
      label: "Battery pack",
      connectors: {
        positive: { x: 188, y: 38, type: "power" },
        negative: { x: 188, y: 74, type: "ground" }
      },
      connectsTo: {
        positive: ["switch.input", "button.input", "fuse.input", "board.power"],
        negative: ["motor.powerNegative", "board.ground", "ledIndicator.ground"]
      }
    },
    wire: {
      label: "Wire",
      connectors: {
        start: { x: 0, y: 0, type: "wire" },
        end: { x: 120, y: 0, type: "wire" }
      },
      connectsTo: { start: ["*.power", "*.signal"], end: ["*.power", "*.signal"] }
    },
    button: {
      label: "Button",
      connectors: {
        input: { x: 0, y: 72, type: "power" },
        output: { x: 132, y: 72, type: "signal" }
      },
      connectsTo: { input: ["batteryPack.positive"], output: ["board.input", "motor.powerPositive"] }
    },
    switch: {
      label: "Switch",
      connectors: {
        input: { x: 0, y: 52, type: "power" },
        output: { x: 150, y: 52, type: "power" }
      },
      connectsTo: { input: ["batteryPack.positive"], output: ["motor.powerPositive", "ledIndicator.input"] }
    },
    knob: {
      label: "Knob",
      connectors: {
        input: { x: 0, y: 70, type: "power" },
        output: { x: 132, y: 70, type: "signal" }
      },
      connectsTo: { output: ["board.input"] }
    },
    joystick: {
      label: "Joystick",
      connectors: {
        input: { x: 0, y: 84, type: "power" },
        output: { x: 150, y: 84, type: "signal" }
      },
      connectsTo: { output: ["board.input", "receiver.input"] }
    },
    ledIndicator: {
      label: "Indicator",
      connectors: {
        input: { x: 0, y: 60, type: "signal" },
        ground: { x: 0, y: 82, type: "ground" }
      },
      connectsTo: { input: ["board.output", "switch.output"], ground: ["batteryPack.negative"] }
    },
    lightSensor: {
      label: "Light sensor",
      connectors: {
        power: { x: 0, y: 70, type: "power" },
        output: { x: 142, y: 65, type: "signal" }
      },
      connectsTo: { output: ["board.input"] }
    },
    distanceSensor: {
      label: "Distance sensor",
      connectors: {
        power: { x: 0, y: 70, type: "power" },
        output: { x: 152, y: 65, type: "signal" }
      },
      connectsTo: { output: ["board.input"] }
    },
    tiltSensor: {
      label: "Tilt sensor",
      connectors: {
        power: { x: 0, y: 58, type: "power" },
        output: { x: 150, y: 58, type: "signal" }
      },
      connectsTo: { output: ["board.input"] }
    },
    board: {
      label: "Board",
      connectors: {
        power: { x: 30, y: 120, type: "power" },
        ground: { x: 70, y: 120, type: "ground" },
        input: { x: 0, y: 70, type: "signal" },
        output: { x: 190, y: 70, type: "signal" },
        signal: { x: 188, y: 38, type: "signal" }
      },
      connectsTo: {
        input: ["button.output", "knob.output", "joystick.output", "lightSensor.output"],
        output: ["ledIndicator.input", "servo.signal", "receiver.input"],
        power: ["batteryPack.positive"]
      }
    },
    antenna: {
      label: "Antenna",
      connectors: {
        input: { x: 0, y: 86, type: "signal" },
        air: { x: 155, y: 36, type: "radio" }
      },
      connectsTo: { input: ["board.output"], air: ["receiver.air"] }
    },
    receiver: {
      label: "Receiver",
      connectors: {
        air: { x: 18, y: 36, type: "radio" },
        input: { x: 0, y: 72, type: "signal" },
        output: { x: 180, y: 72, type: "signal" }
      },
      connectsTo: { air: ["antenna.air"], output: ["ledIndicator.input"] }
    },
    beam: {
      label: "Beam",
      connectors: {
        endA: { x: 0, y: 20, type: "structure" },
        endB: { x: 220, y: 20, type: "structure" }
      },
      connectsTo: { endA: ["brace.endA", "chassis.front"], endB: ["brace.endB", "chassis.back"] }
    },
    brace: {
      label: "Brace",
      connectors: {
        endA: { x: 0, y: 100, type: "structure" },
        endB: { x: 140, y: 0, type: "structure" }
      },
      connectsTo: { endA: ["beam.endA"], endB: ["beam.endB"] }
    },
    hinge: {
      label: "Hinge",
      connectors: {
        pivot: { x: 70, y: 70, type: "pivot" },
        panelA: { x: 0, y: 70, type: "structure" },
        panelB: { x: 140, y: 70, type: "structure" }
      },
      connectsTo: { pivot: ["arm.pivotA"], panelA: ["cardboardPanel.hingeEdge"] }
    },
    chassis: {
      label: "Chassis",
      connectors: {
        front: { x: 30, y: 78, type: "structure" },
        back: { x: 330, y: 78, type: "structure" },
        motorMount: { x: 220, y: 80, type: "mount" },
        axle: { x: 280, y: 138, type: "axle" }
      },
      connectsTo: { motorMount: ["motor.mount"], axle: ["wheel.center"] }
    },
    cardboardPanel: {
      label: "Cardboard panel",
      connectors: {
        hingeEdge: { x: 28, y: 82, type: "structure" },
        tab: { x: 180, y: 82, type: "join" },
        center: { x: 104, y: 82, type: "surface" }
      },
      connectsTo: { hingeEdge: ["hinge.panelA"], tab: ["template.mark"] }
    },
    template: {
      label: "Template",
      connectors: {
        mark: { x: 120, y: 90, type: "mark" },
        corner: { x: 20, y: 24, type: "align" }
      },
      connectsTo: { mark: ["cardboardPanel.tab"] }
    },
    testLeads: {
      label: "Test leads",
      connectors: {
        positive: { x: 0, y: 20, type: "test" },
        negative: { x: 0, y: 64, type: "test" },
        probePositive: { x: 210, y: 20, type: "probe" },
        probeNegative: { x: 210, y: 64, type: "probe" }
      },
      connectsTo: { positive: ["multimeter.leadPositive"], probePositive: ["prototypeBody.testPoint"] }
    },
    multimeter: {
      label: "Multimeter",
      connectors: {
        leadPositive: { x: 34, y: 160, type: "test" },
        leadNegative: { x: 72, y: 160, type: "test" }
      },
      connectsTo: { leadPositive: ["testLeads.positive"], leadNegative: ["testLeads.negative"] }
    },
    magnifier: {
      label: "Magnifier",
      connectors: { focus: { x: 98, y: 98, type: "focus" } },
      connectsTo: { focus: ["prototypeBody.testPoint"] }
    },
    checklist: {
      label: "Checklist",
      connectors: {
        firstItem: { x: 84, y: 66, type: "evidence" },
        lastItem: { x: 84, y: 132, type: "evidence" }
      },
      connectsTo: { firstItem: ["testLeads.probePositive"] }
    },
    decisionFlow: {
      label: "Decision flow",
      connectors: {
        trigger: { x: 48, y: 52, type: "logic" },
        action: { x: 230, y: 52, type: "logic" },
        output: { x: 410, y: 52, type: "logic" }
      },
      connectsTo: { trigger: ["button.output", "lightSensor.output"], output: ["ledIndicator.input"] }
    },
    prototypeBody: {
      label: "Prototype body",
      connectors: {
        input: { x: 0, y: 88, type: "signal" },
        output: { x: 260, y: 88, type: "signal" },
        testPoint: { x: 130, y: 56, type: "test" }
      },
      connectsTo: { input: ["button.output"], output: ["ledIndicator.input"], testPoint: ["magnifier.focus"] }
    },
    fuse: {
      label: "Current protection",
      connectors: {
        input: { x: 0, y: 50, type: "power" },
        output: { x: 132, y: 50, type: "power" }
      },
      connectsTo: { input: ["batteryPack.positive"], output: ["motor.powerPositive", "ledIndicator.input"] }
    },
    timerBoard: {
      label: "Timer board",
      connectors: {
        input: { x: 0, y: 72, type: "signal" },
        output: { x: 190, y: 72, type: "signal" },
        power: { x: 38, y: 124, type: "power" }
      },
      connectsTo: { input: ["button.output"], output: ["ledIndicator.input", "motor.powerPositive"] }
    },
    loadWeight: {
      label: "Load weight",
      connectors: { load: { x: 60, y: 90, type: "load" } },
      connectsTo: { load: ["beam.endB", "chassis.back"] }
    },
    materialSwatch: {
      label: "Material swatch",
      connectors: {
        sample: { x: 90, y: 62, type: "material" },
        join: { x: 168, y: 62, type: "join" }
      },
      connectsTo: { join: ["cardboardPanel.tab"] }
    },
    cueTile: {
      label: "Card-specific cue asset",
      connectors: {
        center: { x: 89, y: 64, type: "cue" },
        input: { x: 0, y: 64, type: "cue" },
        output: { x: 178, y: 64, type: "cue" }
      },
      connectsTo: { center: ["*.cue"], input: ["*.signal", "*.power"], output: ["*.signal", "*.power"] }
    }
  };

  const animationTemplates = {
    motor_spin: { primaryMotion: "spin", parts: ["batteryPack", "switch", "motor", "wheel"] },
    servo_swing: { primaryMotion: "swing", parts: ["batteryPack", "board", "servo", "arm"] },
    button_signal_load: { primaryMotion: "press-pulse", parts: ["button", "board", "ledIndicator"] },
    sensor_threshold: { primaryMotion: "sense-pulse", parts: ["lightSensor", "board", "ledIndicator"] },
    safe_power: { primaryMotion: "safe-flow", parts: ["batteryPack", "fuse", "switch", "ledIndicator"] },
    brace_load: { primaryMotion: "load-test", parts: ["beam", "brace", "chassis", "loadWeight"] },
    hinge_or_linkage: { primaryMotion: "pivot", parts: ["cardboardPanel", "hinge", "servo", "arm"] },
    wireless_signal: { primaryMotion: "radio-pulse", parts: ["button", "antenna", "receiver", "ledIndicator"] },
    logic_sequence: { primaryMotion: "step-sequence", parts: ["decisionFlow", "timerBoard", "ledIndicator"] },
    debug_test: { primaryMotion: "test-pulse", parts: ["multimeter", "testLeads", "prototypeBody", "magnifier"] },
    material_build: { primaryMotion: "make-step", parts: ["template", "cardboardPanel", "materialSwatch"] },
    design_iterate: { primaryMotion: "iterate", parts: ["prototypeBody", "checklist", "materialSwatch"] }
  };

  const cueAssetEntries = [
    ["actionTokensCue", "sequence", "sequence"],
    ["assemblyCue", "material", "pulse"],
    ["axleCue", "mechanism", "spin"],
    ["baseCue", "structure", "pulse"],
    ["batteryCue", "power", "pulse"],
    ["batteryChoiceCue", "batteryChoice", "pulse"],
    ["batteryLoadCue", "batteryLoad", "pulse"],
    ["batteryWeightCue", "power", "load"],
    ["beforeAfterCue", "repair", "pulse"],
    ["boardCue", "display", "pulse"],
    ["braceCue", "brace", "pulse"],
    ["bridgeCue", "structure", "load"],
    ["brokenModelCue", "fault", "wobble"],
    ["buggySequenceCue", "flowchart", "sequence"],
    ["buttonCue", "button", "press"],
    ["buzzerFlagCue", "buzzerFlag", "waves"],
    ["cableTieCue", "fastener", "pulse"],
    ["calibrationCue", "calibration", "pulse"],
    ["camCue", "cam", "spin"],
    ["cardboardPanelCue", "material", "pulse"],
    ["cellCue", "cell", "pulse"],
    ["chartCue", "chart", "pulse"],
    ["challengeCue", "challenge", "pulse"],
    ["chassisCue", "chassis", "wobble"],
    ["checklistCue", "debug", "sequence"],
    ["coinCue", "cell", "pulse"],
    ["commandCue", "command", "pulse"],
    ["commandCardsCue", "sequence", "sequence"],
    ["commonGroundCue", "commonGround", "pulse"],
    ["comparisonCue", "criteria", "pulse"],
    ["componentsCue", "material", "pulse"],
    ["conditionCardsCue", "ifThen", "sequence"],
    ["confusingPanelCue", "panel", "wobble"],
    ["connectorCue", "circuit", "pulse"],
    ["constraintCue", "constraint", "pulse"],
    ["controlBoardCue", "display", "pulse"],
    ["controlPanelCue", "panel", "pulse"],
    ["controlSetCue", "controls", "swing"],
    ["controllerCue", "controls", "swing"],
    ["counterCue", "counter", "sequence"],
    ["criteriaCue", "criteria", "pulse"],
    ["circuitCue", "circuit", "pulse"],
    ["displayCue", "display", "pulse"],
    ["distanceCue", "distanceSensor", "sense"],
    ["debugCue", "debug", "pulse"],
    ["enclosureCue", "enclosure", "pulse"],
    ["eventCardsCue", "sequence", "sequence"],
    ["expectedActualCue", "debug", "pulse"],
    ["fastenersCue", "fastener", "pulse"],
    ["faultCardsCue", "fault", "pulse"],
    ["faultChecklistCue", "debug", "sequence"],
    ["faultyBuildCue", "fault", "wobble"],
    ["feedbackCue", "feedback", "pulse"],
    ["flapCue", "hinge", "swing"],
    ["flowchartCue", "flowchart", "sequence"],
    ["foldCue", "material", "swing"],
    ["footCue", "cam", "swing"],
    ["frameComparisonCue", "criteria", "pulse"],
    ["frameSamplesCue", "frame", "pulse"],
    ["fuseCue", "fuse", "pulse"],
    ["gearCue", "gear", "spin"],
    ["handleCue", "material", "pulse"],
    ["hingeCue", "hinge", "swing"],
    ["holderCue", "cell", "pulse"],
    ["holePunchCue", "hole", "pulse"],
    ["ifThenCue", "ifThen", "sequence"],
    ["indicatorCue", "led", "blink"],
    ["jobCardsCue", "challenge", "pulse"],
    ["joinCue", "fastener", "pulse"],
    ["joinOptionsCue", "fastener", "pulse"],
    ["joystickCue", "joystick", "swing"],
    ["knobCue", "knob", "swing"],
    ["labelsCue", "criteria", "pulse"],
    ["leadsCue", "circuit", "pulse"],
    ["ledCue", "led", "blink"],
    ["ledMotorCue", "led", "blink"],
    ["ledStripCue", "led", "blink"],
    ["lightCue", "lightSensor", "sense"],
    ["linkageCue", "mechanism", "swing"],
    ["loadCardsCue", "criteria", "pulse"],
    ["loadCue", "structure", "load"],
    ["loadDataCue", "chart", "pulse"],
    ["logicBoardCue", "display", "pulse"],
    ["logsCue", "chart", "pulse"],
    ["magnifierCue", "debug", "scan"],
    ["materialComparisonCue", "criteria", "pulse"],
    ["materialListCue", "material", "pulse"],
    ["materialSamplesCue", "material", "pulse"],
    ["measureStripCue", "criteria", "pulse"],
    ["mechanismCue", "mechanism", "spin"],
    ["messageCardsCue", "message", "pulse"],
    ["messageCodeCue", "message", "sequence"],
    ["messageDesignCue", "message", "pulse"],
    ["meterCue", "meter", "pulse"],
    ["motorCue", "motor", "spin"],
    ["motorMountCue", "mount", "wobble"],
    ["motorSupplyCue", "power", "pulse"],
    ["noisyCue", "noisy", "pulse"],
    ["observationCue", "debug", "scan"],
    ["pairingCue", "pair", "waves"],
    ["panelCue", "panel", "pulse"],
    ["partsListCue", "material", "pulse"],
    ["patternCue", "sequence", "sequence"],
    ["pencilCue", "sketch", "pulse"],
    ["planningCue", "taskBoard", "sequence"],
    ["polarityCue", "power", "pulse"],
    ["propCue", "material", "pulse"],
    ["propertyCue", "criteria", "pulse"],
    ["prototypeCue", "repair", "pulse"],
    ["prototypeNotesCue", "criteria", "pulse"],
    ["prototypePartsCue", "material", "pulse"],
    ["prototypeSamplesCue", "material", "pulse"],
    ["radioCue", "radio", "waves"],
    ["radioPairCue", "pair", "waves"],
    ["rangeCue", "range", "pulse"],
    ["receiverCue", "pair", "waves"],
    ["remoteCue", "remote", "press"],
    ["repairNotesCue", "debug", "pulse"],
    ["resultNotesCue", "criteria", "pulse"],
    ["ruleCardsCue", "sequence", "sequence"],
    ["rolesCue", "user", "pulse"],
    ["roughJoinCue", "fastener", "wobble"],
    ["rubberCue", "rubber", "pulse"],
    ["rulerCue", "criteria", "pulse"],
    ["safeCutterCue", "cut", "pulse"],
    ["safetyCue", "fuse", "pulse"],
    ["sensorMountCue", "mount", "pulse"],
    ["sensorSetCue", "sensorSet", "sense"],
    ["senderReceiverCue", "pair", "waves"],
    ["sequenceCue", "sequence", "sequence"],
    ["servoCue", "servo", "swing"],
    ["shadeCue", "threshold", "sense"],
    ["signalDemoCue", "radio", "waves"],
    ["sketchCue", "sketch", "pulse"],
    ["sortingCue", "criteria", "pulse"],
    ["sliderCue", "mechanism", "swing"],
    ["solenoidCue", "solenoid", "pulse"],
    ["spaceCue", "space", "pulse"],
    ["spacerCue", "fastener", "pulse"],
    ["stableFrameCue", "frame", "pulse"],
    ["stateCue", "state", "sequence"],
    ["stopwatchCue", "timer", "sequence"],
    ["subsystemCue", "subsystem", "sequence"],
    ["swapPartCue", "repair", "pulse"],
    ["switchCue", "controls", "press"],
    ["tabsCue", "tabs", "pulse"],
    ["targetWallCue", "distanceSensor", "sense"],
    ["taskBoardCue", "taskBoard", "sequence"],
    ["templateCue", "template", "pulse"],
    ["testCue", "debug", "pulse"],
    ["testLeadsCue", "circuit", "pulse"],
    ["testLogCue", "chart", "pulse"],
    ["testNotesCue", "debug", "pulse"],
    ["testObjectsCue", "material", "pulse"],
    ["testRigCue", "testRig", "load"],
    ["testScriptCue", "sequence", "sequence"],
    ["testSheetCue", "debug", "pulse"],
    ["testWeightsCue", "structure", "load"],
    ["thresholdCue", "threshold", "sense"],
    ["tiltCue", "tiltSensor", "sense"],
    ["timerCue", "timer", "sequence"],
    ["towerCue", "tower", "load"],
    ["tradeoffCue", "criteria", "pulse"],
    ["triangleCue", "truss", "pulse"],
    ["twoBoardsCue", "pair", "waves"],
    ["twoSendersCue", "senders", "waves"],
    ["twoSensorCue", "sensorSet", "sense"],
    ["twoServoCue", "servo", "swing"],
    ["twoSketchesCue", "sketch", "pulse"],
    ["userCue", "user", "pulse"],
    ["voltageDropCue", "voltageDrop", "pulse"],
    ["weakChassisCue", "chassis", "wobble"],
    ["weakFixCue", "repair", "wobble"],
    ["weakFrameCue", "frame", "wobble"],
    ["weightCue", "structure", "load"],
    ["weightsCue", "structure", "load"],
    ["wheelCue", "mechanism", "spin"]
  ];

  const cueAssets = Object.fromEntries(
    cueAssetEntries.map(([id, kind, motion]) => [id, { kind, motion }])
  );

  const familyAccents = {
    movement: "#0e7c86",
    control_input: "#f15f45",
    sensing: "#315eaa",
    structures: "#d28b21",
    power: "#f4be38",
    materials_fabrication: "#7d5bbf",
    logic_sequencing: "#2f8a4b",
    communication: "#5c7cfa",
    debugging_testing: "#d54a3a",
    design_iteration: "#09666b"
  };

  const familyCards = {
    movement: [
      "r_mov_01",
      "r_mov_02",
      "r_mov_03",
      "r_mov_04",
      "r_mov_05",
      "r_mov_06",
      "r_mov_07",
      "r_mov_08",
      "r_mov_09",
      "r_mov_10",
      "r_mov_11",
      "r_mov_12"
    ],
    control_input: [
      "r_ctl_01",
      "r_ctl_02",
      "r_ctl_03",
      "r_ctl_04",
      "r_ctl_05",
      "r_ctl_06",
      "r_ctl_07",
      "r_ctl_08",
      "r_ctl_09",
      "r_ctl_10",
      "r_ctl_11",
      "r_ctl_12"
    ],
    sensing: [
      "r_sen_01",
      "r_sen_02",
      "r_sen_03",
      "r_sen_04",
      "r_sen_05",
      "r_sen_06",
      "r_sen_07",
      "r_sen_08",
      "r_sen_09",
      "r_sen_10",
      "r_sen_11",
      "r_sen_12"
    ],
    structures: [
      "r_str_01",
      "r_str_02",
      "r_str_03",
      "r_str_04",
      "r_str_05",
      "r_str_06",
      "r_str_07",
      "r_str_08",
      "r_str_09",
      "r_str_10",
      "r_str_11",
      "r_str_12"
    ],
    power: [
      "r_pow_01",
      "r_pow_02",
      "r_pow_03",
      "r_pow_04",
      "r_pow_05",
      "r_pow_06",
      "r_pow_07",
      "r_pow_08",
      "r_pow_09",
      "r_pow_10",
      "r_pow_11",
      "r_pow_12"
    ],
    materials_fabrication: [
      "r_mat_01",
      "r_mat_02",
      "r_mat_03",
      "r_mat_04",
      "r_mat_05",
      "r_mat_06",
      "r_mat_07",
      "r_mat_08",
      "r_mat_09",
      "r_mat_10",
      "r_mat_11",
      "r_mat_12"
    ],
    logic_sequencing: [
      "r_log_01",
      "r_log_02",
      "r_log_03",
      "r_log_04",
      "r_log_05",
      "r_log_06",
      "r_log_07",
      "r_log_08",
      "r_log_09",
      "r_log_10",
      "r_log_11",
      "r_log_12"
    ],
    communication: [
      "r_com_01",
      "r_com_02",
      "r_com_03",
      "r_com_04",
      "r_com_05",
      "r_com_06",
      "r_com_07",
      "r_com_08",
      "r_com_09",
      "r_com_10",
      "r_com_11",
      "r_com_12"
    ],
    debugging_testing: [
      "r_dbg_01",
      "r_dbg_02",
      "r_dbg_03",
      "r_dbg_04",
      "r_dbg_05",
      "r_dbg_06",
      "r_dbg_07",
      "r_dbg_08",
      "r_dbg_09",
      "r_dbg_10",
      "r_dbg_11",
      "r_dbg_12"
    ],
    design_iteration: [
      "r_des_01",
      "r_des_02",
      "r_des_03",
      "r_des_04",
      "r_des_05",
      "r_des_06",
      "r_des_07",
      "r_des_08",
      "r_des_09",
      "r_des_10",
      "r_des_11",
      "r_des_12"
    ]
  };

  const familyTemplates = {
    movement: [
      "hinge_or_linkage",
      "motor_spin",
      "servo_swing",
      "motor_spin",
      "hinge_or_linkage",
      "servo_swing",
      "debug_test",
      "design_iterate",
      "hinge_or_linkage",
      "motor_spin",
      "hinge_or_linkage",
      "servo_swing"
    ],
    control_input: [
      "button_signal_load",
      "button_signal_load",
      "button_signal_load",
      "button_signal_load",
      "button_signal_load",
      "button_signal_load",
      "button_signal_load",
      "debug_test",
      "button_signal_load",
      "button_signal_load",
      "sensor_threshold",
      "design_iterate"
    ],
    sensing: [
      "sensor_threshold",
      "sensor_threshold",
      "sensor_threshold",
      "sensor_threshold",
      "debug_test",
      "sensor_threshold",
      "debug_test",
      "debug_test",
      "sensor_threshold",
      "sensor_threshold",
      "sensor_threshold",
      "sensor_threshold"
    ],
    structures: [
      "brace_load",
      "brace_load",
      "brace_load",
      "hinge_or_linkage",
      "brace_load",
      "brace_load",
      "brace_load",
      "design_iterate",
      "brace_load",
      "brace_load",
      "brace_load",
      "motor_spin"
    ],
    power: [
      "safe_power",
      "safe_power",
      "debug_test",
      "safe_power",
      "safe_power",
      "safe_power",
      "debug_test",
      "design_iterate",
      "safe_power",
      "safe_power",
      "debug_test",
      "motor_spin"
    ],
    materials_fabrication: [
      "material_build",
      "material_build",
      "material_build",
      "material_build",
      "material_build",
      "material_build",
      "debug_test",
      "design_iterate",
      "material_build",
      "hinge_or_linkage",
      "material_build",
      "material_build"
    ],
    logic_sequencing: [
      "logic_sequence",
      "logic_sequence",
      "logic_sequence",
      "logic_sequence",
      "logic_sequence",
      "logic_sequence",
      "debug_test",
      "design_iterate",
      "logic_sequence",
      "logic_sequence",
      "sensor_threshold",
      "logic_sequence"
    ],
    communication: [
      "wireless_signal",
      "wireless_signal",
      "wireless_signal",
      "wireless_signal",
      "wireless_signal",
      "wireless_signal",
      "debug_test",
      "design_iterate",
      "wireless_signal",
      "logic_sequence",
      "wireless_signal",
      "wireless_signal"
    ],
    debugging_testing: [
      "debug_test",
      "debug_test",
      "debug_test",
      "debug_test",
      "debug_test",
      "debug_test",
      "debug_test",
      "design_iterate",
      "debug_test",
      "debug_test",
      "debug_test",
      "brace_load"
    ],
    design_iteration: [
      "design_iterate",
      "design_iterate",
      "design_iterate",
      "design_iterate",
      "logic_sequence",
      "design_iterate",
      "design_iterate",
      "design_iterate",
      "design_iterate",
      "material_build",
      "button_signal_load",
      "material_build"
    ]
  };

  const cardCues = {
    r_mov_01: ["motorCue", "servoCue", "solenoidCue"],
    r_mov_02: ["motorCue", "batteryCue", "wheelCue"],
    r_mov_03: ["servoCue", "controlBoardCue"],
    r_mov_04: ["gearCue", "motorCue", "wheelCue"],
    r_mov_05: ["linkageCue", "hingeCue"],
    r_mov_06: ["twoServoCue", "linkageCue", "motorMountCue"],
    r_mov_07: ["spacerCue", "testCue", "mechanismCue"],
    r_mov_08: ["comparisonCue", "mechanismCue", "chartCue"],
    r_mov_09: ["wheelCue", "flapCue", "sliderCue"],
    r_mov_10: ["rubberCue", "axleCue", "chassisCue"],
    r_mov_11: ["camCue", "footCue", "motorCue"],
    r_mov_12: ["twoServoCue", "controllerCue", "linkageCue"],

    r_ctl_01: ["controlSetCue", "buttonCue", "knobCue"],
    r_ctl_02: ["buttonCue", "boardCue", "indicatorCue"],
    r_ctl_03: ["knobCue", "boardCue", "displayCue"],
    r_ctl_04: ["buttonCue", "counterCue", "testSheetCue"],
    r_ctl_05: ["joystickCue", "commandCue", "boardCue"],
    r_ctl_06: ["buttonCue", "joystickCue", "boardCue"],
    r_ctl_07: ["panelCue", "labelsCue", "knobCue"],
    r_ctl_08: ["testSheetCue", "controlPanelCue", "feedbackCue"],
    r_ctl_09: ["controlSetCue", "jobCardsCue", "labelsCue"],
    r_ctl_10: ["knobCue", "rangeCue", "ledCue"],
    r_ctl_11: ["tiltCue", "handleCue", "indicatorCue"],
    r_ctl_12: ["confusingPanelCue", "feedbackCue", "testSheetCue"],

    r_sen_01: ["sensorSetCue", "lightCue", "distanceCue"],
    r_sen_02: ["lightCue", "boardCue", "displayCue"],
    r_sen_03: ["thresholdCue", "chartCue", "sensorSetCue"],
    r_sen_04: ["distanceCue", "targetWallCue", "boardCue"],
    r_sen_05: ["calibrationCue", "chartCue", "testSheetCue"],
    r_sen_06: ["twoSensorCue", "boardCue", "chartCue"],
    r_sen_07: ["logsCue", "materialSamplesCue", "sensorSetCue"],
    r_sen_08: ["noisyCue", "testSheetCue", "sensorSetCue"],
    r_sen_09: ["sensorSetCue", "sortingCue", "materialSamplesCue"],
    r_sen_10: ["tiltCue", "indicatorCue", "boardCue"],
    r_sen_11: ["lightCue", "shadeCue", "thresholdCue"],
    r_sen_12: ["twoSensorCue", "indicatorCue", "testObjectsCue"],

    r_str_01: ["frameSamplesCue", "weightsCue", "triangleCue"],
    r_str_02: ["stableFrameCue", "weightCue", "baseCue"],
    r_str_03: ["braceCue", "weakFrameCue", "testCue"],
    r_str_04: ["hingeCue", "loadCue", "cardboardPanelCue"],
    r_str_05: ["chassisCue", "batteryWeightCue", "motorMountCue"],
    r_str_06: ["motorMountCue", "sensorMountCue", "fastenersCue"],
    r_str_07: ["weakChassisCue", "braceCue", "testWeightsCue"],
    r_str_08: ["frameComparisonCue", "testNotesCue", "tradeoffCue"],
    r_str_09: ["triangleCue", "braceCue", "frameSamplesCue"],
    r_str_10: ["towerCue", "baseCue", "weightsCue"],
    r_str_11: ["bridgeCue", "braceCue", "weightsCue"],
    r_str_12: ["motorMountCue", "chassisCue", "cableTieCue"],

    r_pow_01: ["cellCue", "holderCue", "polarityCue"],
    r_pow_02: ["batteryCue", "ledMotorCue", "leadsCue"],
    r_pow_03: ["meterCue", "batteryCue", "testLeadsCue"],
    r_pow_04: ["batteryChoiceCue", "loadCardsCue", "safetyCue"],
    r_pow_05: ["fuseCue", "motorCue", "batteryCue"],
    r_pow_06: ["motorSupplyCue", "logicBoardCue", "commonGroundCue"],
    r_pow_07: ["voltageDropCue", "faultyBuildCue", "meterCue"],
    r_pow_08: ["batteryChoiceCue", "loadDataCue", "safetyCue"],
    r_pow_09: ["cellCue", "holderCue", "polarityCue"],
    r_pow_10: ["ledStripCue", "switchCue", "batteryCue"],
    r_pow_11: ["voltageDropCue", "motorCue", "meterCue"],
    r_pow_12: ["batteryLoadCue", "motorCue", "switchCue"],

    r_mat_01: ["materialSamplesCue", "propertyCue", "comparisonCue"],
    r_mat_02: ["safeCutterCue", "rulerCue", "foldCue"],
    r_mat_03: ["holePunchCue", "templateCue", "cardboardPanelCue"],
    r_mat_04: ["fastenersCue", "materialSamplesCue", "joinCue"],
    r_mat_05: ["enclosureCue", "componentsCue", "fastenersCue"],
    r_mat_06: ["templateCue", "partsListCue", "assemblyCue"],
    r_mat_07: ["roughJoinCue", "joinOptionsCue", "testNotesCue"],
    r_mat_08: ["materialComparisonCue", "prototypeNotesCue", "tradeoffCue"],
    r_mat_09: ["materialSamplesCue", "jobCardsCue", "propertyCue"],
    r_mat_10: ["hingeCue", "safeCutterCue", "rulerCue"],
    r_mat_11: ["templateCue", "sketchCue", "safeCutterCue"],
    r_mat_12: ["enclosureCue", "tabsCue", "fastenersCue"],

    r_log_01: ["eventCardsCue", "sequenceCue", "actionTokensCue"],
    r_log_02: ["commandCardsCue", "boardCue", "sequenceCue"],
    r_log_03: ["ifThenCue", "conditionCardsCue", "boardCue"],
    r_log_04: ["timerCue", "stopwatchCue", "sequenceCue"],
    r_log_05: ["stateCue", "flowchartCue", "boardCue"],
    r_log_06: ["flowchartCue", "ruleCardsCue", "testScriptCue"],
    r_log_07: ["buggySequenceCue", "testScriptCue", "debugCue"],
    r_log_08: ["flowchartCue", "comparisonCue", "tradeoffCue"],
    r_log_09: ["sequenceCue", "actionTokensCue", "timerCue"],
    r_log_10: ["timerCue", "ledCue", "buttonCue"],
    r_log_11: ["ifThenCue", "sensorSetCue", "propCue"],
    r_log_12: ["timerCue", "motorCue", "servoCue"],

    r_com_01: ["signalDemoCue", "radioCue", "messageCardsCue"],
    r_com_02: ["radioPairCue", "twoBoardsCue", "messageCardsCue"],
    r_com_03: ["pairingCue", "labelsCue", "radioPairCue"],
    r_com_04: ["messageCodeCue", "radioCue", "displayCue"],
    r_com_05: ["remoteCue", "receiverCue", "commandCue"],
    r_com_06: ["twoSendersCue", "receiverCue", "planningCue"],
    r_com_07: ["rangeCue", "radioCue", "testLogCue"],
    r_com_08: ["messageDesignCue", "testLogCue", "tradeoffCue"],
    r_com_09: ["buzzerFlagCue", "radioCue", "ledCue"],
    r_com_10: ["buzzerFlagCue", "timerCue", "patternCue"],
    r_com_11: ["senderReceiverCue", "ledCue", "buttonCue"],
    r_com_12: ["radioPairCue", "indicatorCue", "messageCardsCue"],

    r_dbg_01: ["faultCardsCue", "brokenModelCue", "observationCue"],
    r_dbg_02: ["checklistCue", "prototypeCue", "testCue"],
    r_dbg_03: ["faultChecklistCue", "brokenModelCue", "debugCue"],
    r_dbg_04: ["circuitCue", "meterCue", "checklistCue"],
    r_dbg_05: ["expectedActualCue", "testScriptCue", "prototypeCue"],
    r_dbg_06: ["subsystemCue", "checklistCue", "prototypeCue"],
    r_dbg_07: ["weakFixCue", "testLogCue", "repairNotesCue"],
    r_dbg_08: ["beforeAfterCue", "repairNotesCue", "testLogCue"],
    r_dbg_09: ["observationCue", "magnifierCue", "faultCardsCue"],
    r_dbg_10: ["testLeadsCue", "connectorCue", "ledCue"],
    r_dbg_11: ["swapPartCue", "resultNotesCue", "prototypeCue"],
    r_dbg_12: ["testRigCue", "measureStripCue", "prototypeCue"],

    r_des_01: ["userCue", "constraintCue", "challengeCue"],
    r_des_02: ["sketchCue", "pencilCue", "prototypePartsCue"],
    r_des_03: ["constraintCue", "sketchCue", "tradeoffCue"],
    r_des_04: ["criteriaCue", "twoSketchesCue", "comparisonCue"],
    r_des_05: ["taskBoardCue", "materialListCue", "rolesCue"],
    r_des_06: ["prototypeCue", "testNotesCue", "criteriaCue"],
    r_des_07: ["tradeoffCue", "criteriaCue", "prototypeCue"],
    r_des_08: ["challengeCue", "constraintCue", "planningCue"],
    r_des_09: ["userCue", "jobCardsCue", "prototypeSamplesCue"],
    r_des_10: ["twoSketchesCue", "prototypePartsCue", "pencilCue"],
    r_des_11: ["feedbackCue", "handleCue", "buttonCue"],
    r_des_12: ["spaceCue", "measureStripCue", "prototypeCue"]
  };

  const controlTypes = {
    r_ctl_03: "knob",
    r_ctl_05: "joystick",
    r_ctl_06: "joystick",
    r_ctl_09: "joystick",
    r_ctl_10: "knob"
  };

  const sensorTypes = {
    r_ctl_11: "tiltSensor",
    r_sen_02: "lightSensor",
    r_sen_04: "distanceSensor",
    r_sen_10: "tiltSensor",
    r_sen_11: "lightSensor"
  };

  const controlTypeFor = (id) => controlTypes[id] || "button";
  const sensorTypeFor = (id) => sensorTypes[id] || "lightSensor";

  const commonBoardConnections = [
    { from: "battery.positive", to: "board.power", kind: "power", motion: "flow" },
    { from: "battery.negative", to: "board.ground", kind: "ground" }
  ];

  const cueSlots = [
    { x: 150, y: 224 },
    { x: 272, y: 224 },
    { x: 394, y: 224 }
  ];

  const cuePartsFor = (id, accent) =>
    (cardCues[id] || []).slice(0, cueSlots.length).map((variant, index) => ({
      id: `cue${index + 1}`,
      type: "cueTile",
      variant,
      x: cueSlots[index].x,
      y: cueSlots[index].y,
      scale: 0.52,
      motion: cueAssets[variant]?.motion || "pulse",
      accent
    }));

  const sceneKits = {
    motor_spin: (id, family, accent) => ({
      accent,
      parts: [
        { id: "battery", type: "batteryPack", x: 122, y: 330, scale: 0.92 },
        { id: "switch", type: "switch", x: 340, y: 352, scale: 0.92, motion: "press" },
        { id: "motor", type: "motor", x: 585, y: 304, scale: 0.92, motion: "spin" },
        { id: "wheel", type: "wheel", x: 548, y: 304, scale: 0.92, motion: "spin" },
        { id: "axle", type: "axle", x: 540, y: 425, scale: 0.8 }
      ],
      connections: [
        { from: "battery.positive", to: "switch.input", kind: "power", motion: "flow" },
        { from: "switch.output", to: "motor.powerPositive", kind: "power", motion: "flow" },
        { from: "battery.negative", to: "motor.powerNegative", kind: "ground" }
      ]
    }),
    servo_swing: (id, family, accent) => ({
      accent,
      parts: [
        { id: "battery", type: "batteryPack", x: 120, y: 340, scale: 0.88 },
        { id: "button", type: "button", x: 305, y: 348, scale: 0.88, motion: "press" },
        { id: "board", type: "board", x: 438, y: 322, scale: 0.9 },
        { id: "servo", type: "servo", x: 675, y: 302, scale: 0.95, motion: "swing" },
        { id: "arm", type: "arm", x: 735, y: 342, scale: 0.85, motion: "swing" }
      ],
      connections: [
        { from: "battery.positive", to: "button.input", kind: "power", motion: "flow" },
        { from: "button.output", to: "board.input", kind: "signal", motion: "pulse" },
        ...commonBoardConnections,
        { from: "board.signal", to: "servo.signal", kind: "signal", motion: "pulse" }
      ]
    }),
    button_signal_load: (id, family, accent) => {
      const controlType = controlTypeFor(id);
      return {
        accent,
        parts: [
          { id: "battery", type: "batteryPack", x: 112, y: 344, scale: 0.84 },
          {
            id: "control",
            type: controlType,
            x: 295,
            y: controlType === "joystick" ? 316 : 342,
            scale: 0.92,
            motion: controlType === "button" ? "press" : "swing"
          },
          { id: "board", type: "board", x: 470, y: 320, scale: 0.95 },
          { id: "indicator", type: "ledIndicator", x: 718, y: 328, scale: 0.96, motion: "blink" }
        ],
        connections: [
          { from: "battery.positive", to: "control.input", kind: "power", motion: "flow" },
          { from: "control.output", to: "board.input", kind: "signal", motion: "pulse" },
          ...commonBoardConnections,
          { from: "board.output", to: "indicator.input", kind: "signal", motion: "pulse" },
          { from: "battery.negative", to: "indicator.ground", kind: "ground" }
        ]
      };
    },
    sensor_threshold: (id, family, accent) => {
      const sensorType = sensorTypeFor(id);
      return {
        accent,
        parts: [
          { id: "battery", type: "batteryPack", x: 118, y: 348, scale: 0.82 },
          { id: "sensor", type: sensorType, x: 286, y: 318, scale: 0.98, motion: "sense" },
          { id: "board", type: "board", x: 472, y: 320, scale: 0.95 },
          { id: "indicator", type: "ledIndicator", x: 720, y: 328, scale: 0.96, motion: "blink" },
          { id: "sample", type: "materialSwatch", x: 260, y: 214, scale: 0.72, motion: "pulse" }
        ],
        connections: [
          ...commonBoardConnections,
          { from: "sensor.output", to: "board.input", kind: "signal", motion: "pulse" },
          { from: "board.output", to: "indicator.input", kind: "signal", motion: "pulse" },
          { from: "battery.negative", to: "indicator.ground", kind: "ground" }
        ]
      };
    },
    safe_power: (id, family, accent) => ({
      accent,
      parts: [
        { id: "battery", type: "batteryPack", x: 116, y: 330, scale: 0.9 },
        { id: "fuse", type: "fuse", x: 344, y: 350, scale: 0.92, motion: "pulse" },
        { id: "switch", type: "switch", x: 500, y: 352, scale: 0.9, motion: "press" },
        { id: "indicator", type: "ledIndicator", x: 704, y: 326, scale: 1, motion: "blink" },
        { id: "meter", type: "multimeter", x: 250, y: 212, scale: 0.68, motion: "pulse" }
      ],
      connections: [
        { from: "battery.positive", to: "fuse.input", kind: "power", motion: "flow" },
        { from: "fuse.output", to: "switch.input", kind: "power", motion: "flow" },
        { from: "switch.output", to: "indicator.input", kind: "power", motion: "flow" },
        { from: "battery.negative", to: "indicator.ground", kind: "ground" }
      ]
    }),
    brace_load: (id, family, accent) => ({
      accent,
      parts: [
        { id: "chassis", type: "chassis", x: 164, y: 360, scale: 1, motion: "wobble" },
        { id: "beamTop", type: "beam", x: 238, y: 292, scale: 1.15 },
        { id: "braceA", type: "brace", x: 266, y: 318, scale: 1.05, motion: "pulse" },
        { id: "braceB", type: "brace", x: 444, y: 318, scale: 1.05, motion: "pulse" },
        { id: "load", type: "loadWeight", x: 662, y: 286, scale: 0.98, motion: "load" }
      ],
      connections: [
        { from: "braceA.endA", to: "beamTop.endA", kind: "structure" },
        { from: "braceA.endB", to: "beamTop.endB", kind: "structure" },
        { from: "load.load", to: "beamTop.endB", kind: "load", motion: "pulse" }
      ]
    }),
    hinge_or_linkage: (id, family, accent) => ({
      accent,
      parts: [
        { id: "panel", type: "cardboardPanel", x: 142, y: 328, scale: 1.05 },
        { id: "hinge", type: "hinge", x: 354, y: 302, scale: 1.02, motion: "swing" },
        { id: "servo", type: "servo", x: 574, y: 322, scale: 0.88, motion: "swing" },
        { id: "arm", type: "arm", x: 652, y: 360, scale: 0.92, motion: "swing" },
        { id: "link", type: "linkage", x: 454, y: 270, scale: 0.82, motion: "swing" }
      ],
      connections: [
        { from: "hinge.pivot", to: "arm.pivotA", kind: "structure", motion: "pulse" },
        { from: "link.pivotA", to: "hinge.pivot", kind: "structure" },
        { from: "link.pivotB", to: "servo.horn", kind: "structure" }
      ]
    }),
    wireless_signal: (id, family, accent) => ({
      accent,
      parts: [
        { id: "button", type: "button", x: 126, y: 350, scale: 0.9, motion: "press" },
        { id: "sender", type: "board", x: 306, y: 322, scale: 0.9 },
        { id: "antenna", type: "antenna", x: 502, y: 312, scale: 1, motion: "waves" },
        { id: "receiver", type: "receiver", x: 694, y: 324, scale: 0.9, motion: "pulse" },
        { id: "indicator", type: "ledIndicator", x: 824, y: 330, scale: 0.72, motion: "blink" }
      ],
      connections: [
        { from: "button.output", to: "sender.input", kind: "signal", motion: "pulse" },
        { from: "sender.output", to: "antenna.input", kind: "signal", motion: "pulse" },
        { from: "antenna.air", to: "receiver.air", kind: "radio", motion: "pulse" },
        { from: "receiver.output", to: "indicator.input", kind: "signal", motion: "pulse" }
      ]
    }),
    logic_sequence: (id, family, accent) => ({
      accent,
      parts: [
        { id: "button", type: "button", x: 108, y: 352, scale: 0.82, motion: "press" },
        { id: "flow", type: "decisionFlow", x: 286, y: 280, scale: 0.95, motion: "sequence" },
        { id: "timer", type: "timerBoard", x: 430, y: 394, scale: 0.78, motion: "sequence" },
        { id: "indicator", type: "ledIndicator", x: 746, y: 328, scale: 0.96, motion: "blink" }
      ],
      connections: [
        { from: "button.output", to: "flow.trigger", kind: "signal", motion: "pulse" },
        { from: "flow.output", to: "timer.input", kind: "logic", motion: "pulse" },
        { from: "timer.output", to: "indicator.input", kind: "signal", motion: "pulse" }
      ]
    }),
    debug_test: (id, family, accent) => ({
      accent,
      parts: [
        { id: "meter", type: "multimeter", x: 124, y: 276, scale: 0.86, motion: "pulse" },
        { id: "leads", type: "testLeads", x: 306, y: 372, scale: 1, motion: "pulse" },
        { id: "prototype", type: "prototypeBody", x: 556, y: 326, scale: 0.98, motion: "pulse" },
        { id: "magnifier", type: "magnifier", x: 702, y: 214, scale: 0.72, motion: "scan" },
        { id: "checklist", type: "checklist", x: 322, y: 210, scale: 0.78, motion: "sequence" }
      ],
      connections: [
        { from: "meter.leadPositive", to: "leads.positive", kind: "test", motion: "pulse" },
        { from: "meter.leadNegative", to: "leads.negative", kind: "test" },
        { from: "leads.probePositive", to: "prototype.testPoint", kind: "test", motion: "pulse" },
        { from: "magnifier.focus", to: "prototype.testPoint", kind: "focus", motion: "pulse" }
      ]
    }),
    material_build: (id, family, accent) => ({
      accent,
      parts: [
        { id: "template", type: "template", x: 142, y: 286, scale: 1, motion: "pulse" },
        { id: "panel", type: "cardboardPanel", x: 388, y: 326, scale: 1.08 },
        { id: "sample", type: "materialSwatch", x: 638, y: 320, scale: 1.05, motion: "pulse" },
        { id: "hinge", type: "hinge", x: 494, y: 246, scale: 0.78, motion: "swing" }
      ],
      connections: [
        { from: "template.mark", to: "panel.tab", kind: "mark", motion: "pulse" },
        { from: "sample.join", to: "panel.tab", kind: "join", motion: "pulse" },
        { from: "hinge.panelA", to: "panel.hingeEdge", kind: "structure" }
      ]
    }),
    design_iterate: (id, family, accent) => ({
      accent,
      parts: [
        { id: "before", type: "prototypeBody", x: 124, y: 330, scale: 0.86, motion: "wobble" },
        { id: "checklist", type: "checklist", x: 406, y: 274, scale: 0.9, motion: "sequence" },
        { id: "sample", type: "materialSwatch", x: 440, y: 426, scale: 0.78, motion: "pulse" },
        { id: "after", type: "prototypeBody", x: 648, y: 322, scale: 1, motion: "pulse" }
      ],
      connections: [
        { from: "before.output", to: "checklist.firstItem", kind: "evidence", motion: "pulse" },
        { from: "checklist.lastItem", to: "after.input", kind: "evidence", motion: "pulse" },
        { from: "sample.sample", to: "after.testPoint", kind: "material", motion: "pulse" }
      ]
    })
  };

  const makeScene = (id, family, template) => {
    const accent = familyAccents[family];
    const kit = sceneKits[template](id, family, accent);

    return {
      id,
      family,
      template,
      accent: kit.accent,
      parts: [...kit.parts, ...cuePartsFor(id, accent)],
      connections: kit.connections
    };
  };

  const cards = {};

  Object.entries(familyCards).forEach(([family, ids]) => {
    ids.forEach((id, index) => {
      cards[id] = makeScene(id, family, familyTemplates[family][index]);
    });
  });

  window.INVENTION_CLUB_POWER_CARD_SCENES = {
    version: 1,
    viewBox: { width: 1000, height: 750 },
    parts: partLibrary,
    cueAssets,
    animationTemplates,
    cards
  };
})();
