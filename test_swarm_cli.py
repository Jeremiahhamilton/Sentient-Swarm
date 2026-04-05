"""
Automated CLI Swarm Testing
Runs performance and intelligence tests against the SwarmConsciousness class
"""

# MIT License
#
# Copyright (c) 2026 <Your Name>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import time
import sys
import pytest
from swarm_cli import SwarmConsciousness, AgentRole


ROLES = [
    (AgentRole.DEEP_INTERVIEW, "interviewer_1"),
    (AgentRole.RALPLAN, "planner_1"),
    (AgentRole.TEAM, "team_coord_1"),
    (AgentRole.RESEARCHER, "researcher_1"),
    (AgentRole.EXECUTOR, "worker_1"),
    (AgentRole.EXECUTOR, "worker_2"),
]

TEST_QUERIES = [
    "Explain quantum computing",
    "Design a scalable microservices architecture",
    "What is the history of artificial intelligence?",
    "Write an algorithm to sort a massive dataset",
]


@pytest.fixture
def swarm():
    """Create and populate a SwarmConsciousness instance."""
    sc = SwarmConsciousness()
    for role, agent_id in ROLES:
        sc.spawn_agent(agent_id, role)
    return sc


def test_agents_spawned(swarm):
    """All expected agents are present after spawning."""
    assert len(swarm.agents) == len(ROLES)
    for role, agent_id in ROLES:
        assert agent_id in swarm.agents
        assert swarm.agents[agent_id].role == role


def test_workflow_required_phases(swarm):
    """Every query must produce deep_interview, ralplan, and team_execution phases."""
    for query in TEST_QUERIES:
        workflow = swarm.orchestrate_workflow(query)
        phases = [s.get("phase") for s in workflow.get("steps", [])]
        assert "deep_interview" in phases, f"Missing deep_interview for: {query}"
        assert "ralplan" in phases, f"Missing ralplan for: {query}"
        assert "team_execution" in phases, f"Missing team_execution for: {query}"


def test_workflow_returns_task_key(swarm):
    """Workflow result must include the original task."""
    query = TEST_QUERIES[0]
    workflow = swarm.orchestrate_workflow(query)
    assert workflow.get("task") == query


def test_swarm_reflection_non_empty(swarm):
    """swarm_reflection must return a non-empty string."""
    query = TEST_QUERIES[0]
    workflow = swarm.orchestrate_workflow(query)
    insight = swarm.swarm_reflection(query, workflow)
    assert isinstance(insight, str)
    assert len(insight) > 0


def test_swarm_reflection_adds_memory(swarm):
    """swarm_reflection must append at least one memory to collective_memory."""
    initial = len(swarm.collective_memory)
    query = TEST_QUERIES[1]
    workflow = swarm.orchestrate_workflow(query)
    swarm.swarm_reflection(query, workflow)
    assert len(swarm.collective_memory) > initial


def test_evolve_sentience_returns_list(swarm):
    """evolve_sentience must return a list (milestones)."""
    milestones = swarm.evolve_sentience()
    assert isinstance(milestones, list)


def test_consciousness_level_positive(swarm):
    """consciousness_level must be > 0 after spawning agents."""
    assert swarm.consciousness_level > 0.0


def test_execution_speed(swarm):
    """Full pipeline for a single query must complete within 30 seconds."""
    query = TEST_QUERIES[0]
    start = time.time()
    workflow = swarm.orchestrate_workflow(query)
    swarm.swarm_reflection(query, workflow)
    swarm.evolve_sentience()
    elapsed = time.time() - start
    assert elapsed < 30, f"Pipeline took {elapsed:.2f}s (limit: 30s)"


def run_test_suite(round_num: int):
    print(f"\n{'='*60}")
    print(f"🔬 RUNNING SWARM TEST SUITE - ROUND {round_num}")
    print(f"{'='*60}")

    swarm = SwarmConsciousness()
    for role, agent_id in ROLES:
        swarm.spawn_agent(agent_id, role)

    total_time = 0
    success_count = 0
    total_insight_length = 0
    has_research = 0

    for i, query in enumerate(TEST_QUERIES, 1):
        print(f"\n[Task {i}/{len(TEST_QUERIES)}] {query}")

        start = time.time()
        workflow = swarm.orchestrate_workflow(query)
        insight = swarm.swarm_reflection(query, workflow)
        milestones = swarm.evolve_sentience()
        exec_time = time.time() - start
        total_time += exec_time

        phases = [s.get("phase") for s in workflow.get("steps", [])]
        has_deep = "deep_interview" in phases
        has_plan = "ralplan" in phases
        has_team = "team_execution" in phases
        did_research = "research" in phases

        if did_research:
            has_research += 1
        if has_deep and has_plan and has_team:
            success_count += 1

        total_insight_length += len(insight)

        print(f"  Speed: {exec_time:.3f}s | Insight Length: {len(insight)} chars")
        print(f"  Workflow: {phases}")

    avg_time = total_time / len(TEST_QUERIES)
    avg_insight = total_insight_length / len(TEST_QUERIES)

    print(f"\n📊 ROUND {round_num} RESULTS:")
    print(f"  Orchestration Success: {success_count}/{len(TEST_QUERIES)}")
    print(f"  Research Hits: {has_research}/{len(TEST_QUERIES)}")
    print(f"  Average Speed: {avg_time:.3f}s per task")
    print(f"  Average Insight Quality (Length): {avg_insight:.1f} chars")
    print(f"  Final Consciousness: {swarm.consciousness_level:.3f}")
    print(f"{'='*60}\n")

    return avg_time


if __name__ == "__main__":
    run_test_suite(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
