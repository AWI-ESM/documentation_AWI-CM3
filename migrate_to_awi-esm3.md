# Migrating this documentation to the AWI-ESM3 model family

Status: planned, 2026-07-31. Phases 0 to 5 below; check off as they land.

## The problem

This repository documents AWI-CM3. The model has become a family:

- `AWI-CM3` v3.0 through v3.4.2, still runnable and still supported.
- `AWI-ESM3` v3.4.x, which is AWI-CM3 plus LPJ-GUESS.
- `AWI-ESM3-*-cc` in development, adding REcoM ocean biogeochemistry and a CO2 tracer in OpenIFS.
- `AWI-ESM3-*-is` in development, adding PISM ice sheet coupling (orography, SMB, moving cavity, icebergs) and dEBM.

At v3.5 and v3.6 all of `AWI-CM3-v3.5`, `AWI-CM3-v3.6`, `AWI-ESM3-v3.5`, `AWI-ESM3-v3.6`, `AWI-ESM3-v3.5-cc`, `AWI-ESM3-v3.6-cc`, `AWI-ESM3-v3.5-is` and `AWI-ESM3-v3.6-is` exist side by side, on top of the AWI-CM3 versions back to v3.0 that must stay documented.

## Decision: one repository, one build, no fork

esm_tools forks exactly once and gates everything after that, and the documentation should mirror that shape.

- The one fork is on component set: `configs/setups/awicm3/awicm3.yaml` and `configs/setups/awiesm3/awiesm3.yaml` are separate setups, because AWI-ESM3 contains LPJ-GUESS and AWI-CM3 does not.
- Everything below that is a feature gate inside a single YAML. `develop-cc` and `develop-is` are `choose_version` entries in `awiesm3.yaml`, selecting different `couplings:` strings and flipping `with_co2_tracer`, `with_co2_oce_coupling`, `with_co2_veg_coupling`. `interactive_mesh` is documented in that file as a feature switch that is explicitly not version tied.

Four reasons not to fork the docs:

1. **Forking would model a structure the code does not have.** The reader is editing one `awiesm3.yaml`. Documentation split across four sites tells them there are four models to keep straight, when there is one config with flags in it.
2. **The maintenance budget cannot absorb it.** 23 commits in two years, essentially one maintainer. Four repositories means four times the merge work, and the predictable outcome is three stale copies and one live one, with no way for a reader to tell which is which.
3. **The content is component scoped, not setup scoped.** Twelve of the thirteen sections in `how_to.rst` describe how OpenIFS, FESOM, OASIS or XIOS behaves, and are word for word identical in every setup containing that component. Forking duplicates exactly the material that never differs, including the traps, which are the most valuable and the most expensive to update.
4. **The mixing already happened.** `how_to.rst` documents branching off an LPJ-GUESS restart, in a repository called `documentation_AWI-CM3`, for a component AWI-CM3 does not contain. Single sourcing is already in use; it is just not declared anywhere.

## Decision: gate by feature, not by model name

Because `with_co2_tracer` and `interactive_mesh` are independent booleans, a combined `-cc-is` is already expressible in the config even though nobody plans to build one. If pages are named `carbon_cycle` and `ice_sheet` rather than `awiesm3-cc` and `awiesm3-is`, that hypothetical costs one line on the family page and no page rewrites. If pages are named after the variants, it costs a fifth copy of everything.

The convention: any section that is not universal opens with a single line starting `Applies to:`.

```
Applies to: any setup with LPJ-GUESS (AWI-ESM3 v3.4 and later).
```

Absence of the line means the section applies everywhere. This is prose, so it stays inside the house style, it is greppable, and it still reads correctly for someone who lands on the section from a search engine. Conditional builds via `.. only::` were rejected: they are a fork wearing a different hat, and they hide from each reader what the other variants do.

The docs already gate informally in section headings, for example `Control Aerosol Scaling (AWI-CM3 v3.2 and v3.3)` and `OpenIFS cy43r3 (AWI-CM3 v3.2 and below)`. Migrate those to the `Applies to:` line rather than inventing a second mechanism next to them.

## Decision: curated guides only, not an issue database

