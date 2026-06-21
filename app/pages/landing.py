from __future__ import annotations

from app.components.ui import Button, Card, Grid, Heading, Text, Badge, Row, Stack, Divider
from app.components.layout.document import Document
from htmy import html

STEPS = [
    ("1", "Define your goal", "Name your target, category, and deadline. Set milestone rewards and write your personal commitment contract."),
    ("2", "Commit publicly", "Make your goal visible. Invite an accountability partner. Your commitment statement anchors your motivation."),
    ("3", "Log & adapt", "Check in daily with a tap. The AI reshuffles your plan when life gets in the way. Track blockers and energy."),
    ("4", "Level up", "Earn milestone badges, climb the leaderboard, and let Goal DNA calibrate your next challenge."),
]

FEATURES = [
    ("Commitment contracts", "Write a personal promise. Set milestone rewards (coffee at 25%, movie at 50%). Read it when motivation dips."),
    ("Accountability partner", "Invite a partner via email. Your shared goal progress keeps both of you on track."),
    ("Public progress pages", "Make any goal public. Share your live progress page with friends, mentors, or social media."),
    ("Leaderboard", "Opt in to anonymous rankings by category. Consistency score measures who shows up, not who started strongest."),
    ("Goal DNA", "After 3+ check-ins, see your pace profile, top blockers, best environment, and calibrated suggestions for your next goal."),
    ("Milestone badges", "Cross 25%, 50%, 75%, 100% and unlock your pre-set rewards. Each milestone is a celebration."),
    ("Adaptive AI planning", "Miss a day? The plan reshuffles. Your deadline stays intact. No guilt, just progress."),
    ("Energy & blocker tracking", "Log your energy level and what blocked you. Pattern detection surfaces actionable insights over time."),
    ("Weekly review prompts", "The system nudges you to reflect when you\u2019ve been quiet for a few days. Never drift off course."),
]

TESTIMONIALS = [
    ("\u201cThe commitment contract tricked my brain into taking this seriously. I hit 75% and treated myself to that dinner I promised.\u201d", "Sarah K., Design Student"),
    ("\u201cHaving a public goal page keeps me honest. My mentor checks in without me having to send updates.\u201d", "James L., CS Major"),
    ("\u201cGoal DNA told me I work best in the morning with no phone. That one insight changed my entire routine.\u201d", "Priya M., PhD Candidate"),
]


def _hero_goal_card():
    """Constructed goal-detail illustration for the hero section."""
    return html.div(
        html.div(
            # Goal header
            html.div(
                html.div(
                    html.div("62%", class_="text-4xl font-bold font-mono text-paper-50"),
                    html.span("Active", class_="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-mint-400/10 text-mint-400 border border-mint-400/20"),
                    class_="flex items-center gap-3 mb-3",
                ),
                html.h3("Save for a trip to Japan", class_="text-lg font-semibold text-paper-50 mb-1"),
                html.p("31,000 / 50,000 naira", class_="text-sm text-paper-400 font-mono"),
                class_="mb-4",
            ),
            # Progress bar with ledger ticks
            html.div(
                html.div(class_="ledger-tick left-[25%]"),
                html.div(class_="ledger-tick left-[50%]"),
                html.div(class_="ledger-tick left-[75%]"),
                html.div(style="width: 62%", class_="h-full bg-pulse-500 rounded-full transition-all duration-500"),
                class_="w-full h-3 bg-ink-700 rounded-full overflow-hidden ledger-track mb-3",
            ),
            # Milestone badges
            html.div(
                html.span("25%", class_="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-mint-400/10 text-mint-400 border border-mint-400/20 milestone-stamp-reached"),
                html.span("50%", class_="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-mint-400/10 text-mint-400 border border-mint-400/20 milestone-stamp-reached"),
                html.span("75%", class_="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-ink-700/50 text-paper-400 border border-ink-600/50"),
                html.span("100%", class_="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-ink-700/50 text-paper-400 border border-ink-600/50"),
                class_="flex gap-2 mb-4",
            ),
            # Commitment contract
            html.div(
                html.p("\u201cI will save consistently so I can experience Japan by spring.\u201d", class_="text-signal-300 italic text-sm font-display"),
                class_="border-l-2 border-signal-500/30 pl-3 mb-4",
            ),
            # Recent check-ins
            html.div(
                html.div(
                    html.span("+5,000 naira", class_="text-mint-400 font-medium text-sm font-mono"),
                    html.span("Day 14", class_="text-paper-500 text-xs"),
                    class_="flex justify-between items-center py-1.5 border-b border-ink-700/50",
                ),
                html.div(
                    html.span("+3,500 naira", class_="text-mint-400 font-medium text-sm font-mono"),
                    html.span("Day 13", class_="text-paper-500 text-xs"),
                    class_="flex justify-between items-center py-1.5 border-b border-ink-700/50",
                ),
                html.div(
                    html.span("+4,200 naira", class_="text-mint-400 font-medium text-sm font-mono"),
                    html.span("Day 12", class_="text-paper-500 text-xs"),
                    class_="flex justify-between items-center py-1.5",
                ),
                class_="text-sm",
            ),
            class_="bg-ink-900 border border-ink-700 rounded-2xl p-6 hero-glow",
        ),
        class_="max-w-lg mx-auto",
    )


