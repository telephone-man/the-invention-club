const header = document.querySelector("[data-site-header]");
const menuButton = document.querySelector(".menu-button");
const navLinks = document.querySelectorAll(".site-nav a");
const interestForm = document.querySelector("#interest-form");
const formNote = document.querySelector("#form-note");
const scrollSpinLoops = document.querySelectorAll("[data-scroll-spin]");
const curriculumData = window.INVENTION_CLUB_CURRICULUM;
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

  const renderPowerCards = () => {
    const family = familiesById.get(selectedFamilyId);
    const familyLabel = family?.label || family?.name || "Selected skill";

    setSelectedState();
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

      if (card.result_image) {
        const figure = document.createElement("figure");
        figure.className = "power-card-result";
        const image = document.createElement("img");
        image.src = card.result_image;
        image.alt = card.result_alt || `${copy.title} result build`;
        image.loading = "lazy";
        figure.append(image);
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

  renderPowerCards();
}
