"""The team deployment serves the two agents the sale and hr packages build, each an A2A server."""
import json
import os

os.environ["FAKE_LLM_DELAY"] = "0"
os.environ.pop("MODEL", None)

from crewai_agent_team.crew import CrewaiAgentTeam  # noqa: E402


def test_both_agents_are_a2a_servers():
    crew = CrewaiAgentTeam().crew()
    roles = [a.role.strip() for a in crew.agents]
    assert roles == ["Trưởng phòng kinh doanh", "Trưởng phòng nhân sự"]
    assert all(a.a2a is not None for a in crew.agents)


def test_kickoff_runs_forecast_then_staffing():
    out = CrewaiAgentTeam().crew().kickoff(inputs={"proposal": json.dumps({"target_leads": 1512})})
    staffing = json.loads(out.raw)
    forecast = json.loads(out.tasks_output[0].raw)
    assert staffing["needed"] == forecast["sales_headcount_planned"]
