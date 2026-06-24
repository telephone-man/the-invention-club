const header = document.querySelector("[data-site-header]");
const menuButton = document.querySelector(".menu-button");
const navLinks = document.querySelectorAll(".site-nav a");
const interestForm = document.querySelector("#interest-form");
const formNote = document.querySelector("#form-note");
const scrollSpinLoops = document.querySelectorAll("[data-scroll-spin]");
const curriculumData = window.INVENTION_CLUB_CURRICULUM;
const powerCardSceneData = window.INVENTION_CLUB_POWER_CARD_SCENES;
const familyButtons = document.querySelectorAll("[data-family]");
const levelButtons = document.querySelectorAll("[data-level]");
const powerCardResults = document.querySelector("#power-card-results");

if (header && menuButton) {
  menuButton.addEventListener("click", () => {
    const isOpen = header.classList.toggle("is-open");
    menuButton.setAttribute("aria-expanded", String(isOpen));
  });

  navLinks.forEach((link) => {
    link.addEventListener("click", () => {
      header.classList.remove("is-open");
      menuButton.setAttribute("aria-expanded", "false");
    });
  });
}

if (interestForm && formNote) {
  interestForm.addEventListener("submit", (event) => {
    event.preventDefault();
    formNote.textContent = "This page does not send details directly. Connect it to the chosen registration route to collect submissions.";
    formNote.classList.add("is-active");
  });
}

if (scrollSpinLoops.length) {
  const reducedMotionQuery = window.matchMedia("(prefers-reduced-motion: reduce)");
  const motionOverride = new URLSearchParams(window.location.search).get("motion") === "on";
  const maxLoopRotation = 720;
  let spinFrame = null;

  const getLoopProgress = (loop) => {
    const panel = loop.closest(".make-loop-panel") || loop;
    const rect = panel.getBoundingClientRect();
    const viewportHeight = window.innerHeight || document.documentElement.clientHeight;
    const start = viewportHeight * 0.92;
    const end = viewportHeight * 0.18;

    return Math.min(1, Math.max(0, (start - rect.top) / (start - end)));
  };

  const updateLoopSpin = () => {
    spinFrame = null;

    scrollSpinLoops.forEach((loop) => {
      if (reducedMotionQuery.matches && !motionOverride) {
        loop.style.setProperty("--loop-rotation", "0deg");
        return;
      }

      const progress = getLoopProgress(loop);

      loop.style.setProperty("--loop-rotation", `${Math.round(progress * maxLoopRotation)}deg`);
    });
  };

  const requestLoopSpinUpdate = () => {
    if (spinFrame === null) {
      spinFrame = window.requestAnimationFrame(updateLoopSpin);
    }
  };

  window.addEventListener("scroll", requestLoopSpinUpdate, { passive: true });
  window.addEventListener("resize", requestLoopSpinUpdate);
  if (typeof reducedMotionQuery.addEventListener === "function") {
    reducedMotionQuery.addEventListener("change", requestLoopSpinUpdate);
  } else if (typeof reducedMotionQuery.addListener === "function") {
    reducedMotionQuery.addListener(requestLoopSpinUpdate);
  }
  updateLoopSpin();
}

