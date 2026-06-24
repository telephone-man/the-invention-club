(function () {
  const DEFAULT_FIRST_SESSION_CARD_IDS = ["r_pow_01", "r_ctl_01", "r_pow_02"];
  const OPENING_MINUTES = 5;
  const RESET_WARNING_MINUTES = 5;
  const DIRECT_SUPERVISION_LEVELS = new Set(["direct", "adult_controlled", "demo_only"]);

  const pageDocument = typeof document === "undefined" ? null : document;
  const curriculumData =
    typeof window === "undefined" ? null : window.INVENTION_CLUB_CURRICULUM;

  const escapeHtml = (value) =>
    String(value ?? "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");

  const markdownCell = (value) => {
    if (Array.isArray(value)) {
      return value.join(", ").replaceAll("|", "\\|");
    }
    const text = String(value ?? "-").trim();
    return (text || "-").replaceAll("|", "\\|").replaceAll("\n", "<br>");
  };

  const slugify = (value) =>
    String(value || "session-plan")
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/^-|-$/g, "");

  const firstSessionPack = (data) =>
    (data?.pilotMicroPacks || []).find((pack) => pack.id === "first_session") || null;

  const firstSessionCardIds = (data) => {
    const pack = firstSessionPack(data);
    const ids = pack?.target_power_card_ids;
    return Array.isArray(ids) && ids.length ? ids : DEFAULT_FIRST_SESSION_CARD_IDS;
  };

  const assetsById = (data) =>
    new Map(
      (data?.assetInventory?.physical_assets || [])
        .filter((asset) => asset && asset.id)
        .map((asset) => [asset.id, asset])
    );

  const familiesById = (data) =>
    new Map((data?.families || []).filter((family) => family?.id).map((family) => [family.id, family]));

  const levelsById = (data) =>
    new Map((data?.levels || []).filter((level) => level?.id).map((level) => [level.id, level]));

  const isPilotCard = (card) =>
    Array.isArray(card?.required_assets) &&
    card.required_assets.length > 0 &&
    card.activity_flow &&
    typeof card.activity_flow === "object";

  const getPilotCards = (data) => (data?.powerCards || []).filter(isPilotCard);

  const orderedPilotCards = (data) => {
    const defaultIds = firstSessionCardIds(data);
    const familyOrder = new Map((data?.families || []).map((family, index) => [family.id, index]));
    const byId = new Map(getPilotCards(data).map((card) => [card.id, card]));
    const defaults = defaultIds.map((id) => byId.get(id)).filter(Boolean);
    const rest = getPilotCards(data)
      .filter((card) => !defaultIds.includes(card.id))
      .sort((left, right) => {
        const leftFamily = familyOrder.get(left.primary_family) ?? 999;
        const rightFamily = familyOrder.get(right.primary_family) ?? 999;
        if (leftFamily !== rightFamily) return leftFamily - rightFamily;
        if (left.level !== right.level) return left.level - right.level;
        return String(left.title).localeCompare(String(right.title));
      });
    return [...defaults, ...rest];
  };

  const pairCountForChildren = (childCount) => {
    if (Number(childCount) === 4) return 2;
    if (Number(childCount) === 5) return 3;
    return 3;
  };

  const quantityForRequirement = (requirement, childCount) => {
    const quantity = Number(requirement.quantity || 0);
    switch (requirement.quantity_basis) {
      case "per_child":
        return quantity * Number(childCount);
      case "per_pair":
        return quantity * pairCountForChildren(childCount);
      case "per_table":
      case "per_session":
      case "demo_only":
        return quantity;
      default:
        return quantity;
    }
  };

  const quantityFormula = (requirement, childCount) => {
    const quantity = Number(requirement.quantity || 0);
    switch (requirement.quantity_basis) {
      case "per_child":
        return `${quantity} x ${childCount} children`;
      case "per_pair":
        return `${quantity} x ${pairCountForChildren(childCount)} build teams`;
      case "per_table":
        return `${quantity} x 1 table`;
      case "demo_only":
        return `${quantity} adult-controlled demo item`;
      case "per_session":
        return `${quantity} per session`;
      default:
        return String(quantity);
    }
  };

  const requirementUsesExcludedAsset = (card, requirement, options) =>
    options.ledOnly === true && card.id === "r_pow_02" && requirement.asset_id === "part_dc_motor";

  const selectedRequirements = (card, options) =>
    (card.required_assets || []).filter((requirement) => !requirementUsesExcludedAsset(card, requirement, options));

  const activitySteps = (card, section, options) =>
    (card.activity_flow?.[section] || []).filter((step) => {
      if (!step || typeof step !== "object") return false;
      if (options.ledOnly === true && card.id === "r_pow_02") {
        return !(step.asset_ids || []).includes("part_dc_motor");
      }
      return true;
    });

  const assetHasText = (asset, pattern) =>
    pattern.test(`${asset?.id || ""} ${asset?.label || ""} ${asset?.short_label || ""} ${asset?.category || ""}`);

  const riskFlagsForRequirements = (requirements, assetMap) => {
    const flags = new Set();
    requirements.forEach((requirement) => {
      const asset = assetMap.get(requirement.asset_id) || {};
      const safety = asset.safety || {};
      const hazards = safety.hazards || [];
      if (requirement.preload_profile_id || requirement.preparation_state === "preloaded") {
        flags.add("preloaded");
      }
      if (asset.category === "programmable_board" || asset.category === "programmable_board_accessory") {
        flags.add("preloaded");
      }
      if (
        asset.category === "actuator" ||
        hazards.includes("moving_shaft") ||
        assetHasText(asset, /\b(motor|servo|solenoid)\b/i)
      ) {
        flags.add("moving");
      }
      if (assetHasText(asset, /\bcoin cell\b/i) || requirement.asset_id === "part_coin_cell") {
        flags.add("coin");
      }
      if (assetHasText(asset, /\bled strip\b/i) || requirement.asset_id === "part_led_strip") {
        flags.add("led-strip");
      }
      if (DIRECT_SUPERVISION_LEVELS.has(safety.supervision_level)) {
        flags.add("direct");
      }
    });
    return [...flags];
  };

  const riskLabel = (flag) =>
    ({
      preloaded: "Preloaded",
      moving: "Moving",
      coin: "Coin cell",
      "led-strip": "LED strip",
      direct: "Direct",
    })[flag] || flag;

  const riskWarning = (flag) =>
    ({
      preloaded: "Selected cards include preloaded-board assets; defer delivery until board labels, firmware state and helper coverage are confirmed.",
      moving: "Selected cards include moving parts; defer delivery until moving-shaft safety and adult coverage are confirmed.",
      coin: "Selected cards include coin-cell handling; keep coin cells adult-controlled and count them back immediately.",
      "led-strip": "Selected cards include LED-strip work; defer delivery until current limits and switching path are confirmed.",
      direct: "Selected cards include direct-supervision assets; confirm helper coverage before running this plan.",
    })[flag] || `Selected cards include ${flag} risk; confirm kit and supervision before running this plan.`;

  const kitRowsForPlan = (data, selectedCards, options) => {
    const assetMap = assetsById(data);
    const rowsByKey = new Map();
    selectedCards.forEach((card) => {
      selectedRequirements(card, options).forEach((requirement) => {
        const asset = assetMap.get(requirement.asset_id) || {};
        const safety = asset.safety || {};
        const storage = asset.storage || {};
        const key = [
          requirement.asset_id,
          requirement.quantity_basis || "",
          requirement.preparation_state || "",
          requirement.preload_profile_id || "",
        ].join("|");
        const calculated = quantityForRequirement(requirement, options.childCount);
        if (!rowsByKey.has(key)) {
          rowsByKey.set(key, {
            assetId: requirement.asset_id,
            kitCode: asset.kit_code || "",
            item: asset.short_label || asset.label || requirement.asset_id,
            category: asset.category || "",
            bin: storage.bin_id || "",
            compartment: storage.compartment || "",
            packOrder: Number(storage.pack_order || 0),
            cards: [],
            basis: requirement.quantity_basis || "-",
            calculation: quantityFormula(requirement, options.childCount),
            quantity: calculated,
            preparation: requirement.preparation_notes || "",
            supervision: safety.supervision_level || "",
            hazards: safety.hazards || [],
            returnCheck: safety.return_check || "",
          });
        }
        const row = rowsByKey.get(key);
        row.quantity = Math.max(row.quantity, calculated);
        if (!row.cards.includes(card.id)) row.cards.push(card.id);
      });
    });
    return [...rowsByKey.values()].sort((left, right) => {
      const binSort = String(left.bin).localeCompare(String(right.bin));
      if (binSort) return binSort;
      if (left.packOrder !== right.packOrder) return left.packOrder - right.packOrder;
      return String(left.kitCode).localeCompare(String(right.kitCode));
    });
  };

  const resetRowsForKit = (kitRows) =>
    kitRows.filter((row) =>
      row.category === "power_source" ||
      /\b(cell|battery|pack)\b/i.test(`${row.assetId} ${row.item}`) ||
      row.assetId === "part_croc_clip_lead"
    );

  const durationForCard = (card) => (Number(card.level) === 1 ? 10 : 15);

  const defaultTimingScript = (card) => {
    const flow = card.activity_flow || {};
    const prompt = flow.child_start_state?.prompt || card.i_can_statement || "";
    const starter = flow.child_start_state?.starter_question;
    return [prompt, starter ? `Ask: ${starter}` : ""].filter(Boolean).join(" ");
  };

  const timingScriptForCard = (card, pack) => {
    const matchingBlock = (pack?.timing_blocks || []).find(
      (block) => Array.isArray(block.target_power_card_ids) &&
        block.target_power_card_ids.length === 1 &&
        block.target_power_card_ids[0] === card.id
    );
    return matchingBlock?.facilitator_script || defaultTimingScript(card);
  };

  const sequenceMetaForCard = (card, pack) =>
    (pack?.card_sequence || []).find((item) => item.power_card_id === card.id) || {};

  const createSessionPlan = (data, options) => {
    const selectedIds = options.selectedCardIds || [];
    const childCount = Number(options.childCount || 6);
    const sessionLength = Number(options.sessionLength || 60);
    const pack = firstSessionPack(data);
    const cardMap = new Map(getPilotCards(data).map((card) => [card.id, card]));
    const selectedCards = selectedIds.map((id) => cardMap.get(id)).filter(Boolean);
    const assetMap = assetsById(data);
    const familyMap = familiesById(data);
    const levelMap = levelsById(data);
    const warnings = [];

    if (!selectedCards.length) {
      warnings.push("Select at least one Power Card before using this plan.");
    }

    let cursor = OPENING_MINUTES;
    const timingBlocks = [
      {
        time: `0-${OPENING_MINUTES}`,
        title: "Open the room rules",
        cards: [],
        minutes: OPENING_MINUTES,
        script: "No power is connected until an adult checks the path, polarity and switch state.",
      },
    ];

    selectedCards.forEach((card) => {
      const minutes = durationForCard(card);
      timingBlocks.push({
        time: `${cursor}-${cursor + minutes}`,
        title: card.title,
        cards: [card.id],
        minutes,
        script: timingScriptForCard(card, pack),
      });
      cursor += minutes;
    });

    const resetMinutes = sessionLength - cursor;
    if (resetMinutes < RESET_WARNING_MINUTES) {
      if (resetMinutes < 0) {
        warnings.push(`Too many cards for ${sessionLength} minutes: the plan overruns before reset/count-back by ${Math.abs(resetMinutes)} minutes.`);
      } else {
        warnings.push(`Too many cards for ${sessionLength} minutes: reset/count-back has only ${resetMinutes} minutes.`);
      }
    }

    timingBlocks.push({
      time: cursor <= sessionLength ? `${cursor}-${sessionLength}` : `${sessionLength}+`,
      title: "Reset, count back and capture evidence",
      cards: selectedCards.map((card) => card.id),
      minutes: Math.max(0, resetMinutes),
      script: "Switch off, unclip leads, count key kit items back and record what needed more explanation.",
    });

    const kitRows = kitRowsForPlan(data, selectedCards, { ...options, childCount });
    const riskFlags = new Set();
    selectedCards.forEach((card) => {
      riskFlagsForRequirements(selectedRequirements(card, options), assetMap).forEach((flag) => riskFlags.add(flag));
    });
    [...riskFlags].forEach((flag) => warnings.push(riskWarning(flag)));
    if (options.ledOnly && selectedCards.some((card) => card.id === "r_pow_02")) {
      warnings.push("r_pow_02 is constrained to the LED module only; the optional motor load is excluded from kit quantities and activity steps.");
    }

    const safetyRules = [
      "No child-authored code in this session.",
      "No power connected until an adult checks polarity, circuit path and switch state.",
      "Switch battery packs off before handout, checking, reset or pack-away.",
      "Children handle only the prepared low-voltage parts named for the active card.",
    ];
    if (options.ledOnly && selectedCards.some((card) => card.id === "r_pow_02")) {
      safetyRules.push("Use r_pow_02 with the LED module only; do not use the optional motor comparison load.");
    }
    if (riskFlags.has("coin")) {
      safetyRules.push("Coin cells stay adult-controlled and are counted back immediately.");
    }
    if (riskFlags.has("moving")) {
      safetyRules.push("Keep fingers, hair and loose material clear of moving parts.");
    }
    if (riskFlags.has("preloaded")) {
      safetyRules.push("Preloaded boards must be adult-flashed, checked and labelled before the session.");
    }

    const resetSteps = [
      "Switch off every battery pack before leads are removed.",
      "Unclip and untangle all clip leads.",
      "Return controls and modules dry, unplugged and in their labelled compartments.",
      "Count batteries, cells, packs and clip leads before closing the kit.",
      "Record warm wires, damaged insulation, missing labels or confusing prompts.",
    ];
    if (riskFlags.has("preloaded")) {
      resetSteps.push("Return preloaded boards to adult-controlled storage and record firmware or labelling issues.");
    }
    if (riskFlags.has("moving")) {
      resetSteps.push("Return motors and moving parts unplugged, with shafts clear of loose wire.");
    }

    const title = `Generated ${sessionLength}-minute pilot session`;
    const plan = {
      title,
      childCount,
      sessionLength,
      pairCount: pairCountForChildren(childCount),
      helperNote: String(options.helperNote || "").trim(),
      ledOnly: Boolean(options.ledOnly),
      selectedCards,
      familyMap,
      levelMap,
      timingBlocks,
      kitRows,
      resetRows: resetRowsForKit(kitRows),
      safetyRules,
      resetSteps,
      warnings: [...new Set(warnings)],
      cardDetails: selectedCards.map((card) => ({
        card,
        family: familyMap.get(card.primary_family),
        level: levelMap.get(card.level),
        sequence: sequenceMetaForCard(card, pack),
        prompt: card.activity_flow?.child_start_state?.prompt || "",
        starter: card.activity_flow?.child_start_state?.starter_question || "",
        buildSteps: activitySteps(card, "build_steps", options),
        testSteps: activitySteps(card, "test_steps", options),
        debugSteps: activitySteps(card, "debug_steps", options),
      })),
    };
    plan.markdown = renderMarkdown(plan);
    return plan;
  };

  const markdownTable = (headers, rows) => {
    const header = `| ${headers.map(markdownCell).join(" | ")} |`;
    const divider = `| ${headers.map(() => "---").join(" | ")} |`;
    const body = rows.length
      ? rows.map((row) => `| ${row.map(markdownCell).join(" | ")} |`).join("\n")
      : `| ${headers.map(() => "-").join(" | ")} |`;
    return `${header}\n${divider}\n${body}`;
  };

  function renderMarkdown(plan) {
    const lines = [
      `# ${plan.title}`,
      "",
      "Generated from the static session-plan generator. Review before delivery.",
      "",
      "## Summary",
      "",
      `- Children: ${plan.childCount}`,
      `- Build teams: ${plan.pairCount}`,
      `- Session length: ${plan.sessionLength} minutes`,
      `- Cards: ${plan.selectedCards.map((card) => card.id).join(", ") || "none selected"}`,
      `- LED-only r_pow_02: ${plan.ledOnly ? "yes" : "no"}`,
      `- Helper note: ${plan.helperNote || "Not specified."}`,
      "",
      "## Warnings",
      "",
      ...(plan.warnings.length ? plan.warnings.map((warning) => `- ${warning}`) : ["- No generated warnings."]),
      "",
      "## Timing And Facilitator Script",
      "",
      markdownTable(
        ["Time", "Block", "Cards", "Script"],
        plan.timingBlocks.map((block) => [
          block.time,
          block.title,
          block.cards.join(", ") || "-",
          block.script,
        ])
      ),
      "",
      "## Card Sequence And Child Prompts",
      "",
      markdownTable(
        ["Card", "Title", "Level", "Prompt", "Starter question", "Success evidence"],
        plan.cardDetails.map((detail) => [
          detail.card.id,
          detail.card.title,
          `${detail.card.level} - ${detail.level?.name || ""}`,
          detail.prompt,
          detail.starter,
          detail.card.success_condition,
        ])
      ),
      "",
      "## Activity Flow",
      "",
    ];

    plan.cardDetails.forEach((detail) => {
      lines.push(`### ${detail.card.id} - ${detail.card.title}`, "");
      [
        ["Build", detail.buildSteps],
        ["Test", detail.testSteps],
        ["Debug", detail.debugSteps],
      ].forEach(([label, steps]) => {
        if (!steps.length) return;
        lines.push(`- ${label}:`);
        steps.forEach((step) => {
          const expected = step.expected_result ? ` Expected evidence: ${step.expected_result}` : "";
          lines.push(`  - ${step.instruction}${expected}`);
        });
      });
      if (detail.sequence?.handoff_cue) {
        lines.push(`- Handoff cue: ${detail.sequence.handoff_cue}`);
      }
      lines.push("");
    });

    lines.push(
      "## Kit Quantities",
      "",
      markdownTable(
        ["Kit", "Item", "Bin", "Cards", "Calculation", "Quantity", "Preparation", "Return check"],
        plan.kitRows.map((row) => [
          row.kitCode,
          row.item,
          row.bin,
          row.cards.join(", "),
          row.calculation,
          row.quantity,
          row.preparation,
          row.returnCheck,
        ])
      ),
      "",
      "## Battery And Count-Back",
      "",
      markdownTable(
        ["Kit", "Item", "Quantity", "Return check"],
        plan.resetRows.map((row) => [row.kitCode, row.item, row.quantity, row.returnCheck])
      ),
      "",
      "## Safety Rules",
      "",
      ...plan.safetyRules.map((rule) => `- ${rule}`),
      "",
      "## Reset And Pack-Away",
      "",
      ...plan.resetSteps.map((step) => `- ${step}`),
      ""
    );

    return `${lines.join("\n").trim()}\n`;
  }

  const htmlList = (items, emptyText = "None.") =>
    items.length
      ? `<ul>${items.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>`
      : `<p class="empty-card-note">${escapeHtml(emptyText)}</p>`;

  const htmlTable = (headers, rows) => {
    const head = `<thead><tr>${headers.map((header) => `<th scope="col">${escapeHtml(header)}</th>`).join("")}</tr></thead>`;
    const bodyRows = rows.length
      ? rows
          .map(
            (row) =>
              `<tr>${row
                .map((cell, index) => {
                  const tag = index === 0 ? "th scope=\"row\"" : "td";
                  return `<${tag} data-label="${escapeHtml(headers[index])}">${escapeHtml(cell)}</${index === 0 ? "th" : "td"}>`;
                })
                .join("")}</tr>`
          )
          .join("")
      : `<tr><td data-label="${escapeHtml(headers[0])}" colspan="${headers.length}">No rows.</td></tr>`;
    return `<table class="planner-table">${head}<tbody>${bodyRows}</tbody></table>`;
  };

  const renderSummary = (plan) => `
    <dl class="planner-summary-grid">
      <div><dt>Children</dt><dd>${plan.childCount}</dd></div>
      <div><dt>Build teams</dt><dd>${plan.pairCount}</dd></div>
      <div><dt>Length</dt><dd>${plan.sessionLength} minutes</dd></div>
      <div><dt>Cards</dt><dd>${plan.selectedCards.length}</dd></div>
    </dl>
    <p>${escapeHtml(plan.helperNote || "No helper note supplied.")}</p>
  `;

  const renderWarnings = (plan) => htmlList(plan.warnings, "No generated warnings.");

  const renderTiming = (plan) =>
    htmlTable(
      ["Time", "Block", "Cards", "Script"],
      plan.timingBlocks.map((block) => [
        block.time,
        block.title,
        block.cards.join(", ") || "-",
        block.script,
      ])
    );

  const renderSequence = (plan) =>
    plan.cardDetails.length
      ? plan.cardDetails
          .map(
            (detail) => `
              <article class="planner-sequence-card">
                <span>${escapeHtml(detail.card.id)}</span>
                <h4>${escapeHtml(detail.card.title)}</h4>
                <p>${escapeHtml(detail.prompt || detail.card.i_can_statement)}</p>
                <dl>
                  <div><dt>Level</dt><dd>${escapeHtml(`${detail.card.level} - ${detail.level?.name || ""}`)}</dd></div>
                  <div><dt>Starter</dt><dd>${escapeHtml(detail.starter || "-")}</dd></div>
                  <div><dt>Evidence</dt><dd>${escapeHtml(detail.card.success_condition || "-")}</dd></div>
                </dl>
              </article>
            `
          )
          .join("")
      : `<p class="empty-card-note">Select at least one Power Card.</p>`;

  const renderKit = (plan) =>
    htmlTable(
      ["Kit", "Item", "Bin", "Cards", "Calculation", "Qty", "Preparation", "Return check"],
      plan.kitRows.map((row) => [
        row.kitCode,
        row.item,
        row.bin,
        row.cards.join(", "),
        row.calculation,
        row.quantity,
        row.preparation,
        row.returnCheck,
      ])
    );

  const renderSafety = (plan) => `
    <div class="planner-safety-grid">
      <div>
        <h4>Safety rules</h4>
        ${htmlList(plan.safetyRules)}
      </div>
      <div>
        <h4>Reset and count-back</h4>
        ${htmlList(plan.resetSteps)}
      </div>
    </div>
  `;

  const cardBadges = (card, data) => {
    const assetMap = assetsById(data);
    const flags = riskFlagsForRequirements(card.required_assets || [], assetMap);
    const kitCount = (card.required_assets || []).length;
    return [
      `<span class="planner-badge">Level ${escapeHtml(card.level)}</span>`,
      `<span class="planner-badge">${kitCount} kit ${kitCount === 1 ? "item" : "items"}</span>`,
      ...flags.map((flag) => `<span class="planner-badge risk-badge">${escapeHtml(riskLabel(flag))}</span>`),
    ].join("");
  };

  const renderCardPicker = (root, data) => {
    const picker = root.querySelector("[data-card-picker]");
    if (!picker) return;
    const defaultIds = firstSessionCardIds(data);
    const cards = orderedPilotCards(data);
    const familyMap = familiesById(data);
    const defaultCards = cards.filter((card) => defaultIds.includes(card.id));
    const remaining = cards.filter((card) => !defaultIds.includes(card.id));
    const groups = [];
    if (defaultCards.length) {
      groups.push(["First-session defaults", defaultCards]);
    }
    const remainingByFamily = new Map();
    remaining.forEach((card) => {
      const label = familyMap.get(card.primary_family)?.label || card.primary_family;
      if (!remainingByFamily.has(label)) remainingByFamily.set(label, []);
      remainingByFamily.get(label).push(card);
    });
    remainingByFamily.forEach((groupCards, label) => groups.push([label, groupCards]));

    picker.innerHTML = groups
      .map(
        ([label, groupCards]) => `
          <section class="planner-card-group">
            <h4>${escapeHtml(label)}</h4>
            <div class="planner-card-options">
              ${groupCards
                .map(
                  (card) => `
                    <label class="planner-card-option">
                      <input type="checkbox" name="power-card" value="${escapeHtml(card.id)}" data-card-id="${escapeHtml(card.id)}" ${defaultIds.includes(card.id) ? "checked" : ""}>
                      <span>
                        <strong>${escapeHtml(card.title)}</strong>
                        <small>${escapeHtml(card.i_can_statement || "")}</small>
                        <span class="planner-badges">${cardBadges(card, data)}</span>
                      </span>
                    </label>
                  `
                )
                .join("")}
            </div>
          </section>
        `
      )
      .join("");
  };

  const readOptions = (root) => ({
    selectedCardIds: [...root.querySelectorAll("[data-card-id]:checked")].map((input) => input.value),
    childCount: Number(root.querySelector("input[name='child-count']:checked")?.value || 6),
    sessionLength: Number(root.querySelector("input[name='session-length']:checked")?.value || 60),
    ledOnly: Boolean(root.querySelector("input[name='led-only']")?.checked),
    helperNote: root.querySelector("textarea[name='helper-note']")?.value || "",
  });

  const setHtml = (root, selector, html) => {
    const element = root.querySelector(selector);
    if (element) element.innerHTML = html;
  };

  const setText = (root, selector, text) => {
    const element = root.querySelector(selector);
    if (element) element.textContent = text;
  };

  const renderPlan = (root, plan) => {
    setText(root, "[data-plan-title]", plan.title);
    setHtml(root, "[data-plan-summary]", renderSummary(plan));
    setHtml(root, "[data-plan-warnings]", renderWarnings(plan));
    setHtml(root, "[data-plan-timing]", renderTiming(plan));
    setHtml(root, "[data-plan-sequence]", renderSequence(plan));
    setHtml(root, "[data-plan-kit]", renderKit(plan));
    setHtml(root, "[data-plan-safety]", renderSafety(plan));
    const markdown = root.querySelector("[data-markdown-output]");
    if (markdown) markdown.value = plan.markdown;
  };

  const updatePlan = (root, data) => {
    const options = readOptions(root);
    const plan = createSessionPlan(data, options);
    root.__currentSessionPlan = plan;
    renderPlan(root, plan);
  };

  const copyMarkdown = async (root) => {
    const textarea = root.querySelector("[data-markdown-output]");
    const status = root.querySelector("[data-planner-status]");
    if (!textarea) return;
    try {
      if (navigator.clipboard?.writeText) {
        await navigator.clipboard.writeText(textarea.value);
        if (status) status.textContent = "Markdown copied.";
        return;
      }
    } catch (error) {
      // Fall through to manual selection.
    }
    textarea.focus();
    textarea.select();
    if (status) status.textContent = "Markdown selected. Press Ctrl+C or Cmd+C to copy.";
  };

  const downloadMarkdown = (root) => {
    const plan = root.__currentSessionPlan;
    const textarea = root.querySelector("[data-markdown-output]");
    if (!plan || !textarea) return;
    const blob = new Blob([textarea.value], { type: "text/markdown" });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = `${slugify(plan.title)}.md`;
    document.body.append(anchor);
    anchor.click();
    anchor.remove();
    URL.revokeObjectURL(url);
    const status = root.querySelector("[data-planner-status]");
    if (status) status.textContent = "Markdown download started.";
  };

  const initPlanner = (root, data) => {
    renderCardPicker(root, data);
    updatePlan(root, data);
    root.addEventListener("change", () => updatePlan(root, data));
    root.addEventListener("input", (event) => {
      if (event.target?.matches("textarea[name='helper-note']")) {
        updatePlan(root, data);
      }
    });
    root.querySelector("[data-copy-markdown]")?.addEventListener("click", () => copyMarkdown(root));
    root.querySelector("[data-download-markdown]")?.addEventListener("click", () => downloadMarkdown(root));
  };

  const api = {
    createSessionPlan,
    getPilotCards,
    kitRowsForPlan,
    orderedPilotCards,
    pairCountForChildren,
    quantityForRequirement,
    renderMarkdown,
    riskFlagsForRequirements,
  };

  if (typeof window !== "undefined") {
    window.InventionSessionPlanner = api;
  }

  if (pageDocument && curriculumData) {
    const root = pageDocument.querySelector("[data-session-planner]");
    if (root) {
      initPlanner(root, curriculumData);
    }
  }
})();
