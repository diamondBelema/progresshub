# Progress Hub v2 — Design System & Direction

This document is the single source of truth for UI work on Progress Hub. It covers what
exists today (so you don't redesign blind) and where the design should go (so changes add
up to one coherent product instead of a pile of one-off improvements). Read it before
touching `app/components/ui.py` or any page/component file.

If you change a token or variant, update this file in the same commit. If this file and
the code disagree, the code is probably stale — fix the code to match this file, not the
other way around.

---

## 1. What this product is

Progress Hub is a **goal commitment tracker**, not a habit app and not a journaling app.
The mechanism that makes it work: you name a number (50,000 words, ₦200,000, 30 runs),
a deadline, and a commitment statement. The product's only job is to make breaking that
promise feel harder than keeping it — daily targets that adapt when you fall behind,
milestone rewards you picked yourself, an optional public page, an optional accountability
partner, and a leaderboard that rewards showing up over starting strong.

Everything in this UI should reinforce **stakes and motion**: numbers ticking toward a
deadline, visible consequences for slipping, visible proof of momentum. Avoid anything
that reads as a soft, ambient "wellness app" feeling — that's a different product.

Audience: students and early-career builders (the product's own first users), tracking
things like word counts, savings targets, workout volume, study hours. Mobile-first; most
check-ins happen on a phone between other things, so the check-in flow is the most
performance-critical screen in the app.

---

## 2. Current state (as of this audit)

**Stack:** FastAPI + HTMY (Python components, not JSX) + FastHX, server-rendered, HTMX for
interactivity. Tailwind CSS utility classes, compiled (not CDN). No JavaScript framework.

**The "design system" today is `app/components/ui.py`.** It explicitly replaces an earlier
`fasttailwind` token library — that library is *not* wired into this app. There is no
design-token layer between components and raw Tailwind class names. This is the main
structural gap: colors, radii, and spacing are hardcoded into variant dictionaries inside
`ui.py` rather than defined once and referenced everywhere. Section 4 covers this.

### Current tokens (literal values in `ui.py` today)

```python
# Spacing scale (maps semantic names -> Tailwind spacing units)
SPACING = { none: 0, xs: 1, sm: 2, md: 4, lg: 8, xl: 12, "2xl": 20 }

# Radius scale
RADIUS = { sm: rounded-lg, md: rounded-xl, lg: rounded-2xl, full: rounded-full }
```

### Current palette (Tailwind defaults, used directly — not a designed palette)

| Role | Class | Hex (approx) |
|---|---|---|
| Background | `bg-zinc-950` | `#09090b` |
| Surface (default card) | `bg-zinc-900` | `#18181b` |
| Surface (elevated card) | `bg-zinc-800` | `#27272a` |
| Border | `border-zinc-800` / `border-zinc-700` | `#27272a` / `#3f3f46` |
| Text primary | `text-zinc-50` / `text-zinc-100` | `#fafafa` / `#f4f4f5` |
| Text muted | `text-zinc-400` / `text-zinc-500` | `#a1a1aa` / `#71717a` |
| Accent / brand | `violet-500/600` | `#8b5cf6` / `#7c3aed` |
| Success | `emerald-400/500` | `#34d399` / `#10b981` |
| Warning | `amber-400/500` | `#fbbf24` / `#f59e0b` |
| Danger | `red-400/500/600` | `#f87171` / `#ef4444` / `#dc2626` |
| Info | `blue-400/500` | `#60a5fa` / `#3b82f6` |

This is **stock Tailwind zinc + violet**, the default dark-mode palette every Tailwind
starter ships with. It's clean and legible but carries zero brand identity — swap the
`violet-` for `indigo-` or `sky-` and nothing about this would feel like a different
product. Section 5 proposes a real palette.

### Current typography

- Display/body font: **Inter** (Google Fonts, weights 300–700), loaded for the whole app.
- Mono font: **JetBrains Mono** (400, 500), loaded but only referenced via `font-mono`
  utility on numbers — used well already (progress %, amounts, dates) and worth keeping.
- No type scale beyond Tailwind's default `text-xs` → `text-6xl` steps. `Heading` maps a
  `size` prop to a Tailwind size class and picks an HTML tag (`h1`–`h4`); `Text` maps a
  smaller set. There's no defined scale ratio, no display-specific tracking/leading rules
  beyond `leading-snug`/`leading-relaxed` flat defaults.

### Current components (`app/components/ui.py`)

`Button`, `Card`, `Badge`, `Alert`, `Toast`, `Spinner`, `EmptyState`, `ProgressBar`,
`TextField`, `Select`, `Heading`, `Text`, `Label`, `Caption`, `Row`, `Column`, `Stack`,
`Grid`, `Divider`, `Spacer`, `FormField`. Each is a Python class with an `htmy()` method
that returns Tailwind-classed HTML. Variants are plain dicts keyed by string (`variant:
"primary" | "secondary" | "ghost" | "danger"`, etc.) — easy to read, easy to extend, no
build step. **Keep this pattern.** Don't introduce a CSS-in-JS or component-library
dependency; the constraint is deliberate (see product history — Tailwind CDN and
duplicate-head bugs were already fixed once, don't reintroduce build complexity).

### Known UI gaps (not bugs, just unfinished — fix as part of any UI pass)

- No favicon, no OG/social preview meta tags.
- No loading state pattern beyond `Spinner` sitting hidden in two auth forms — HTMX
  requests elsewhere (status changes, check-in submit) have no visible pending state.
  HTMX ships `htmx-request` / `htmx-settling` classes for free; nothing currently styles
  them.
- No dark/light toggle — fine, this product should likely stay dark-only (see Section 5),
  but that should be a stated decision, not an omission.
- No 404 / error page styling — unhandled errors currently fall through to FastAPI's
  default response, not a themed page.
- `ProgressBar` component exists in `ui.py` but the actual goal/dashboard progress bars
  are hand-rolled `html.div` pairs repeated in `goal_card.py`, `goal_progress.py`,
  `public_goal.py`, and `dashboard/widgets.py` instead of using the component. Consolidate
  to one `ProgressBar` usage — today a global tweak (e.g. adding a gradient fill, a
  shimmer-on-update animation) requires editing four files instead of one.
- `TrajectoryChart` in `dashboard/widgets.py` is a hand-built CSS bar chart (flex columns
  with `style="height: x%"`). It works but has no axis labels, no value-on-hover, and bars
  can look identical at a glance when values are close. Fine as v1; flag as the first
  thing to upgrade if check-in history becomes a bigger part of the product story.

---

## 3. Design principles for this product

These are the rules any UI change should be checked against, in priority order.

1. **The number is the hero.** On every screen that shows progress (dashboard cards, goal
   detail, public page, check-in form), the achieved/target numbers and the percentage are
   the largest, highest-contrast things on the screen. Everything else — labels, badges,
   metadata — is supporting cast. If a redesign makes a badge or icon visually louder than
   the number, that's a regression.
2. **Mono for anything that counts, sans for anything that explains.** This convention
   already exists (`font-mono` on percentages/amounts) and is correct — extend it
   consistently rather than introducing a third typeface or abandoning it under time
   pressure.
3. **Status has one honest color, always.** Active = success green, Paused = warning
   amber, Completed = info blue, Abandoned = danger red. Don't let any other UI element
   borrow these colors for unrelated meaning (e.g. don't use amber for "AI is thinking" —
   pick a neutral or violet treatment for that instead) or status communication gets
   muddy.
4. **Motion signals consequence, not decoration.** A progress bar filling, a milestone
   badge lighting up, a streak counter incrementing — these moments are the product's
   emotional payoff and deserve a real transition (300–500ms, ease-out). Hover states on
   static chrome (nav links, secondary buttons) should be fast and quiet (150ms) so they
   don't compete for attention with the moments that matter.
5. **Forms are obstacles; minimize the time between intent and submit.** The goal-setup
   simplification (24 fields → 5 visible + collapsed advanced section) is the right
   direction — apply the same instinct everywhere. The check-in form in particular should
   be answerable one-handed in under 15 seconds for a returning user.
6. **Empty and broken states are in-voice, not generic.** "No goals yet" / "No check-ins
   recorded yet" currently read like placeholder text. Section 6 has rewrite suggestions —
   the interface should sound like the coach/guide/friend tone the product already lets
   users pick during onboarding, not like a neutral system message.

---

## 4. Structural fix: introduce a real token layer

Before any visual reskinning, separate **tokens** (what the values are) from
**components** (how they're applied). Right now they're the same dictionaries in the same
file, which means changing the brand accent color means hunting through six variant maps
across `ui.py`, plus hardcoded color classes sprinkled directly in `dashboard/widgets.py`,
`goal_progress.py`, `goal_card.py`, `public_goal.py`, and `navbar.py`.

Concretely:

1. Move color, spacing, radius, and type-scale values into `app/theme/colors.py`,
   `app/theme/typography.py`, `app/theme/theme.py` (currently empty stub files — this is
   what they were always meant to hold). These should export plain Python dicts/constants,
   no new dependency.
2. `ui.py`'s variant maps (`_BUTTON_VARIANTS`, `_CARD_VARIANTS`, etc.) should build their
   class strings from those constants, not from hardcoded `"bg-violet-600"` literals.
3. Every hand-rolled progress bar / status-color lookup outside `ui.py` should either call
   the existing `ProgressBar` / `Badge` components, or import the same constants — never
   restate a hex-adjacent Tailwind class inline in a page or feature component.
4. Update `app/components/_safelist.py` if new dynamic classes are introduced — anything
   built via string interpolation (`f"bg-{color}-500"`) won't be picked up by Tailwind's
   static scanner and must be added explicitly, the same way the existing grid/spacing
   classes are.

This is a refactor, not a redesign — it should produce **zero visual change** on its own.
Do it first so the actual redesign (Section 5) only has to change values in three small
files instead of touching every component and page.

---

## 5. Design direction: where this should go

The current look is competent stock dark-mode Tailwind. It is not wrong, but it is not
*this product* — it would work unchanged for a budgeting app, a habit tracker, or a CRM.
The brief gives us real material to design from: **commitment, deadlines, stakes,
milestones, a contract you sign with yourself.** Lean into that vocabulary instead of
generic SaaS-dashboard chrome.

### Direction: "Ledger" — a commitment kept like a contract, tracked like a ledger

**Why this fits:** the product's actual mechanic is a personal contract (the commitment
statement, literally called a "contract" in the UI copy) with milestones paid out like an
installment plan. A ledger/contract visual language — precise rules, tabular numbers,
ruled dividers, a stamped/signed feeling at completion — is native to that idea, distinct
from the soft-card SaaS look every dashboard defaults to, and still entirely achievable in
Tailwind with no new build tooling.

**Palette** (replace stock zinc/violet with a warmer, more deliberate set):

| Role | Token name | Hex | Notes |
|---|---|---|---|
| Background | `ink-950` | `#0B0D10` | Slightly blue-black, not pure zinc — less generic than `#09090b` |
| Surface | `ink-900` | `#14171C` | Card/panel background |
| Surface raised | `ink-800` | `#1C2026` | Elevated card, modal |
| Border / rule | `ink-700` | `#2A2F37` | Replaces zinc borders — slightly warmer |
| Text primary | `paper-50` | `#F2F0EA` | Warm off-white, not pure white — reads like paper, not a phone screen |
| Text muted | `paper-400` | `#8B8A85` | Desaturated warm gray |
| Accent (brand/commitment) | `signal-500` | `#C9A646` | Muted gold — "contract signed," milestone, commitment statement border. Replaces violet as primary brand color. |
| Accent bright (interactive) | `signal-400` | `#E0C36B` | Hover/active state for the gold accent |
| Progress / momentum | `pulse-500` | `#3FA37D` | A deliberately different green from "success" — used specifically for progress bars and trajectory bars so "things are moving" reads distinctly from "this is correct/done" |
| Success / Active status | `mint-400` | `#5FCB94` | Status badge only |
| Warning / Paused status | `amber-400` | `#E5A94B` | Keep close to current amber — already correct semantically |
| Danger / Abandoned status | `rose-500` | `#D1495B` | Slightly warmer than stock red, fits the palette |
| Info / Completed status | `slate-400` | `#7C93A8` | Cool, deliberately quiet — "completed" is calm, not exciting |

This is 4–6 named hues plus status colors, not a full Tailwind palette swap — `signal`
(gold) becomes the one accent that means "commitment, milestone, the contract," and
`pulse` (green, distinct from `mint` success-green) becomes the one accent that means
"motion, today's progress." Two different greens sound redundant on paper but solve a real
problem: today, the same `violet-500` is used for the brand color, primary buttons, *and*
progress bars, which means "this is a button" and "this is 40% done" look like the same
kind of thing. Separating brand/commitment (gold) from progress/motion (green) from status
(mint/amber/rose/slate) gives each color exactly one job, per Principle 3.

**Typography:**

- Keep **Inter** for body text — it's a fine, neutral choice for a data-dense product and
  changing it isn't worth the risk for this brief.
- Replace the implicit "everything is Inter at different sizes" with a real display
  treatment for the few moments that should feel like a signature: the landing page H1,
  the big percentage on the goal detail page, and the milestone-reached moment. Use a
  serif with some editorial weight — something like **Fraunces** or **Source Serif 4**
  (both on Google Fonts, both free) at a heavy weight, set tight. The contrast between a
  serif "contract" headline and the mono "ledger" numbers is the typographic version of
  the Ledger concept: a promise written in serif, a result tallied in mono.
- Keep **JetBrains Mono** for all numeric data — percentages, amounts, dates, day counts.
  Extend its use to anywhere a number currently renders in Inter (e.g. `Caption` text that
  includes a count).
- Type scale: define one explicit ratio (1.25, "major third") from a 16px base instead of
  reaching for whatever Tailwind size class looks about right per component. Document the
  resulting scale in `app/theme/typography.py` once chosen.

**Layout / signature element:**

- Replace the plain progress bar (a single flat-colored rounded rect) with a **ledger-tick
  bar**: same filled-bar mechanic, but with thin tick marks at 25/50/75/100 baked into the
  track itself (not just badges below it), so the bar visually resembles a ruler being
  filled in rather than a generic loading bar. This is the one "signature" element per the
  design process (Section 2 of the studio brief) — spend the visual risk here, keep
  buttons/cards/badges quiet and disciplined elsewhere.
- Milestone badges (25/50/75/100%) currently render as small pills below the bar. Treat
  reached milestones as **stamped**, not just colored — a subtle rotation (-2deg), a
  border instead of a fill, something that reads as "stamped onto the ledger" rather than
  "this chip is now green." Keep it restrained: one visual idea, not a sticker explosion.
- Commitment statement card: already visually distinct (italic, violet text) — keep that
  instinct, restate in the new palette (gold-bordered card, serif heading "Commitment
  contract," the statement itself in a slightly larger serif italic, like a pull-quote
  from a signed document).
- Dashboard trajectory chart: keep the bar-chart shape (it's legible and on-brand for
  "ledger") but add baseline rule + value labels on hover/tap, and switch the fill from
  brand-violet to the new `pulse` green so it visually separates from buttons/links.

**Motion:**

- Milestone crossed (25/50/75/100%): this is the single moment worth an orchestrated
  animation per Principle 4 — bar fill animates to the new percentage (500ms ease-out),
  then the newly-reached badge does a brief scale-up + settle (150ms scale to 1.08, back to
  1.0). Don't animate anything else on that page at the same time, so this moment reads as
  deliberate.
- Page-level transitions: none needed. This is a server-rendered, HTMX-swapped app —
  resist the urge to add page-transition libraries. A `fade-in` on `htmx-settling` for
  swapped fragments (150ms opacity) is enough to avoid jarring pop-in.
- Respect `prefers-reduced-motion` globally — disable the milestone animation and fall
  back to an instant state change when set.

### What not to do

- Don't add a second accent hue beyond gold + green. Two purposeful accents on top of a
  warm neutral base is already a lot for a utility product used daily; a third will start
  competing for attention with the numbers (Principle 1).
- Don't round every corner more aggressively as a default "modernization" — the current
  `rounded-xl`/`rounded-2xl` scale is fine. A ledger/contract concept benefits from slightly
  *less* roundness on structural elements (cards, dividers) than a typical SaaS app, not
  more. Reserve fuller rounding (`rounded-full`) for pills/badges/avatars only, as today.
- Don't introduce illustration, gradients-as-decoration, or stock photography. The hero
  section currently has a gradient placeholder block (`hero-glow` class in
  `pages/landing.py`) standing in for a real visual — replace it with an actual product
  shot (a real goal-detail screen, post-redesign) or a constructed ledger/contract motif,
  not a generic gradient blob.

---

## 6. Copy direction

A few concrete rewrites to set the tone — apply this voice anywhere new copy is written.

| Context | Current | Direction |
|---|---|---|
| Empty goals list | "No goals yet" / "Create your first goal and start making real progress." | "Nothing on the ledger yet." / "Name a number, set a deadline, sign the contract." |
| Empty check-in history | "No check-ins recorded yet." | "The ledger's empty. Log today's number to start the trail." |
| Login error | "Invalid email or password" | Keep as-is — this is a system message, plain and factual is correct here per Principle 6 (errors don't apologize, aren't vague, but also don't need personality). |
| Weekly review nudge | "You haven't logged in a few days. Take a moment to reflect..." | Keep the instinct, tighten: "Three days quiet. Check the contract, log today, or adjust the target — but don't let it go unanswered." |
| Milestone reward reached | (currently just a badge: "Reward: Coffee") | Consider a one-line acknowledgment alongside the badge: "25% kept. Cash it in: Coffee." — ties the number to the promise instead of presenting the badge as decoration. |

Buttons already follow active-voice + persistent-vocabulary correctly ("Log progress",
"Make public", "Mark complete") — keep that pattern for any new actions. Name the button
for exactly what happens, and don't rename the concept on the confirmation screen (e.g. a
"Make public" button shouldn't lead to a toast that says "Visibility updated" — it should
say "Now public").

---

## 7. Implementation checklist for whoever picks this up

1. Read Section 4 first. Extract tokens into `app/theme/*.py` before changing any visual
   value. Verify zero visual diff after the extraction (this is a refactor commit).
2. Update `app/theme/colors.py` with the Section 5 palette. Update `_BUTTON_VARIANTS`,
   `_CARD_VARIANTS`, `_BADGE_VARIANTS`, `_INPUT_VARIANTS`, `_ALERT_VARIANTS`,
   `_TOAST_VARIANTS` in `ui.py` to reference the new tokens instead of literal Tailwind
   color classes.
3. Add the serif display font (Fraunces or Source Serif 4) to `document.py`'s font link,
   alongside the existing Inter/JetBrains Mono import. Apply it only to: landing H1,
   goal-detail big percentage, milestone-reached moment. Do not apply it to body Heading
   instances broadly.
4. Build the ledger-tick progress bar as a new variant on the existing `ProgressBar`
   component in `ui.py` (don't fork it into a new component) and migrate the four
   hand-rolled progress-bar instances (`goal_card.py`, `goal_progress.py`,
   `public_goal.py`, `dashboard/widgets.py`) to use it.
5. Re-skin status badges and milestone badges with the new palette; add the stamped-badge
   treatment for reached milestones in `goal_progress.py`.
6. Update `_safelist.py` with any new dynamically-built classes before assuming Tailwind
   will pick them up.
7. Apply Section 6 copy changes to `goal_list.py` (EmptyState), `goal_progress.py`
   (check-ins empty state, weekly review prompt), `_milestone_rewards_list`.
8. Sweep the gaps in Section 2: add favicon + OG tags to `document.py`, style
   `htmx-request`/`htmx-settling` classes globally for pending-state feedback, build a
   themed 404/error fallback, replace the landing-page `hero-glow` gradient placeholder.
9. Test at 375px width (the product is mobile-first) before testing desktop. Check the
   check-in form specifically for one-handed thumb reach on real device widths.
10. Respect `prefers-reduced-motion` for the milestone animation from day one, not as a
    follow-up.

Do not start a parallel component library, do not add a CSS framework beyond Tailwind, and
do not introduce a JS framework. Every constraint above is deliberate, not a placeholder
for "do this properly later."
