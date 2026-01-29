from app.agents.graph.call_qc_graph import call_qc_graph

def run_test_pipeline():
    # Mock input state
    initial_state = {
        "recording_url": "https://raw.githubusercontent.com/yuvraaj2002/OHC-Dashboard-Backend/main/assets/perfect_test_call.wav",
        "llm_cost": 0.0
    }

    print("--- Starting End-to-End QC Pipeline (Sequential) ---")
    
    try:
        final_state = call_qc_graph.invoke(initial_state)
        
        print("\n--- Pipeline Execution Complete ---")
        
        # Metrics (with None handling)
        analysis_dur = final_state.get('analysis_duration') or 0.0
        llm_cost = final_state.get('llm_cost') or 0.0
        
        print(f"\n[METRICS]")
        print(f"Analysis Time: {analysis_dur:.2f} seconds")
        print(f"Total LLM Cost: ${llm_cost:.4f}")
        
        print("\nNode Execution Check:")
        print(f"- Transcription: {'Generated' if final_state.get('call_transcript') else 'Missing'}")
        print(f"- Diarization: {'Done' if final_state.get('call_diarization') else 'Missing'}")
        print(f"- Script Adherence: {'Analyzed' if final_state.get('script_adherence') else 'Missing'}")
        print(f"- Qualification: {'Analyzed' if final_state.get('qualification_completeness') else 'Missing'}")
        print(f"- Consent: {'Analyzed' if final_state.get('consent_capture') else 'Missing'}")
        print(f"- Report: {'Generated' if final_state.get('final_qc_report') else 'Missing'}")
        
        if final_state.get('final_qc_report'):
            report = final_state['final_qc_report']
            print("\n=== FINAL QC REPORT ===")
            print(f"SCORE: {report.overall_score}/100")
            print(f"SUMMARY: {report.summary}")
            print(f"CRITICAL FLAGS: {report.critical_flags}")
            print(f"STRENGTHS: {report.key_strengths}")
            
    except Exception as e:
        import traceback
        print(f"Error during pipeline execution: {e}")
        print(traceback.format_exc())

if __name__ == "__main__":
    # uv run -m app.agents.graph.test_graph
    run_test_pipeline()