Open, specific, closing problems belong in GitHub issues and must not come here. This documentation carries only permanent, class level knowledge.

The test before anything lands: **would this still be true in two years, and will a new user hit it without doing anything wrong?** Both yes, it is a curated guide. Otherwise it is a ticket.

Concretely, "run 26555148 aborted in `spinup_couplePI`" is an issue. "`interactive_mesh: true` is accepted on any awiesm3 version but silently does nothing unless the coupling string also carries PISM" is a doc entry: it never closes, a fresh user hits it every time, and its whole value is being findable when somebody pastes an error into a search box.

That keeps the pitfalls page at fifteen to twenty entries for the life of the project rather than hundreds.

There is already a separate home for the rest: `AWI-ESM/common-errors`, "Common Runtime Errors and Recommended Fixes", public, last touched August 2024. The pitfalls page links out to it rather than absorbing it or competing with it. Whether that repository gets revived is a decision to take before phase 5, because if it stays dormant the pressure to dump errors into the documentation comes straight back.

`known_errors.rst` and `pitfalls_and_solutions.rst` are both empty stubs and the distinction between them was never defined. They merge into one page, because keeping two invites exactly the sprawl this rule exists to prevent.

## Decision: rename, and migrate the Read the Docs project

The GitHub organisation is already `AWI-ESM`; every `github.com/AWI-CM3/...` link in the docs is surviving on GitHub's org rename redirect and should be updated.

**Repository rename is safe, and is done.** `AWI-ESM/documentation_AWI-CM3` is now `AWI-ESM/documentation`. GitHub issues permanent redirects for renamed repositories, covering both web URLs and `git remote` fetches, so no clone breaks. The redirect only dies if somebody later creates a new repository under the old name.

The unqualified name works because the organisation already carries the model name, and because "AWI-ESM3" reads as the generation rather than as one configuration in it. That is the same convention as MPI-ESM, CESM and NorESM, all of which name the family at the ESM level and carry atmosphere ocean only configurations underneath without a separate documentation site. AWI-CM3 is the AOGCM configuration of generation 3, sharing one version line, v3.0 through v3.6, and one esm_tools release cadence with AWI-ESM3. The family page should say so in those words, because that framing is what makes the repository and site names honest.

