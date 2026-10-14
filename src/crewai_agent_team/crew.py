"""One AMP deployment, two A2A agents: Sale and HR (the Basic plan allows two crews: this one and Marketing).

The agents are built by their own packages (crewai-agent-sale, crewai-agent-hr, pinned in uv.lock), so their
tools, scripted LLM and A2AServerConfig are exactly what those repos test. AMP mounts each agent that has an
A2AServerConfig at /a2a/agents/{role}/ and routes /a2a by the message's `target_agent`.
"""
from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task
from crewai_agent_hr.crew import CrewaiAgentHr
from crewai_agent_sale.crew import CrewaiAgentSale


@CrewBase
class CrewaiAgentTeam():
    """Sale + HR. /kickoff runs forecast → staffing; A2A calls reach one agent at a time."""

    agents: list[BaseAgent]
    tasks: list[Task]

    @agent
    def sales_lead(self) -> Agent:
        return CrewaiAgentSale().sales_lead()

    @agent
    def hr_lead(self) -> Agent:
        return CrewaiAgentHr().hr_lead()

    @task
    def team_forecast(self) -> Task:
        return Task(config=self.tasks_config['team_forecast'])  # type: ignore[index]

    @task
    def team_staffing(self) -> Task:
        return Task(config=self.tasks_config['team_staffing'])  # type: ignore[index]

    @crew
    def crew(self) -> Crew:
        return Crew(agents=self.agents, tasks=self.tasks, process=Process.sequential, verbose=True)
