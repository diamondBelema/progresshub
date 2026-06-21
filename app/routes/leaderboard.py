from __future__ import annotations

from collections import defaultdict
from fastapi import APIRouter, Request
from app.htmy import htmy
from app.components.layout.page import PageShell
from app.components.ui import Heading, Text, Card, Badge, Row, Column, Stack, Divider
from htmy import html
router = APIRouter(prefix="/leaderboard", tags=["leaderboard"])


@router.get("", response_model=None)
@htmy.page()
def leaderboard_page(request: Request):
    token = request.cookies.get("session_token")
    if not token:
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/auth/login", status_code=302)
    from app.services.appwrite import verify_session
    user_id = verify_session(token)
    if not user_id:
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/auth/login", status_code=302)

    from app.services.appwrite import list_profiles, get_users_service
    from app.repositories.goal_repo import list_by_user as get_goals
    from app.repositories.checkin_repo import list_by_goal as get_checkins

    try:
        user = get_users_service().get(user_id)
        username = user.name if user else "User"
    except Exception:
        username = "User"

    profiles = list_profiles()
    opt_in = [p for p in profiles if p.get("leaderboard_opt_in")]

    entries: list[dict] = []
    for p in opt_in:
        uid = p.get("user_id", "")
        goals = get_goals(uid, status=None)
        for g in goals:
            if not g.category:
                continue
            checkins = get_checkins(g.id)
            if not checkins:
                continue
            hits = 0
            for c in checkins:
                plan_entry = next((d for d in (g.daily_plan or []) if d.get("day") == c.day), None)
                target = plan_entry.get("target", 0) if plan_entry else 0
                if target > 0 and c.amount >= target * 0.8:
                    hits += 1
            consistency = round((hits / len(checkins)) * 100)
            entries.append({
                "category": g.category,
                "consistency": consistency,
                "goal_name": g.name,
                "pct": min(100, round((g.achieved_so_far / g.target_amount) * 100)) if g.target_amount > 0 else 0,
                "total_checkins": len(checkins),
            })

    if not entries:
        return PageShell(
            "Leaderboard",
            html.div(
                Heading("Leaderboard", size="2xl"),
                Divider(margin="md"),
                Text("No leaderboard data yet. Opt in from Settings and start logging.", muted=True, class_="text-center py-12"),
            ),
            active="/leaderboard",
            user_name=username,
        )

    by_category: dict[str, list[dict]] = defaultdict(list)
    for e in entries:
        by_category[e["category"]].append(e)

    sections = []
    for cat in sorted(by_category.keys()):
        ranked = sorted(by_category[cat], key=lambda x: x["consistency"], reverse=True)[:20]
        label = chr(ord("A") - 1)
        cards = []
        for i, e in enumerate(ranked):
            label = chr(ord("A") + i) if i < 26 else f"User{i+1}"
            badge_var = "success" if e["consistency"] >= 80 else ("warning" if e["consistency"] >= 50 else "danger")
            cards.append(
                Card(
                    Row(
                        html.span(label, class_="text-lg font-bold text-signal-400 w-8"),
                        Column(
                            Row(
                                Badge(f"{e['consistency']}%", variant=badge_var),
                                Text(f"{e['pct']}% complete", muted=True, size="xs"),
                                gap="sm",
                                align="center",
                            ),
                            Text(f"{e['total_checkins']} check-ins \u2014 {e['goal_name']}", muted=True, size="xs"),
                            gap="xs",
                            class_="flex-1",
                        ),
                        align="center",
                    ),
                    variant="default", padding="md",
                )
            )

        sections.append(
            Column(
                Heading(cat, size="lg", class_="capitalize"),
                Stack(*cards, gap="sm"),
                gap="md",
            )
        )

    return PageShell(
        "Leaderboard",
        html.div(
            Heading("Leaderboard", size="2xl"),
            Text("Anonymous rankings by consistency score. Opt in from Settings.", muted=True),
            Divider(margin="md"),
            Stack(*sections, gap="lg"),
        ),
        active="/leaderboard",
        user_name=username,
    )
