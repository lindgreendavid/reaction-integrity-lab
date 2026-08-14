const cells = {
  "labels-other": {
    cell: "A", baseline: 52, model: 67, aib: 32,
    interpretation: "Trusting stored labels produces a comparatively easy combined condition target. The score cannot be read as prospective laboratory performance.",
  },
  "labels-delete": {
    cell: "B", baseline: 52, model: 68, aib: 33,
    interpretation: "Removing reactions with rare components raises both the baseline and model score. It also narrows the population to common recorded conditions.",
  },
  "reaction-string-other": {
    cell: "C", baseline: 20, model: 35, aib: 19,
    interpretation: "Chemically informed role assignment makes the combined target much harder. Mapping rare labels to ‘other’ keeps more reactions but coarsens the task.",
  },
  "reaction-string-delete": {
    cell: "D", baseline: 20, model: 36, aib: 19,
    interpretation: "This is the authors’ preferred benchmark construction: chemically informed roles with rare-component reactions removed.",
  },
};

const stages = {
  source: { number: "01", title: "Source extraction", count: "1,771,032 reactions enter", retained: 100, description: "The official USPTO-derived ORD extraction before the condition-benchmark filters.", boundary: "A large source count says nothing about independence, coverage, or label quality." },
  shape: { number: "02", title: "Component limits", count: "1,279,207 reactions remain", retained: 72.23, description: "Rows exceeding two reactants, one product, two solvents, or three agents are removed for the fixed task shape.", boundary: "The resulting benchmark no longer represents reactions with more complex recorded compositions." },
  required: { number: "03", title: "Required inputs", count: "1,261,701 reactions remain", retained: 71.24, description: "Rows without at least one reactant and one product are excluded.", boundary: "Completeness for these fields does not guarantee chemically correct role assignment." },
  duplicates: { number: "04", title: "Exact duplicates", count: "753,338 reactions remain", retained: 42.54, description: "Exact duplicates across the declared input and output columns are collapsed.", boundary: "Exact deduplication does not remove near-duplicates, patent families, or highly similar transformations." },
  rare: { number: "05", title: "Rare components", count: "691,142 reactions remain", retained: 39.02, description: "Reactions containing a solvent or agent observed fewer than 100 times are removed in this variant.", boundary: "The easier label space is also a narrower population; conclusions do not extend automatically to rare chemistry." },
  split: { number: "06", title: "Split collisions", count: "3,541 test rows moved", retained: 94.69, description: "Rows whose reactant/product input key appeared in training were moved out of the initial test allocation.", boundary: "Identity separation is not chemical-similarity, temporal, or patent-family separation." },
};

const similarityThresholds = {
  "0.70": { proportion: 60.5, interval: "57.44–63.48%", count: 605, interpretation: "A majority of the prespecified sample has a moderately similar training product. This describes product representation overlap, not reaction equivalence." },
  "0.80": { proportion: 30.0, interval: "27.24–32.91%", count: 300, interpretation: "Three in ten sampled test products have a high-similarity training product under the frozen fingerprint." },
  "0.90": { proportion: 11.7, interval: "9.85–13.84%", count: 117, interpretation: "A smaller but non-trivial share has a very highly similar training product. Model behavior was not stratified by this threshold." },
  "1.00": { proportion: 8.4, interval: "6.84–10.28%", count: 84, interpretation: "Fingerprint similarity 1.0 is not canonical identity: finite fingerprints can collide or omit chemical distinctions." },
};

let selectedRole = "labels";
let selectedRare = "other";

function selectedCellKey() {
  return `${selectedRole}-${selectedRare}`;
}

function renderCell() {
  const value = cells[selectedCellKey()];
  document.querySelector("#cell-label").textContent = value.cell;
  document.querySelector("#baseline-score").textContent = `${value.baseline}%`;
  document.querySelector("#model-score").textContent = `${value.model}%`;
  document.querySelector("#gain-score").textContent = `+${value.model - value.baseline} pp`;
  document.querySelector("#aib-score").textContent = `${value.aib}%`;
  document.querySelector("#baseline-bar").style.width = `${value.baseline}%`;
  document.querySelector("#model-bar").style.width = `${value.model}%`;
  document.querySelector("#interpretation").textContent = value.interpretation;
  document.querySelectorAll("[data-role]").forEach((button) => button.setAttribute("aria-pressed", String(button.dataset.role === selectedRole)));
  document.querySelectorAll("[data-rare]").forEach((button) => button.setAttribute("aria-pressed", String(button.dataset.rare === selectedRare)));
  document.querySelectorAll("[data-cell]").forEach((button) => button.toggleAttribute("data-selected", button.dataset.cell === selectedCellKey()));
}

document.querySelectorAll("[data-role]").forEach((button) => button.addEventListener("click", () => {
  selectedRole = button.dataset.role;
  renderCell();
}));

document.querySelectorAll("[data-rare]").forEach((button) => button.addEventListener("click", () => {
  selectedRare = button.dataset.rare;
  renderCell();
}));

document.querySelectorAll("[data-cell]").forEach((button) => button.addEventListener("click", () => {
  [selectedRole, selectedRare] = button.dataset.cell.split(/-(?=[^-]+$)/);
  renderCell();
  document.querySelector("#microscope-title").scrollIntoView({ behavior: "smooth", block: "start" });
}));

function renderStage(stageName) {
  const stage = stages[stageName];
  document.querySelector("#stage-number").textContent = `Stage ${stage.number}`;
  document.querySelector("#stage-title").textContent = stage.title;
  document.querySelector("#stage-count").textContent = stage.count;
  document.querySelector("#stage-description").textContent = stage.description;
  document.querySelector("#stage-boundary").textContent = stage.boundary;
  document.querySelector("#retention-bar").style.width = `${stage.retained}%`;
  document.querySelectorAll("[data-stage]").forEach((button) => button.toggleAttribute("aria-current", button.dataset.stage === stageName));
}

document.querySelectorAll("[data-stage]").forEach((button) => button.addEventListener("click", () => renderStage(button.dataset.stage)));

function renderSimilarity(threshold) {
  const value = similarityThresholds[threshold];
  document.querySelector("#similarity-threshold").textContent = `≥ ${threshold}`;
  document.querySelector("#similarity-proportion").textContent = `${value.proportion.toFixed(1)}%`;
  document.querySelector("#similarity-count").textContent = `${value.count} / 1,000`;
  document.querySelector("#similarity-interval").textContent = value.interval;
  document.querySelector("#similarity-bar").style.width = `${value.proportion}%`;
  document.querySelector("#similarity-interpretation").textContent = value.interpretation;
  document.querySelectorAll("[data-threshold]").forEach((button) => button.setAttribute("aria-pressed", String(button.dataset.threshold === threshold)));
}

document.querySelectorAll("[data-threshold]").forEach((button) => button.addEventListener("click", () => renderSimilarity(button.dataset.threshold)));

renderCell();
renderStage("source");
renderSimilarity("0.70");
