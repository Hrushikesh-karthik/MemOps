import streamlit as st
from memory import IncidentMemory


st.set_page_config(
    page_title="MemOps",
    page_icon="🧠",
    layout="wide"
)


st.title("🧠 MemOps")

st.subheader(
    "Memory-Augmented DevOps Incident Agent"
)

st.write(
    "Diagnose DevOps failures using knowledge "
    "from previously resolved incidents."
)


memory = IncidentMemory()


error_log = st.text_area(
    "Paste CI/CD or infrastructure error",
    height=200,
    placeholder="Example: Back-off pulling image myrepo/app:v14..."
)


if st.button("Analyze Incident"):

    if error_log:

        incident, similarity = memory.search(error_log)

        st.subheader("🧠 Incident Memory")

        st.metric(
            "Memory Similarity",
            f"{similarity * 100:.1f}%"
        )

        st.write("**Similar Incident:**")
        st.write(incident["id"])

        st.write("**System:**")
        st.write(incident["system"])

        st.write("**Previous Root Cause:**")
        st.warning(incident["root_cause"])

        st.write("**Previously Successful Fix:**")
        st.success(incident["resolution"])

    else:

        st.warning("Please paste an error log.")