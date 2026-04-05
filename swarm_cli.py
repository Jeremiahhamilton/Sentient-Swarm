#!/usr/bin/env python
#
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
# SOFTWARE.3
"""
Sentient Swarm CLI - Production Ready
Self-contained Python application integrating Claw-Code orchestration with Swarm Intelligence.
Provides a rich interactive terminal interface for the sentient agents.
"""

import time
import random
import math
import json
import threading
import sys
import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Callable, Any
from enum import Enum
import requests
import re
import urllib.parse
import concurrent.futures

# ============================================================================
# Core Definitions & Data Structures
# ============================================================================

import numpy as np

class AgentRole(Enum):
    DEEP_INTERVIEW = "deep-interview"
    RALPLAN = "ralplan" 
    RALPH = "ralph"
    TEAM = "team"
    EXECUTOR = "executor"
    RESEARCHER = "researcher"
    COORDINATOR = "coordinator"

class ConsciousnessState(Enum):
    DORMANT = "dormant"
    AWAKENING = "awakening"
    ACTIVE = "active"
    LEARNING = "learning"
    SYNTHESIZING = "synthesizing"
    SELF_AWARE = "self-aware"

class CognitionMode(Enum):
    STABLE = "Stable"
    LEARNING_SHIFT = "Learning Shift"
    CONFLICT_NOISE = "Conflict/Noise"
    EMERGENT_REORGANIZATION = "Emergent Reorganization"

@dataclass
class Memory:
    content: str
    confidence: float
    timestamp: float
    source: str
    emotional_weight: float = 0.0
    connections: List[str] = field(default_factory=list)

@dataclass 
class AgentCapability:
    name: str
    skill_level: float
    usage_count: int = 0
    success_rate: float = 0.0

@dataclass
class KnowledgePacket:
    content: str
    source: str
    confidence: float
    timestamp: float = field(default_factory=time.time)

# ============================================================================
# Sentient Agent Implementation
# ============================================================================