def landing_page():
    return Document(
        "Progress Hub \u2014 Goal Commitment Tracker",
        html.nav(
            html.div(
                html.a(
                    html.span("Progress Hub", class_="text-xl font-semibold text-paper-50 tracking-tight"),
                    href="/",
                    class_="flex items-center gap-2",
                ),
                html.div(
                    html.a("Features", href="#features", class_="text-sm text-paper-400 hover:text-paper-50 transition-colors"),
                    html.a("How it works", href="#how", class_="text-sm text-paper-400 hover:text-paper-50 transition-colors"),
                    html.a("Log in", href="/auth/login", class_="text-sm text-paper-200 hover:text-paper-50 transition-colors"),
                    Button("Get started", variant="primary", size="sm", hx_get="/auth/signup", hx_target="body", hx_push_url="true"),
                    class_="hidden md:flex items-center gap-4",
                ),
                html.button(
                    html.span("\u2630", class_="text-xl"),
                    type="button",
                    class_="md:hidden text-paper-400 hover:text-paper-50 p-2",
                    **{"onclick": """
                        const menu = document.getElementById('landing-mobile-menu');
                        const icon = this.querySelector('span');
                        const isOpen = menu.classList.toggle('hidden');
                        icon.textContent = isOpen ? '\u2630' : '\u2715';
                    """},
                ),
                class_="flex items-center justify-between max-w-6xl mx-auto px-6 py-4",
            ),
            html.div(
                html.a("Features", href="#features", class_="block px-4 py-2.5 text-sm rounded-lg text-paper-400 hover:text-paper-50 hover:bg-ink-800/50 transition-colors"),
                html.a("How it works", href="#how", class_="block px-4 py-2.5 text-sm rounded-lg text-paper-400 hover:text-paper-50 hover:bg-ink-800/50 transition-colors"),
                html.a("Log in", href="/auth/login", class_="block px-4 py-2.5 text-sm rounded-lg text-paper-400 hover:text-paper-50 hover:bg-ink-800/50 transition-colors"),
                html.a("Get started", href="/auth/signup", class_="block px-4 py-2.5 text-sm rounded-lg text-signal-400 hover:text-signal-300 hover:bg-ink-800/50 transition-colors"),
                id="landing-mobile-menu",
                class_="hidden md:hidden max-w-6xl mx-auto px-6 pb-4 space-y-1",
            ),
            class_="border-b border-ink-700 bg-ink-950/80 backdrop-blur-sm sticky top-0 z-50",
        ),
        Stack(
            html.section(
                Stack(
                    Badge("v2 \u2014 Commitment tracking is here", variant="info"),
                    html.h1(
                        "Make a promise. ",
                        html.span("Keep it.", class_="gradient-text"),
                        class_="text-5xl md:text-6xl font-bold tracking-tight text-paper-50 leading-tight font-display",
                    ),
                    Text(
                        "Not another habit tracker. Progress Hub is a goal commitment system: "
                        "write a contract, invite a partner, earn milestones, and let AI "
                        "replan your path when life gets messy.",
                        muted=True, size="lg",
                        class_="max-w-2xl mx-auto",
                    ),
                    Row(
                        Button("Get started free", variant="primary", size="lg", hx_get="/auth/signup", hx_target="body", hx_push_url="true"),
                        html.a("How it works \u2193", href="#how", class_="inline-flex items-center justify-center font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 px-6 py-3 text-lg gap-2 rounded-xl bg-transparent text-paper-200 hover:bg-ink-800/50 focus:ring-ink-600 transition-all duration-200"),
                        gap="md",
                        align="center",
                    ),
                    html.div(
                        html.div(
                            _hero_goal_card(),
                            class_="relative z-10",
                        ),
                        class_="mt-16 rounded-2xl overflow-hidden max-w-4xl mx-auto w-full",
                    ),
                    align="center",
                    class_="text-center pt-20 pb-16 px-4",
                ),
                class_="max-w-6xl mx-auto",
            ),

            html.section(
                Stack(
                    Heading("How it works", size="3xl", class_="text-center"),
                    Text("Define, commit, log, level up. Four steps to your first milestone.", muted=True, size="lg", class_="text-center"),
                    html.div(class_="h-8"),
                    Grid(
                        *[
                            Card(
                                html.div(
                                    html.span(num, class_="text-3xl font-bold text-signal-400 font-mono"),
                                    class_="mb-4",
                                ),
                                Heading(title, size="lg"),
                                Text(desc, muted=True),
                                variant="elevated", padding="lg",
                                class_="h-full",
                            )
                            for num, title, desc in STEPS
                        ],
                        cols={"base": 1, "md": 2, "lg": 4},
                        gap="lg",
                    ),
                    align="center",
                ),
                class_="py-16 px-6 max-w-6xl mx-auto",
                id="how",
            ),

            html.section(
                Stack(
                    Heading("Everything you need", size="3xl", class_="text-center"),
                    Text("Accountability, insights, and celebration baked into every goal.", muted=True, size="lg", class_="text-center"),
                    html.div(class_="h-8"),
                    Grid(
                        *[
                            Card(
                                Heading(title, size="md"),
                                Text(desc, muted=True),
                                variant="ghost", padding="lg",
                                class_="h-full border-ink-700/80",
                            )
                            for title, desc in FEATURES
                        ],
                        cols={"base": 1, "md": 2, "lg": 3},
                        gap="md",
                    ),
                    align="center",
                ),
                class_="py-16 px-6 max-w-6xl mx-auto",
                id="features",
            ),

            html.section(
                Stack(
                    Heading("What people are saying", size="2xl", class_="text-center"),
                    Text("Early users are already hitting milestones.", muted=True, class_="text-center"),
                    html.div(class_="h-6"),
                    Grid(
                        *[
                            Card(
                                Text(quote, muted=True, size="sm", class_="italic leading-relaxed"),
                                Text(f"\u2014 {author}", size="xs", class_="text-paper-500 mt-4"),
                                variant="default", padding="lg",
                            )
                            for quote, author in TESTIMONIALS
                        ],
                        cols={"base": 1, "md": 3},
                        gap="lg",
                    ),
                    align="center",
                ),
                class_="py-16 px-6 max-w-5xl mx-auto",
            ),

            html.section(
                Card(
                    Stack(
                        Heading("Ready to make a real promise?", size="3xl"),
                        Text("Join early users who are committing to goals that matter. Free during beta.", muted=True, size="lg"),
                        Button("Create your account", variant="primary", size="lg", hx_get="/auth/signup", hx_target="body", hx_push_url="true"),
                        gap="md",
                        align="center",
                        class_="text-center py-8",
                    ),
                    variant="elevated", padding="2xl",
                    class_="max-w-3xl mx-auto",
                ),
                class_="py-16 px-6",
            ),

            Divider(margin="lg"),
            html.footer(
                Row(
                    Text("Built with FastAPI, HTMY & Python", muted=True, size="sm"),
                    Text("\u00a9 2026 Progress Hub", muted=True, size="sm"),
                    justify="between",
                    class_="max-w-6xl mx-auto px-6 py-8",
                ),
            ),

            gap="none",
        ),
    )
