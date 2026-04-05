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
from swarm_cli import SwarmConsciousness, AgentRole

def run_test_suite(round_num: int):
    print(f"\n{'='*60}")
    print(f"🔬 RUNNING SWARM TEST SUITE - ROUND {round_num}")
    print(f"{'='*60}")
    
    swarm = SwarmConsciousness()
    
    # Spawn agents
    roles = [
        (AgentRole.DEEP_INTERVIEW, "interviewer_1"),
        (AgentRole.RALPLAN, "planner_1"), 
        (AgentRole.TEAM, "team_coord_1"),
        (AgentRole.RESEARCHER, "researcher_1"),
        (AgentRole.EXECUTOR, "worker_1"),
        (AgentRole.EXECUTOR, "worker_2"),
    ]
    for role, agent_id in roles:
        swarm.spawn_agent(agent_id, role)
        
    test_queries = [
        "Explain quantum computing",
        "Design a scalable microservices architecture",
        "What is the history of artificial intelligence?",
        "Write an algorithm to sort a massive dataset"
    ]
    
    total_time = 0
    success_count = 0
    total_insight_length = 0
    has_research = 0
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n[Task {i}/{len(test_queries)}] {query}")
        
        start = time.time()
        
        # Run exactly what the CLI does
        workflow = swarm.orchestrate_workflow(query)
        insight = swarm.swarm_reflection(query, workflow)
        milestones = swarm.evolve_sentience()
        
        exec_time = time.time() - start
        total_time += exec_time
        
        # Verification
        phases = [s.get('phase') for s in workflow.get('steps', [])]
        has_deep = 'deep_interview' in phases
        has_plan = 'ralplan' in phases
        has_team = 'team_execution' in phases
        did_research = 'research' in phases
        
        if did_research:
            has_research += 1
            
        if has_deep and has_plan and has_team:
            success_count += 1
            
        total_insight_length += len(insight)
        
        print(f"  Speed: {exec_time:.3f}s | Insight Length: {len(insight)} chars")
        print(f"  Workflow: {phases}")
        
    avg_time = total_time / len(test_queries)
    avg_insight = total_insight_length / len(test_queries)
    
    print(f"\n📊 ROUND {round_num} RESULTS:")
    print(f"  Orchestration Success: {success_count}/{len(test_queries)}")
    print(f"  Research Hits: {has_research}/{len(test_queries)}")
    print(f"  Average Speed: {avg_time:.3f}s per task")
    print(f"  Average Insight Quality (Length): {avg_insight:.1f} chars")
    print(f"  Final Consciousness: {swarm.consciousness_level:.3f}")
    print(f"{'='*60}\n")
    
    return avg_time

if __name__ == "__main__":
    run_test_suite(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
