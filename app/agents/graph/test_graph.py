from app.agents.graph.call_qc_graph import call_qc_graph

def run_test_pipeline():
    # Mock input state
    initial_state = {
        "recording_url": "https://www.rev.ai/2.0/streaming/media/example.wav",
        "llm_cost": 0.0
    }

    print("--- Starting End-to-End QC Pipeline ---")
    
    # Running the graph
    # Note: This will actually call the LLMs for each node since we haven't mocked them here.
    # For a purely structural test, we could mock the nodes.
    # But since the user wants to "run the entire pipeline", we'll provide the tool to do so.
    
    try:
        final_state = call_qc_graph.invoke(initial_state)
        
        print("\n--- Pipeline Execution Complete ---")
        print(f"Total LLM Cost: ${final_state.get('llm_cost', 0.0):.4f}")
        
        print("\nResults Summary:")
        print(f"- Transcription: {'Generated' if final_state.get('call_transcript') else 'Missing'}")
        print(f"- Diarization: {'Done' if final_state.get('call_diarization') else 'Missing'}")
        print(f"- Script Adherence: {'Analyzed' if final_state.get('script_adherence') else 'Missing'}")
        print(f"- Qualification Completeness: {'Analyzed' if final_state.get('qualification_completeness') else 'Missing'}")
        print(f"- Consent Capture: {'Analyzed' if final_state.get('consent_capture') else 'Missing'}")
        print(f"- Objection Handling: {'Analyzed' if final_state.get('objection_handling') else 'Missing'}")
        print(f"- Communication Quality: {'Analyzed' if final_state.get('communication_quality') else 'Missing'}")
        print(f"- Keyword Detection: {'Analyzed' if final_state.get('keyword_detection') else 'Missing'}")
        print(f"- Sentiment Detection: {'Analyzed' if final_state.get('sentiment_detection') else 'Missing'}")
        
    except Exception as e:
        print(f"Error during pipeline execution: {e}")

if __name__ == "__main__":
    # uv run -m app.agents.graph.test_graph
    run_test_pipeline()
