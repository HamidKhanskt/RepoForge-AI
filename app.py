import streamlit as st
from src.graph.workflow import agentforge_graph

st.set_page_config(
    page_title="AgentForge",
    page_icon="⚡",
    layout="wide",
)

st.title("⚡ AgentForge")
st.caption("Evidence-driven AI repository engineering analysis")

st.divider()

repo_url = st.text_input(
    "GitHub Repository URL",
    placeholder="https://github.com/username/repository.git",
)

if st.button("🚀 Analyze Repository", type="primary"):
    if not repo_url.strip():
        st.warning("Please enter a GitHub repository URL.")
    else:
        with st.spinner("AgentForge is analyzing the repository..."):
            try:
                result = agentforge_graph.invoke(
                    {
                        "repository_url": repo_url.strip(),
                        "question": (
                            "Investigate this repository for performance "
                            "problems and identify evidence-grounded "
                            "optimization opportunities."
                        ),
                    }
                )

                st.success("Analysis completed!")

                st.subheader("📊 Analysis Result")

                if isinstance(result, dict):
                    status = result.get("status")
                    if status:
                        st.metric("Status", str(status))

                    findings = result.get("performance_findings")

                    if findings:
                        st.subheader("🔎 Performance Findings")
                        for i, finding in enumerate(findings, 1):
                            with st.expander(
                                f"Finding {i}: "
                                f"{finding.get('type', 'Unknown')}"
                            ):
                                st.write(finding)

                    solution = result.get("solution")
                    if solution:
                        st.subheader("💡 Engineering Recommendation")
                        st.markdown(str(solution))

                    evaluation = result.get("evaluation")
                    if evaluation:
                        st.subheader("✅ Evaluation")
                        st.json(evaluation)

                    verification = result.get("verification")
                    if verification:
                        st.subheader("🧪 Verification")
                        st.json(verification)

                    with st.expander("Raw AgentForge State"):
                        st.json(result)

                else:
                    st.write(result)

            except Exception as e:
                st.error("AgentForge encountered an error.")
                st.exception(e)
