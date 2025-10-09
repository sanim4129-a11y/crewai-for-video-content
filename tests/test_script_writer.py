# tests/test_script_writer.py

from agents import script_writer_agent
from tasks import script_task

def test_script_writer():
    inputs = {"topic": "AI in Education", "sections": ["Intro", "Impact", "Future"]}
    result = script_writer_agent.execute(script_task, inputs)
    print("Script output:", result)
    assert "narration" in result