**Read the Docs does not support renaming a project slug.** It has been declined for years, precisely because every existing URL would break (readthedocs/readthedocs.org#5836). The supported migration is:

1. Import a new project `awi-esm3` from the same repository.
2. Reduce the old `awi-cm3-documentation` project to a stub with a single `index.rst`.
3. Add an Exact redirect on the old project: From URL `/*`, To URL `https://awi-esm3.readthedocs.io/:splat`, with **Force Redirect** ticked.
4. Never delete the old project.

Two things bite here, and both did.

The placeholder syntax is `*` in the From URL and `:splat` in the To URL. The older `$rest` form is what most search results still show and it silently does nothing.

Force Redirect is required because the old project keeps serving its last successful build after the webhook is removed. Read the Docs applies redirects only to pages that do not exist, so while every old URL still returns 200 no redirect ever fires. Force Redirect makes it apply to existing pages too, which is exactly the documented case for it. The alternative is deactivating the old project's versions so that everything 404s, but the checkbox is less destructive.

Verify with `curl -s -o /dev/null -w "%{http_code} %{redirect_url}\n" https://awi-cm3-documentation.readthedocs.io/en/latest/how_to.html` rather than in a browser, since browsers cache redirects aggressively. You want a 3xx and a Location on the new domain.

The slug is `awi-esm3` and not `awi-esm3-documentation` because `readthedocs.io` already says documentation, and because the bare model name is what the neighbouring projects use: `fesom2.readthedocs.io` and `esm-tools.readthedocs.io`, which are the ocean component and the framework that installs and runs the model, so a reader is moving between all three. NorESM adds `-docs` and E3SM uses a custom `docs.` subdomain, but neither is in this reader's path. Keep the `3`, because AWI-ESM 1.x and 2.x exist and are ECHAM based, and keep the hyphen, because the published model names carry it.

Doing this now rather than later matters because three papers are due in 2027 and 2028 and will cite a documentation URL. Migrate before those citations are frozen into print.

**On SEO.** The slug is a weak ranking signal; `<title>`, `<h1>` and body text dominate, so once the title says AWI-ESM3 the site ranks for AWI-ESM3 whatever the URL is. The reason to get the slug right is that it goes into three papers, not that it moves rankings. The real risk is running both projects as live builds of the same repository: duplicate content splits ranking signal between them and lets a search engine pick a canonical arbitrarily. The 301 stub avoids that entirely, and 301s pass accumulated authority forward rather than abandoning it. The rule is one live site, always.

## Decision: single `latest` build

No Read the Docs per-version branches. In-page version gating already works in this doc set (`releases.rst` spans v3.0 to v3.4 on one page today), and per-version branches are a fork wearing a different hat, with the same backporting failure mode.

## Citations

Three papers are in preparation: AWI-ESM3 and AWI-ESM3-cc in 2027, AWI-ESM3-is in 2028. AWI-CM3 is Streffing et al. 2022, GMD 15, 6399-6427.

Citation is one more column of the name to components to `esm_master` target mapping, so it lives on the family page rather than in `how_to`. Until each paper lands, the variant gets an explicit "in preparation, cite Streffing et al. 2022 plus the component papers" line rather than silence, so nobody has to guess.

## Out of scope

- `frontiers-xios` is not documented.
- Whether `-cc` and `-is` ever merge is a question for a few years' time. The feature gating means it costs one family page line if it happens.

## Target page tree

```
index                      family landing page, not an AWI-CM3 page
model_family          NEW  the naming rule; name -> components -> esm_master target
                           -> runscript directory -> citation
before_you_start           plus LPJ-GUESS, PISM, dEBM, REcoM licences
quickstart                 one short block per setup; -is needs its own, because it is
                           two runscripts and --coupling-chain, not one command
releases                   split into releases/index plus per-version pages
contribute                 plus the Applies to convention and the two-year test
how_to/               SPLIT by component, which is how it already clusters
  coupling_oasis           lucia, offline weight generation, oasis_reorder
  openifs                  nproc change, SSP/RCP, aerosol scaling, orbital, branch-off
  fesom                    branch-off restart
  lpj_guess                branch-off restart
  carbon_cycle        NEW  REcoM, CO2 tracer, concentration versus emission driven
  ice_sheet           NEW  PISM/dEBM, iterative coupling, moving cavity, icebergs
  xios_output              pressure levels
  debugging                debug flags, per component and per OpenIFS cycle
paleo
workfolder                 stays tabular, restructured per component
pitfalls                   merged from known_errors and pitfalls_and_solutions
```

`how_to.rst` is 514 lines against a healthy maximum of about 287, and `-cc` plus `-is` would push it past 800. The component split is the natural cut and is content preserving.

## How the feature switches actually behave

Checked against esm_tools rather than assumed, because the two variants look inconsistent and are not.

The rule is that a switch which needs a recompile is owned by the version, and a switch which only changes what runs is set in the runscript. The mechanism enforcing it is where the switch is written. `interactive_mesh` is a plain `general` default, so a runscript can override it. The three `with_co2_*` switches are assigned inside every `choose_version` entry, so `choose_version` wins and a runscript cannot override them.

Verified by check-running `awiesm3-develop` with `with_co2_oce_coupling: true` forced in the runscript. The resolved config came back with `with_co2_oce_coupling: False`, `fesom.branch: 2.7.0` rather than the REcoM branch, an empty `recom_comp_flag`, and no `XCO2_oce` coupling field. The runscript value was discarded.

So there is no build against config mismatch to guard against, and nothing structural to fix. What is left is a documentation problem: the setting is accepted and silently ignored, with no message, so somebody asking for the carbon cycle this way gets a clean run without one. That is a pitfalls entry for phase 5, and the answer it should give is to install the `-cc` target instead.

## Phases

### Phase 0: naming and structure (half day)

- [x] Rename the GitHub repository. Now `AWI-ESM/documentation`.
- [x] Rename the default branch from `master` to `main`.
- [x] Update the repository description and the README badge.
- [x] Migrate the Read the Docs project. Now `awi-esm3`, serving at https://awi-esm3.readthedocs.io/, with the old project forced-redirecting to it and verified 301 to 200 end to end.
- [x] Rewrite `index.rst` as a family landing page.
- [x] Write `model_family.rst`, the name to components to target to citation mapping.
- [x] Update `conf.py`: project title, copyright year.
- [x] Record the `Applies to:` convention and the two-year test in `contribute.rst`.
- [x] Fix the stale `github.com/AWI-CM3/...` URLs. Also corrected FESOM2 from GPL-2.0 to GPL-3.0, which was simply wrong.

Open, carried into later phases:

- `before_you_start.rst` says "OASIS4 is available under LGPL" while linking the OASIS3-MCT page, and the model builds `oasis3mct-5.2`. Fix when phase 3 revisits that page for the new component licences.
- `AWI-ESM/common-errors` has been dormant since August 2024 and `contribute.rst` now points people at it. Revive it or pick a different target before phase 5.
- In esm_tools, `awicm3` version `v3.4.1` selects coupling `awicm3_v3.4.0` although `awicm3_v3.4.1` exists. Looks like a typo in that repository, not this one.

### Phase 1: split `how_to` (1 day)

- [ ] Split by component into `how_to/`, moving text verbatim.
- [ ] Prove the rendered output is unchanged: strip tags from the built HTML before and after and diff the text.
- [ ] Add `:ref:` labels so the existing `oasis_reorder` and `orbital_parameters` cross references survive.

### Phase 2: gate everything (1 day)

- [ ] Add `Applies to:` lines to every non-universal section.
- [ ] Migrate the existing in-heading gates to the new form.
- [ ] Audit each section against FESOM 2.7 and OpenIFS 48r1, which most predate.

### Phase 3: per setup entry points (half day)

- [ ] `quickstart.rst`: one block per setup, including the `-is` two runscript `--coupling-chain` form.
- [ ] `before_you_start.rst`: LPJ-GUESS, PISM, dEBM and REcoM licences, and the component list per setup.

### Phase 4: the new pages. Deferred.

- [ ] `how_to/carbon_cycle.rst`.
- [ ] `how_to/ice_sheet.rst`.

Deferred deliberately. Both variants exist only on `develop` so far, neither is released, and neither is described in a paper. Anything written now would document an interface that is still moving, and would be stale before the first reader arrives.

The trigger to start is the v3.5.0 release, at which point the switches and runscripts stop moving, or the papers, expected 2027 for `-cc` and 2028 for `-is`, whichever lands first.

Raw material is already identified and does not need finding again. For `-is`: the moving cavity investigation report at `postprocessing/investigation_awiesm3_moving_cavity_crash/report/moving_cavity_investigation.tex`, 1300 lines with named bugs, a verified switch set, a "what is proven" section and struck-through falsified claims, plus the `crashhunt` and `bisect` runscript families under `pism_repro/scripts_is`. For `-cc`: nothing written down yet beyond the esm_tools plumbing.

When it does start, the filter is the two-year test in the curated-guides decision above. Most of that report is campaign history, bugs found and fixed, which does not belong here. What belongs is whatever is still true for a new user: the switch set they have to set themselves, the bootstrap they cannot produce without the pool directory, and the open limitations.

### Phase 5: ongoing. Not blocked by phase 4.

Both items below concern components that are already released, so they proceed while phase 4 waits. `workfolder.rst` gets its per-component split for OpenIFS, FESOM2, OASIS3-MCT, XIOS and LPJ-GUESS now, and leaves empty slots for PISM and REcoM rather than guessing at file lists that are still changing.


- [ ] Restructure `workfolder.rst` per component, with feature gates, keeping the grid table form.
- [ ] Decide whether `AWI-ESM/common-errors` is revived or retired, since the pitfalls page links to it.
- [ ] Seed the merged `pitfalls.rst` from the `-is` bring-up, applying the two-year test to every candidate, and send everything that fails the test to `common-errors` instead.

Phases 0 to 3 are restructuring and can all land before v3.5 exists.
