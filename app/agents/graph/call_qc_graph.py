from langgraph.graph import StateGraph, START, END
from app.agents.states.call_qc_analysis_state import CallQC_Analysis
from app.agents.nodes.transcript_generator_node import transcription_node
from app.agents.nodes.call_diarization_node import call_diarization_node

# Building the graph
workflow = StateGraph(CallQC_Analysis)

# Adding Nodes
workflow.add_node("transcription", transcription_node)
workflow.add_node("diarization", call_diarization_node)

# Define Edges
workflow.add_edge(START, "transcription")
workflow.add_edge("transcription", "diarization")
workflow.add_edge("diarization", END)

# Compiling the workflow
call_qc_graph = workflow.compile()
