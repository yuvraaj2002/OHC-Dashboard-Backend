from langgraph.graph import StateGraph, START, END
from app.agents.states.call_qc_analysis_state import CallQC_Analysis
from app.agents.nodes.transcript_generator_node import transcription_node
from app.agents.nodes.call_diarization_node import call_diarization_node
from app.agents.nodes.consent_capture_node import consent_capture_node
from app.agents.nodes.communication_quality_node import communication_quality_node
from app.agents.nodes.keyword_detection_node import keyword_detection_node
from app.agents.nodes.sentiment_detection_node import sentiment_detection_node
from app.agents.nodes.qualification_completeness_node import qualification_completeness_node
from app.agents.nodes.script_adherence_node import script_adherence_node
from app.agents.nodes.objection_handling_node import objection_handling_node
from app.agents.nodes.final_qc_node import final_qc_node

# Building the graph
workflow = StateGraph(CallQC_Analysis)

# Adding Nodes
workflow.add_node("transcription", transcription_node)
workflow.add_node("diarization", call_diarization_node)

# Analysis Nodes
workflow.add_node("script_adherence", script_adherence_node)
workflow.add_node("qualification_completeness", qualification_completeness_node)
workflow.add_node("consent_capture", consent_capture_node)
workflow.add_node("objection_handling", objection_handling_node)
workflow.add_node("communication_quality", communication_quality_node)
workflow.add_node("keyword_detection", keyword_detection_node)
workflow.add_node("sentiment_detection", sentiment_detection_node)

# Final Summarizer
workflow.add_node("final_qc", final_qc_node)

# Define Edges (Sequential Pipeline to Avoid Rate Limits)
# This will run one analysis node after another, ensuring no parallel blasts to the LLM API.
workflow.add_edge(START, "transcription")
workflow.add_edge("transcription", "diarization")
workflow.add_edge("diarization", "script_adherence")
workflow.add_edge("script_adherence", "qualification_completeness")
workflow.add_edge("qualification_completeness", "consent_capture")
workflow.add_edge("consent_capture", "objection_handling")
workflow.add_edge("objection_handling", "communication_quality")
workflow.add_edge("communication_quality", "keyword_detection")
workflow.add_edge("keyword_detection", "sentiment_detection")
workflow.add_edge("sentiment_detection", "final_qc")
workflow.add_edge("final_qc", END)

# Compiling the workflow
call_qc_graph = workflow.compile()
