"""Verify all components import and instantiate cleanly."""

from app.components.ui import (
    Button, Card, Badge, Heading, Text, Row, Column, Stack, Grid,
    Divider, TextField, Select, Label, Caption, Toast, Alert,
    EmptyState, Spinner, ProgressBar,
)
from app.utils.cn import cn
from app.components.layout.page import PageShell
from app.components.layout.navbar import Navbar
from app.components.dashboard.widgets import TrajectoryChart, GoalSummaryCard, ProgressIntel, ConflictAlert
from app.components.goals.goal_progress import GoalProgress
from app.components.goals.goal_list import GoalList
from app.components.goals.goal_setup import GoalSetupForm
from app.components.goals.public_goal import PublicGoalPage
from app.components.checkins.progress_form import ProgressForm
from app.pages.landing import landing_page


def test_cn():
    assert cn("a", "b") == "a b"
    assert cn("a", False, "b") == "a b"
    assert cn("a", None, "b") == "a b"
    assert cn() == ""


def test_button_creates():
    b = Button("Click", variant="primary")
    assert b is not None


def test_card_creates():
    c = Card(Text("hello"), variant="default")
    assert c is not None


def test_badge_creates():
    b = Badge("new", variant="success")
    assert b is not None


def test_heading_creates():
    h = Heading("Title", size="2xl")
    assert h is not None


def test_text_creates():
    t = Text("Hello", muted=True)
    assert t is not None


def test_layout_creates():
    r = Row(Text("a"), Text("b"), gap="md")
    assert r is not None
    c = Column(Text("a"), Text("b"), gap="md")
    assert c is not None
    s = Stack(Text("a"), Text("b"), gap="md")
    assert s is not None
    g = Grid(Text("a"), Text("b"), cols={"base": 1}, gap="md")
    assert g is not None


def test_divider_creates():
    d = Divider(margin="md")
    assert d is not None


def test_form_controls():
    tf = TextField(name="test", placeholder="Enter")
    assert tf is not None
    s = Select(name="cat", options=[("a", "A"), ("b", "B")])
    assert s is not None
    l = Label("Name", html_for="name")
    assert l is not None


def test_caption_toast_alert():
    c = Caption("small text")
    assert c is not None
    t = Toast("Message", variant="success")
    assert t is not None
    a = Alert("Warning", variant="warning")
    assert a is not None


def test_empty_spinner_progress():
    e = EmptyState(title="Nothing here")
    assert e is not None
    s = Spinner()
    assert s is not None
    p = ProgressBar(value=50)
    assert p is not None


def test_page_shell():
    p = PageShell("Test", Text("body"))
    assert p is not None


def test_navbar():
    n = Navbar(user_name="TestUser")
    assert n is not None


def test_widgets():
    tc = TrajectoryChart(data=[], title="Test")
    assert tc is not None
    gs = GoalSummaryCard(
        goal_name="Test", pct=50, pace_pct=80,
        prediction="On track", today_amount=10, unit="pages",
        href="/goals/test", status="active",
    )
    assert gs is not None
    pi = ProgressIntel(consistency_pct=75, momentum="Steady", best_env="Home", total_checkins=10)
    assert pi is not None
    ca = ConflictAlert(conflicts=["Test conflict"])
    assert ca is not None
    ca_empty = ConflictAlert(conflicts=[])
    assert ca_empty is not None


def test_goal_progress():
    from app.schemas.goal import Goal
    from app.schemas.checkin import CheckIn
    g = Goal(id="test", name="Test", target_amount=100, unit="pages")
    gp = GoalProgress(goal=g, checkins=[])
    assert gp is not None
    gp_with_data = GoalProgress(goal=g, checkins=[
        CheckIn(amount=10, day=1, note="ok"),
        CheckIn(amount=15, day=2),
        CheckIn(amount=12, day=3, blocker="distracted"),
    ])
    assert gp_with_data is not None


def test_goal_list():
    from app.schemas.goal import Goal
    gl = GoalList(goals=[])
    assert gl is not None
    gl2 = GoalList(goals=[Goal(id="g1", name="Goal 1", target_amount=50, unit="x")])
    assert gl2 is not None


def test_goal_setup():
    gs = GoalSetupForm()
    assert gs is not None
    from app.schemas.goal import Goal
    gs2 = GoalSetupForm(goal=Goal(id="g1", name="Edit me", target_amount=100, unit="x"))
    assert gs2 is not None


def test_public_goal():
    from app.schemas.goal import Goal
    pv = PublicGoalPage(goal=Goal(name="Test", target_amount=100, unit="x"), checkins=[])
    assert pv is not None


def test_progress_form():
    from app.schemas.goal import Goal
    pf = ProgressForm(goal=Goal(name="Test", target_amount=100, unit="x"), day_number=5)
    assert pf is not None


def test_landing():
    lp = landing_page()
    assert lp is not None


def test_goal_schema():
    from app.schemas.goal import Goal, GOAL_CATEGORIES
    assert len(GOAL_CATEGORIES) == 10
    g = Goal(id="g1", name="Test", target_amount=100, unit="kg", category="Fitness")
    assert g.commitment_statement == ""
    assert g.milestone_rewards == {}
    assert g.milestones == []
    d = g.to_dict()
    assert d["name"] == "Test"
    assert d["category"] == "Fitness"
    g2 = Goal.from_doc("g1", d)
    assert g2.name == "Test"
    assert g2.category == "Fitness"


def test_checkin_schema():
    from app.schemas.checkin import CheckIn
    c = CheckIn(amount=10.5, unit="pages", day=1)
    d = c.to_dict()
    assert d["amount"] == 10.5
    c2 = CheckIn.from_doc("c1", d)
    assert c2.amount == 10.5