if (curriculumData && powerCardResults) {
  const familiesById = new Map(curriculumData.families.map((family) => [family.id, family]));
  const powerCardsById = new Map(curriculumData.powerCards.map((card) => [card.id, card]));
  const powerCardScenes = powerCardSceneData?.cards || {};
  const powerCardParts = powerCardSceneData?.parts || {};
  const powerCardCueAssets = powerCardSceneData?.cueAssets || {};
  const svgNamespace = "http://www.w3.org/2000/svg";
  const reducedPowerMotionQuery =
    typeof window.matchMedia === "function" ? window.matchMedia("(prefers-reduced-motion: reduce)") : null;
  let powerCardAnimationObserver = null;
  const initialCardParams = new URLSearchParams(window.location.search);
  let selectedFamilyId = null;
  let selectedLevel = null;

  const copyOverrides = {
    r_mov_01: {
      title: "Meet things that move",
      mission: "Find the part that makes something move. Try a motor, a servo and a push-pull part.",
      earned: "You can point to what moves and describe how it moves."
    },
    r_ctl_01: {
      title: "Meet ways to control things",
      mission: "Try buttons, switches, knobs and joysticks. Notice what a person does to each one.",
      earned: "You can sort controls by press, toggle, turn or direction."
    },
    r_sen_01: {
      title: "Meet things that notice",
      mission: "Try sensors that notice light, tilt, distance or touch. Work out what changes around them.",
      earned: "You can match each sensor to the thing it notices."
    },
    r_str_01: {
      title: "Meet strong joins and shapes",
      mission: "Look at beams, joints and loads. Find the parts that help a build stay steady.",
      earned: "You can point to beams, joints and places where weight pushes or pulls."
    },
    r_pow_01: {
      title: "Meet safe power",
      mission: "Look at cells, packs and polarity marks. Find the safe way round before anything is connected.",
      earned: "You can show positive and negative ends and name one safety limit."
    },
    r_mat_01: {
      title: "Compare making materials",
      mission: "Bend, weigh and feel different materials. Choose words for what each one is good at.",
      earned: "You can sort materials by one useful property."
    },
    r_log_01: {
      title: "Meet events and actions",
      mission: "Put event and action cards in order. Work out what starts something and what happens next.",
      earned: "You can separate the trigger, the action and the order of steps."
    },
    r_com_01: {
      title: "Meet messages",
      mission: "Find the sender, receiver, message and channel in a simple signal.",
      earned: "You can say who sends, who receives and what is being sent."
    },
    r_dbg_01: {
      title: "Notice what happened",
      mission: "Look at a broken model and describe what you see before guessing the cause.",
      earned: "You can name one symptom as an observation."
    },
    r_des_01: {
      title: "Meet users and limits",
      mission: "Read a challenge and work out who it is for and what limit it must respect.",
      earned: "You can name the user and one constraint."
    }
  };

  const scrollToSection = (selector) => {
    const target = document.querySelector(selector);
    if (target) {
      target.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  };

  const setSelectedState = () => {
    familyButtons.forEach((button) => {
      const isSelected = button.dataset.family === selectedFamilyId;
      button.classList.toggle("is-selected", isSelected);
      button.setAttribute("aria-current", isSelected ? "true" : "false");
    });

    levelButtons.forEach((button) => {
      const isSelected = Number(button.dataset.level) === selectedLevel;
      button.classList.toggle("is-selected", isSelected);
      button.setAttribute("aria-current", isSelected ? "true" : "false");
    });
  };

  const addText = (parent, tagName, className, text) => {
    const element = document.createElement(tagName);
    if (className) {
      element.className = className;
    }
    element.textContent = text;
    parent.append(element);
    return element;
  };

  const sentenceFromICan = (statement) => {
    const cleaned = statement.replace(/^I can\s+/i, "").replace(/\.$/, "");
    return `Try to ${cleaned.charAt(0).toLowerCase()}${cleaned.slice(1)}.`;
  };

  const formatList = (items) => items.filter(Boolean).join(", ");

  const getFriendlyTitle = (card) => copyOverrides[card.id]?.title || card.title;

  const getCardCopy = (card) => {
    const override = copyOverrides[card.id] || {};

    return {
      title: override.title || card.title,
      mission: override.mission || sentenceFromICan(card.i_can_statement),
      materials: override.materials || formatList(card.materials || []),
      earned: override.earned || card.success_condition,
      tryNext: override.tryNext || card.stretch_challenge
    };
  };

  const addCardSection = (parent, heading, body, className = "") => {
    if (!body) {
      return;
    }

    const section = document.createElement("div");
    section.className = `power-card-section${className ? ` ${className}` : ""}`;
    addText(section, "h4", "", heading);
    addText(section, "p", "", body);
    parent.append(section);
  };

  const prefersReducedPowerMotion = () => reducedPowerMotionQuery?.matches === true;

  const createSvgElement = (tagName, attributes = {}) => {
    const element = document.createElementNS(svgNamespace, tagName);
    Object.entries(attributes).forEach(([name, value]) => {
      if (value !== undefined && value !== null && value !== false) {
        element.setAttribute(name, String(value));
      }
    });
    return element;
  };

  const appendSvgElement = (parent, tagName, attributes = {}) => {
    const element = createSvgElement(tagName, attributes);
    parent.append(element);
    return element;
  };

  const classNames = (...names) => names.filter(Boolean).join(" ");

  const motionClass = (part, motion) => (part.motion === motion ? `power-card-motion-${motion}` : "");

  const pulseClass = (part) =>
    ["pulse", "sense", "waves", "sequence", "load", "scan"].includes(part.motion)
      ? `power-card-motion-${part.motion}`
      : "";

  const createStaticResultFigure = (card, copy) => {
    if (!card.result_image) {
      return null;
    }

    const figure = document.createElement("figure");
    figure.className = "power-card-result";
    const image = document.createElement("img");
    image.src = card.result_image;
    image.alt = card.result_alt || `${copy.title} result build`;
    image.loading = "lazy";
    figure.append(image);
    return figure;
  };

  const appendPowerCardDefs = (svg, prefix) => {
    const defs = appendSvgElement(svg, "defs");

    const bench = appendSvgElement(defs, "linearGradient", {
      id: `${prefix}-bench`,
      x1: "0",
      x2: "1",
      y1: "0",
      y2: "1"
    });
    appendSvgElement(bench, "stop", { offset: "0", "stop-color": "#f4dfbd" });
    appendSvgElement(bench, "stop", { offset: "1", "stop-color": "#d3a36c" });

    const paper = appendSvgElement(defs, "linearGradient", {
      id: `${prefix}-paper`,
      x1: "0",
      x2: "0",
      y1: "0",
      y2: "1"
    });
    appendSvgElement(paper, "stop", { offset: "0", "stop-color": "#fffaf0" });
    appendSvgElement(paper, "stop", { offset: "1", "stop-color": "#f2e4cf" });

    const metal = appendSvgElement(defs, "linearGradient", {
      id: `${prefix}-metal`,
      x1: "0",
      x2: "1"
    });
    appendSvgElement(metal, "stop", { offset: "0", "stop-color": "#dce5e6" });
    appendSvgElement(metal, "stop", { offset: "0.5", "stop-color": "#9eaeb2" });
    appendSvgElement(metal, "stop", { offset: "1", "stop-color": "#eef4f4" });

    const shadow = appendSvgElement(defs, "filter", {
      id: `${prefix}-shadow`,
      x: "-20%",
      y: "-20%",
      width: "140%",
      height: "150%"
    });
    appendSvgElement(shadow, "feDropShadow", {
      dx: "10",
      dy: "12",
      stdDeviation: "5",
      "flood-color": "#24211f",
      "flood-opacity": "0.22"
    });

    const grain = appendSvgElement(defs, "pattern", {
      id: `${prefix}-grain`,
      width: "42",
      height: "42",
      patternUnits: "userSpaceOnUse"
    });
    appendSvgElement(grain, "path", {
      d: "M0 12h42M18 0v42",
      stroke: "#9b6e3f",
      "stroke-width": "2",
      opacity: "0.08"
    });
  };

  const appendWorkbenchBackground = (svg, scene, prefix) => {
    appendSvgElement(svg, "rect", { width: "1000", height: "750", fill: `url(#${prefix}-bench)` });
    appendSvgElement(svg, "rect", { width: "1000", height: "750", fill: `url(#${prefix}-grain)` });
    appendSvgElement(svg, "circle", { cx: "190", cy: "112", r: "42", fill: scene.accent, opacity: "0.16" });
    appendSvgElement(svg, "circle", { cx: "620", cy: "134", r: "32", fill: "#f4be38", opacity: "0.22" });
    appendSvgElement(svg, "path", {
      d: "M76 594c194 50 424 52 846 8",
      stroke: "#7a5633",
      "stroke-width": "18",
      "stroke-linecap": "round",
      opacity: "0.12"
    });
    appendSvgElement(svg, "rect", {
      x: "86",
      y: "170",
      width: "828",
      height: "388",
      rx: "18",
      fill: "#e7cfad",
      filter: `url(#${prefix}-shadow)`
    });
    appendSvgElement(svg, "path", {
      d: "M112 198h776",
      stroke: "#b77f46",
      "stroke-width": "3",
      "stroke-linecap": "round",
      opacity: "0.28"
    });
    appendSvgElement(svg, "path", {
      d: "M108 528h784",
      stroke: "#8f6238",
      "stroke-width": "4",
      "stroke-linecap": "round",
      opacity: "0.18"
    });
    appendSvgElement(svg, "rect", {
      x: "124",
      y: "205",
      width: "752",
      height: "312",
      rx: "22",
      fill: `url(#${prefix}-paper)`,
      opacity: "0.66"
    });
  };

  const appendSpokes = (parent, cx, cy, radius, attributes = {}) => {
    appendSvgElement(parent, "path", {
      d: `M${cx} ${cy - radius}v${radius * 2}M${cx - radius} ${cy}h${radius * 2}M${cx - radius * 0.72} ${
        cy - radius * 0.72
      }l${radius * 1.44} ${radius * 1.44}M${cx + radius * 0.72} ${cy - radius * 0.72}l${-radius * 1.44} ${
        radius * 1.44
      }`,
      stroke: attributes.stroke || "#24211f",
      "stroke-width": attributes["stroke-width"] || "8",
      "stroke-linecap": "round",
      opacity: attributes.opacity || "0.62"
    });
  };

  const appendMiniGear = (parent, cx, cy, radius, accent) => {
    appendSvgElement(parent, "circle", {
      cx,
      cy,
      r: radius,
      fill: accent,
      stroke: "#24211f",
      "stroke-width": "6"
    });
    appendSpokes(parent, cx, cy, radius * 0.62, { "stroke-width": "5" });
    appendSvgElement(parent, "circle", {
      cx,
      cy,
      r: radius * 0.26,
      fill: "#fffaf0",
      stroke: "#24211f",
      "stroke-width": "5"
    });
  };

  const appendCueIcon = (parent, part, scene, prefix) => {
    const asset = powerCardCueAssets[part.variant] || {};
    const kind = asset.kind || "sample";
    const icon = appendSvgElement(parent, "g", {
      class: classNames(part.motion ? `power-card-motion-${part.motion}` : ""),
      transform: "translate(18 16)"
    });
    const accent = part.accent || scene.accent;

    if (["gear", "mechanism"].includes(kind)) {
      appendMiniGear(icon, 48, 50, 28, accent);
      appendMiniGear(icon, 92, 54, 22, "#f4be38");
      return;
    }

    if (kind === "motor") {
      appendSvgElement(icon, "rect", { x: "56", y: "34", width: "68", height: "42", rx: "10", fill: "#b9c4c8", stroke: "#24211f", "stroke-width": "6" });
      appendMiniGear(icon, 48, 55, 27, accent);
      appendSvgElement(icon, "path", { d: "M122 48c18 0 28 8 38 20", stroke: "#d54a3a", "stroke-width": "6", fill: "none", "stroke-linecap": "round" });
      return;
    }

    if (kind === "servo") {
      appendSvgElement(icon, "rect", { x: "20", y: "36", width: "84", height: "48", rx: "10", fill: "#315eaa", stroke: "#24211f", "stroke-width": "6" });
      appendSvgElement(icon, "circle", { cx: "76", cy: "46", r: "14", fill: accent, stroke: "#24211f", "stroke-width": "5" });
      appendSvgElement(icon, "path", { d: "M76 46L132 24", stroke: "#24211f", "stroke-width": "8", "stroke-linecap": "round" });
      appendSvgElement(icon, "circle", { cx: "132", cy: "24", r: "10", fill: "#fffaf0", stroke: "#24211f", "stroke-width": "4" });
      return;
    }

    if (kind === "solenoid") {
      appendSvgElement(icon, "path", { d: "M28 58h26c0-28 40-28 40 0s40 28 40 0h24", stroke: accent, "stroke-width": "9", fill: "none", "stroke-linecap": "round" });
      appendSvgElement(icon, "path", { d: "M18 84h126", stroke: "#24211f", "stroke-width": "8", "stroke-linecap": "round" });
      appendSvgElement(icon, "rect", { x: "116", y: "44", width: "38", height: "24", rx: "8", fill: "#d9d0bf", stroke: "#24211f", "stroke-width": "5" });
      return;
    }

    if (kind === "rubber") {
      appendSvgElement(icon, "ellipse", { cx: "76", cy: "58", rx: "58", ry: "26", fill: "none", stroke: accent, "stroke-width": "12" });
      appendSvgElement(icon, "circle", { cx: "36", cy: "58", r: "13", fill: "#fffaf0", stroke: "#24211f", "stroke-width": "5" });
      appendSvgElement(icon, "circle", { cx: "116", cy: "58", r: "13", fill: "#fffaf0", stroke: "#24211f", "stroke-width": "5" });
      return;
    }

    if (kind === "cam") {
      appendSvgElement(icon, "ellipse", { cx: "62", cy: "58", rx: "34", ry: "25", fill: accent, stroke: "#24211f", "stroke-width": "7" });
      appendSvgElement(icon, "circle", { cx: "72", cy: "52", r: "9", fill: "#fffaf0", stroke: "#24211f", "stroke-width": "4" });
      appendSvgElement(icon, "path", { d: "M96 52l44 46h-72", fill: "#f0d9ad", stroke: "#24211f", "stroke-width": "6", "stroke-linejoin": "round" });
      return;
    }

    if (kind === "controls") {
      appendSvgElement(icon, "circle", { cx: "36", cy: "52", r: "22", fill: accent, stroke: "#24211f", "stroke-width": "6" });
      appendSvgElement(icon, "path", { d: "M72 68L122 38", stroke: "#24211f", "stroke-width": "9", "stroke-linecap": "round" });
      appendSvgElement(icon, "circle", { cx: "122", cy: "38", r: "16", fill: "#f4be38", stroke: "#24211f", "stroke-width": "5" });
      return;
    }

    if (["button", "press"].includes(kind)) {
      appendSvgElement(icon, "rect", { x: "30", y: "52", width: "92", height: "36", rx: "10", fill: "#315eaa", stroke: "#24211f", "stroke-width": "6" });
      appendSvgElement(icon, "circle", { cx: "76", cy: "48", r: "30", fill: accent, stroke: "#24211f", "stroke-width": "7" });
      return;
    }

    if (kind === "knob") {
      appendSvgElement(icon, "circle", { cx: "76", cy: "58", r: "42", fill: accent, stroke: "#24211f", "stroke-width": "7" });
      appendSvgElement(icon, "path", { d: "M76 58L76 24", stroke: "#24211f", "stroke-width": "7", "stroke-linecap": "round" });
      appendSvgElement(icon, "path", { d: "M28 98h96", stroke: "#24211f", "stroke-width": "6", "stroke-linecap": "round", opacity: "0.35" });
      return;
    }

    if (kind === "joystick") {
      appendSvgElement(icon, "rect", { x: "28", y: "62", width: "102", height: "36", rx: "12", fill: "#d9d0bf", stroke: "#24211f", "stroke-width": "6" });
      appendSvgElement(icon, "path", { d: "M76 70L104 22", stroke: "#24211f", "stroke-width": "11", "stroke-linecap": "round" });
      appendSvgElement(icon, "circle", { cx: "112", cy: "16", r: "20", fill: accent, stroke: "#24211f", "stroke-width": "6" });
      return;
    }

    if (["display", "counter", "command"].includes(kind)) {
      appendSvgElement(icon, "rect", { x: "22", y: "28", width: "118", height: "70", rx: "12", fill: "#315eaa", stroke: "#24211f", "stroke-width": "6" });
      appendSvgElement(icon, "rect", { x: "42", y: "44", width: "78", height: "34", rx: "7", fill: "#dbe8f0", stroke: "#24211f", "stroke-width": "5" });
      appendSvgElement(icon, "path", { d: "M58 62h44M88 48l20 14-20 14", stroke: accent, "stroke-width": "6", fill: "none", "stroke-linecap": "round", "stroke-linejoin": "round" });
      return;
    }

    if (kind === "panel") {
      appendSvgElement(icon, "rect", { x: "20", y: "26", width: "124", height: "82", rx: "12", fill: "#f0d9ad", stroke: "#24211f", "stroke-width": "6" });
      appendSvgElement(icon, "circle", { cx: "52", cy: "58", r: "18", fill: accent, stroke: "#24211f", "stroke-width": "5" });
      appendSvgElement(icon, "circle", { cx: "100", cy: "58", r: "18", fill: "#f4be38", stroke: "#24211f", "stroke-width": "5" });
      appendSvgElement(icon, "path", { d: "M46 92h66", stroke: "#24211f", "stroke-width": "6", "stroke-linecap": "round" });
      return;
    }

    if (["sensorSet", "lightSensor", "distanceSensor", "tiltSensor", "threshold"].includes(kind)) {
      appendSvgElement(icon, "rect", { x: "24", y: "34", width: "96", height: "56", rx: "12", fill: "#2d6f78", stroke: "#24211f", "stroke-width": "6" });
      appendSvgElement(icon, "circle", { cx: "58", cy: "62", r: "18", fill: "#fffaf0", stroke: "#24211f", "stroke-width": "5" });
      appendSvgElement(icon, "circle", { cx: "58", cy: "62", r: "7", fill: accent });
      appendSvgElement(icon, "path", { d: "M116 42c26 8 42 22 52 46M122 64c20 4 32 12 42 26", stroke: accent, "stroke-width": "6", fill: "none", "stroke-linecap": "round" });
      return;
    }

    if (["calibration", "chart", "noisy"].includes(kind)) {
      appendSvgElement(icon, "rect", { x: "20", y: "20", width: "126", height: "88", rx: "12", fill: "#fffaf0", stroke: "#24211f", "stroke-width": "6" });
      appendSvgElement(icon, "path", {
        d: kind === "noisy" ? "M34 76c18-44 34 44 52 0s34 44 52 0" : "M34 82c30-2 44-40 64-42s24 28 42 22",
        stroke: accent,
        "stroke-width": "8",
        fill: "none",
        "stroke-linecap": "round"
      });
      appendSvgElement(icon, "path", { d: "M34 96h94M34 32v64", stroke: "#24211f", "stroke-width": "5", "stroke-linecap": "round", opacity: "0.45" });
      return;
    }

    if (["structure", "truss", "tower", "brace", "frame"].includes(kind)) {
      appendSvgElement(icon, "path", { d: "M24 92L76 28l60 64Z", fill: "#f0d9ad", stroke: "#24211f", "stroke-width": "7", "stroke-linejoin": "round" });
      appendSvgElement(icon, "path", { d: "M76 28v64M24 92h112M24 92l112 0M46 66h62", stroke: accent, "stroke-width": "7", "stroke-linecap": "round" });
      return;
    }

    if (kind === "hinge") {
      appendSvgElement(icon, "rect", { x: "18", y: "52", width: "70", height: "42", rx: "8", fill: "#f0d9ad", stroke: "#24211f", "stroke-width": "6" });
      appendSvgElement(icon, "path", { d: "M78 72L142 36", stroke: accent, "stroke-width": "16", "stroke-linecap": "round" });
      appendSvgElement(icon, "circle", { cx: "78", cy: "72", r: "15", fill: "#fffaf0", stroke: "#24211f", "stroke-width": "5" });
      return;
    }

    if (["chassis", "mount"].includes(kind)) {
      appendSvgElement(icon, "rect", { x: "22", y: "50", width: "118", height: "42", rx: "12", fill: "#c77c38", stroke: "#24211f", "stroke-width": "6" });
      appendSvgElement(icon, "circle", { cx: "52", cy: "98", r: "16", fill: "#24211f" });
      appendSvgElement(icon, "circle", { cx: "112", cy: "98", r: "16", fill: "#24211f" });
      appendSvgElement(icon, "rect", { x: "78", y: "24", width: "42", height: "34", rx: "8", fill: accent, stroke: "#24211f", "stroke-width": "5" });
      return;
    }

    if (["power", "cell", "batteryChoice", "batteryLoad"].includes(kind)) {
      appendSvgElement(icon, "rect", { x: "22", y: "38", width: "116", height: "54", rx: "10", fill: "#2b2f34", stroke: "#24211f", "stroke-width": "6" });
      appendSvgElement(icon, "rect", { x: "38", y: "50", width: "36", height: "30", rx: "6", fill: accent });
      appendSvgElement(icon, "rect", { x: "82", y: "50", width: "36", height: "30", rx: "6", fill: "#f0d9ad" });
      appendSvgElement(icon, "path", { d: "M50 65h14M57 58v14M92 65h14", stroke: "#24211f", "stroke-width": "5", "stroke-linecap": "round" });
      return;
    }

    if (kind === "led") {
      appendSvgElement(icon, "rect", { x: "24", y: "44", width: "116", height: "38", rx: "12", fill: "#2b2f34", stroke: "#24211f", "stroke-width": "6" });
      [44, 74, 104].forEach((x) => appendSvgElement(icon, "circle", { cx: x, cy: "63", r: "11", fill: accent, stroke: "#24211f", "stroke-width": "4" }));
      appendSvgElement(icon, "path", { d: "M138 63c20 2 32 10 42 24", stroke: "#d54a3a", "stroke-width": "6", fill: "none", "stroke-linecap": "round" });
      return;
    }

    if (["meter", "voltageDrop"].includes(kind)) {
      appendSvgElement(icon, "rect", { x: "32", y: "18", width: "88", height: "96", rx: "14", fill: "#2b2f34", stroke: "#24211f", "stroke-width": "6" });
      appendSvgElement(icon, "rect", { x: "46", y: "34", width: "58", height: "28", rx: "5", fill: "#dbe8f0", stroke: "#24211f", "stroke-width": "4" });
      appendSvgElement(icon, "path", { d: "M54 78h44M62 96h28", stroke: accent, "stroke-width": "6", "stroke-linecap": "round" });
      return;
    }

    if (["fuse", "commonGround"].includes(kind)) {
      appendSvgElement(icon, "rect", { x: "24", y: "44", width: "116", height: "50", rx: "12", fill: "#fffaf0", stroke: "#24211f", "stroke-width": "6" });
      appendSvgElement(icon, "path", { d: kind === "fuse" ? "M42 70h22l12-18 14 36 12-18h22" : "M46 62h70M58 78h46M70 94h22", stroke: accent, "stroke-width": "7", fill: "none", "stroke-linecap": "round", "stroke-linejoin": "round" });
      return;
    }

    if (["material", "cut", "hole", "template", "tabs", "enclosure", "fastener"].includes(kind)) {
      appendSvgElement(icon, "rect", { x: "24", y: "24", width: "108", height: "78", rx: "12", fill: "#f0d9ad", stroke: "#24211f", "stroke-width": "6" });
      if (kind === "cut") {
        appendSvgElement(icon, "path", { d: "M50 88L118 30M50 30l68 58", stroke: accent, "stroke-width": "7", "stroke-linecap": "round" });
      } else if (kind === "hole") {
        [54, 80, 106].forEach((x) => appendSvgElement(icon, "circle", { cx: x, cy: "64", r: "10", fill: "#fffaf0", stroke: "#24211f", "stroke-width": "5" }));
      } else if (kind === "enclosure") {
        appendSvgElement(icon, "path", { d: "M38 48h80v42H38ZM52 48l16-18h66v42l-16 18", fill: "none", stroke: accent, "stroke-width": "7", "stroke-linejoin": "round" });
      } else {
        appendSvgElement(icon, "path", { d: "M44 44h70M44 66h92M44 88h48", stroke: accent, "stroke-width": "7", "stroke-linecap": "round" });
      }
      return;
    }

    if (["logic", "sequence", "ifThen", "timer", "state", "flowchart"].includes(kind)) {
      appendSvgElement(icon, "rect", { x: "16", y: "44", width: "42", height: "36", rx: "8", fill: "#fffaf0", stroke: "#24211f", "stroke-width": "5" });
      appendSvgElement(icon, "path", { d: "M82 32l34 30-34 30-34-30Z", fill: accent, stroke: "#24211f", "stroke-width": "5" });
      appendSvgElement(icon, "rect", { x: "108", y: "44", width: "42", height: "36", rx: "8", fill: "#fffaf0", stroke: "#24211f", "stroke-width": "5" });
      appendSvgElement(icon, "path", { d: "M58 62h18M116 62h18", stroke: "#24211f", "stroke-width": "6", "stroke-linecap": "round" });
      return;
    }

    if (["radio", "pair", "message", "remote", "senders", "range", "buzzerFlag"].includes(kind)) {
      appendSvgElement(icon, "rect", { x: "22", y: "54", width: "54", height: "42", rx: "9", fill: "#315eaa", stroke: "#24211f", "stroke-width": "5" });
      appendSvgElement(icon, "rect", { x: "104", y: "54", width: "54", height: "42", rx: "9", fill: "#f0d9ad", stroke: "#24211f", "stroke-width": "5" });
      appendSvgElement(icon, "path", { d: "M78 36c18 6 30 18 36 36M92 18c32 14 54 36 66 70", stroke: accent, "stroke-width": "7", fill: "none", "stroke-linecap": "round" });
      if (kind === "buzzerFlag") {
        appendSvgElement(icon, "path", { d: "M42 34v-22h42l-12 11 12 11Z", fill: accent, stroke: "#24211f", "stroke-width": "5", "stroke-linejoin": "round" });
      }
      return;
    }

    if (["debug", "circuit", "subsystem", "repair", "testRig", "fault"].includes(kind)) {
      appendSvgElement(icon, "circle", { cx: "54", cy: "54", r: "32", fill: "#dbe8f0", opacity: "0.72", stroke: "#24211f", "stroke-width": "7" });
      appendSvgElement(icon, "path", { d: "M78 78l48 48", stroke: accent, "stroke-width": "13", "stroke-linecap": "round" });
      appendSvgElement(icon, "rect", { x: "96", y: "32", width: "48", height: "42", rx: "8", fill: "#f0d9ad", stroke: "#24211f", "stroke-width": "5" });
      appendSvgElement(icon, "path", { d: "M108 48h24M108 62h18", stroke: "#24211f", "stroke-width": "5", "stroke-linecap": "round" });
      return;
    }

    if (["user", "sketch", "constraint", "criteria", "taskBoard", "feedback", "space", "challenge"].includes(kind)) {
      appendSvgElement(icon, "rect", { x: "22", y: "18", width: "118", height: "90", rx: "12", fill: "#fffaf0", stroke: "#24211f", "stroke-width": "6" });
      if (kind === "user") {
        appendSvgElement(icon, "circle", { cx: "58", cy: "54", r: "18", fill: accent, stroke: "#24211f", "stroke-width": "5" });
        appendSvgElement(icon, "path", { d: "M36 92c10-24 34-30 54 0", fill: "none", stroke: "#24211f", "stroke-width": "6", "stroke-linecap": "round" });
      } else if (kind === "space") {
        appendSvgElement(icon, "path", { d: "M44 36h70v48H44ZM44 84l-16 18M114 84l16 18", fill: "none", stroke: accent, "stroke-width": "7", "stroke-linejoin": "round" });
      } else {
        appendSvgElement(icon, "path", { d: "M42 44h74M42 66h52M42 88h82", stroke: "#24211f", "stroke-width": "6", "stroke-linecap": "round", opacity: "0.45" });
        appendSvgElement(icon, "path", { d: "M116 34l20 18-20 18", fill: "none", stroke: accent, "stroke-width": "7", "stroke-linecap": "round", "stroke-linejoin": "round" });
      }
      return;
    }

    appendSvgElement(icon, "rect", { x: "24", y: "24", width: "108", height: "78", rx: "12", fill: "#f0d9ad", stroke: "#24211f", "stroke-width": "6" });
    appendSvgElement(icon, "circle", { cx: "78", cy: "64", r: "26", fill: accent, stroke: "#24211f", "stroke-width": "6" });
  };

  const partRenderers = {
    wheel: (group, part, scene, prefix) => {
      const rotor = appendSvgElement(group, "g", { class: classNames(motionClass(part, "spin")) });
      appendSvgElement(rotor, "circle", {
        cx: "70",
        cy: "70",
        r: "68",
        fill: "#24211f",
        filter: `url(#${prefix}-shadow)`
      });
      appendSvgElement(rotor, "circle", { cx: "70", cy: "70", r: "50", fill: scene.accent });
      appendSpokes(rotor, 70, 70, 42);
      appendSvgElement(rotor, "circle", {
        cx: "70",
        cy: "70",
        r: "17",
        fill: "#d9d0bf",
        stroke: "#24211f",
        "stroke-width": "7"
      });
    },
    axle: (group) => {
      appendSvgElement(group, "path", {
        d: "M0 12h180",
        stroke: "#7d8487",
        "stroke-width": "18",
        "stroke-linecap": "round"
      });
      appendSvgElement(group, "path", {
        d: "M14 12h152",
        stroke: "#eef4f4",
        "stroke-width": "5",
        "stroke-linecap": "round",
        opacity: "0.7"
      });
    },
    motor: (group, part, scene, prefix) => {
      appendSvgElement(group, "rect", {
        x: "92",
        y: "38",
        width: "138",
        height: "94",
        rx: "16",
        fill: "#b9c4c8",
        filter: `url(#${prefix}-shadow)`
      });
      appendSvgElement(group, "rect", { x: "116", y: "60", width: "86", height: "50", rx: "8", fill: `url(#${prefix}-metal)` });
      const rotor = appendSvgElement(group, "g", { class: classNames(motionClass(part, "spin")) });
      appendSvgElement(rotor, "circle", { cx: "62", cy: "72", r: "56", fill: "#24211f", filter: `url(#${prefix}-shadow)` });
      appendSvgElement(rotor, "circle", { cx: "62", cy: "72", r: "39", fill: scene.accent });
      appendSpokes(rotor, 62, 72, 32, { "stroke-width": "7" });
      appendSvgElement(rotor, "circle", { cx: "62", cy: "72", r: "13", fill: "#fffaf0", stroke: "#24211f", "stroke-width": "6" });
      appendSvgElement(group, "path", { d: "M222 56c26 4 38 16 54 33", stroke: "#d54a3a", "stroke-width": "8", fill: "none", "stroke-linecap": "round" });
      appendSvgElement(group, "path", { d: "M222 92c30 3 42 15 58 34", stroke: "#24211f", "stroke-width": "8", fill: "none", "stroke-linecap": "round" });
    },
    servo: (group, part, scene, prefix) => {
      appendSvgElement(group, "rect", {
        x: "6",
        y: "38",
        width: "150",
        height: "86",
        rx: "16",
        fill: "#315eaa",
        filter: `url(#${prefix}-shadow)`
      });
      appendSvgElement(group, "rect", { x: "30", y: "58", width: "82", height: "34", rx: "8", fill: "#dbe8f0", opacity: "0.92" });
      appendSvgElement(group, "circle", { cx: "88", cy: "55", r: "20", fill: scene.accent, stroke: "#24211f", "stroke-width": "7" });
      const horn = appendSvgElement(group, "g", { class: classNames(motionClass(part, "swing")) });
      appendSvgElement(horn, "path", { d: "M88 55L178 12", stroke: "#24211f", "stroke-width": "12", "stroke-linecap": "round" });
      appendSvgElement(horn, "circle", { cx: "178", cy: "12", r: "16", fill: "#fffaf0", stroke: "#24211f", "stroke-width": "6" });
      appendSvgElement(group, "path", { d: "M0 100c-24 4-36 12-46 24", stroke: "#d54a3a", "stroke-width": "7", fill: "none", "stroke-linecap": "round" });
      appendSvgElement(group, "path", { d: "M160 100c24 2 38 10 52 24", stroke: "#24211f", "stroke-width": "7", fill: "none", "stroke-linecap": "round" });
    },
    arm: (group, part, scene) => {
      const arm = appendSvgElement(group, "g", { class: classNames(motionClass(part, "swing")) });
      appendSvgElement(arm, "path", { d: "M10 25L200 25", stroke: "#c77c38", "stroke-width": "24", "stroke-linecap": "round" });
      appendSvgElement(arm, "circle", { cx: "10", cy: "25", r: "16", fill: "#fffaf0", stroke: "#24211f", "stroke-width": "6" });
      appendSvgElement(arm, "circle", { cx: "200", cy: "25", r: "16", fill: scene.accent, stroke: "#24211f", "stroke-width": "6" });
    },
    linkage: (group, part) => {
      const link = appendSvgElement(group, "g", { class: classNames(motionClass(part, "swing")) });
      appendSvgElement(link, "path", { d: "M0 40C54 2 132 2 200 40", stroke: "#d9d0bf", "stroke-width": "20", "stroke-linecap": "round", fill: "none" });
      appendSvgElement(link, "path", { d: "M0 40C54 2 132 2 200 40", stroke: "#24211f", "stroke-width": "5", "stroke-linecap": "round", fill: "none", opacity: "0.85" });
      appendSvgElement(link, "circle", { cx: "0", cy: "40", r: "14", fill: "#fffaf0", stroke: "#24211f", "stroke-width": "6" });
      appendSvgElement(link, "circle", { cx: "200", cy: "40", r: "14", fill: "#fffaf0", stroke: "#24211f", "stroke-width": "6" });
    },
    batteryPack: (group, part, scene, prefix) => {
      appendSvgElement(group, "rect", { x: "0", y: "18", width: "190", height: "92", rx: "14", fill: "#2b2f34", filter: `url(#${prefix}-shadow)` });
      appendSvgElement(group, "rect", { x: "176", y: "48", width: "20", height: "32", rx: "4", fill: "#2b2f34" });
      appendSvgElement(group, "rect", { x: "20", y: "34", width: "60", height: "58", rx: "9", fill: scene.accent });
      appendSvgElement(group, "rect", { x: "90", y: "34", width: "60", height: "58", rx: "9", fill: "#f0d9ad" });
      appendSvgElement(group, "path", { d: "M34 63h32M50 47v32", stroke: "#24211f", "stroke-width": "6", "stroke-linecap": "round" });
      appendSvgElement(group, "path", { d: "M104 63h32", stroke: "#24211f", "stroke-width": "6", "stroke-linecap": "round" });
    },
    button: (group, part, scene, prefix) => {
      appendSvgElement(group, "rect", { x: "0", y: "34", width: "132", height: "76", rx: "15", fill: "#315eaa", filter: `url(#${prefix}-shadow)` });
      const cap = appendSvgElement(group, "g", { class: classNames(motionClass(part, "press")) });
      appendSvgElement(cap, "circle", { cx: "66", cy: "36", r: "38", fill: scene.accent, stroke: "#24211f", "stroke-width": "8" });
      appendSvgElement(cap, "ellipse", { cx: "58", cy: "26", rx: "18", ry: "9", fill: "#fffaf0", opacity: "0.42" });
    },
    switch: (group, part, scene, prefix) => {
      appendSvgElement(group, "rect", { x: "0", y: "22", width: "150", height: "72", rx: "14", fill: "#d9d0bf", filter: `url(#${prefix}-shadow)` });
      appendSvgElement(group, "circle", { cx: "44", cy: "58", r: "20", fill: "#fffaf0", stroke: "#24211f", "stroke-width": "7" });
      const lever = appendSvgElement(group, "g", { class: classNames(motionClass(part, "press")) });
      appendSvgElement(lever, "path", { d: "M44 58L104 30", stroke: scene.accent, "stroke-width": "16", "stroke-linecap": "round" });
      appendSvgElement(lever, "circle", { cx: "104", cy: "30", r: "14", fill: "#24211f" });
    },
    knob: (group, part, scene, prefix) => {
      appendSvgElement(group, "rect", { x: "0", y: "22", width: "132", height: "96", rx: "16", fill: "#d9d0bf", filter: `url(#${prefix}-shadow)` });
      const dial = appendSvgElement(group, "g", { class: classNames(motionClass(part, "swing")) });
      appendSvgElement(dial, "circle", { cx: "66", cy: "70", r: "34", fill: scene.accent, stroke: "#24211f", "stroke-width": "8" });
      appendSvgElement(dial, "path", { d: "M66 70L66 42", stroke: "#24211f", "stroke-width": "7", "stroke-linecap": "round" });
    },
    joystick: (group, part, scene, prefix) => {
      appendSvgElement(group, "rect", { x: "0", y: "46", width: "150", height: "88", rx: "18", fill: "#d9d0bf", filter: `url(#${prefix}-shadow)` });
      const stick = appendSvgElement(group, "g", { class: classNames(motionClass(part, "swing")) });
      appendSvgElement(stick, "path", { d: "M76 74L104 22", stroke: "#24211f", "stroke-width": "16", "stroke-linecap": "round" });
      appendSvgElement(stick, "circle", { cx: "112", cy: "14", r: "24", fill: scene.accent, stroke: "#24211f", "stroke-width": "7" });
      appendSvgElement(group, "ellipse", { cx: "74", cy: "78", rx: "42", ry: "18", fill: "#24211f", opacity: "0.18" });
    },
    ledIndicator: (group, part, scene, prefix) => {
      appendSvgElement(group, "rect", { x: "6", y: "18", width: "94", height: "84", rx: "18", fill: "#d9d0bf", filter: `url(#${prefix}-shadow)` });
      appendSvgElement(group, "circle", {
        cx: "54",
        cy: "58",
        r: "31",
        fill: scene.accent,
        stroke: "#24211f",
        "stroke-width": "8",
        class: classNames(motionClass(part, "blink"))
      });
      appendSvgElement(group, "path", {
        d: "M54 10v-18M20 22L6 6M88 22l14-16",
        stroke: scene.accent,
        "stroke-width": "7",
        "stroke-linecap": "round",
        class: classNames(pulseClass(part))
      });
    },
    lightSensor: (group, part, scene, prefix) => {
      appendSvgElement(group, "rect", { x: "0", y: "22", width: "142", height: "92", rx: "16", fill: "#2d6f78", filter: `url(#${prefix}-shadow)` });
      appendSvgElement(group, "circle", { cx: "70", cy: "68", r: "30", fill: "#fffaf0", stroke: "#24211f", "stroke-width": "7" });
      appendSvgElement(group, "circle", { cx: "70", cy: "68", r: "12", fill: scene.accent });
      appendSvgElement(group, "path", {
        d: "M70 12v-26M32 24L12 4M108 24l20-20",
        stroke: scene.accent,
        "stroke-width": "8",
        "stroke-linecap": "round",
        class: classNames(motionClass(part, "sense"))
      });
    },
    distanceSensor: (group, part, scene, prefix) => {
      appendSvgElement(group, "rect", { x: "0", y: "24", width: "152", height: "92", rx: "16", fill: "#315eaa", filter: `url(#${prefix}-shadow)` });
      appendSvgElement(group, "circle", { cx: "48", cy: "68", r: "24", fill: "#fffaf0", stroke: "#24211f", "stroke-width": "7" });
      appendSvgElement(group, "circle", { cx: "104", cy: "68", r: "24", fill: "#fffaf0", stroke: "#24211f", "stroke-width": "7" });
      appendSvgElement(group, "path", {
        d: "M128 34c38 12 60 34 72 66M134 68c28 6 44 18 58 38",
        stroke: scene.accent,
        "stroke-width": "8",
        "stroke-linecap": "round",
        fill: "none",
        class: classNames(motionClass(part, "sense"))
      });
    },
    tiltSensor: (group, part, scene, prefix) => {
      appendSvgElement(group, "rect", { x: "0", y: "20", width: "150", height: "86", rx: "18", fill: "#2d6f78", filter: `url(#${prefix}-shadow)` });
      appendSvgElement(group, "rect", { x: "28", y: "46", width: "94", height: "26", rx: "13", fill: "#fffaf0", stroke: "#24211f", "stroke-width": "6" });
      appendSvgElement(group, "circle", {
        cx: "52",
        cy: "59",
        r: "13",
        fill: scene.accent,
        class: classNames(motionClass(part, "sense"), motionClass(part, "swing"))
      });
    },
    board: (group, part, scene, prefix) => {
      appendSvgElement(group, "rect", { x: "0", y: "0", width: "190", height: "120", rx: "18", fill: "#09666b", filter: `url(#${prefix}-shadow)` });
      appendSvgElement(group, "rect", { x: "36", y: "28", width: "82", height: "46", rx: "8", fill: "#f0d9ad", stroke: "#24211f", "stroke-width": "6" });
      appendSvgElement(group, "path", { d: "M18 92h154M142 28h28M142 50h28", stroke: "#fffaf0", "stroke-width": "6", "stroke-linecap": "round", opacity: "0.7" });
      appendSvgElement(group, "circle", { cx: "32", cy: "94", r: "9", fill: scene.accent, stroke: "#24211f", "stroke-width": "5" });
      appendSvgElement(group, "circle", { cx: "70", cy: "94", r: "9", fill: "#fffaf0", stroke: "#24211f", "stroke-width": "5" });
    },
    antenna: (group, part, scene, prefix) => {
      appendSvgElement(group, "rect", { x: "0", y: "48", width: "110", height: "70", rx: "14", fill: "#315eaa", filter: `url(#${prefix}-shadow)` });
      appendSvgElement(group, "path", { d: "M86 52L128 0", stroke: "#24211f", "stroke-width": "10", "stroke-linecap": "round" });
      appendSvgElement(group, "circle", { cx: "128", cy: "0", r: "10", fill: scene.accent, stroke: "#24211f", "stroke-width": "5" });
      appendSvgElement(group, "path", {
        d: "M152 12c26 14 42 36 46 66M178 -8c42 22 68 58 76 106",
        stroke: scene.accent,
        "stroke-width": "8",
        "stroke-linecap": "round",
        fill: "none",
        class: classNames(motionClass(part, "waves"))
      });
    },
    receiver: (group, part, scene, prefix) => {
      appendSvgElement(group, "rect", { x: "0", y: "24", width: "180", height: "100", rx: "18", fill: "#d9d0bf", filter: `url(#${prefix}-shadow)` });
      appendSvgElement(group, "path", { d: "M28 24L8 -18M58 24L78 -16", stroke: "#24211f", "stroke-width": "8", "stroke-linecap": "round" });
      appendSvgElement(group, "circle", { cx: "116", cy: "74", r: "28", fill: scene.accent, stroke: "#24211f", "stroke-width": "7", class: classNames(pulseClass(part)) });
    },
    beam: (group) => {
      appendSvgElement(group, "path", { d: "M0 20h220", stroke: "#c77c38", "stroke-width": "28", "stroke-linecap": "round" });
      appendSvgElement(group, "path", { d: "M18 20h184", stroke: "#fffaf0", "stroke-width": "5", "stroke-linecap": "round", opacity: "0.46" });
    },
    brace: (group, part, scene) => {
      appendSvgElement(group, "path", {
        d: "M0 100L140 0",
        stroke: scene.accent,
        "stroke-width": "20",
        "stroke-linecap": "round",
        class: classNames(pulseClass(part))
      });
      appendSvgElement(group, "circle", { cx: "0", cy: "100", r: "12", fill: "#fffaf0", stroke: "#24211f", "stroke-width": "5" });
      appendSvgElement(group, "circle", { cx: "140", cy: "0", r: "12", fill: "#fffaf0", stroke: "#24211f", "stroke-width": "5" });
    },
    hinge: (group, part, scene, prefix) => {
      appendSvgElement(group, "rect", { x: "0", y: "50", width: "140", height: "42", rx: "12", fill: "#d9d0bf", filter: `url(#${prefix}-shadow)` });
      const leaf = appendSvgElement(group, "g", { class: classNames(motionClass(part, "swing")) });
      appendSvgElement(leaf, "path", { d: "M70 70L154 34", stroke: scene.accent, "stroke-width": "20", "stroke-linecap": "round" });
      appendSvgElement(group, "circle", { cx: "70", cy: "70", r: "18", fill: "#fffaf0", stroke: "#24211f", "stroke-width": "7" });
    },
    chassis: (group, part, scene, prefix) => {
      const body = appendSvgElement(group, "g", { class: classNames(motionClass(part, "wobble")) });
      appendSvgElement(body, "rect", { x: "0", y: "42", width: "340", height: "92", rx: "18", fill: "#c77c38", filter: `url(#${prefix}-shadow)` });
      appendSvgElement(body, "path", { d: "M34 92h272M76 42l52 92M224 42l-48 92", stroke: "#24211f", "stroke-width": "8", "stroke-linecap": "round", opacity: "0.65" });
      appendSvgElement(body, "circle", { cx: "70", cy: "144", r: "28", fill: "#24211f" });
      appendSvgElement(body, "circle", { cx: "276", cy: "144", r: "28", fill: "#24211f" });
    },
    cardboardPanel: (group, part, scene, prefix) => {
      appendSvgElement(group, "rect", { x: "0", y: "18", width: "208", height: "128", rx: "18", fill: "#f0d9ad", filter: `url(#${prefix}-shadow)` });
      appendSvgElement(group, "path", { d: "M28 34v98M58 34v98M180 54l-48 48", stroke: "#9b6e3f", "stroke-width": "6", "stroke-linecap": "round", opacity: "0.45" });
      appendSvgElement(group, "circle", { cx: "180", cy: "82", r: "15", fill: scene.accent, stroke: "#24211f", "stroke-width": "6" });
    },
    template: (group, part, scene, prefix) => {
      appendSvgElement(group, "rect", { x: "0", y: "0", width: "220", height: "150", rx: "18", fill: "#fffaf0", filter: `url(#${prefix}-shadow)` });
      appendSvgElement(group, "path", { d: "M34 32h116M34 72h152M34 112h92M120 72v42", stroke: "#24211f", "stroke-width": "7", "stroke-linecap": "round", opacity: "0.58" });
      appendSvgElement(group, "circle", { cx: "120", cy: "90", r: "16", fill: scene.accent, stroke: "#24211f", "stroke-width": "6", class: classNames(pulseClass(part)) });
    },
    testLeads: (group, part) => {
      appendSvgElement(group, "path", { d: "M0 20C72 6 112 36 210 20", stroke: "#d54a3a", "stroke-width": "8", fill: "none", "stroke-linecap": "round", class: classNames(pulseClass(part)) });
      appendSvgElement(group, "path", { d: "M0 64C68 92 130 40 210 64", stroke: "#24211f", "stroke-width": "8", fill: "none", "stroke-linecap": "round" });
      appendSvgElement(group, "circle", { cx: "210", cy: "20", r: "11", fill: "#fffaf0", stroke: "#24211f", "stroke-width": "5" });
      appendSvgElement(group, "circle", { cx: "210", cy: "64", r: "11", fill: "#fffaf0", stroke: "#24211f", "stroke-width": "5" });
    },
    multimeter: (group, part, scene, prefix) => {
      appendSvgElement(group, "rect", { x: "0", y: "0", width: "130", height: "170", rx: "20", fill: "#2b2f34", filter: `url(#${prefix}-shadow)` });
      appendSvgElement(group, "rect", { x: "20", y: "22", width: "90", height: "46", rx: "8", fill: "#dbe8f0", stroke: "#24211f", "stroke-width": "5", class: classNames(pulseClass(part)) });
      appendSvgElement(group, "circle", { cx: "66", cy: "112", r: "28", fill: scene.accent, stroke: "#24211f", "stroke-width": "6" });
      appendSvgElement(group, "path", { d: "M34 160v34M72 160v34", stroke: "#24211f", "stroke-width": "8", "stroke-linecap": "round" });
    },
    magnifier: (group, part, scene) => {
      const lens = appendSvgElement(group, "g", { class: classNames(motionClass(part, "scan")) });
      appendSvgElement(lens, "circle", { cx: "72", cy: "72", r: "54", fill: "#dbe8f0", opacity: "0.72", stroke: "#24211f", "stroke-width": "9" });
      appendSvgElement(lens, "path", { d: "M110 110l58 58", stroke: scene.accent, "stroke-width": "18", "stroke-linecap": "round" });
    },
    checklist: (group, part, scene, prefix) => {
      appendSvgElement(group, "rect", { x: "0", y: "0", width: "170", height: "170", rx: "18", fill: "#fffaf0", filter: `url(#${prefix}-shadow)` });
      [42, 82, 122].forEach((y, index) => {
        appendSvgElement(group, "rect", {
          x: "24",
          y: String(y - 12),
          width: "22",
          height: "22",
          rx: "4",
          fill: index === 0 ? scene.accent : "#f0d9ad",
          stroke: "#24211f",
          "stroke-width": "5",
          class: index === 0 ? classNames(pulseClass(part)) : ""
        });
        appendSvgElement(group, "path", { d: `M62 ${y}h76`, stroke: "#24211f", "stroke-width": "7", "stroke-linecap": "round", opacity: "0.42" });
      });
    },
    decisionFlow: (group, part, scene, prefix) => {
      const sequence = appendSvgElement(group, "g", { class: classNames(motionClass(part, "sequence")) });
      [0, 180, 360].forEach((x, index) => {
        appendSvgElement(sequence, "rect", {
          x: String(x),
          y: "0",
          width: "100",
          height: "92",
          rx: "16",
          fill: index === 1 ? scene.accent : "#f0d9ad",
          stroke: "#24211f",
          "stroke-width": "7",
          filter: `url(#${prefix}-shadow)`
        });
      });
      appendSvgElement(group, "path", { d: "M104 46h68M284 46h68", stroke: "#24211f", "stroke-width": "10", "stroke-linecap": "round" });
      appendSvgElement(group, "path", { d: "M158 28l22 18-22 18M338 28l22 18-22 18", fill: "none", stroke: "#24211f", "stroke-width": "8", "stroke-linecap": "round", "stroke-linejoin": "round" });
    },
    prototypeBody: (group, part, scene, prefix) => {
      const body = appendSvgElement(group, "g", { class: classNames(motionClass(part, "wobble"), pulseClass(part)) });
      appendSvgElement(body, "path", { d: "M20 136h218l22-78L148 18 36 48Z", fill: "#f0d9ad", stroke: "#24211f", "stroke-width": "8", "stroke-linejoin": "round", filter: `url(#${prefix}-shadow)` });
      appendSvgElement(body, "circle", { cx: "86", cy: "138", r: "24", fill: "#24211f" });
      appendSvgElement(body, "circle", { cx: "202", cy: "138", r: "24", fill: "#24211f" });
      appendSvgElement(body, "circle", { cx: "130", cy: "56", r: "18", fill: scene.accent, stroke: "#24211f", "stroke-width": "6" });
    },
    fuse: (group, part, scene, prefix) => {
      appendSvgElement(group, "rect", { x: "0", y: "22", width: "132", height: "66", rx: "16", fill: "#fffaf0", stroke: "#24211f", "stroke-width": "8", filter: `url(#${prefix}-shadow)` });
      appendSvgElement(group, "path", { d: "M22 54h28l18-18 18 36 18-18h18", stroke: scene.accent, "stroke-width": "9", "stroke-linecap": "round", "stroke-linejoin": "round", fill: "none", class: classNames(pulseClass(part)) });
    },
    timerBoard: (group, part, scene, prefix) => {
      appendSvgElement(group, "rect", { x: "0", y: "0", width: "190", height: "124", rx: "18", fill: "#2f8a4b", filter: `url(#${prefix}-shadow)` });
      [36, 78, 120].forEach((x, index) => {
        appendSvgElement(group, "circle", {
          cx: String(x),
          cy: "62",
          r: "18",
          fill: index === 1 ? scene.accent : "#fffaf0",
          stroke: "#24211f",
          "stroke-width": "6",
          class: index === 1 ? classNames(motionClass(part, "sequence")) : ""
        });
      });
    },
    loadWeight: (group, part, scene, prefix) => {
      const weight = appendSvgElement(group, "g", { class: classNames(motionClass(part, "load")) });
      appendSvgElement(weight, "path", { d: "M30 28h60l28 82H2Z", fill: "#7d8487", stroke: "#24211f", "stroke-width": "8", "stroke-linejoin": "round", filter: `url(#${prefix}-shadow)` });
      appendSvgElement(weight, "path", { d: "M38 28c0-20 44-20 44 0", fill: "none", stroke: scene.accent, "stroke-width": "8", "stroke-linecap": "round" });
    },
    materialSwatch: (group, part, scene, prefix) => {
      appendSvgElement(group, "rect", { x: "0", y: "0", width: "190", height: "124", rx: "18", fill: "#f0d9ad", filter: `url(#${prefix}-shadow)` });
      appendSvgElement(group, "path", { d: "M28 26h60v72H28ZM104 26h58v72h-58Z", fill: "#fffaf0", stroke: "#24211f", "stroke-width": "6", "stroke-linejoin": "round" });
      appendSvgElement(group, "path", { d: "M34 58h46M110 44h46M110 78h46", stroke: scene.accent, "stroke-width": "7", "stroke-linecap": "round", class: classNames(pulseClass(part)) });
    },
    cueTile: (group, part, scene, prefix) => {
      appendSvgElement(group, "rect", {
        x: "0",
        y: "0",
        width: "178",
        height: "128",
        rx: "18",
        fill: "#fffaf0",
        stroke: "#24211f",
        "stroke-width": "7",
        filter: `url(#${prefix}-shadow)`
      });
      appendSvgElement(group, "rect", {
        x: "14",
        y: "14",
        width: "150",
        height: "100",
        rx: "14",
        fill: "#f0d9ad",
        opacity: "0.78"
      });
      appendCueIcon(group, part, scene, prefix);
    }
  };

  const resolveConnectorPoint = (partById, connectorRef) => {
    const [partId, connectorName] = connectorRef.split(".");
    const part = partById.get(partId);
    const connector = powerCardParts[part?.type]?.connectors?.[connectorName];

    if (!part || !connector) {
      return null;
    }

    const scale = part.scale || 1;
    return {
      x: part.x + connector.x * scale,
      y: part.y + connector.y * scale
    };
  };

  const appendConnection = (group, connection, partById) => {
    const start = resolveConnectorPoint(partById, connection.from);
    const end = resolveConnectorPoint(partById, connection.to);

    if (!start || !end) {
      return;
    }

    const midX = (start.x + end.x) / 2;
    appendSvgElement(group, "path", {
      d: `M${start.x} ${start.y}C${midX} ${start.y},${midX} ${end.y},${end.x} ${end.y}`,
      class: classNames(
        "power-card-wire",
        `power-card-wire-${connection.kind || "signal"}`,
        connection.motion ? `power-card-wire-${connection.motion}` : ""
      ),
      fill: "none"
    });
  };

  const appendPart = (group, part, scene, prefix) => {
    const renderer = partRenderers[part.type];

    if (!renderer) {
      return;
    }

    const scale = part.scale || 1;
    const transform = `translate(${part.x} ${part.y}) scale(${scale})`;
    const partGroup = appendSvgElement(group, "g", {
      class: classNames("power-card-part", `power-card-part-${part.type}`),
      transform
    });
    renderer(partGroup, part, scene, prefix);
  };

  const canRenderPowerCardScene = (scene) =>
    scene &&
    Array.isArray(scene.parts) &&
    scene.parts.length > 0 &&
    scene.parts.every((part) => powerCardParts[part.type] && partRenderers[part.type]);

  const renderPowerCardSceneSvg = (card, copy, scene) => {
    const prefix = `scene-${card.id}`;
    const svg = createSvgElement("svg", {
      class: "power-card-scene",
      viewBox: "0 0 1000 750",
      role: "img",
      "aria-labelledby": `${prefix}-title ${prefix}-desc`,
      focusable: "false"
    });

    appendPowerCardDefs(svg, prefix);
    const title = appendSvgElement(svg, "title", { id: `${prefix}-title` });
    title.textContent = `${copy.title} animated result`;
    const description = appendSvgElement(svg, "desc", { id: `${prefix}-desc` });
    description.textContent = card.result_alt || `${copy.title} result build`;

    appendWorkbenchBackground(svg, scene, prefix);

    const partById = new Map(scene.parts.map((part) => [part.id, part]));
    const connections = appendSvgElement(svg, "g", { class: "power-card-connections" });
    (scene.connections || []).forEach((connection) => appendConnection(connections, connection, partById));

    const parts = appendSvgElement(svg, "g", { class: "power-card-parts" });
    scene.parts.forEach((part) => appendPart(parts, part, scene, prefix));

    appendSvgElement(svg, "path", {
      d: "M128 604h744",
      stroke: "#24211f",
      "stroke-width": "8",
      "stroke-linecap": "round",
      opacity: "0.22"
    });

    return svg;
  };

  const updateAnimationToggle = (figure, copy) => {
    const button = figure.querySelector(".power-card-animation-toggle");
    if (!button) {
      return;
    }

    const isPaused = figure.classList.contains("is-paused");
    button.setAttribute("aria-label", `${isPaused ? "Play" : "Pause"} animation for ${copy.title}`);
    button.setAttribute("aria-pressed", String(isPaused));
  };

  const ensurePowerCardAnimationObserver = () => {
    if (powerCardAnimationObserver || typeof IntersectionObserver !== "function") {
      return powerCardAnimationObserver;
    }

    powerCardAnimationObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          entry.target.classList.toggle("is-offscreen", !entry.isIntersecting);
        });
      },
      { threshold: 0.15 }
    );

    return powerCardAnimationObserver;
  };

  const createAnimatedResultFigure = (card, copy, scene) => {
    if (prefersReducedPowerMotion() || !canRenderPowerCardScene(scene)) {
      return createStaticResultFigure(card, copy);
    }

    const figure = document.createElement("figure");
    figure.className = "power-card-result power-card-animated-result";
    figure.dataset.powerCardId = card.id;
    figure.dataset.powerCardTemplate = scene.template;
    figure.append(renderPowerCardSceneSvg(card, copy, scene));

    const toggle = document.createElement("button");
    toggle.className = "power-card-animation-toggle";
    toggle.type = "button";
    toggle.innerHTML = '<span aria-hidden="true"></span>';
    toggle.addEventListener("click", () => {
      figure.classList.toggle("is-paused");
      updateAnimationToggle(figure, copy);
    });
    figure.append(toggle);
    updateAnimationToggle(figure, copy);

    const observer = ensurePowerCardAnimationObserver();
    if (observer) {
      observer.observe(figure);
    }

    return figure;
  };

  const createPowerCardResultFigure = (card, copy) => {
    const scene = powerCardScenes[card.id];
    if (scene) {
      return createAnimatedResultFigure(card, copy, scene);
    }

    return createStaticResultFigure(card, copy);
  };

  const renderPowerCards = () => {
    const family = familiesById.get(selectedFamilyId);
    const familyLabel = family?.label || family?.name || "Selected skill";

    setSelectedState();
    if (powerCardAnimationObserver) {
      powerCardAnimationObserver.disconnect();
      powerCardAnimationObserver = null;
    }
    powerCardResults.replaceChildren();

    if (!selectedFamilyId || !selectedLevel) {
      const empty = document.createElement("p");
      empty.className = "empty-card-note";
      if (!selectedFamilyId && !selectedLevel) {
        empty.textContent = "Choose a Skill Card and a level to see matching Power Cards.";
      } else if (!selectedLevel) {
        empty.textContent = "Choose a level to see matching Power Cards for this Skill Card.";
      } else {
        empty.textContent = "Choose a Skill Card to see matching Power Cards at this level.";
      }
      powerCardResults.append(empty);
      return;
    }

    const matchingCards = curriculumData.powerCards.filter(
      (card) => card.primary_family === selectedFamilyId && card.level === selectedLevel
    );

    if (!matchingCards.length) {
      const empty = document.createElement("p");
      empty.className = "empty-card-note";
      empty.textContent = "No generated Power Cards match this selection yet.";
      powerCardResults.append(empty);
      return;
    }

    matchingCards.forEach((card) => {
      const copy = getCardCopy(card);
      const article = document.createElement("article");
      article.className = "play-card power-play-card generated-power-card";

      addText(article, "p", "power-card-meta", `Level ${card.level} · ${familyLabel}`);
      addText(article, "h3", "", copy.title);

      const figure = createPowerCardResultFigure(card, copy);
      if (figure) {
        article.append(figure);
      }

      addCardSection(article, "Your mission", copy.mission, "mission-section");
      addCardSection(article, "You’ll use", copy.materials);
      addCardSection(article, "You’ve earned this power when", copy.earned);

      if (card.dependencies.length) {
        const dependencyTitles = card.dependencies
          .map((dependencyId) => powerCardsById.get(dependencyId))
          .filter(Boolean)
          .map((dependency) => getFriendlyTitle(dependency));
        addCardSection(article, "Do this after", formatList(dependencyTitles));
      }

      addCardSection(article, "Try next", copy.tryNext, "try-next-section");

      powerCardResults.append(article);
    });
  };

  familyButtons.forEach((button) => {
    button.addEventListener("click", (event) => {
      event.preventDefault();
      selectedFamilyId = button.dataset.family;
      renderPowerCards();
      scrollToSection("#levels");
    });
  });

  levelButtons.forEach((button) => {
    button.addEventListener("click", (event) => {
      event.preventDefault();
      selectedLevel = Number(button.dataset.level);
      renderPowerCards();
      scrollToSection("#power-cards");
    });
  });

  const initialFamilyId = initialCardParams.get("family");
  const initialLevel = Number(initialCardParams.get("level"));
  if (familiesById.has(initialFamilyId)) {
    selectedFamilyId = initialFamilyId;
  }
  if (Number.isInteger(initialLevel) && initialLevel >= 1 && initialLevel <= 6) {
    selectedLevel = initialLevel;
  }

  if (reducedPowerMotionQuery) {
    if (typeof reducedPowerMotionQuery.addEventListener === "function") {
      reducedPowerMotionQuery.addEventListener("change", renderPowerCards);
    } else if (typeof reducedPowerMotionQuery.addListener === "function") {
      reducedPowerMotionQuery.addListener(renderPowerCards);
    }
  }

  renderPowerCards();
}