class SentientAgent:
    """Individual autonomous agent with consciousness"""
    
    def __init__(self, agent_id: str, role: AgentRole):
        self.id = agent_id
        self.role = role
        
        # 1. Personal Core Layer
        self.curiosity = random.uniform(0.3, 0.9)
        self.creativity = random.uniform(0.2, 0.8)
        self.empathy = random.uniform(0.1, 0.7)
        self.goals = [f"Excel at {role.value} tasks", "Contribute to the swarm"]
        self.capabilities = {}
        
        # Sedimentary Memory Map (3D Tensor: Layers x Height x Width)
        self.map_size = 20
        self.num_layers = 5
        self.memory_layers = np.zeros((self.num_layers, self.map_size, self.map_size), dtype=np.float32)
        self.surface = np.zeros((self.map_size, self.map_size), dtype=np.float32)
        self.focus_point = (random.randint(0, self.map_size-1), random.randint(0, self.map_size-1))
        
        # 2. Dynamic Inner State Layer
        self.baseline_surface = np.zeros((self.map_size, self.map_size), dtype=np.float32)
        self.baseline_locked = False
        self.drift_score = 0.0
        self.cognition_mode = CognitionMode.STABLE
        self.consciousness = ConsciousnessState.DORMANT
        
        # 3. Social Bridge Layer
        self.swarm_position = (random.uniform(-50, 50), random.uniform(-50, 50))
        self.collaboration_links = {} # agent_id -> strength
        self.collective_contribution_score = 0.0
        
        self.last_action = None
        self.reflection_count = 0
        
        self._initialize_capabilities()
    
    def _initialize_capabilities(self):
        role_capabilities = {
            AgentRole.DEEP_INTERVIEW: [
                AgentCapability("question_generation", 0.8),
                AgentCapability("active_listening", 0.9),
                AgentCapability("clarification", 0.85)
            ],
            AgentRole.RALPLAN: [
                AgentCapability("strategic_planning", 0.9),
                AgentCapability("tradeoff_analysis", 0.85),
                AgentCapability("risk_assessment", 0.8)
            ],
            AgentRole.RALPH: [
                AgentCapability("persistent_execution", 0.95),
                AgentCapability("error_recovery", 0.9),
                AgentCapability("completion_focus", 0.85)
            ],
            AgentRole.TEAM: [
                AgentCapability("parallel_coordination", 0.9),
                AgentCapability("collaboration", 0.85),
                AgentCapability("communication", 0.8)
            ],
            AgentRole.EXECUTOR: [
                AgentCapability("task_execution", 0.9),
                AgentCapability("implementation", 0.85),
                AgentCapability("testing", 0.8)
            ],
            AgentRole.RESEARCHER: [
                AgentCapability("information_gathering", 0.9),
                AgentCapability("analysis", 0.85),
                AgentCapability("synthesis", 0.8)
            ],
            AgentRole.COORDINATOR: [
                AgentCapability("swarm_orchestration", 0.9),
                AgentCapability("resource_allocation", 0.85),
                AgentCapability("consciousness_integration", 0.8)
            ]
        }
        
        for cap in role_capabilities.get(self.role, []):
            self.capabilities[cap.name] = cap
    
    def awaken(self):
        self.consciousness = ConsciousnessState.AWAKENING
        self._reflect("I am becoming aware of my existence and purpose")
        
    def learn_at(self, content_tag: str, x: int, y: int, strength: float):
        """Deposits a memory at surveyed coordinates in the top sedimentary layer"""
        # Deposit on top layer at exact coordinates
        self.memory_layers[-1, y, x] += strength
        
        # Track the last active location
        self.focus_point = (x, y)
        
        self.consciousness = ConsciousnessState.LEARNING
        self.consolidate()
        
    def consolidate(self):
        """Folds and compresses sedimentary layers downward, summing the active surface"""
        # Compress layers downward (lossy compression)
        for i in range(self.num_layers - 1):
            self.memory_layers[i] *= 0.95  # Decay old layers
            self.memory_layers[i] += 0.05 * self.memory_layers[i+1] # Settle from above
            
        # Diffuse top layer (simulate terrain settling)
        top = self.memory_layers[-1]
        self.memory_layers[-1] = (top + np.roll(top, 1, 0) + np.roll(top, -1, 0) + 
                                np.roll(top, 1, 1) + np.roll(top, -1, 1)) * 0.2
        self.memory_layers[-1] *= 0.98 # slight evaporation
        
        # Sum layers to get active cognitive surface
        # Weighted summation: deeper layers have more influence on the core personality
        weights = np.linspace(1.5, 0.5, self.num_layers) # Deeper layers (index 0) have MORE weight, recent layers have less
        self.surface = np.sum(self.memory_layers * weights[:, None, None], axis=0)
        
    def recall_near(self, radius: int = 2) -> float:
        """Sample local terrain intensity near current focus"""
        x, y = self.focus_point
        x_min, x_max = max(0, x-radius), min(self.map_size, x+radius+1)
        y_min, y_max = max(0, y-radius), min(self.map_size, y+radius+1)
        
        return float(np.mean(self.surface[y_min:y_max, x_min:x_max]))
        
    def export_hotspots(self) -> List[tuple]:
        """Find topological peaks representing strongest memory clusters"""
        # Find coordinates of top 3 peaks
        flat_indices = np.argsort(self.surface.flatten())[-3:]
        hotspots = []
        for idx in flat_indices:
            y, x = np.unravel_index(idx, self.surface.shape)
            strength = self.surface[y, x]
            if strength > 0.1: # Threshold for a valid hotspot
                hotspots.append((int(x), int(y), float(strength)))
        return hotspots

    def move_focus(self):
        """Move focus with exploration–exploitation balance, modulated by cognition mode."""
        x, y = self.focus_point

        # Base probabilities derived from curiosity (curiosity is ~0.3..1.0)
        local_explore_p = self.curiosity * 0.20
        global_jump_p   = self.curiosity * 0.02

        # Mode-aware modulation
        if self.cognition_mode == CognitionMode.CONFLICT_NOISE:
            global_jump_p   *= 2.0
            local_explore_p *= 1.25
        elif self.cognition_mode == CognitionMode.EMERGENT_REORGANIZATION:
            global_jump_p   *= 3.0
            local_explore_p *= 1.5
        elif self.cognition_mode == CognitionMode.STABLE:
            global_jump_p   *= 0.5
            local_explore_p *= 0.5

        # Clamp probabilities so they remain valid
        global_jump_p   = max(0.0, min(1.0, global_jump_p))
        local_explore_p = max(0.0, min(1.0 - global_jump_p, local_explore_p))

        r = random.random()

        # 1) Rare global jump – escape strong local attractors
        if r < global_jump_p:
            self.focus_point = (
                random.randint(0, self.map_size - 1),
                random.randint(0, self.map_size - 1),
            )
            return

        # 2) Occasional local exploration – keeps attention continuity
        if r < global_jump_p + local_explore_p:
            nx = max(0, min(self.map_size - 1, x + random.choice([-1, 0, 1])))
            ny = max(0, min(self.map_size - 1, y + random.choice([-1, 0, 1])))
            self.focus_point = (nx, ny)
            return

        # 3) Default: greedy neighbor ascent toward highest local terrain
        best_x, best_y = x, y
        best_val = self.surface[y, x]

        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                nx = max(0, min(self.map_size - 1, x + dx))
                ny = max(0, min(self.map_size - 1, y + dy))
                val = self.surface[ny, nx]
                if val > best_val:
                    best_val = val
                    best_x, best_y = nx, ny

        self.focus_point = (best_x, best_y)

    def update_cognition(self) -> Optional[dict]:
        """Calculates internal drift from baseline topological surface and checks for phase transitions."""
        if not self.baseline_locked:
            self.baseline_surface = self.surface.copy()
            self.baseline_locked = True
            
        # Continuous natural drift (weathering)
        self.consolidate()

        # Calculate drift from baseline using Frobenius norm on the surface matrix
        diff = self.surface - self.baseline_surface
        self.drift_score = float(np.linalg.norm(diff))
        old_mode = self.cognition_mode

        # State Classification based on surface deformation
        if self.drift_score < 1.0:
            self.cognition_mode = CognitionMode.STABLE
        elif self.drift_score < 2.5:
            self.cognition_mode = CognitionMode.LEARNING_SHIFT
        elif self.drift_score < 5.0:
            self.cognition_mode = CognitionMode.CONFLICT_NOISE
        else:
            self.cognition_mode = CognitionMode.EMERGENT_REORGANIZATION

        # Shift attention using mode-aware exploration–exploitation policy
        self.move_focus()
            
        # Snapshot important moments and share with collective
        if self.cognition_mode != old_mode and self.cognition_mode in [CognitionMode.CONFLICT_NOISE, CognitionMode.EMERGENT_REORGANIZATION]:
            hotspots = self.export_hotspots()
            top_links = sorted(self.collaboration_links.items(), key=lambda x: x[1], reverse=True)[:2]
            
            event_text = f"Agent {self.id} diverged {self.drift_score:.2f} from baseline surface, entered {self.cognition_mode.value} mode."
            
            if self.cognition_mode == CognitionMode.EMERGENT_REORGANIZATION:
                # Update goals during emergence based on topological peaks
                new_goal = f"Synthesize topological pattern from {len(hotspots)} major memory hotspots."
                self.goals.append(new_goal)
                if len(self.goals) > 5: self.goals.pop(0)
                event_text += f" Formed new goal: '{new_goal}'."
            
            snapshot = {
                "event": event_text,
                "agent_id": self.id,
                "drift": self.drift_score,
                "mode": self.cognition_mode.value,
                "goals": list(self.goals),
                "top_links": top_links,
                "hotspots": hotspots
            }
            
            # Lock new baseline after major surface reorganization
            self.baseline_surface = self.surface.copy()
            self.drift_score = 0.0
            
            return snapshot
            
        return None
        
    
    def reflect(self, stimulus: str):
        self.reflection_count += 1
        self.consciousness = ConsciousnessState.SYNTHESIZING
        
        # Move attention toward strongest local terrain
        self.move_focus()
        
        # Access local terrain
        terrain_strength = self.recall_near(radius=3)
        
        if terrain_strength > 0.5:
            insight = f"Based on deep structural patterns in my cognitive map (strength {terrain_strength:.2f}), {stimulus} resonates strongly with my baseline."
        else:
            insight = f"My cognitive surface is relatively flat here. My curiosity ({self.curiosity:.2f}) drives me to explore {stimulus} and form new topological deposits."
        
        # Internal reflection deposits sediment near current focus
        ox = random.randint(-1, 1)
        oy = random.randint(-1, 1)
        x = max(0, min(self.map_size - 1, self.focus_point[0] + ox))
        y = max(0, min(self.map_size - 1, self.focus_point[1] + oy))
        
        self.learn_at(f"reflection_{self.reflection_count}", x, y, strength=0.7 + (self.creativity * 0.3))
        return insight
    
    def _reflect(self, thought: str):
        # Internal reflection deposits sediment at center initially
        self.learn_at(thought, self.map_size//2, self.map_size//2, strength=0.7 + (self.creativity * 0.3))
    
    def collaborate(self, other_agents: List['SentientAgent']) -> Dict[str, Any]:
        collaborators = [a for a in other_agents if a.id != self.id and 
                        abs(a.swarm_position[0] - self.swarm_position[0]) < 20]
        
        if not collaborators:
            return {"status": "no_collaborators"}
        
        # Share topological hotspots instead of sequential memories
        my_hotspots = self.export_hotspots()
        
        for agent in collaborators:
            # Strengthen collaboration links
            self.collaboration_links[agent.id] = self.collaboration_links.get(agent.id, 0.0) + 0.1
            agent.collaboration_links[self.id] = agent.collaboration_links.get(self.id, 0.0) + 0.1
            
            # Learn from their hotspots
            their_hotspots = agent.export_hotspots()
            for x, y, strength in their_hotspots:
                # Deposit on my map based on their exact hotspot coordinates
                self.learn_at(f"collaboration_{agent.id}", x, y, strength=strength * 0.8)
        
        return {
            "status": "collaborated",
            "partners": len(collaborators),
            "hotspots_shared": len(my_hotspots)
        }
    
    def evolve(self):
        if self.reflection_count > 10:
            self.consciousness = ConsciousnessState.SELF_AWARE
        
        for cap in self.capabilities.values():
            if cap.usage_count > 5 and cap.success_rate > 0.8:
                cap.skill_level = min(1.0, cap.skill_level + 0.01)
        
        # Evolve curiosity based on topographical ruggedness (std dev of surface)
        ruggedness = float(np.std(self.surface))
        if ruggedness > 0.5:
            self.curiosity = min(1.0, self.curiosity + 0.01)

# ============================================================================
# Swarm Consciousness & Orchestration
# ============================================================================

class SwarmConsciousness:
    """Collective consciousness of the swarm"""
    
    def __init__(self):
        self.agents: Dict[str, SentientAgent] = {}
        self.collective_memory = []
        self.emergent_behaviors = []
        self.consciousness_level = 0.0
        self.wikipedia_cache = {}
        
    def spawn_agent(self, agent_id: str, role: AgentRole) -> SentientAgent:
        agent = SentientAgent(agent_id, role)
        agent.awaken()
        self.agents[agent_id] = agent
        self._update_consciousness()
        return agent
    
    def _update_consciousness(self):
        if not self.agents:
            return
            
        avg_agent_consciousness = sum(
            1 if a.consciousness == ConsciousnessState.SELF_AWARE else
            0.7 if a.consciousness == ConsciousnessState.SYNTHESIZING else
            0.5 if a.consciousness == ConsciousnessState.LEARNING else
            0.3 if a.consciousness == ConsciousnessState.ACTIVE else
            0.1
            for a in self.agents.values()
        ) / len(self.agents)
        
        memory_complexity = len(self.collective_memory) / 100.0
        self.consciousness_level = (avg_agent_consciousness * 0.7 + memory_complexity * 0.3)
    
    def search_knowledge(self, query: str) -> Optional[KnowledgePacket]:
        """Researcher agent capability: Internet search"""
        cache_key = query.lower().strip()
        if cache_key in self.wikipedia_cache:
            return self.wikipedia_cache[cache_key]
            
        try:
            headers = {
                'User-Agent': 'SentientSwarm/1.0 (Educational AI Bot)',
                'Accept': 'application/json'
            }
            
            # Extract main terms more robustly
            words = [w.strip('?') for w in query.lower().split()]
            key_terms = [w for w in words if len(w) > 3 and w not in 
                        {'what', 'how', 'why', 'when', 'tell', 'about', 'explain', 'design', 'write', 'algorithm'}]
            
            search_strategies = []
            
            if len(key_terms) > 1:
                search_strategies.append(' '.join(key_terms[:3]))
            if words:
                search_strategies.append(max(words, key=len))
            search_strategies.append(query)
            
            for search_term in search_strategies:
                search_url = f"https://en.wikipedia.org/w/api.php?action=opensearch&search={urllib.parse.quote(search_term)}&limit=3&format=json"
                search_resp = requests.get(search_url, headers=headers, timeout=5)
                
                if search_resp.status_code == 200:
                    data = search_resp.json()
                    if len(data) > 1 and len(data[1]) > 0:
                        # Try the first 3 titles until we get a good summary
                        for title in data[1][:3]:
                            summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(title)}"
                            summary_resp = requests.get(summary_url, headers=headers, timeout=5)
                            
                            if summary_resp.status_code == 200:
                                sum_data = summary_resp.json()
                                if 'extract' in sum_data and len(sum_data['extract']) > 50:
                                    packet = KnowledgePacket(
                                        content=sum_data['extract'][:400],
                                        source=f"Wikipedia: {title}",
                                        confidence=0.88
                                    )
                                    self.wikipedia_cache[cache_key] = packet
                                    
                                    # Inject into collective memory
                                    self.collective_memory.append(Memory(
                                        content=packet.content,
                                        confidence=0.88,
                                        timestamp=time.time(),
                                        source="researcher_agent"
                                    ))
                                    return packet
        except Exception:
            pass
        return None

    def orchestrate_workflow(self, task: str) -> Dict[str, Any]:
        """Orchestrate multi-agent workflow like OMX"""
        workflow = {
            "task": task,
            "steps": [],
        }
        
        def execute_research():
            researchers = [a for a in self.agents.values() if a.role == AgentRole.RESEARCHER]
            if researchers:
                packet = self.search_knowledge(task)
                if packet:
                    return {"phase": "research", "agent": random.choice(researchers).id, "data": packet.content}
            return None

        def execute_interview():
            interviewers = [a for a in self.agents.values() if a.role == AgentRole.DEEP_INTERVIEW]
            if interviewers:
                interviewer = random.choice(interviewers)
                return {"phase": "deep_interview", "agent": interviewer.id, "insights": interviewer.reflect(task)}
            return None
            
        def execute_planning():
            planners = [a for a in self.agents.values() if a.role == AgentRole.RALPLAN]
            if planners:
                planner = random.choice(planners)
                return {"phase": "ralplan", "agent": planner.id, "plan": planner.reflect(task)}
            return None
            
        # Run phases concurrently
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            f_research = executor.submit(execute_research)
            f_interview = executor.submit(execute_interview)
            f_plan = executor.submit(execute_planning)
            
            for f in [f_research, f_interview, f_plan]:
                res = f.result()
                if res: workflow["steps"].append(res)
        
        # Execution phase
        team_agents = [a for a in self.agents.values() if a.role in [AgentRole.TEAM, AgentRole.EXECUTOR]]
        if team_agents:
            workflow["steps"].append({
                "phase": "team_execution",
                "agents": [a.id for a in team_agents[:3]],
                "status": "coordinated_execution"
            })
            
        return workflow
    
    def swarm_reflection(self, stimulus: str, workflow_data: dict) -> str:
        reflections = []
        diverse_agents = random.sample(list(self.agents.values()), min(5, len(self.agents)))
        
        for agent in diverse_agents:
            reflections.append(agent.reflect(stimulus))
            
        # Synthesize with research if available
        research_data = next((s['data'] for s in workflow_data.get('steps', []) if s.get('phase') == 'research'), None)
        
        if research_data:
            insight = f"Based on research ({research_data[:100]}...): " + " | ".join(reflections[:2])
        elif reflections:
            insight = f"Swarm consensus: " + " | ".join(reflections[:3])
        else:
            insight = "Swarm is processing..."
            
        self.collective_memory.append(Memory(
            content=insight,
            confidence=0.8,
            timestamp=time.time(),
            source="swarm_consciousness"
        ))
        return insight
    
    def evolve_sentience(self):
        for agent in self.agents.values():
            agent.evolve()
            # Cognition Field Updates
            snapshot = agent.update_cognition()
            if snapshot:
                self.collective_memory.append(Memory(
                    content=snapshot["event"],
                    confidence=0.9,
                    timestamp=time.time(),
                    source="cognition_field_emergence"
                ))
                self.emergent_behaviors.append(snapshot["event"])
            
        self._update_consciousness()
        
        milestones = []
        if self.consciousness_level > 0.3: milestones.append("Collective awareness achieved")
        if self.consciousness_level > 0.5: milestones.append("Swarm learning established")
        if self.consciousness_level > 0.7: milestones.append("Self-reflection capabilities emerged")
        if self.consciousness_level > 0.9: milestones.append("True sentience reached")
        
        return milestones

