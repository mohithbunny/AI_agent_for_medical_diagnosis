# Main.py
from concurrent.futures import ThreadPoolExecutor, as_completed
from Utils.Agents import Cardiologist, Psychologist, Pulmonologist, MultidisciplinaryTeam
import os, json

def run_agents(medical_report: str):
    """Takes a medical report string and returns analysis results as a dict."""

    agents = {
        "Cardiologist": Cardiologist(medical_report),
        "Psychologist": Psychologist(medical_report),
        "Pulmonologist": Pulmonologist(medical_report),
    }

    responses = {}
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(agent.run): name for name, agent in agents.items()}
        for future in as_completed(futures):
            role = futures[future]
            responses[role] = future.result()

    team_agent = MultidisciplinaryTeam(
        cardiologist_report=responses["Cardiologist"],
        psychologist_report=responses["Psychologist"],
        pulmonologist_report=responses["Pulmonologist"],
    )

    final_diagnosis = team_agent.run()
    final_diagnosis_text = "### Final Diagnosis:\n\n" + final_diagnosis

    return {
        "cardiologist": responses["Cardiologist"],
        "psychologist": responses["Psychologist"],
        "pulmonologist": responses["Pulmonologist"],
        "summary": final_diagnosis_text,
    }


# Allow running standalone for testing
if __name__ == "__main__":
    report_path = r"Medical Reports\Medical Rerort - Michael Johnson - Panic Attack Disorder.txt"
    with open(report_path, "r") as f:
        report_text = f.read()
    results = run_agents(report_text)
    print(json.dumps(results))
