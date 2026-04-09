# main.py
# Author: Yair Levi
# Entry point: launches RL worker process and GUI

import multiprocessing as mp
import sys
import os

# Ensure relative imports work when running as script
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rl_drone.logger_setup import setup_logger
from rl_drone.environment import Environment
from rl_drone.agent import Agent
from rl_drone.gui import App

log = setup_logger("main")


def rl_worker(cmd_q: mp.Queue, state_q: mp.Queue):
    """RL computation process."""
    from rl_drone.logger_setup import setup_logger as slg
    log_w = slg("worker")
    log_w.info("RL worker started")

    env = Environment()
    agent = Agent(env)

    paused = True
    speed = 0.05
    running = True

    def process_commands():
        nonlocal paused, speed, running
        while not cmd_q.empty():
            try:
                cmd = cmd_q.get_nowait()
                ctype = cmd.get("type")
                if ctype == "resume":
                    paused = False
                elif ctype == "pause":
                    paused = True
                elif ctype == "speed":
                    speed = cmd["value"]
                elif ctype == "soft_reset":
                    agent.soft_reset()
                    paused = True
                elif ctype == "hard_reset":
                    agent.hard_reset()
                    paused = True
                elif ctype == "set_struct":
                    env.set_structure(cmd["row"], cmd["col"], cmd["stype"])
                    agent.soft_reset()
                    paused = True
                elif ctype == "quit":
                    running = False
            except Exception:
                break

    import time
    while running:
        process_commands()
        if paused:
            time.sleep(0.05)
            continue

        training_complete = False
        for step_state in agent.run_episode(
            speed_getter=lambda: speed,
            paused_getter=lambda: paused,
            cmd_handler=process_commands,
        ):
            try:
                payload = {
                    "episode": step_state["episode"],
                    "step": step_state["step"],
                    "total_steps": step_state["total_steps"],
                    "drone_pos": step_state["drone_pos"],
                    "reward": step_state["reward"],
                    "epsilon": step_state["epsilon"],
                    "Q": step_state["Q"],
                    "V": step_state["V"],
                    "arrows": step_state["arrows"],
                    "grid": env.get_grid_copy(),
                    "done": step_state["done"],
                    "training_done": step_state["training_done"],
                    "best_path": step_state["best_path"],
                    "ep_rewards": step_state.get("ep_rewards", []),
                }
                state_q.put_nowait(payload)
            except Exception:
                pass

            if step_state["training_done"]:
                training_complete = True

        process_commands()
        if training_complete:
            paused = True
            log_w.info("Training complete — %d target arrivals reached", agent.target_arrivals)
            continue
        if paused:
            continue

    log_w.info("RL worker exiting")


def main():
    log.info("=== RL Drone starting ===")
    cmd_q   = mp.Queue(maxsize=50)
    state_q = mp.Queue(maxsize=100)

    worker = mp.Process(target=rl_worker, args=(cmd_q, state_q), daemon=True)
    worker.start()
    log.info("Worker process PID=%d", worker.pid)

    app = App(cmd_q, state_q)
    try:
        app.mainloop()
    finally:
        cmd_q.put({"type": "quit"})
        worker.join(timeout=2)
        log.info("=== RL Drone stopped ===")


if __name__ == "__main__":
    mp.set_start_method("spawn", force=True)
    main()