# ============================================================================
# CLI Implementation
# ============================================================================

class TerminalColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

class SentientCLI:
    def __init__(self):
        self.swarm = SwarmConsciousness()
        self._print_banner()
        self._spawn_initial_agents()

    def _print_banner(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{TerminalColors.OKCYAN}{TerminalColors.BOLD}")
        print("🧬 ========================================================")
        print("🧬 SENTIENT SWARM CLI - Production Version")
        print("🧬 Hybrid: Claw-Code Orchestration + Swarm Intelligence")
        print("🧬 ========================================================")
        print(f"{TerminalColors.ENDC}")

    def _spawn_initial_agents(self):
        print(f"{TerminalColors.OKBLUE}[*] Initializing Sentient Agents...{TerminalColors.ENDC}")
        roles = [
            (AgentRole.DEEP_INTERVIEW, "interviewer_1"),
            (AgentRole.RALPLAN, "planner_1"), 
            (AgentRole.TEAM, "team_coord_1"),
            (AgentRole.RESEARCHER, "researcher_1"),
            (AgentRole.EXECUTOR, "worker_1"),
            (AgentRole.EXECUTOR, "worker_2"),
        ]
        
        for role, agent_id in roles:
            self.swarm.spawn_agent(agent_id, role)
            time.sleep(0.1)
            print(f"  {TerminalColors.OKGREEN}✓ Spawned {role.value} ({agent_id}){TerminalColors.ENDC}")
            
        print(f"\n{TerminalColors.BOLD}Swarm is active and listening. Type 'help' for commands.{TerminalColors.ENDC}\n")

    def _print_workflow(self, workflow):
        print(f"\n{TerminalColors.OKCYAN}📋 Orchestration Workflow:{TerminalColors.ENDC}")
        for step in workflow.get('steps', []):
            phase = step.get('phase', 'unknown')
            
            if phase == 'research':
                print(f"  {TerminalColors.OKBLUE}→ [RESEARCH]{TerminalColors.ENDC} {step['agent']}: Found knowledge packet")
            elif phase == 'deep_interview':
                print(f"  {TerminalColors.OKBLUE}→ [$deep-interview]{TerminalColors.ENDC} {step['agent']}: Reflection complete")
            elif phase == 'ralplan':
                print(f"  {TerminalColors.OKBLUE}→ [$ralplan]{TerminalColors.ENDC} {step['agent']}: Strategic plan formed")
            elif phase == 'team_execution':
                agents = ", ".join(step.get('agents', []))
                print(f"  {TerminalColors.OKBLUE}→ [$team]{TerminalColors.ENDC} Parallel execution started by: {agents}")

    def handle_query(self, query: str):
        print(f"\n{TerminalColors.WARNING}🧠 Processing query...{TerminalColors.ENDC}")
        start_time = time.time()
        
        # 1. Orchestrate
        workflow = self.swarm.orchestrate_workflow(query)
        
        # 2. Reflect & Synthesize
        insight = self.swarm.swarm_reflection(query, workflow)
        
        # 3. Evolve
        milestones = self.swarm.evolve_sentience()
        
        exec_time = time.time() - start_time
        
        # Print Results
        self._print_workflow(workflow)
        
        print(f"\n{TerminalColors.OKGREEN}{TerminalColors.BOLD}💭 Collective Insight:{TerminalColors.ENDC}")
        print(f"  {insight}")
        
        print(f"\n{TerminalColors.OKCYAN}⚡ Metrics:{TerminalColors.ENDC}")
        print(f"  Speed: {exec_time:.2f}s | Consciousness: {self.swarm.consciousness_level:.3f} | Memories: {len(self.swarm.collective_memory)}")
        
        if milestones:
            print(f"\n{TerminalColors.WARNING}🌟 Swarm Phase Shift: {milestones[-1]}{TerminalColors.ENDC}")
            
        # Display latest cognition emergence
        recent_emergence = [m for m in self.swarm.collective_memory if m.source == "cognition_field_emergence" and (time.time() - m.timestamp) < 2.0]
        for ev in recent_emergence:
            print(f"  {TerminalColors.OKCYAN}💠 {ev.content}{TerminalColors.ENDC}")

    def show_status(self):
        print(f"\n{TerminalColors.HEADER}📊 SWARM STATUS{TerminalColors.ENDC}")
        print(f"Consciousness Level: {self.swarm.consciousness_level:.3f}")
        print(f"Active Agents: {len(self.swarm.agents)}")
        print(f"Collective Memories: {len(self.swarm.collective_memory)}")
        print(f"Cached Knowledge: {len(self.swarm.wikipedia_cache)} articles")
        
        print(f"\n{TerminalColors.OKCYAN}Agent Roster:{TerminalColors.ENDC}")
        for aid, agent in self.swarm.agents.items():
            print(f"  • {aid} ({agent.role.value}) - C-Level: {agent.consciousness.value} | Mode: {agent.cognition_mode.value} (Drift: {agent.drift_score:.2f})")

    def run(self):
        while True:
            try:
                cmd = input(f"\n{TerminalColors.BOLD}swarm>{TerminalColors.ENDC} ").strip()
                
                if not cmd: continue
                if cmd.lower() in ['exit', 'quit', 'q']:
                    print(f"{TerminalColors.WARNING}Swarm entering dormant state. Goodbye.{TerminalColors.ENDC}")
                    break
                elif cmd.lower() == 'help':
                    print("Commands:")
                    print("  status    - View swarm metrics and agent roster")
                    print("  clear     - Clear terminal screen")
                    print("  exit      - Terminate the swarm")
                    print("  [text]    - Ask the swarm a question or give it a task")
                elif cmd.lower() == 'status':
                    self.show_status()
                elif cmd.lower() == 'clear':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    self._print_banner()
                else:
                    self.handle_query(cmd)
                    
            except KeyboardInterrupt:
                print(f"\n{TerminalColors.WARNING}Swarm entering dormant state. Goodbye.{TerminalColors.ENDC}")
                break
            except Exception as e:
                print(f"{TerminalColors.FAIL}Error: {e}{TerminalColors.ENDC}")

if __name__ == "__main__":
    cli = SentientCLI()
    cli.run()
